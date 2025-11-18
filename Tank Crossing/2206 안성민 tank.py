import pygame
import random
from pygame.locals import *

# --- 상수 정의 ---

# 화면 크기
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

# 벽 두께
WALL_THICKNESS = 10

# 총알 개수 제한
BULLET_LIMIT = 5


# --- 클래스 정의 ---

class Player(pygame.sprite.Sprite):
	"""플레이어 탱크 클래스"""

	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("tank.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.reset()
		self.speed = 3
		self.last_shot_time = 0
		self.shoot_delay = 500  # 500ms

	def reset(self):
		"""탱크를 초기 위치로 이동"""
		self.rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT)

	def update(self, walls):
		"""키 입력에 따라 탱크를 이동"""
		keys = pygame.key.get_pressed()
		if keys[K_LEFT]:
			self.rect.x -= self.speed
		if keys[K_RIGHT]:
			self.rect.x += self.speed
		if keys[K_UP]:
			self.rect.y -= self.speed

		# 벽 충돌 처리
		if pygame.sprite.spritecollide(self, walls, False):
			if self.rect.left < WALL_THICKNESS:
				self.rect.left = WALL_THICKNESS
			if self.rect.right > SCREEN_WIDTH - WALL_THICKNESS:
				self.rect.right = SCREEN_WIDTH - WALL_THICKNESS

	def shoot(self):
		"""
		[Ploblem 1] 포탄의 재장전 시간을 고려하여 포탄을 발사합니다.

		TODO: 이전 발사로부터 경과 시간이 shoot_delay(500ms)를 초과하면 Bullet 객체를 생성해서 반환합니다.
		      이 때 포탄의 초기 생성 위치는 탱크의 전면 중앙입니다.
		Hint 1. 먼저 Bullet 클래스에서 포탄의 생성 위치(기준 좌표)를 확인하세요.
		     2. pygame.time.get_ticks() 함수는 pygame.init() 후 경과한 시간(millisecond)을 리턴해줍니다.
		"""

		now = pygame.time.get_ticks()
		if now - self.last_shot_time >= self.shoot_delay:
			self.last_shot_time = now
			return Bullet(self.rect.centerx, self.rect.top)
		return None



class Stone(pygame.sprite.Sprite):
	"""장애물 돌 클래스"""

	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("stone.png").convert()
		self.image.set_colorkey("white")
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WALL_THICKNESS, SCREEN_WIDTH - WALL_THICKNESS - self.rect.width)
		self.rect.y = random.randrange(50, SCREEN_HEIGHT - 150)
		self.speedx = random.choice([-2, -1, 1, 2])

	def update(self, walls):
		"""
		[Ploblem 2] 돌을 이동시킵니다.

		TODO: 돌을 speedx만큼 x 방향으로 이동시키고 벽에 닿으면 방향을 바꿉니다.
		      즉, 오른쪽 벽에 닿으면 speedx의 부호를 바꿔서 왼쪽으로 이동시킵니다.
		"""

		self.rect.x += self.speedx
		if self.rect.left <= WALL_THICKNESS or self.rect.right >= SCREEN_WIDTH - WALL_THICKNESS:
			self.speedx *= -1
			if self.rect.left <= WALL_THICKNESS:
				self.rect.left = WALL_THICKNESS
			if self.rect.right >= SCREEN_WIDTH - WALL_THICKNESS:
				self.rect.right = SCREEN_WIDTH - WALL_THICKNESS



class Bullet(pygame.sprite.Sprite):
	"""포탄 클래스"""

	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.Surface((20, 20))
		self.image.fill("black")
		self.rect = self.image.get_rect()
		self.rect.midbottom = (x, y)
		self.speedy = -10

	def update(self):
		"""포탄을 위로 이동시키고 화면을 벗어나면 제거"""
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()


class Wall(pygame.sprite.Sprite):
	"""게임 화면 양쪽의 벽 클래스"""

	def __init__(self, x, y, width, height):
		super().__init__()
		self.image = pygame.Surface([width, height])
		self.image.fill("black")
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


