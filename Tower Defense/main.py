import math
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import pygame


WIDTH, HEIGHT = 1000, 700
FPS = 60
HEX_SIZE = 38
MAP_COLS = 11
MAP_ROWS = 7
MAP_OFFSET = (120, 120)
TOWER_COST = 50
FONT_NAME = "arial"


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
    def __init__(self, cols: int, rows: int, hex_size: float, origin: Tuple[int, int]):
        self.cols = cols
        self.rows = rows
        self.hex_size = hex_size
        self.origin = origin
        self.tiles: Dict[Tuple[int, int], Tile] = {}
        self.path_coords: List[Tuple[int, int]] = []
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
        for q in range(self.cols):
            for r in range(self.rows):
                coord = (q, r)
                center = self.axial_to_pixel(coord)
                self.tiles[coord] = Tile(coord=coord, center=center)
        mid_row = self.rows // 2
        self.path_coords = [(q, mid_row) for q in range(self.cols)]
        for coord in self.path_coords:
            if coord in self.tiles:
                self.tiles[coord].is_path = True
                self.tiles[coord].buildable = False

    def get_tile_at_pixel(self, x: float, y: float) -> Optional[Tile]:
        coord = self.pixel_to_axial(x, y)
        return self.tiles.get(coord)

    def draw(self, surface: pygame.Surface, highlight_tile: Optional[Tile]) -> None:
        for tile in self.tiles.values():
            tile.draw(surface, self.hex_size - 1, tile is highlight_tile)

    def path_points(self) -> List[Tuple[float, float]]:
        return [self.tiles[coord].center for coord in self.path_coords if coord in self.tiles]


class Enemy(pygame.sprite.Sprite):
    def __init__(self, path: List[Tuple[float, float]], speed: float, hp: int, reward: int):
        super().__init__()
        self.path = path
        self.current_index = 0
        self.speed = speed
        self.max_hp = hp
        self.hp = hp
        self.reward = reward
        self.image = pygame.Surface((28, 28), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (220, 60, 60), (14, 14), 14)
        self.rect = self.image.get_rect(center=self.path[0])
        self.pos = pygame.Vector2(self.rect.center)
        self.game: Optional["Game"] = None

    def update(self, dt: float, game: "Game") -> None:
        if self.current_index >= len(self.path):
            game.lives -= 1
            self.kill()
            return
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
        self.pos += direction * self.speed * dt
        self.rect.center = self.pos

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


class Tower(pygame.sprite.Sprite):
    def __init__(self, tile: Tile):
        super().__init__()
        self.tile = tile
        self.range = 160
        self.fire_rate = 0.9
        self.damage = 20
        self.projectile_speed = 320
        self.time_since_last_shot = 0.0
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (100, 160, 220), (25, 25), 24)
        self.rect = self.image.get_rect(center=tile.center)

    def update(self, dt: float, game: "Game") -> None:
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


class WaveDefinition:
    def __init__(self, count: int, interval: float, speed: float, hp: int):
        self.count = count
        self.interval = interval
        self.speed = speed
        self.hp = hp


class WaveManager:
    def __init__(self, waves: List[WaveDefinition]):
        self.waves = waves
        self.current_wave = -1
        self.spawned = 0
        self.time_since_last_spawn = 0.0
        self.active = False

    def start_next_wave(self) -> None:
        if self.active:
            return
        if self.current_wave + 1 >= len(self.waves):
            return
        self.current_wave += 1
        self.spawned = 0
        self.time_since_last_spawn = 0.0
        self.active = True

    def update(self, dt: float, game: "Game") -> None:
        if not self.active or self.current_wave >= len(self.waves):
            return
        self.time_since_last_spawn += dt
        wave = self.waves[self.current_wave]
        if self.spawned < wave.count and self.time_since_last_spawn >= wave.interval:
            self.spawn_enemy(game, wave)
            self.time_since_last_spawn = 0.0
        if self.spawned >= wave.count and not game.enemies:
            self.active = False

    def spawn_enemy(self, game: "Game", wave: WaveDefinition) -> None:
        enemy = Enemy(game.hex_map.path_points(), wave.speed, wave.hp, reward=20)
        enemy.game = game
        game.enemies.add(enemy)
        self.spawned += 1


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Hex Tower Defense")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(FONT_NAME, 22)
        self.hex_map = HexMap(MAP_COLS, MAP_ROWS, HEX_SIZE, MAP_OFFSET)
        self.enemies = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.money = 200
        self.lives = 20
        self.wave_manager = WaveManager([
            WaveDefinition(8, 1.0, 60, 60),
            WaveDefinition(12, 0.8, 70, 80),
            WaveDefinition(16, 0.7, 80, 100),
        ])
        self.selected_tile: Optional[Tile] = None
        self.running = True
        self.wave_manager.start_next_wave()

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()
        sys.exit()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEMOTION:
                self.selected_tile = self.hex_map.get_tile_at_pixel(*event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                tile = self.hex_map.get_tile_at_pixel(*event.pos)
                if tile:
                    self.try_build_tower(tile)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    self.wave_manager.start_next_wave()

    def try_build_tower(self, tile: Tile) -> None:
        if not tile.buildable or tile.tower is not None:
            return
        if self.money < TOWER_COST:
            return
        tower = Tower(tile)
        tile.tower = tower
        self.towers.add(tower)
        self.money -= TOWER_COST

    def update(self, dt: float) -> None:
        self.wave_manager.update(dt, self)
        for enemy in list(self.enemies):
            enemy.update(dt, self)
        for tower in self.towers:
            tower.update(dt, self)
        for projectile in list(self.projectiles):
            projectile.update(dt)

    def draw(self) -> None:
        self.screen.fill((15, 20, 35))
        self.hex_map.draw(self.screen, self.selected_tile)
        self.towers.draw(self.screen)
        self.enemies.draw(self.screen)
        self.projectiles.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw_health(self.screen)
        self.draw_ui()
        pygame.display.flip()

    def draw_ui(self) -> None:
        texts = [
            f"Money: {self.money}",
            f"Lives: {self.lives}",
            f"Wave: {self.wave_manager.current_wave + 1}/{len(self.wave_manager.waves)}",
            "Click to build tower (50). Press N for next wave.",
        ]
        for i, text in enumerate(texts):
            label = self.font.render(text, True, (240, 240, 240))
            self.screen.blit(label, (20, 20 + i * 26))


if __name__ == "__main__":
    Game().run()
