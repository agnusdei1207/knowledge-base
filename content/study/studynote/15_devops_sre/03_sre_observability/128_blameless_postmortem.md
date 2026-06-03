---
title: 128. Blameless Postmortem - 비난 없는 장애 사후 분석
date: '2026-04-19'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Blameless Postmortem은 **장애 발생 후 '누가' 실수했는가가 아니라 '무엇이(시스템·프로세스)' 실패했는가**를 분석하여 재발을 방지하는 [[100_sre_site_reliability_engineering_error_budget|SRE]] 핵심 문화이다.
> 2. **가치**: 개인을 비난하면 **실수를 숨기는 문화**가 형성되어 장애 원인이 은폐되지만, Blameless 문화에서는 **솔직한 공유**가 가능하여 시스템 개선·자동화·프로세스 강화로 이어진다.
> 3. **판단 포인트**: Postmortem 문서에는 **타임라인·영향 범위·근본 원인(5 Whys)·Action Items**이 포함되며, 모든 주요 장애 후 필수 작성하고 **팀 전체에 공유**한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    Blameless Postmortem 구조                          │
├───────────────────────────────────────────────────────┤
│  1. 장애 요약: 무엇이 언제 발생했는가               │
│  2. 영향: 사용자 수·다운타임·매출 손실              │
│  3. 타임라인: 분 단위 이벤트 기록                    │
│  4. 근본 원인: 5 Whys 분석                           │
│  5. Action Items: 재발 방지 조치 (담당자·기한)       │
│  6. 교훈: 잘한 점·개선할 점                          │
│                                                       │
│  원칙: 사람이 아닌 시스템·프로세스를 개선한다        │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Blameless Postmortem은 항공 사고 조사처럼 **"조종사가 나쁘다"가 아니라 "계기판 설계가 혼동을 유발했다"**를 찾는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 5 Whys 예시

| Why | 답 |
|:---|:---|
| **Why 1** | DB 연결 풀 고갈 |
| **Why 2** | 슬로우 [[298_qkv_attention|쿼리]] 급증 |
| **Why 3** | [[154_database_index_b_tree_search_optimization|인덱스]] 미적용 |
| **Why 4** | [[330_code_review|코드 리뷰]] 시 [[298_qkv_attention|쿼리]] 검토 누락 |
| **Why 5** | **[[298_qkv_attention|쿼리]] 리뷰 프로세스 부재** |

→ Action Item: [[298_qkv_attention|쿼리]] 리뷰 [[435_checklist_based_testing|체크리스트]] 도입.

- **📢 섹션 요약 비유**: 5 Whys는 의사가 "왜 열이 나?"→"왜 감염?"→"왜 면역력 저하?"로 **근본 원인을 파는 진단법**이다.

---

## Ⅲ. 비교 및 연결

| 비교 | Blame 문화 | Blameless 문화 |
|:---|:---|:---|
| **실수** | 숨김 | **공유** |
| **분석** | 범인 찾기 | **시스템 개선** |
| **재발** | 반복 | **방지** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### Postmortem 도구
- **Incident.io**: 자동 타임라인·Postmortem [[087_process_state_transition|생성]].
- **Jeli**: Postmortem 관리 플랫폼.
- **Confluence/Notion**: 문서 기반 Postmortem.

---

## Ⅴ. 기대효과 및 결론

Blameless Postmortem은 **[[100_sre_site_reliability_engineering_error_budget|SRE]] 문화의 가장 중요한 실천**이며, 장애를 **학습 기회**로 전환하는 조직의 성숙도를 보여준다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Blameless** | 비난 없는 분석 문화 |
| **5 Whys** | 근본 원인 분석 기법 |
| **Action Items** | 재발 방지 조치 |
| **타임라인** | 분 단위 장애 이벤트 기록 |
| **[[806_incident_response|Incident Response]]** | Postmortem 이전의 장애 대응 |

### 📈 관련 키워드 및 발전 흐름도

```text
[장애 → 범인 찾기 (전통, ~2010s)]
    │
    ▼
[Blameless Postmortem (Google SRE, 2003~2016)]
    │
    ▼
[Postmortem 템플릿 표준화 (2018~)]
    │
    ▼
[자동 Postmortem 생성 (Incident.io, 2022~)]
    │
    ▼
[현재: AI Postmortem — 로그 분석→근본 원인·Action 자동 추천]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Blameless Postmortem은 **"누가 틀렸어?"가 아니라 "왜 틀렸어?"**를 찾는 거예요.
2. 사람을 혼내면 다음에 **실수를 숨기게** 되니까, 시스템을 고쳐요.
3. 비행기 사고 조사처럼 **원인을 찾아 고치면** 같은 사고가 다시 안 일어나요!
