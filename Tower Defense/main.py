import math
import random
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pygame


WIDTH, HEIGHT = 1280, 900
FPS = 60
HEX_SIZE = 44
MAP_RADIUS = 7
MAP_OFFSET = (WIDTH // 2, HEIGHT // 2 + 20)
FONT_NAME = "arial"
MUSIC_FILES = {
    "menu": "start-272637.mp3",
    "game": "warrior-defense-fighting-music-335681.mp3",
}


Color = Tuple[int, int, int]


@dataclass
class Tile:
    coord: Tuple[int, int]
    center: Tuple[float, float]
    is_path: bool = False
    buildable: bool = True
    tower: Optional["Tower"] = None

    def polygon(self, size: float) -> List[Tuple[float, float]]:
        cx, cy = self.center
        points = []
        for i in range(6):
            angle = math.radians(60 * i - 30)
            x = cx + size * math.cos(angle)
            y = cy + size * math.sin(angle)
            points.append((x, y))
        return points

    def draw(self, surface: pygame.Surface, size: float, highlight: bool = False) -> None:
        if self.is_path:
            color: Color = (181, 137, 91)
        elif not self.buildable:
            color = (120, 120, 120)
        else:
            color = (180, 180, 180)
        points = self.polygon(size)
        pygame.draw.polygon(surface, color, points)
        border_color = (255, 255, 255) if highlight else (80, 80, 80)
        pygame.draw.polygon(surface, border_color, points, 2)


class HexMap:
    def __init__(
        self,
        radius: int,
        hex_size: float,
        origin: Tuple[int, int],
        base_coord: Tuple[int, int] = (0, 0),
    ):
        self.radius = radius
        self.hex_size = hex_size
        self.origin = origin
        self.base_coord = base_coord
        self.tiles: Dict[Tuple[int, int], Tile] = {}
        self.border_coords: List[Tuple[int, int]] = []
        self.generate_hex_grid()

    def axial_to_pixel(self, coord: Tuple[int, int]) -> Tuple[float, float]:
        q, r = coord
        x = self.hex_size * math.sqrt(3) * (q + r / 2) + self.origin[0]
        y = self.hex_size * 1.5 * r + self.origin[1]
        return x, y

    def pixel_to_axial(self, x: float, y: float) -> Tuple[int, int]:
        x -= self.origin[0]
        y -= self.origin[1]
        q = (math.sqrt(3) / 3 * x - 1.0 / 3 * y) / self.hex_size
        r = (2.0 / 3 * y) / self.hex_size
        return self.cube_round(q, -q - r, r)

    @staticmethod
    def cube_round(x: float, y: float, z: float) -> Tuple[int, int]:
        rx, ry, rz = round(x), round(y), round(z)
        dx, dy, dz = abs(rx - x), abs(ry - y), abs(rz - z)
        if dx > dy and dx > dz:
            rx = -ry - rz
        elif dy > dz:
            ry = -rx - rz
        else:
            rz = -rx - ry
        return rx, rz

    def generate_hex_grid(self) -> None:
        self.tiles.clear()
        for q in range(-self.radius, self.radius + 1):
            for r in range(-self.radius, self.radius + 1):
                s = -q - r
                if max(abs(q), abs(r), abs(s)) <= self.radius:
                    coord = (q, r)
                    center = self.axial_to_pixel(coord)
                    self.tiles[coord] = Tile(coord=coord, center=center)
        if self.base_coord in self.tiles:
            self.tiles[self.base_coord].buildable = False
        self.border_coords = [
            coord
            for coord in self.tiles
            if self.hex_distance(coord, (0, 0)) == self.radius
        ]

    @staticmethod
    def axial_to_cube(coord: Tuple[int, int]) -> Tuple[int, int, int]:
        q, r = coord
        return q, -q - r, r

    @staticmethod
    def cube_to_axial(cube: Tuple[int, int, int]) -> Tuple[int, int]:
        x, z = cube
        return x, z

    @staticmethod
    def hex_distance(a: Tuple[int, int], b: Tuple[int, int]) -> int:
        ax, ay, az = HexMap.axial_to_cube(a)
        bx, by, bz = HexMap.axial_to_cube(b)
        return max(abs(ax - bx), abs(ay - by), abs(az - bz))

    def axial_line(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        n = self.hex_distance(start, end)
        if n == 0:
            return [start]
        start_cube = self.axial_to_cube(start)
        end_cube = self.axial_to_cube(end)
        results = []
        for i in range(n + 1):
            t = i / n
            x = start_cube[0] + (end_cube[0] - start_cube[0]) * t
            y = start_cube[1] + (end_cube[1] - start_cube[1]) * t
            z = start_cube[2] + (end_cube[2] - start_cube[2]) * t
            results.append(self.cube_to_axial(self.cube_round(x, y, z)))
        return results

    def path_from_border_to_base(self) -> List[Tuple[float, float]]:
        if not self.border_coords or self.base_coord not in self.tiles:
            return []
        start = random.choice(self.border_coords)
        coords = self.axial_line(start, self.base_coord)
        return [self.tiles[coord].center for coord in coords if coord in self.tiles]

    def get_tile_at_pixel(self, x: float, y: float) -> Optional[Tile]:
        coord = self.pixel_to_axial(x, y)
        return self.tiles.get(coord)

    def draw(self, surface: pygame.Surface, highlight_tile: Optional[Tile]) -> None:
        for tile in self.tiles.values():
            tile.draw(surface, self.hex_size - 1, tile is highlight_tile)


@dataclass(frozen=True)
class EnemyType:
    name: str
    speed: float
    hp: int
    reward: int
    color: Color
    radius: int
    melee_damage: int
    melee_range: float
    melee_cooldown: float
    ranged_damage: int
    ranged_range: float
    ranged_cooldown: float


class Enemy(pygame.sprite.Sprite):
    def __init__(
        self,
        path: List[Tuple[float, float]],
        enemy_type: EnemyType,
        hp_multiplier: float = 1.0,
        speed_multiplier: float = 1.0,
        reward_multiplier: float = 1.0,
    ):
        super().__init__()
        self.path = path
        self.current_index = 0
        self.enemy_type = enemy_type
        self.base_speed = enemy_type.speed * speed_multiplier
        self.max_hp = math.ceil(enemy_type.hp * hp_multiplier)
        self.hp = self.max_hp
        self.reward = math.ceil(enemy_type.reward * reward_multiplier)
        diameter = enemy_type.radius * 2
        self.image = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        pygame.draw.circle(self.image, enemy_type.color, (enemy_type.radius, enemy_type.radius), enemy_type.radius)
        self.rect = self.image.get_rect(center=self.path[0])
        self.pos = pygame.Vector2(self.rect.center)
        self.game: Optional["Game"] = None
        self.melee_timer = 0.0
        self.ranged_timer = 0.0

    def update(self, dt: float, game: "Game") -> None:
        if self.current_index >= len(self.path):
            game.lives -= 1
            self.kill()
            return
        self.melee_timer += dt
        self.ranged_timer += dt
        target = pygame.Vector2(self.path[self.current_index])
        direction = target - self.pos
        distance = direction.length()
        if distance < 1:
            self.current_index += 1
            if self.current_index >= len(self.path):
                game.lives -= 1
                self.kill()
            return
        if distance != 0:
            direction = direction.normalize()
        effective_speed = self.base_speed * game.get_speed_modifier(self.pos)
        self.pos += direction * effective_speed * dt
        self.rect.center = self.pos
        self.try_attack_towers(game)

    def take_damage(self, amount: float, game: "Game") -> None:
        self.hp -= amount
        if self.hp <= 0:
            game.money += self.reward
            self.kill()

    def draw_health(self, surface: pygame.Surface) -> None:
        bar_w = self.rect.width
        ratio = max(self.hp, 0) / self.max_hp
        bar_rect = pygame.Rect(0, 0, bar_w, 4)
        bar_rect.midbottom = (self.rect.centerx, self.rect.top - 4)
        pygame.draw.rect(surface, (50, 50, 50), bar_rect)
        inner = bar_rect.copy()
        inner.width = int(bar_w * ratio)
        pygame.draw.rect(surface, (50, 200, 50), inner)

    def try_attack_towers(self, game: "Game") -> None:
        if not game.towers:
            return
        closest = None
        closest_dist = float("inf")
        for tower in game.towers:
            dist = pygame.Vector2(tower.rect.center).distance_to(self.rect.center)
            if dist < closest_dist:
                closest = tower
                closest_dist = dist
        if closest is None:
            return
        if (
            closest_dist <= self.enemy_type.melee_range
            and self.melee_timer >= self.enemy_type.melee_cooldown
        ):
            closest.take_damage(self.enemy_type.melee_damage)
            self.melee_timer = 0.0
        elif (
            closest_dist <= self.enemy_type.ranged_range
            and self.ranged_timer >= self.enemy_type.ranged_cooldown
        ):
            closest.take_damage(self.enemy_type.ranged_damage)
            self.ranged_timer = 0.0


class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos: Tuple[float, float], target: Enemy, damage: float, speed: float, game: "Game"):
        super().__init__()
        self.target = target
        self.damage = damage
        self.speed = speed
        self.game = game
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (240, 240, 120), (5, 5), 5)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(pos)

    def update(self, dt: float) -> None:
        if not self.target.alive():
            self.kill()
            return
        direction = pygame.Vector2(self.target.rect.center) - self.pos
        distance = direction.length()
        if distance <= self.speed * dt or distance == 0:
            self.target.take_damage(self.damage, self.game)
            self.kill()
            return
        direction = direction.normalize()
        self.pos += direction * self.speed * dt
        self.rect.center = self.pos


