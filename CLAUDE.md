# CLAUDE.md

## 프로젝트 개요

pymahjongutil - 리치 마작(Riichi Mahjong) 점수 계산 Python 라이브러리

손패 분석(샨텐, 아가리 판정, 분할) → 야쿠 판정(42종) → 부수/판수 계산 → 점수 분배까지의 전체 파이프라인 구현

## 기술 스택

- Python: 3.13
- 패키지 매니저: uv (hatchling 빌드 백엔드)
- 린터/포매터: ruff (format + check)
- 타입체크: mypy (strict mode)
- 테스트: pytest + pytest-cov (커버리지 95% 이상)
- 의존성: numpy
- pre-commit 훅

## 명령어

- `uv sync` — 의존성 설치
- `uv run pytest --cov=pymahjongutil --cov-report=term-missing` — 커버리지 포함 테스트
- `uv run mypy pymahjongutil` — 타입 체크
- `uv run ruff check . && uv run ruff format .` — 린트 + 포맷
- `pre-commit run --all-files` — 전체 훅 실행

## 프로젝트 구조

- `schema/` — 데이터 구조 (Tile, TileIndex, TileCount, Hand, Call, Division, DivisionPart, AgariInfo, PointInfo, YakuRule, EfficiencyData)
- `enum/` — 열거형 (TileType, CallType, DivisionPartType, YakuEnum, WindEnum, FuReason 등)
- `hand_parser.py` — 문자열 → Hand 파싱 (예: `"123p45699s,chi123s,pon5-55z"`)
- `hand_checker/` — 손패 검증 (NormalChecker, SevenPairChecker, ThirteenOrphanChecker, RiichiChecker)
- `yaku_checker/` — 42개 야쿠 패턴 체커 (각각 독립 클래스)
- `point_calculator/` — 점수 계산 (FuCalculator, HanCalculator, PointCalculator)
- `rule/` — 룰 정의 (RiichiMahjongRule, DefaultRuleDictFactory)

## 코딩 컨벤션

- Enum: `UpperStrEnum` 패턴 — `str, Enum` 상속 + `_generate_next_value_`로 `name.upper()` 반환
- 타입 안전 int 서브클래스: `__new__`에서 범위 검증

## 개발 워크플로우

### 작업 유형 1: 새 엔티티(데이터 타입) 추가

예: Tile, Hand, Division 같은 새로운 데이터 구조

1. 필요한 열거형이 있으면 `enum/`에 추가
2. `schema/`에 dataclass 생성
3. 기존 모듈에서 import하여 연동
4. 테스트 작성

### 작업 유형 2: 새 로직 모듈 추가

예: 새로운 checker, calculator 등 비즈니스 로직

1. ABC 기반 인터페이스 정의 (기존 베이스 클래스가 있으면 상속)
2. 구현 클래스 작성
3. 기존 시스템에 등록/연동
4. 테스트 작성

### 작업 유형 3: 외부 API(공개 인터페이스) 추가

예: 라이브러리 사용자가 호출할 새로운 함수/클래스

1. 공개 함수/클래스 시그니처 설계 (입출력 타입 먼저 확정)
2. 내부 모듈 조합으로 구현
3. docstring 작성 (공개 API이므로)
4. 테스트 작성 (사용자 관점 시나리오)

### 공통 규칙

- 개발 순서: 타입/스키마 → 로직 → 테스트
- import 방향: `enum → schema → 로직 모듈` (역방향 금지)
- `__init__.py`에서 re-export하지 않음, 전체 경로 import
- 팩토리 메서드: `@staticmethod` + `create_from_*` 네이밍
