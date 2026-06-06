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

---

## 🔧 작업 규칙

- **studynote에 추가**: `keyword_list.md` 참조 → 빠진 개념 파일 생성
- **exam에 추가**: 시험 문제 요약만 (개념 설명 X)
- **Quartz**: `---` YAML frontmatter 사용 (TOML `+++` 금지)
- **빌드 확인**: `npm run build`
- **금지**: Zola, Pagefind, `templates/`, `static/assets/`, `config.toml` 재도입 금지

## Study Note (기술사 스터디 노트)

기술 도메인 지식이 필요할 때 `content/studynote/` 아래 문서들을 우선 참조한다.

- 과목 구성: 01~16번 폴더 (각 폴더에 세부 챕터 및 키워드 목록 포함)
- 허브 문서: `content/studynote/_index.md`
- 검색 예시: `search_docs("캐시 메모리")`, `get_doc("studynote/01_computer_architecture/_index")`

## Quartz Migration

- This repository is now a Quartz site. Do not reintroduce Zola, Pagefind, `templates/`, `static/assets/`, or `config.toml`.
- Keep the Quartz implementation aligned with `../codex-skills`; project-specific changes should be limited to site metadata, CI/CD, deployment paths, and this repository's `content/`.
- Use `npm run build` to verify the site.
