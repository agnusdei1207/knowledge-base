---
title: "칸반 (Kanban)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 37
---

# 📖 【암기용】 개념 완전 이해

> 목적: Kanban을 처음 보는 사람도 WIP 제한과 흐름 관리의 의미를 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: Kanban은 작업을 시각화하고 WIP를 제한해 흐름을 관리하는 방식
- **왜 필요한가**: 개발·운영 업무는 동시에 시작한 일이 많을수록 대기와 전환 비용이 늘어난다. Kanban은 작업 수를 제한해 lead time과 bottleneck을 드러낸다.
- **핵심 직관**: 도로에 차량이 과도하게 들어오면 속도가 떨어지므로 진입량을 제한해 전체 통과 시간을 관리하는 방식이다.

## 깊이 이해
- **배경·문제의식**: 팀은 많은 일을 병렬로 시작하면 바빠 보이지만 완료 건수는 줄어든다. 특히 운영 요청, 결함 수정, 유지보수는 sprint 계획보다 흐름 관리가 더 적합하다. Kanban은 board, WIP limit, pull system, cumulative flow diagram으로 병목을 관찰한다.
- **작동 원리**: 작업은 To Do, In Progress, Review, Done 같은 열을 이동한다. 각 열에는 WIP limit을 둔다. 새 작업은 앞 단계 여유가 생길 때 당겨오며, lead time과 cycle time으로 흐름을 측정한다.
- **비유**: 병원 접수-진료-검사-수납 대기열에서 검사실 수용 인원을 제한해야 전체 대기 시간이 예측 가능해지는 것과 같다.
- **구체 예시**: Review 열 WIP limit이 3인데 7건이 쌓이면 개발을 더 시작하지 않고 리뷰 병목을 먼저 해소한다. 이후 cycle time p85가 8일에서 5일로 감소하는지 확인함.
- **흔한 오해·주의점**: Kanban은 일정이 없는 자유 작업이 아니다. WIP limit, service class, flow metrics가 없으면 단순 보드판에 그친다.

## 연결 개념
- WIP Limit: 동시에 진행 가능한 작업 수 제한
- Lead Time/Cycle Time: 요청부터 완료, 시작부터 완료까지 걸린 시간
- Cumulative Flow Diagram: 단계별 작업 누적량으로 병목을 보는 차트

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Kanban 답안은 보드 설명이 아니라 WIP 제한, pull system, lead time/cycle time으로 흐름 병목을 통제하는 구조를 보여야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Kanban은 작업 흐름을 시각화하고 WIP limit으로 병목과 대기 시간을 관리하는 pull 기반 방법이다.
> 2. **가치**: lead time, cycle time, throughput, CFD로 납기 예측성과 흐름 병목을 수치화한다.
> 3. **판단 포인트**: 반복 sprint보다 운영 요청, 유지보수, 결함 처리처럼 변동 유입 업무에 적합하다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Kanban 구조 이해 확인 | visual board, WIP limit, pull, flow metrics | To Do/In Progress/Done 보드만 설명 |
| 흐름 지표 판단 확인 | lead time, cycle time, throughput, CFD | 생산성 표현만 사용하고 수치 지표 누락 |
| Scrum과 선택 기준 확인 | sprint cadence vs continuous flow | Scrum보다 자유로운 방식으로 오해 |

> 요약: Kanban 문제는 작업 시각화보다 WIP 제한과 흐름 지표로 병목을 관리하는 판단을 요구한다.

---

## Ⅰ. 개요 및 필요성

Kanban은 WIP 제한 기반 흐름 관리 방식이다.
동시 작업이 증가하면 대기열, context switching, review 병목이 늘어난다.
Kanban은 시각화와 pull system으로 lead time과 cycle time을 통제함.

---

## Ⅱ. 구조 및 구성요소

```text
Request Intake -> Backlog -> Ready -> In Progress -> Review -> Done
               +-> WIP Limit / Pull Policy / Service Class / Flow Metrics
```

| 구성요소 | 역할 | 산출물·지표 |
|:---|:---|:---|
| Kanban Board | 작업 상태 시각화 | column, swimlane, blocked marker |
| WIP Limit | 단계별 동시 작업 수 제한 | In Progress 5건, Review 3건 |
| Pull Policy | 다음 단계 여유 시 작업 이동 | explicit policy, class of service |
| Flow Metrics | 흐름 성과 측정 | lead time, cycle time, throughput, CFD |