@dataclass(frozen=True)
class TowerType:
    name: str
    cost: int
    range: float
    fire_rate: float
    damage: float
    projectile_speed: float
    color: Color
    is_wall: bool = False
    slow_factor: float = 1.0
    slow_radius: float = 0.0
    max_hp: int = 160


class Tower(pygame.sprite.Sprite):
    def __init__(self, tile: Tile, tower_type: TowerType):
        super().__init__()
        self.tile = tile
        self.tower_type = tower_type
        self.range = tower_type.range
        self.fire_rate = tower_type.fire_rate
        self.damage = tower_type.damage
        self.projectile_speed = tower_type.projectile_speed
        self.time_since_last_shot = 0.0
        self.level = 1
        self.max_level = 5
        self.is_wall = tower_type.is_wall
        self.max_hp = tower_type.max_hp if not self.is_wall else tower_type.max_hp + 60
        self.hp = self.max_hp
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.image, tower_type.color, (25, 25), 24)
        self.rect = self.image.get_rect(center=tile.center)

    def update(self, dt: float, game: "Game") -> None:
        if self.is_wall:
            return
        self.time_since_last_shot += dt
        if self.time_since_last_shot < self.fire_rate:
            return
        target = self.find_target(game.enemies)
        if target is None:
            return
        projectile = Projectile(self.rect.center, target, self.damage, self.projectile_speed, game)
        game.projectiles.add(projectile)
        self.time_since_last_shot = 0.0

    def find_target(self, enemies: pygame.sprite.Group) -> Optional[Enemy]:
        closest = None
        closest_dist = float("inf")
        for enemy in enemies:
            dist = pygame.Vector2(enemy.rect.center).distance_to(self.rect.center)
            if dist <= self.range and dist < closest_dist:
                closest = enemy
                closest_dist = dist
        return closest

    def upgrade_cost(self) -> int:
        return int(self.tower_type.cost * (0.7 + 0.4 * self.level))

    def upgrade(self) -> None:
        if self.level >= self.max_level:
            return
        self.level += 1
        if self.is_wall:
            updated_fields = {**vars(self.tower_type), "slow_radius": self.tower_type.slow_radius + 8}
            self.tower_type = TowerType(**updated_fields)
        else:
            self.range *= 1.12
            self.damage *= 1.18
            self.fire_rate = max(0.2, self.fire_rate * 0.92)

    def take_damage(self, amount: float) -> None:
        self.hp -= amount
        if self.hp <= 0:
            self.destroy()

    def heal(self, amount: float) -> None:
        self.hp = min(self.max_hp, self.hp + amount)

    def destroy(self) -> None:
        if self.tile.tower is self:
            self.tile.tower = None
        self.kill()

    def draw_health(self, surface: pygame.Surface) -> None:
        bar_w = self.rect.width
        ratio = max(self.hp, 0) / self.max_hp
        bar_rect = pygame.Rect(0, 0, bar_w, 4)
        bar_rect.midtop = (self.rect.centerx, self.rect.bottom + 6)
        pygame.draw.rect(surface, (40, 40, 40), bar_rect)
        inner = bar_rect.copy()
        inner.width = int(bar_w * ratio)
        pygame.draw.rect(surface, (80, 200, 80), inner)


