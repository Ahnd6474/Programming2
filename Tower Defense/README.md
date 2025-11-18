# Tower Defense Game Plan

## 1. 게임 컨셉 & 목표

**컨셉**

* 위에서 내려다본 **육각 격자(hex grid)** 맵 위로 몬스터가 한 경로를 따라 이동
* 플레이어는 육각 타일에 **타워를 배치**해서 몬스터를 처리
* 체력이 0이 되면 패배, 웨이브를 버티면 승리/스코어 기록

**목표**

* 최소 기능:

  * 육각 격자 렌더링
  * 하나의 고정된 경로(path)를 따라 이동하는 적
  * 기본 타워 1종 (범위 내 자동 공격)
  * 간단한 웨이브 시스템
* 확장 가능 기능:

  * 타워 업그레이드
  * 적 타입 여러 개(빠른/탱키 등)
  * 맵 여러 개 / 난이도 조절

---

## 2. 핵심 시스템 설계

### 2.1 육각 격자 좌표계 선택

* **축(axial) 좌표계** 사용: `(q, r)`

  * 이웃 오프셋 예 (pointy-top 기준):

    * `[(+1, 0), (+1, -1), (0, -1), (-1, 0), (-1, +1), (0, +1)]`
* pygame 좌표(픽셀) ↔ hex 좌표 변환 함수 필요:

```
axial (q, r) → pixel (x, y)
pixel (x, y) → axial (q, r)
```

* 원칙:

  * `HEX_SIZE`: 육각형 한 변 길이
  * pointy-top(뾰족한 꼭짓점 위쪽) 기준으로 설계

### 2.2 맵 데이터 구조

* 맵을 그래프처럼 다루되, 구현은 간단히:

```
tiles: dict[(q, r)] -> Tile
```

* `Tile`에 들어갈 정보:

  * `coord`: (q, r)
  * `world_pos`: (x, y) 중심 픽셀 좌표
  * `is_path`: 적이 이동하는 경로인지 여부
  * `buildable`: 타워 건설 가능 여부
  * `tower`: 이 타일에 있는 타워 참조(없으면 None)

* **경로(path)**:

  * 가장 단순하게는 `path_coords: list[(q, r)]` 로 고정된 길 하나 정의
  * 적은 이 리스트를 따라 순서대로 이동

### 2.3 게임 루프 개요

기본 pygame 루프:

1. 이벤트 처리 (마우스 클릭, 종료)
2. 게임 상태 업데이트 (적 이동, 타워 공격, 투사체 이동, 충돌 판정)
3. 화면 렌더링 (타일 → 타워 → 적 → 투사체 → UI)

---

## 3. 주요 클래스 설계

이건 나중에 코드 만들 때 거의 그대로 가져다 쓰면 된다.

### 3.1 `Game` (전체 관리)

* 역할:

  * 초기화 (pygame, 화면, clock, 맵 로드)
  * 메인 루프 실행
  * 전역 상태 관리 (돈, 생명, 현재 웨이브, 게임 오버 여부)

* 주요 변수:

  * `screen`, `clock`
  * `hex_map: HexMap`
  * `enemies: pygame.sprite.Group`
  * `towers: pygame.sprite.Group`
  * `projectiles: pygame.sprite.Group`
  * `wave_manager: WaveManager`
  * `money`, `lives`, `current_wave`

### 3.2 `HexMap`

* 역할:

  * 육각 맵 생성 (타일 좌표/픽셀 계산)
  * `path_coords` 정의
  * 렌더 함수 제공

* 메서드 예:

  * `generate_hex_grid(radius or width,height)`
  * `draw(surface)`
  * `get_tile_at_pixel(x, y) -> Tile or None`

### 3.3 `Tile`

* 필드:

  * `coord` (q, r)
  * `center_x`, `center_y`
  * `is_path: bool`
  * `buildable: bool`
  * `tower: Tower | None`

* 메서드:

  * `draw(surface)` : 타일 배경 색(경로/건설불가/일반) 다르게

### 3.4 `Enemy` (적)

* pygame.sprite.Sprite 상속
* 필드:

  * `path: list[(q, r)]` 또는 미리 픽셀 리스트
  * `current_index` (path에서 현재 목표 인덱스)
  * `speed`, `hp`, `max_hp`
  * `reward` (죽었을 때 돈)
* 로직:

  * 현재 목표 지점까지 방향 벡터로 이동
  * 마지막 지점 도달 시 플레이어 `lives` 감소 후 제거

### 3.5 `Tower` (타워)

* pygame.sprite.Sprite 상속
* 필드:

  * `range` (사거리, 픽셀 또는 hex 거리)
  * `fire_rate` (발사 주기, 초/발)
  * `last_shot_time`
  * `damage`
  * `tile` (어느 타일 위인지)