> 요약: Kanban은 보드, WIP 제한, pull 정책, 흐름 지표가 함께 있어야 병목 통제가 가능하다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요청 접수 -> 우선순위 분류 -> Ready 보관 -> WIP 여유 확인
-> 작업 Pull -> Review 병목 확인 -> Done -> Lead Time 측정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 요청 유형과 service class 분류 | expedite, fixed date, standard |
| 2 | Ready 기준 충족 여부 확인 | acceptance criteria, size limit |
| 3 | WIP limit 내에서 작업 pull | column limit 위반 0건 |
| 4 | blocked item과 review 병목 제거 | blocked aging 2일 이하 |
| 5 | 완료 후 lead time/cycle time 측정 | p85 cycle time 5일 이하 |

> 요약: Kanban은 새 작업을 밀어 넣지 않고 WIP 여유가 생길 때 당겨오며 완료 시간을 지속 측정한다.

---

## Ⅳ. 특징

| 구분 | Scrum | Kanban | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 시간 단위 | 1~4주 sprint | continuous flow | 운영 요청 유입 변동 시 Kanban |
| 작업 통제 | sprint backlog | WIP limit | column WIP 위반 0건 |
| 성과 지표 | velocity, burndown | lead time, cycle time, throughput | p85 cycle time 기준 |
| 변경 수용 | sprint 중 변경 제한 | pull 정책 기반 상시 유입 | class of service 필요 |

> 요약: Kanban은 고정 sprint보다 작업 유입이 불규칙한 운영·유지보수에서 흐름 시간을 관리하는 데 적합하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | Push 방식 | Kanban Pull 방식 | 선택 기준 |
|:---|:---|:---|:---|
| 작업 시작 | 요청 즉시 착수 | WIP 여유 시 착수 | 미완료 작업 증가 시 pull 필요 |
| 병목 인식 | 담당자 보고 의존 | CFD와 aging으로 확인 | Review 대기 비율 30% 이상 |
| 납기 예측 | 평균 완료일 추정 | percentile lead time | p85/p95 기준 SLA 설정 |

> 요약: Kanban은 미완료 작업을 줄이고 percentile 기반 납기 예측을 가능하게 하는 흐름 통제 방식이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 보드 형식화 | WIP limit 없음 | 열별 limit과 pull policy 명문화 | WIP violation count |
| 긴급 작업 남용 | expedite class 과다 | expedite quota, 승인 기준 | expedite ratio 10% 이하 |
| 병목 방치 | blocked aging 미관리 | daily flow review, blocker owner 지정 | blocked aging 2일 이하 |

> 요약: Kanban 리스크는 WIP 기준 부재와 긴급 작업 남용이므로 policy와 aging 지표로 관리한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 흐름 시간 | p85 cycle time 5일 이하 | control chart |
| 처리량 | 주간 throughput 변동률 20% 이하 | throughput trend |
| 병목 | Review WIP limit 3건, blocked aging 2일 이하 | CFD, aging report |

> 요약: Kanban 성과는 cycle time, throughput, blocked aging의 추세로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 업무 유형별 swimlane과 service class를 설정하고 expedite 비율을 전체 작업의 10% 이하로 제한
2. Ready, In Progress, Review, Done 열별 WIP limit을 설정하고 daily flow review에서 limit 위반을 즉시 조정
3. CFD, control chart, aging report를 dashboard로 운영해 p85 cycle time과 blocked aging을 매주 점검

**결론 (2줄):**
- 기술사 판단: 제품 기능 개발은 Scrum, 운영·유지보수·결함 처리처럼 유입 변동이 큰 업무는 Kanban을 선택함
- 향후 방향: Kanban은 DevOps value stream, SRE incident flow, ITSM ticket flow와 결합되어 흐름 기반 운영 관리로 확장됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Kanban을 설명하시오" | pull system과 WIP 흐름 | Scrum 대비 흐름 관리 특징 |
| 요구사항 명시형 | "운영 방안을 제시하시오", "비교하시오" | lead time/cycle time 측정 절차 | WIP limit, CFD, service class |

> 요약: 설명형은 구성요소, 운영형은 WIP 정책과 흐름 지표 중심으로 답안을 전환한다.