TOWER_TYPES: Dict[str, TowerType] = {
    "basic": TowerType(
        name="Basic",
        cost=50,
        range=170,
        fire_rate=0.9,
        damage=20,
        projectile_speed=320,
        color=(100, 160, 220),
        max_hp=160,
    ),
    "sniper": TowerType(
        name="Sniper",
        cost=85,
        range=280,
        fire_rate=1.8,
        damage=40,
        projectile_speed=420,
        color=(220, 200, 120),
        max_hp=140,
    ),
    "rapid": TowerType(
        name="Rapid",
        cost=70,
        range=140,
        fire_rate=0.45,
        damage=12,
        projectile_speed=360,
        color=(150, 220, 140),
        max_hp=150,
    ),
    "wall": TowerType(
        name="Wall",
        cost=40,
        range=0,
        fire_rate=0,
        damage=0,
        projectile_speed=0,
        color=(90, 90, 110),
        is_wall=True,
        slow_factor=0.35,
        slow_radius=65,
        max_hp=200,
    ),
}


ENEMY_TYPES: Dict[str, EnemyType] = {
    "grunt": EnemyType(
        "Grunt",
        speed=60,
        hp=60,
        reward=18,
        color=(220, 80, 80),
        radius=14,
        melee_damage=8,
        melee_range=26,
        melee_cooldown=1.1,
        ranged_damage=5,
        ranged_range=140,
        ranged_cooldown=2.4,
    ),
    "swift": EnemyType(
        "Swift",
        speed=95,
        hp=45,
        reward=15,
        color=(120, 200, 140),
        radius=13,
        melee_damage=6,
        melee_range=26,
        melee_cooldown=0.8,
        ranged_damage=4,
        ranged_range=120,
        ranged_cooldown=1.8,
    ),
    "tank": EnemyType(
        "Tank",
        speed=40,
        hp=130,
        reward=35,
        color=(170, 140, 220),
        radius=16,
        melee_damage=14,
        melee_range=32,
        melee_cooldown=1.3,
        ranged_damage=9,
        ranged_range=170,
        ranged_cooldown=2.8,
    ),
}