class Game:
	"""게임의 전체 흐름을 관리하는 메인 클래스"""

	def __init__(self):
		"""게임 초기화"""
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption("Tank Crossing")
		self.clock = pygame.time.Clock()
		self.running = True
		self.game_over = False
		self.start_time = 0
		self.bullets_remaining = 0

	def setup(self):
		"""게임 객체들 설정 및 초기화"""
		self.all_sprites = pygame.sprite.Group()
		self.stones = pygame.sprite.Group()
		self.bullets = pygame.sprite.Group()
		self.walls = pygame.sprite.Group()

		# 플레이어 생성
		self.player = Player()
		self.all_sprites.add(self.player)

		# 벽 생성
		left_wall = Wall(0, 0, WALL_THICKNESS, SCREEN_HEIGHT)
		right_wall = Wall(SCREEN_WIDTH - WALL_THICKNESS, 0, WALL_THICKNESS, SCREEN_HEIGHT)
		self.walls.add(left_wall, right_wall)
		self.all_sprites.add(left_wall, right_wall)

		# 초기 돌 생성
		self.create_stones(15)
		self.start_time = pygame.time.get_ticks()
		self.bullets_remaining = BULLET_LIMIT

	def run(self):
		"""메인 게임 루프"""
		self.setup()
		while self.running:
			self.clock.tick(60)
			self.event()
			if not self.game_over:
				self.update()
			self.draw()
		pygame.quit()

	def create_stones(self, count):
		"""
		[Ploblem 3] 지정된 개수만큼 서로 겹치지 않는 돌을 생성합니다.

		TODO: 새로운 돌을 생성할 때마다, 이미 존재하는 다른 돌들과 충돌하는지 확인해야 합니다.
			  만약 위치가 겹친다면, 겹치지 않는 새 위치를 찾아야 합니다.
			  생성된 돌은 돌 그룹(stones)과 모든 스프라이트 그룹(all_sprites)에 추가해야 합니다.
		"""

		for _ in range(count):
			placed = False
			attempts = 0
			while not placed and attempts < 200:
				attempts += 1
				stone = Stone()
				if not pygame.sprite.spritecollide(stone, self.stones, False):
					self.stones.add(stone)
					self.all_sprites.add(stone)
					placed = True
			if not placed:
				self.stones.add(stone)
				self.all_sprites.add(stone)



	def event(self):
		"""
		[Ploblem 4] 사용자 입력(발사 및 재시작)을 처리합니다.

		TODO: 게임 상태(gameover)에 따라 키보드 입력(Space키, Enter키)를 처리합니다.
		- Space키: 게임이 진행 중일 때 스페이스바를 누르면 포탄이 발사되어야 합니다.
		           (단, 남은 총알이 있을 때만 발사되어야 합니다.)
		- Return/Enter키: 게임이 종료되었을 때 Return(Enter) 키를 누르면,
		           게임의 모든 상태가 초기화되고 새 게임이 시작되어야 합니다.
		"""
		for event in pygame.event.get():
			if event.type == QUIT:
				self.running = False

			if event.type == KEYDOWN:
				if not self.game_over and event.key == K_SPACE and self.bullets_remaining > 0:
					bullet = self.player.shoot()
					if bullet:
						self.all_sprites.add(bullet)
						self.bullets.add(bullet)
						self.bullets_remaining -= 1
				if self.game_over and event.key in (K_RETURN, K_KP_ENTER):
					self.game_over = False
					self.setup()



	def update(self):
		"""게임 상태 업데이트"""
		self.player.update(self.walls)
		self.stones.update(self.walls)
		self.bullets.update()
		self.check_collisions()
		self.check_game_over()

	def check_collisions(self):
		"""
		[Ploblem 5] 게임 내 충돌 검사 및 처리를 합니다.

		TODO: 두 가지 충돌(탱크와 돌, 포탄과 돌)의 결과를 각각 구현하세요.
		- 탱크-돌 충돌: 충돌 시 플레이어를 시작 지점으로 되돌려야 합니다.
		- 포탄-돌 충돌: 포탄이 돌 그룹과 충돌하면 해당 포탄과 돌은 모두 화면에서 제거되어야 하며,
		               50%의 확률로 새로운 돌이 하나 생성되어야 합니다.
		               이때 포탄이 2개 이상의 돌을 한 번에 맞췄을 때를 고려해서
		               각 돌에 대해 50%의 확률로 새로운 돌이 하나씩 생성하도록 구현하세요.
		"""

		if pygame.sprite.spritecollide(self.player, self.stones, False):
			self.player.reset()

		collisions = pygame.sprite.groupcollide(self.stones, self.bullets, True, True)
		for _stone, _bullets in collisions.items():
			if random.random() < 0.5:
				placed = False
				attempts = 0
				while not placed and attempts < 200:
					attempts += 1
					new_stone = Stone()
					if not pygame.sprite.spritecollide(new_stone, self.stones, False):
						self.stones.add(new_stone)
						self.all_sprites.add(new_stone)
						placed = True
				if not placed:
					self.stones.add(new_stone)
					self.all_sprites.add(new_stone)



	def check_game_over(self):
		"""게임 종료 조건 확인"""
		if self.player.rect.top <= 0:
			self.game_over = True
			self.final_time = pygame.time.get_ticks() - self.start_time

	def draw_text(self, text, size, x, y, color, align="center"):
		"""화면에 텍스트 그리기"""
		font = pygame.font.Font(None, 40)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect()
		if align == "center":
			text_rect.midtop = (x, y)
		elif align == "right":
			text_rect.topright = (x, y)
		elif align == "left":
			text_rect.topleft = (x, y)
		self.screen.blit(text_surface, text_rect)

	def draw(self):
		"""전체 게임 화면 그리기 """
		self.screen.fill("lightyellow")
		self.all_sprites.draw(self.screen)

		"""
		[Problem 6] 게임 정보를 화면에 그리고, 화면을 업데이트합니다.

		TODO: 게임 진행 중에 필요한 UI(시간, 총알 수)를 그리는 부분을 완성하세요.
		- 화면 좌측 상단에 시작 후 흐른 시간을 표시합니다.
		- 우측 상단에는 남은 포탄의 개수를 표시합니다.
		- 단, 게임 오버 화면에서는 이 정보들이 보이지 않아야 합니다.
		- 경과 시간과 남은 포탄의 개수를 출력하는 서식은 문제지의 예시 화면을 참고하세요.
		"""

		if self.game_over:
			self.draw_text("Mission Complete!", 70, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, "darkgreen")
			self.draw_text(f"Your Time: {self.final_time / 1000:.2f} sec", 60, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, "black")
			self.draw_text("Press Enter to Restart", 55, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.85, "gray")

		else:
			elapsed = pygame.time.get_ticks() - self.start_time
			self.draw_text(f"Time: {elapsed / 1000:.2f} sec", 40, 10, 10, "black", align="left")
			self.draw_text(f"Bullets: {self.bullets_remaining}", 40, SCREEN_WIDTH - 10, 10, "black", align="right")

		pygame.display.flip()



# --- 게임 실행 ---
if __name__ == "__main__":
	game = Game()
	game.run()
