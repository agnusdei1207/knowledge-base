# 📚 Study — 기술사 CS 학습 노트 (Zola 정적 사이트)

Zola 기반 개인 지식베이스. **CS 기초 학습(studynote)** 과 **기술사 시험 요약(exam)** 을 분리하여 관리한다.

---

## 🗂️ 콘텐츠 두 영역 — 절대 섞지 말 것

| 영역 | 경로 | 목적 | 대상 |
|---|---|---|---|
| **스터디 노트** | `content/studynote/` | CS 개념 깊이 이해, 학습 전용 | 모든 CS 개념 |
| **기술사 시험** | `content/exam/` | 시험 문제 형식 요약 답안 | 기출·예상 문제 |

> ⚠️ **AI 모델 주의**: studynote와 exam은 용도가 완전히 다르다.  
> studynote에 시험 요약을 넣거나, exam에 개념 설명을 넣으면 **절대 안 된다**.

---

## 📁 디렉토리 구조

```
content/
├── studynote/                        ← CS 기초 학습 노트 (16개 과목)
│   ├── _index.md                     ← 전체 과목 인덱스
│   ├── 01_computer_architecture/
│   │   ├── _index.md                 ← 과목 개요 (weight: 1)
│   │   ├── keyword_list.md           ← 키워드 전체 목록 + 링크 (weight: 50, 사이드바 표시)
│   │   ├── 01_basic_electronics_logic/
│   │   │   ├── _index.md             ← 챕터 인덱스
│   │   │   ├── 001_voltage.md        ← 개별 개념 파일
│   │   │   ├── 002_current.md
│   │   │   └── ...
│   │   ├── 02_data_representation_arithmetic/
│   │   └── ... (챕터 폴더)
│   ├── 02_operating_system/
│   └── ... (02~16 동일 구조)
│
└── exam/                             ← 기술사 시험 요약 (문제 형식)
    ├── _index.md
    ├── 02_operating_system/
    ├── 05_database/
    └── ...
```

---

## 🏷️ 파일 명명 규칙 — 반드시 준수

### studynote 파일명

```
NNN_영문슬러그.md
```

- `NNN`: 3자리 0패딩 숫자 (001, 002, ..., 999)
- `영문슬러그`: 소문자 + 언더스코어만 허용, 대문자 절대 금지
- 과목 내에서 번호는 **전역 고유** (챕터 구분 없이 과목 전체에서 중복 없음)

**✅ 올바른 예시**

```
001_voltage.md
042_nand_gate_universal.md
285_api_gateway_auth_throttling.md
```

**❌ 금지 패턴**

```
001_topic_1.md          ← topic_N 패턴 금지
042_NAND_Gate.md        ← 대문자 금지
085_관리.md              ← 한글 금지
process.md              ← 번호 없는 generic 이름 금지
audit.md                ← 번호 없는 generic 이름 금지
042_concept_42.md       ← concept_N 패턴 금지
```

### 폴더 명명 규칙

```
NN_영문슬러그/
```

- 과목 폴더: `01_computer_architecture` ~ `16_bigdata`
- 챕터 폴더: `01_basic_electronics_logic`, `02_data_representation_arithmetic`, ...
- 번호 순서가 파일 순서와 정확히 일치해야 함
- `uncategorized/` 폴더에 파일을 방치하면 안 됨 — 반드시 올바른 챕터 폴더에 배치

---

## 📝 studynote 파일 작성 포맷

```yaml
---
title: "개념명 (영문명)"
date: "YYYY-MM-DD"
tags:
  - "studynote-과목태그"
weight: NNN
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ...
> 2. **가치**: ...
> 3. **판단 포인트**: ...

---

## Ⅰ. 개요 및 필요성

...

## Ⅱ. 아키텍처 및 핵심 원리

...

## Ⅲ. 융합 비교 및 다각도 분석

...

## Ⅳ. 실무 적용 및 기술사적 판단

...

## Ⅴ. 기대효과 및 결론

...
```

### 태그 규칙 (과목별 고정값)

| 과목 폴더 | 태그 |
|---|---|
| `01_computer_architecture` | `studynote-computer-architecture` |
| `02_operating_system` | `studynote-operating-system` |
| `03_network` | `studynote-network` |
| `04_software_engineering` | `studynote-software-engineering` |
| `05_database` | `studynote-database` |
| `07_enterprise_systems` | `studynote-enterprise-systems` |
| `08_algorithm_stats` | `studynote-algorithm-stats` |
| `09_security` | `studynote-security` |
| `10_ai` | `studynote-ai` |
| `11_design_supervision` | `studynote-design-supervision` |
| `12_it_management` | `studynote-it-management` |
| `13_cloud_architecture` | `studynote-cloud-architecture` |
| `14_data_engineering` | `studynote-data-engineering` |
| `15_devops_sre` | `studynote-devops-sre` |
| `16_bigdata` | `studynote-bigdata` |

---

## 🔑 keyword_list.md — 과목별 내비게이션 핵심 파일