* 로직:

  * 매 프레임마다:

    * 사거리 내 적 탐색
    * 가장 가까운/가장 앞에 있는 적 선택
    * 쿨다운 지나면 `Projectile` 생성

### 3.6 `Projectile` (투사체)

* Sprite
* 필드:

  * `target: Enemy`
  * `speed`
  * `damage`
* 로직:

  * target 방향으로 이동
  * target과 충돌 시 적 HP 감소, 자기 자신 제거

### 3.7 `WaveManager` (웨이브 관리)

* 필드:

  * `wave_definitions`: 각 웨이브 별 적 수, 스폰 간격, 적 타입
  * 현재 웨이브, 다음 스폰 시간, 남은 적 수
* 메서드:

  * `update(dt, game)`:

    * 일정 시간 간격으로 적 스폰
    * 웨이브 종료 체크
  * `start_next_wave()`

### 3.8 간단 UI

* 돈, 생명, 현재 웨이브 표시
* 하단/측면에 타워 선택 UI (기본 타워 하나면 매우 단순)

  * 클릭으로 “건설 모드” 진입 → 빈 타일 클릭 시 타워 배치

---

## 4. 육각 격자 세부 구현 계획

### 4.1 렌더링

* 각 타일 중심과 육각형 꼭짓점 계산:

  * `HEX_SIZE` 기반으로 6개의 정점 좌표 계산 (한 번 precompute)
* `pygame.draw.polygon` 으로 타일 테두리/배경 그리기
* 색 분리:

  * 일반 타일: 연한 회색
  * path 타일: 갈색
  * 건설 불가: 어두운 회색

### 4.2 마우스 클릭 → 타일 선택

* `HexMap.get_tile_at_pixel(x, y)`:

  * pixel → axial 변환 후 가장 가까운 hex를 골라서 반환
* 건설 모드일 때:

  * `tile.buildable and tile.tower is None` 이면 타워 생성

---

## 5. 개발 단계 로드맵

이 순서대로 하면 삽질이 최소다.

### 1단계: 기본 pygame 틀 + 빈 육각 맵

* pygame 윈도우 열기, 메인 루프, FPS 고정
* `HexMap` 만들고 hex 타일만 그리기
* 마우스 클릭 시 선택한 타일 하이라이트 테스트

### 2단계: 경로(path) 정의 & 시각화

* `path_coords` 리스트 몇 개 지정
* 해당 타일 `is_path=True`로 표시
* 경로 타일을 다른 색으로 렌더

### 3단계: Enemy 구현 및 이동

* `Enemy` 클래스 구현
* path를 따라 이동하는 적 스폰
* 마지막 지점 도달 시 생명 감소 로직 추가
* 적 HP, 속도, 기본 애니메이션(그냥 사각형/원 이동이면 충분)

### 4단계: Tower & Projectile 구현

* `Tower`를 건설하고, 사거리 내 적 공격
* `Projectile` 생성/이동/충돌 처리
* 적 죽이면 돈 증가

### 5단계: WaveManager & 게임 진행

* 간단한 웨이브 정의:

  * 예: 웨이브 1: 10마리, 1초 간격 / 웨이브 2: 15마리, 0.8초 간격 등
* 모든 적 제거 시 “다음 웨이브” 버튼 활성화
* 웨이브가 올라갈수록 적 HP 증가

### 6단계: UI & 품질 개선

* 상단 HUD: 돈, 생명, 웨이브 표시
* 타워 선택/건설 UI 버튼
* 간단한 사운드 효과(발사, 죽음) 추가 가능
* 게임 오버/게임 클리어 화면

---

## 6. 필수/선택 기능 정리

**필수**

* 육각 격자 렌더 / 클릭
* 고정 경로, 적 이동
* 타워 건설, 사거리 공격
* 웨이브 시스템
* 기본 UI (돈/생명/웨이브)

**선택**

* 여러 타워 타입 (슬로우, 스플래시, 긴사거리 등)
* 여러 적 타입
* 타워 업그레이드
* 맵 여러 개 + 맵 선택 메뉴
* 저장/로드, 난이도 옵션

---

이 정도면 설계는 충분히 잡혔다.
다음 단계로 바로 이어서 하고 싶으면, 예를 들어:

* “1단계 코드 짜 줘 (pygame 기본 + 육각 맵 렌더)”
* “Enemy 포함한 3단계까지 한 파일로 코드 써 줘”

처럼 단계 지정해서 말해. 그러면 이 설계 기준으로 통짜 코드 바로 뽑아줄 수 있다.