@dataclass
class WaveEntry:
    enemy_type: str
    count: int
    interval: float
    hp_multiplier: float = 1.0
    speed_multiplier: float = 1.0
    reward_multiplier: float = 1.0


@dataclass
class WaveDefinition:
    entries: List[WaveEntry]


def generate_wave_definitions(total_waves: int) -> List[WaveDefinition]:
    waves: List[WaveDefinition] = []
    for idx in range(total_waves):
        wave_number = idx + 1
        base_count = 8 + wave_number // 2
        burst_count = 4 + wave_number // 4
        hp_scale = 1.0 + wave_number * 0.05
        reward_scale = 1.0 + wave_number * 0.02
        grunt_interval = max(0.22, 1.05 - wave_number * 0.008)
        entries: List[WaveEntry] = [
            WaveEntry(
                "grunt",
                count=base_count,
                interval=grunt_interval,
                hp_multiplier=hp_scale * 0.85,
                speed_multiplier=1.0 + wave_number * 0.004,
                reward_multiplier=reward_scale * 0.65,
            )
        ]
        if wave_number % 3 == 0:
            entries.append(
                WaveEntry(
                    "swift",
                    count=burst_count,
                    interval=max(0.18, 0.9 - wave_number * 0.006),
                    hp_multiplier=hp_scale * 0.7,
                    speed_multiplier=1.1 + wave_number * 0.006,
                    reward_multiplier=reward_scale * 0.5,
                )
            )
        if wave_number % 5 == 0:
            entries.append(
                WaveEntry(
                    "tank",
                    count=max(3, wave_number // 8),
                    interval=max(0.35, 1.4 - wave_number * 0.0045),
                    hp_multiplier=hp_scale * 1.4,
                    speed_multiplier=0.9 + wave_number * 0.0025,
                    reward_multiplier=reward_scale,
                )
            )
        waves.append(WaveDefinition(entries))
    return waves


class WaveManager:
    def __init__(
        self,
        waves: List[WaveDefinition],
        cooldown_duration: float = 3.5,
        base_mob_cap: int = 20,
        mob_cap_growth: int = 2,
        base_spawn_rate_multiplier: float = 2.0,
        spawn_rate_growth: float = 0.05,
    ):
        self.waves = waves
        self.current_wave = -1
        self.time_since_last_spawn = 0.0
        self.active = False
        self.entry_index = 0
        self.spawned_in_entry = 0
        self.cooldown_duration = cooldown_duration
        self.cooldown_remaining = 0.0
        self.base_mob_cap = base_mob_cap
        self.mob_cap_growth = mob_cap_growth
        self.base_spawn_rate_multiplier = base_spawn_rate_multiplier
        self.spawn_rate_growth = spawn_rate_growth
        self.current_mob_cap = base_mob_cap
        self.current_spawn_rate_multiplier = base_spawn_rate_multiplier

    def start_next_wave(self) -> None:
        if self.active or self.cooldown_remaining > 0:
            return
        if self.current_wave + 1 >= len(self.waves):
            return
        self.current_wave += 1
        self.entry_index = 0
        self.spawned_in_entry = 0
        self.time_since_last_spawn = 0.0
        self.cooldown_remaining = 0.0
        self.active = True
        wave_number = self.current_wave + 1
        self.current_mob_cap = self.base_mob_cap + self.mob_cap_growth * wave_number
        self.current_spawn_rate_multiplier = self.base_spawn_rate_multiplier + self.spawn_rate_growth * wave_number

    def update(self, dt: float, game: "Game") -> None:
        if self.cooldown_remaining > 0 and not self.active:
            self.cooldown_remaining = max(0.0, self.cooldown_remaining - dt)
        if not self.active or self.current_wave >= len(self.waves):
            return
        self.time_since_last_spawn += dt
        wave = self.waves[self.current_wave]
        while self.entry_index < len(wave.entries):
            entry = wave.entries[self.entry_index]
            if self.spawned_in_entry >= entry.count:
                self.entry_index += 1
                self.spawned_in_entry = 0
                self.time_since_last_spawn = 0.0
                continue
            if self.time_since_last_spawn >= entry.interval / self.current_spawn_rate_multiplier:
                self.spawn_enemy(game, entry)
                self.time_since_last_spawn = 0.0
            break
        if self.entry_index >= len(wave.entries) and not game.enemies:
            self.active = False
            if self.current_wave < len(self.waves) - 1:
                self.cooldown_remaining = self.cooldown_duration

    def spawn_enemy(self, game: "Game", entry: WaveEntry) -> None:
        if len(game.enemies) >= self.current_mob_cap:
            return
        path = game.hex_map.path_from_border_to_base()
        if len(path) < 2:
            return
        enemy_type = game.enemy_types[entry.enemy_type]
        enemy = Enemy(
            path,
            enemy_type,
            hp_multiplier=entry.hp_multiplier,
            speed_multiplier=entry.speed_multiplier,
            reward_multiplier=entry.reward_multiplier,
        )
        enemy.game = game
        game.enemies.add(enemy)
        self.spawned_in_entry += 1


class HomeBase:
    def __init__(self, tile: Tile):
        self.tile = tile
        self.radius = 32
        self.font = pygame.font.SysFont(FONT_NAME, 20)

    def draw(self, surface: pygame.Surface, lives: int) -> None:
        center = self.tile.center
        outer_color = (80, 160, 220)
        inner_color = (20, 35, 60)
        pygame.draw.circle(surface, outer_color, center, self.radius)
        pygame.draw.circle(surface, inner_color, center, self.radius - 8)
        text = self.font.render(str(max(lives, 0)), True, (240, 240, 240))
        text_rect = text.get_rect(center=center)
        surface.blit(text, text_rect)


class MusicPlayer:
    def __init__(self, base_path: Path):
        self.enabled = True
        try:
            pygame.mixer.init()
        except pygame.error as exc:
            self.enabled = False
            print(f"[music] Audio disabled: {exc}")
            return
        self.tracks = {key: base_path / filename for key, filename in MUSIC_FILES.items()}

    def play(self, key: str, *, loop: bool, volume: float, fade_ms: int = 500) -> None:
        if not self.enabled:
            return
        track = self.tracks.get(key)
        if track is None or not track.exists():
            print(f"[music] Missing track: {track}")
            return
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(fade_ms)
        try:
            pygame.mixer.music.load(str(track))
            pygame.mixer.music.set_volume(volume)
            loops = -1 if loop else 0
            pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)
        except pygame.error as exc:
            print(f"[music] Failed to play {track}: {exc}")

    def play_menu(self) -> None:
        self.play("menu", loop=True, volume=0.55)

    def play_game(self) -> None:
        self.play("game", loop=True, volume=0.45)

    def stop(self, fade_ms: int = 300) -> None:
        if not self.enabled:
            return
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(fade_ms)


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Hex Tower Defense")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(FONT_NAME, 22)
        self.title_font = pygame.font.SysFont(FONT_NAME, 64)
        self.sub_title_font = pygame.font.SysFont(FONT_NAME, 30)
        self.button_font = pygame.font.SysFont(FONT_NAME, 26)
        self.music = MusicPlayer(Path(__file__).resolve().parent)
        self.enemy_types = ENEMY_TYPES
        self.tower_types = TOWER_TYPES
        self.wave_definitions = generate_wave_definitions(600)
        self.state = "intro"
        self.running = True
        self.rules_text = [
            "Goal: defend the central base until every wave is cleared.",
            "Waves: a short break begins after each wave; press N once it is ready.",
            "Building: click a tile or press Space/Enter to build the selected item.",
            "Navigation: move the selector with arrows, WASD, or Q/E diagonals.",
            "Numbers: change build type with 1-9. Click an existing tower to upgrade it.",
            "Breaks: right-click a tower to heal it during wave breaks using coins.",
        ]
        self.intro_buttons = {
            "start": pygame.Rect(WIDTH // 2 - 170, HEIGHT // 2 + 20, 340, 70),
            "rules": pygame.Rect(WIDTH // 2 - 170, HEIGHT // 2 + 110, 340, 70),
        }
        self.rules_back_button = pygame.Rect(WIDTH // 2 - 130, HEIGHT - 140, 260, 60)
        self.outro_buttons = {
            "menu": pygame.Rect(WIDTH // 2 - 150, HEIGHT - 170, 300, 70),
        }
        self.game_result = ""
        self.outro_summary: List[str] = []
        self.setup_gameplay()
        self.music.play_menu()

    def setup_gameplay(self) -> None:
        self.hex_map = HexMap(MAP_RADIUS, HEX_SIZE, MAP_OFFSET)
        self.enemies = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.tower_keys = list(self.tower_types.keys())
        self.selected_tower_key = self.tower_keys[0]
        self.money = 200
        self.lives = 20
        self.wave_manager = WaveManager(self.wave_definitions, cooldown_duration=4.0)
        self.home_base = HomeBase(self.hex_map.tiles[self.hex_map.base_coord])
        self.selected_tile: Optional[Tile] = self.hex_map.tiles.get(self.hex_map.base_coord)

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.handle_events()
            self.update(dt)
            self.draw()
        self.music.stop()
        pygame.quit()
        sys.exit()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                continue
            if self.state == "intro":
                self.handle_intro_events(event)
            elif self.state == "rules":
                self.handle_rules_events(event)
            elif self.state == "playing":
                self.handle_gameplay_events(event)
            elif self.state == "outro":
                self.handle_outro_events(event)

    def handle_intro_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.intro_buttons["start"].collidepoint(event.pos):
                self.start_game()
            elif self.intro_buttons["rules"].collidepoint(event.pos):
                self.state = "rules"

    def handle_rules_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rules_back_button.collidepoint(event.pos):
                self.state = "intro"

    def handle_outro_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.outro_buttons["menu"].collidepoint(event.pos):
                self.state = "intro"
                self.game_result = ""
                self.outro_summary = []
                self.music.play_menu()

    def handle_gameplay_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self.selected_tile = self.hex_map.get_tile_at_pixel(*event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                tile = self.hex_map.get_tile_at_pixel(*event.pos)
                if tile:
                    self.selected_tile = tile
                    self.try_build_tower(tile)
            elif event.button == 3:
                self.try_heal_selected_tower()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                self.wave_manager.start_next_wave()
            elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                if self.selected_tile:
                    self.try_build_tower(self.selected_tile)
            elif pygame.K_1 <= event.key <= pygame.K_9:
                index = event.key - pygame.K_1
                if index < len(self.tower_keys):
                    self.selected_tower_key = self.tower_keys[index]
            else:
                self.handle_keyboard_selection(event.key)

    def start_game(self) -> None:
        self.setup_gameplay()
        self.state = "playing"
        self.wave_manager.start_next_wave()
        self.music.play_game()

    def handle_keyboard_selection(self, key: int) -> None:
        if not self.selected_tile:
            self.selected_tile = self.hex_map.tiles.get(self.hex_map.base_coord)
            return
        axial_moves = {
            pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1),
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_w: (0, -1),
            pygame.K_s: (0, 1),
            pygame.K_a: (-1, 0),
            pygame.K_d: (1, 0),
            pygame.K_q: (-1, 1),
            pygame.K_e: (1, -1),
        }
        if key not in axial_moves:
            return
        dq, dr = axial_moves[key]
        coord = self.selected_tile.coord
        new_coord = (coord[0] + dq, coord[1] + dr)
        if new_coord in self.hex_map.tiles:
            self.selected_tile = self.hex_map.tiles[new_coord]

    def try_build_tower(self, tile: Tile) -> None:
        if not tile.buildable:
            return
        if tile.tower is not None:
            self.try_upgrade_tower(tile.tower)
            return
        tower_type = self.tower_types[self.selected_tower_key]
        if self.money < tower_type.cost:
            return
        tower = Tower(tile, tower_type)
        tile.tower = tower
        self.towers.add(tower)
        self.money -= tower_type.cost

    def try_upgrade_tower(self, tower: Tower) -> None:
        if tower.level >= tower.max_level:
            return
        cost = tower.upgrade_cost()
        if self.money < cost:
            return
        self.money -= cost
        tower.upgrade()

    def heal_cost(self, tower: Tower) -> int:
        missing_hp = tower.max_hp - tower.hp
        return max(1, math.ceil(missing_hp / 10))

    def can_heal_towers(self) -> bool:
        return not self.wave_manager.active and self.wave_manager.cooldown_remaining > 0

    def try_heal_selected_tower(self) -> None:
        if not self.selected_tile or not self.selected_tile.tower:
            return
        if not self.can_heal_towers():
            return
        tower = self.selected_tile.tower
        missing_hp = tower.max_hp - tower.hp
        if missing_hp <= 0:
            return
        cost = self.heal_cost(tower)
        if self.money < cost:
            return
        self.money -= cost
        tower.heal(missing_hp)

    def get_speed_modifier(self, position: pygame.Vector2) -> float:
        modifier = 1.0
        for tower in self.towers:
            if not tower.is_wall:
                continue
            distance = pygame.Vector2(tower.rect.center).distance_to(position)
            if distance <= tower.tower_type.slow_radius:
                modifier = min(modifier, tower.tower_type.slow_factor)
        return max(0.1, modifier)

    def update(self, dt: float) -> None:
        if self.state != "playing":
            return
        self.wave_manager.update(dt, self)
        for enemy in list(self.enemies):
            enemy.update(dt, self)
        for tower in self.towers:
            tower.update(dt, self)
        for projectile in list(self.projectiles):
            projectile.update(dt)
        if self.lives <= 0:
            self.finish_game("Defense failed!")
        elif self.all_waves_cleared():
            self.finish_game("All 600 waves have been defended!")

    def draw(self) -> None:
        if self.state == "intro":
            self.draw_intro()
        elif self.state == "rules":
            self.draw_rules()
        elif self.state == "playing":
            self.draw_gameplay()
        elif self.state == "outro":
            self.draw_outro()
        pygame.display.flip()

    def draw_gameplay(self) -> None:
        self.screen.fill((15, 20, 35))
        self.hex_map.draw(self.screen, self.selected_tile)
        self.home_base.draw(self.screen, self.lives)
        self.towers.draw(self.screen)
        self.enemies.draw(self.screen)
        self.projectiles.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw_health(self.screen)
        for tower in self.towers:
            tower.draw_health(self.screen)
        self.draw_ui()

    def draw_ui(self) -> None:
        wave_total = len(self.wave_manager.waves)
        wave_current = min(self.wave_manager.current_wave + 1, wave_total)
        selected_type = self.tower_types[self.selected_tower_key]
        tower_text = " / ".join(
            f"{idx + 1}:{self.tower_types[key].name}({self.tower_types[key].cost})" +
            ("*" if key == self.selected_tower_key else "")
            for idx, key in enumerate(self.tower_keys)
        )
        cooldown = (
            "ready" if self.wave_manager.cooldown_remaining <= 0 else f"{self.wave_manager.cooldown_remaining:0.1f}s"
        )
        upgrade_text = "Click a built tower to upgrade it"
        heal_text = "Healing available only during breaks (right-click)."
        if not self.can_heal_towers():
            heal_text = "Healing disabled until the next break between waves."
        if self.selected_tile and self.selected_tile.tower:
            tower = self.selected_tile.tower
            if tower.level >= tower.max_level:
                upgrade_text = "Selected tower is at max level"
            else:
                upgrade_text = (
                    f"Upgrade cost: {tower.upgrade_cost()} (Lv {tower.level}/{tower.max_level})"
                )
            missing_hp = tower.max_hp - tower.hp
            if missing_hp > 0:
                heal_cost = self.heal_cost(tower)
                heal_text = (
                    f"Heal (right-click) costs {heal_cost} to restore {missing_hp} HP during breaks"
                )
            else:
                heal_text = "Tower is at full health"
        texts = [
            f"Money: {self.money}",
            f"Lives: {self.lives}",
            f"Wave: {wave_current}/{wave_total}",
            f"Selected: {selected_type.name} (Cost {selected_type.cost})",
            f"[1-{len(self.tower_keys)}] {tower_text}",
            f"Next wave cooldown: {cooldown} — press N when ready",
            "Walls slow enemies inside their radius; towers attack automatically.",
            upgrade_text,
            heal_text,
        ]
        for i, text in enumerate(texts):
            label = self.font.render(text, True, (240, 240, 240))
            self.screen.blit(label, (20, 20 + i * 26))

    def draw_intro(self) -> None:
        self.screen.fill((8, 12, 25))
        title = self.title_font.render("Hex Tower Defense", True, (245, 245, 245))
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 120))
        self.screen.blit(title, title_rect)
        subtitle = self.sub_title_font.render("Strategize and hold the line", True, (200, 200, 220))
        self.screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60)))
        mouse_pos = pygame.mouse.get_pos()
        self.draw_button(self.intro_buttons["start"], "Start", mouse_pos)
        self.draw_button(self.intro_buttons["rules"], "Rules", mouse_pos)

    def draw_rules(self) -> None:
        self.screen.fill((10, 15, 30))
        title = self.title_font.render("Rules", True, (240, 240, 240))
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 140)))
        for i, line in enumerate(self.rules_text):
            label = self.sub_title_font.render(line, True, (230, 230, 240))
            self.screen.blit(label, (120, 240 + i * 48))
        self.draw_button(self.rules_back_button, "Back", pygame.mouse.get_pos())

    def draw_outro(self) -> None:
        self.screen.fill((5, 10, 20))
        title = self.title_font.render("Game Over", True, (240, 240, 240))
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 150)))
        result = self.sub_title_font.render(self.game_result or "", True, (200, 220, 255))
        self.screen.blit(result, result.get_rect(center=(WIDTH // 2, 230)))
        for i, line in enumerate(self.outro_summary):
            label = self.button_font.render(line, True, (220, 220, 230))
            self.screen.blit(label, label.get_rect(center=(WIDTH // 2, 320 + i * 40)))
        self.draw_button(self.outro_buttons["menu"], "Main Menu", pygame.mouse.get_pos())

    def draw_button(self, rect: pygame.Rect, text: str, mouse_pos: Tuple[int, int]) -> None:
        hovered = rect.collidepoint(mouse_pos)
        base_color = (70, 120, 210) if hovered else (40, 70, 140)
        pygame.draw.rect(self.screen, base_color, rect, border_radius=14)
        pygame.draw.rect(self.screen, (255, 255, 255), rect, width=2, border_radius=14)
        label = self.button_font.render(text, True, (255, 255, 255))
        self.screen.blit(label, label.get_rect(center=rect.center))

    def finish_game(self, message: str) -> None:
        if self.state != "playing":
            return
        total_waves = len(self.wave_manager.waves)
        current_wave = max(0, self.wave_manager.current_wave + 1)
        self.game_result = message
        self.outro_summary = [
            f"Waves survived: {current_wave}/{total_waves}",
            f"Money left: {self.money}",
            f"Lives left: {max(self.lives, 0)}",
        ]
        self.state = "outro"
        self.music.play_menu()

    def all_waves_cleared(self) -> bool:
        if not self.wave_manager.waves:
            return False
        last_wave_index = len(self.wave_manager.waves) - 1
        return (
            self.wave_manager.current_wave == last_wave_index
            and not self.wave_manager.active
            and not self.enemies
        )


if __name__ == "__main__":
    Game().run()