각 과목 폴더 최상위에 `keyword_list.md` 가 있다. 이 파일이 **사이드바 내비게이션** 역할을 한다.

### 형식

```markdown
---
title: "키워드 목록 — 01 컴퓨터 구조"
weight: 50
---

1. [전압 (Voltage)](/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/)
2. [전류 (Current)](/studynote/01_computer_architecture/01_basic_electronics_logic/002_current/)
...
```

### keyword_list 관리 규칙

- 링크 형식: `/studynote/{과목폴더}/{챕터폴더}/{파일슬러그}/`
- 파일을 추가하면 반드시 keyword_list에도 링크 추가
- 파일을 리네임하면 반드시 keyword_list 링크도 동일하게 수정
- 링크가 깨지면 사이드바에서 404 발생 → 반드시 검증 후 커밋

---

## 📐 16개 과목 목록

| 번호 | 폴더명 | 과목 |
|---|---|---|
| 01 | `01_computer_architecture` | 컴퓨터 구조 |
| 02 | `02_operating_system` | 운영체제 |
| 03 | `03_network` | 네트워크 |
| 04 | `04_software_engineering` | 소프트웨어 공학 |
| 05 | `05_database` | 데이터베이스 |
| 07 | `07_enterprise_systems` | 경영정보시스템 |
| 08 | `08_algorithm_stats` | 알고리즘·통계 |
| 09 | `09_security` | 정보보안 |
| 10 | `10_ai` | 인공지능 |
| 11 | `11_design_supervision` | 설계·감리 |
| 12 | `12_it_management` | IT 경영관리 |
| 13 | `13_cloud_architecture` | 클라우드 아키텍처 |
| 14 | `14_data_engineering` | 데이터 엔지니어링 |
| 15 | `15_devops_sre` | DevOps·SRE |
| 16 | `16_bigdata` | 빅데이터 |

---

## 🛠️ 개발 명령어

```bash
npm ci                # 의존성 설치
npm run build         # Zola 검증 후 빌드 출력 자동 삭제
npm run build:keep    # 결과 확인이 필요할 때 public/ 유지
npm run build:search  # 보존한 public/에 Pagefind 검색 색인 생성
npm run clean         # 모든 로컬 빌드·임시 출력 삭제
npm run dev           # 로컬 개발 서버 (http://localhost:8080/study)
```

`npm run build`는 성공·실패와 관계없이 `public/`, `public_new/`, `public_temp/`, `temp_public/`, `temp_public_vN/`을 정리한다. `npm run build:keep`으로 결과를 보존했다면 필요할 때만 `npm run build:search`를 실행하고, 확인이 끝난 직후 `npm run clean`으로 정리한다. Pagefind 전체 색인은 배포 워크플로에서 자동 생성하므로 일반 콘텐츠 검증에는 포함하지 않는다. 이 경로들은 생성 산출물 전용이며 소스 파일을 두지 않는다.

---

## ⚙️ 기술 스택

- **Static Site Generator**: [Zola](https://www.getzola.org/)
- **Frontmatter**: YAML (`---`) 형식만 사용 — TOML (`+++`) 절대 금지
- **Markdown**: GitHub Flavored Markdown
- **Deploy**: GitHub Pages (`.github/workflows/`)

---

## 🚫 절대 하지 말 것 (AI 모델 필독)

1. **TOML frontmatter 사용 금지** — `+++` 대신 반드시 `---` 사용
2. **한글 파일명 금지** — 영문 슬러그만 허용
3. **대문자 파일명 금지** — `OFDMA.md` → `ofdma.md`
4. **`topic_N`, `concept_N` 패턴 금지** — 반드시 의미있는 영문 이름
5. **`uncategorized/` 에 파일 방치 금지** — 올바른 챕터 폴더에 배치
6. **번호 중복 금지** — 과목 전체 통틀어 번호 고유해야 함
7. **keyword_list 링크 깨뜨리기 금지** — 파일 리네임 시 링크도 동시에 수정
8. **studynote/exam 혼합 금지** — 용도에 맞는 폴더에만 작성
9. **임시 스크립트 파일 루트에 방치 금지** — `fix_*.py`, `temp_*.py` 등은 작업 후 즉시 삭제
10. **빌드 체인 혼용 금지** — 이전 정적 사이트 체인 흔적과 현재 `Zola` 체인을 섞지 말 것

---

## ✅ 파일 추가/수정 시 체크리스트

새 파일을 추가하거나 기존 파일을 수정할 때 반드시 확인:

- [ ] 파일명이 `NNN_영문슬러그.md` 형식인가?
- [ ] 번호가 과목 내 다른 파일과 중복되지 않는가?
- [ ] 올바른 챕터 폴더에 배치했는가?
- [ ] keyword_list.md 에 링크를 추가/수정했는가?
- [ ] YAML frontmatter (`---`)를 사용했는가?
- [ ] 태그가 과목에 맞는 `studynote-{과목태그}` 인가?
- [ ] `npm run build`가 오류 없이 통과하고 빌드 출력이 자동 정리됐는가?
