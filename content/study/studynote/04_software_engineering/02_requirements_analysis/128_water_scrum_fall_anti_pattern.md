+++
weight = 128
title = "128. Water-Scrum-Fall (안티패턴) - 하이브리드 Agile의 함정"
date = "2026-04-19"
[extra]
categories = "studynote-software-engineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Water-[[658_agile_scrum_roles|Scrum]]-Fall은 **요구사항은 Waterfall식(상의하달), 개발만 [[658_agile_scrum_roles|Scrum]], 배포는 다시 Waterfall식(긴 릴리스 주기)**으로 운영되는 안티패턴이며, Agile의 외형만 차용하고 핵심 원칙은 실행하지 않는다.
> 2. **가치**: 조직이 "우리는 Agile을 한다"고 주장하지만 **실제로는 계획·배포에서 Waterfall을 유지**하면 Agile의 이점(빠른 피드백·적응)이 사라지고, 개발팀만 [[067_sprint_timebox|스프린트]] 압박을 받는 악순환이 발생한다.
> 3. **판단 포인트**: 진정한 [[004_agile_relation|Agile]] 전환은 **요구사항 발견(Discovery)·배포([[090_configuration_item|CI]]/CD)·조직 문화까지 전체 흐름**의 변화가 필요하며, 개발 프로세스만 바꾸는 것은 부분 적용에 불과하다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    Water-Scrum-Fall 구조                              │
├───────────────────────────────────────────────────────┤
│  [Water] — 요구사항: 6개월 전 확정, 변경 불가        │
│     ↓                                                 │
│  [Scrum] — 개발: 2주 스프린트, 데일리 스크럼          │
│     ↓                                                 │
│  [Fall]  — 배포: 3개월 릴리스, 수동 QA, 승인 절차    │
│                                                       │
│  문제: 개발만 Agile, 전후는 Waterfall                │
│  → Agile 이점 소멸, 개발팀만 고통                    │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Water-[[658_agile_scrum_roles|Scrum]]-Fall은 **고속도로([[658_agile_scrum_roles|Scrum]]) 양쪽에 비포장 도로(Water·Fall)**를 붙인 것이다. 고속도로에서 빨라도 비포장에서 막히면 의미 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 진정한 [[004_agile_relation|Agile]] vs Water-[[658_agile_scrum_roles|Scrum]]-Fall

| 비교 | 진정한 [[004_agile_relation|Agile]] | Water-[[658_agile_scrum_roles|Scrum]]-Fall |
|:---|:---|:---|
| **요구사항** | 지속적 발견 | **사전 확정** |
| **개발** | [[067_sprint_timebox|스프린트]] | [[067_sprint_timebox|스프린트]] |
| **배포** | [[090_configuration_item|CI]]/CD 지속 배포 | **분기별 릴리스** |
| **피드백** | 매 [[067_sprint_timebox|스프린트]] | **배포 후에야** |

- **📢 섹션 요약 비유**: 진정한 Agile은 전체 [[123_pipe|파이프]]라인이 물처럼 흐르는 것, WSF는 [[123_pipe|파이프]] 중간만 넓은 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | Waterfall | [[004_agile_relation|Agile]] | WSF |
|:---|:---|:---|:---|
| **계획** | 전체 | 적응 | **전체 (Water)** |
| **개발** | 순차 | 반복 | 반복 ([[658_agile_scrum_roles|Scrum]]) |
| **배포** | 빅뱅 | 지속 | **빅뱅 (Fall)** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### WSF 탈출 방법
1. 요구사항: Discovery [[067_sprint_timebox|Sprint]] 도입 (지속적 탐색).
2. 배포: [[090_configuration_item|CI]]/CD [[123_pipe|파이프]]라인 구축 (자동화).
3. 조직: Product Owner 권한 강화.
4. 문화: 실패 허용·학습 문화 정착.

---

## Ⅴ. 기대효과 및 결론

Water-[[658_agile_scrum_roles|Scrum]]-Fall은 **"[[004_agile_relation|Agile]] 흉내"의 대표 안티패턴**이며, 진정한 Agile은 개발뿐 아니라 **요구사항 발견·배포·조직 문화의 총체적 전환**을 요구한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Water-[[658_agile_scrum_roles|Scrum]]-Fall** | [[004_agile_relation|Agile]] 부분 적용 안티패턴 |
| **[[090_configuration_item|CI]]/CD** | Fall(배포) 해결 핵심 |
| **Discovery [[067_sprint_timebox|Sprint]]** | Water(요구사항) 해결 |
| **[[652_devops_calms_culture|DevOps]]** | 개발-운영 통합 (Fall 해소) |
| **[[004_agile_relation|Agile]] Transformation** | 전체 흐름 변환 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Waterfall (전통, ~2000s)]
    │
    ▼
[Agile 도입 시도 (2001~) — Scrum만 적용]
    │
    ▼
[Water-Scrum-Fall (안티패턴 인식, 2010~)]
    │
    ▼
[DevOps + CI/CD (2015~) — Fall 해소]
    │
    ▼
[현재: 전체 흐름 Agile — Discovery → Dev → Deploy 통합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Water-[[658_agile_scrum_roles|Scrum]]-Fall은 **고속도로 양쪽에 비포장 도로**를 붙인 거예요.
2. 고속도로([[658_agile_scrum_roles|Scrum]])에서 빨리 달려도 비포장(Water·Fall)에서 **막혀서** 의미 없어요.
3. 전체 도로를 **다 포장([[004_agile_relation|Agile]] 전환)**해야 빠르게 갈 수 있답니다!
