# CSPE 노트 형식 규격

기준 파일(골드 스탠다드): `src/content/docs/notes/02-hardware/001_von_neumann_vs_harvard.md` (2026-08-19 재작성본)

## 1. 디렉터리·파일명

| 과목 디렉터리 | 노트 수 | tags |
|:---|---:|:---|
| `01-basic-theory` | 62 | `notes-basic-theory` |
| `02-hardware` | 94 | `notes-hardware` |
| `03-software` | 229 | `notes-software` |
| `04-network` | 116 | `notes-network` |
| `05-security` | 147 | `notes-security` |
| `06-evaluation` | 51 | `notes-evaluation` |
| `07-law-policy` | 45 | `notes-law-policy` |
| `08-latest-tech` | 226 | `notes-latest-tech` |

- 파일명: `{3자리번호}_{snake_case_영문}.md` (예: `014_cache_coherence_protocol.md`)
- 임시 사본은 저장소 밖에 둔다. `*.local.md`는 `.gitignore` 대상이지만 Astro 콘텐츠 컬렉션에는 잡혀 중복 페이지가 생긴다.

## 2. 프론트매터

```yaml
---
sidebar:
  order: 14
  label: "014. 제목: 부제 (English Title)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "제목: 부제 (English Title)"
date: "YYYY-MM-DDTHH:MM:SS+09:00"
tags:
  - "notes-hardware"
weight: 14
extra:
  question_no: "014"
  source_status: "기출"
  source_history: "123회, 135회"
  priority: 70
  priority_note: "한줄 설명"
---
```

## 3. 7섹션 구조

제목을 그대로 사용한다. 877개 파일 실측 일치.

- `## Ⅰ. 개요`
- `## Ⅱ. 특징`
- `## Ⅲ. 구조 및 구성요소`
- `## Ⅳ. 흐름도`
- `## Ⅴ. 종류 및 비교`
- `## Ⅵ. 실무 고려사항 및 대책`
- `## Ⅶ. 결론`

## 4. 섹션별 용어 설명

각 섹션 바로 아래에 배치하되, **그 섹션에서 처음 굵게 쓰는 용어만** 선정의한다. 앞 섹션에서 정의한 용어의 재정의는 금지(중복 정의 = 검수 위반).

```markdown
<details><summary>용어 설명</summary>

- **한국어(English)**: 작동방식·맥락을 포함한 정의.

</details>
```

- 단순 `~이다`, `~을 말한다`, `~을 의미한다` 종결 금지. 무엇을 어떻게 하는지가 정의에 들어가야 한다.
- 본문의 모든 굵은 용어는 어딘가의 용어 설명 블록에 정의돼 있어야 한다(미정의 굵은 용어 0건이 검수 기준).

## 5. 섹션별 필수 구성

| 섹션 | 필수 구성 |
|:---|:---|
| Ⅲ | ` ```text ` 트리 다이어그램 → `선의 의미:` 범례 한 줄 → `\| 구성요소 \| 책임 \|` 2열 표 |
| Ⅳ | ` ```text ` 분기 흐름도 → `분기 결과:` 해설 한 줄 |
| Ⅴ | `적용 기준` / `핵심 특징` / `한계` 3행 비교표 (열 = 비교 대상) |
| Ⅵ | `\| 문제 \| 대책 \| 효과 \|` 3열 표 |
| Ⅶ | 선택 기준을 담은 결론 불릿 |

## 6. 한줄 요약

7개 섹션 **전부**가 `#### 한줄 요약` + 불릿 1개로 끝난다(총 6,724개 실측).

- **요약이 아니라 통찰**이다. 본문 나열의 재탕이 아니라 그 섹션이 드러낸 트레이드오프·판단 기준을 짚는다.
- 종결은 서술형 완결문(`~한다`, `~이다`). 구형 노트의 명사구 종결은 레거시다.
- 존댓말(`~입니다`, `~습니다`) 금지. 978개 중 29개만 잔존하는 오염이다.

## 7. 금지 사항

- **키워드 날조**: 실제 시험 범위·표준 교재·규격서에 없는 용어를 만들어 쓰지 않는다. `~Controller`, `~Selector`, `~Evaluator`, `~Enforcer`, `~Verifier`, `~Analyzer`, `~Planner` 접미사 조어는 출처가 불명확하면 사용을 보류한다. 실재 용어만 채택한다(예: 버스 트랜잭션명 BusRd·BusRdX·BusUpgr, 프로토콜명 MESI·MOESI·MESIF).
- **굵은 구조 표제**: `**동작 원리**` 같은 굵은 글씨 소제목을 쓰지 않는다(검수 기준: 굵은 구조 표제 0건). Ⅳ의 해설은 `분기 결과:` 평문으로 쓴다.
- 7섹션 구조 훼손·형식 축약.

## 8. 검증

1. `npm.cmd run check` — 오류·경고·힌트 0건
2. `npm.cmd run build` — 982 pages / Pagefind 982 HTML 통과
3. 파일별 점검 항목: 미정의 굵은 용어 · 종결 규칙 위반 · 중복 정의 · 미사용 핵심 용어 · 굵은 구조 표제 각 0건
4. 작업 후 `agent-guides/CSPE_PROGRESS.md`에 체크포인트 추가
