# Agent Rules

When you need company policy, process, architecture, project history, or document context, use the `knowledgebase` MCP server first.

Usage policy:

- Use `search_docs` before guessing a filename.
- Use `get_doc` before summarizing any policy or workflow.
- Use `related_docs` when the current page may be a hub or partial view.
- Treat `content/*.md` as the canonical source of truth.
- If the MCP server has a relevant document, do not answer from memory alone.

---

## 📁 콘텐츠 구조 (Content Structure)

이 레포는 두 영역으로 명확히 분리되어 있습니다.

### 1. `content/studynote/` — CS 기초 학습 노트

- **목적**: CS 개념을 깊이 있게 이해하기 위한 학습 전용 공간
- **구성**: 01~16번 과목 폴더, 각 폴더 하위에 세부 챕터별 개념 파일
- **키워드 목록**: 각 과목 폴더에 `keyword_list.md` (사이드바에 표시됨, weight: 50)
- **작성 포맷**: YAML frontmatter(`---`) + 핵심 인사이트 3줄 요약 + 본문

```
content/studynote/
├── _index.md                        ← 전체 과목 인덱스
├── 01_computer_architecture/
│   ├── _index.md                    ← 과목 개요 (weight: 1)
│   ├── keyword_list.md              ← 키워드 전체 목록 (네비게이션, weight: 50)
│   └── 01_basic_electronics_logic/
│       ├── _index.md
│       └── 001_voltage.md, ...      ← 개별 개념 파일
└── ... (02~16 동일 구조)
```

### 2. `content/exam/` — 기술사 시험 문제 요약

- **목적**: 정보통신기술사·컴퓨터응용시스템기술사 시험 대비 요약 답안
- **구성**: 과목별 폴더 + 시험 문제 형식의 요약 파일들

```
content/exam/
├── _index.md                        ← 시험 과목 인덱스
├── 02_operating_system/             ← (130개 요약)
├── 05_database/                     ← (127개 요약)
├── 07_enterprise_systems/           ← (400개 요약)
└── ... (기타 과목)
```

---

## ✍️ 파일 작성 포맷 (studynote)

**섹션 구조 원칙:**
- `Ⅱ. 구조 및 구성요소` — 구조도(ASCII)와 구성요소 표를 함께 묶는다
- `Ⅲ. 동작원리 및 흐름도` — 원리(단계 표)와 흐름도(ASCII)를 함께 묶는다
- 표를 쓰면 반드시 한 줄 요약을 바로 아래 적는다 (`> 요약: ...`)
- 구조·흐름도는 ASCII 아트와 표 **양쪽 다** 작성한다
- `Ⅳ. 특징` — "핵심 특징" 금지, 반드시 "특징"만 사용

```yaml
---
title: "개념명 (영문명)"
date: "YYYY-MM-DD"
tags:
  - "studynote-과목태그"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ...
> 2. **가치**: ...
> 3. **판단 포인트**: ...

---

## Ⅰ. 개요 및 필요성

정의 1문장. 배경·필요성 2~3줄.

---

## Ⅱ. 구조 및 구성요소

```text
[ASCII 구조도: 박스 3~5개 + 화살표]
┌──────────┐   ┌──────────┐   ┌──────────┐
│ 구성 A   │──▶│ 구성 B   │──▶│ 구성 C   │
└──────────┘   └──────────┘   └──────────┘
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| 구성 A | ... | ... |
| 구성 B | ... | ... |
| 구성 C | ... | ... |

> 요약: [구성요소 표 한 줄 핵심 — 어떤 요소가 어떤 역할을 하는지 1문장]

---

## Ⅲ. 동작원리 및 흐름도

```text
[ASCII 흐름도: 입력 → 처리 → 출력]
입력/요구 → 핵심 처리 → 검증/통제 → 결과 출력
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 입력/요구 식별 | ... |
| 2 | 핵심 처리 | ... |
| 3 | 검증·통제 | ... |
| 4 | 출력·효과 | ... |

> 요약: [흐름 표 한 줄 핵심 — 어떤 순서로 어떻게 동작하는지 1문장]

---

## Ⅳ. 특징

| 구분 | 내용 | 판단 포인트 |
|:---|:---|:---|
| 장점 | ... | ... |
| 한계 | ... | ... |
| 비교 대상 | ... | ... |

> 요약: [특징 표 한 줄 핵심 — 핵심 장단점 또는 비교 포인트 1문장]

---

## Ⅴ. 실무 적용 및 결론

- **적용 조건**: ...
- **기술사 판단**: [조건별 선택 기준 1줄]
- **향후 방향**: ...
```

---

## ⛔ 답안 작성 절대 금지 — 추상 표현

콘텐츠 파일 작성 시 아래 추상 표현이 나오면 즉시 구체 표현으로 교체한다. **형용사·부사로 끝나는 문장은 작성하지 않는다.**

| 금지 표현 | 대체 표현 (수치·표준명·기술명 필수) |
|:---|:---|
| 성능이 좋다 / 빠르다 | p99 지연 50ms, 처리량 10,000 TPS, 캐시 적중률 95% |
| 보안이 강화된다 | AES-256, mTLS, RBAC, CVE 자동 스캔 |
| 안정적이다 | RTO 4분, RPO 15분, 가용성 99.9%, MTTR 10분 |
| 효율적이다 | CPU 70%→40%, 배포 시간 45분→8분 |
| 확장성이 있다 | HPA min2/max20, 수평 스케일아웃 30초 반응 |
| 최신 기술이다 | 기존 한계 + 신기술이 해결하는 수치를 함께 명시 |

## 🔧 작업 규칙

- **studynote에 추가**: `keyword_list.md` 참조 → 빠진 개념 파일 생성
- **exam에 추가**: 시험 문제 요약만 (개념 설명 X)
- **Zola**: `---` YAML frontmatter 사용 (TOML `+++` 금지)
- **빌드 확인**: `npm run build`
- **금지**: 빌드 체인 혼용 금지. 이전 정적 사이트 체인 관련 코드/설정과 현재 `Zola` 체인을 섞지 말 것.

## Study Note (기술사 스터디 노트)

기술 도메인 지식이 필요할 때 `content/studynote/` 아래 문서들을 우선 참조한다.

- 과목 구성: 01~16번 폴더 (각 폴더에 세부 챕터 및 키워드 목록 포함)
- 허브 문서: `content/studynote/_index.md`
- 검색 예시: `search_docs("캐시 메모리")`, `get_doc("studynote/01_computer_architecture/_index")`

## Build Baseline

- This repository currently builds with `Zola` and `Pagefind`.
- Do not introduce a second static-site build chain, extra plugin runtime, or conflicting workflow steps unless the build system is intentionally migrated.
- Use `zola build` and the existing GitHub workflow as the build baseline.
