---
title: "6G 핵심 기술 - 테라헤르츠·AI 네이티브 (6G Technologies)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 49
---

# 📖 【암기용】 개념 완전 이해

> 목적: 6G 핵심 기술을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 6G는 IMT-2030을 목표로 THz 통신, AI-native 네트워크, sensing-communication 통합, NTN 등을 연구·표준화 중인 차세대 이동통신 방향
- **왜 필요한가**: 5G 이후 XR, 디지털 트윈, 자율 시스템, 위성·지상 통합망은 더 높은 주파수, 지능형 제어, 초정밀 위치·센싱을 요구한다.
- **핵심 직관**: 6G는 더 넓은 도로만 만드는 것이 아니라, 도로가 주변 상황을 감지하고 AI가 신호 체계를 계속 조정하는 네트워크를 지향한다.

## 깊이 이해
- **배경·문제의식**: 5G는 eMBB·URLLC·mMTC를 제공하지만 THz 대역, AI 기반 제어, 통신·센싱 통합, 지상·비지상망 통합은 표준화와 실증이 더 필요하다. 6G는 이러한 연구 주제를 IMT-2030 목표로 묶는다.
- **작동 원리**: THz는 넓은 대역폭으로 초고속 전송 가능성을 제공하나 경로손실과 차폐가 크다. AI-native는 RAN·Core·운영 데이터로 자원 제어, 장애 예측, slice assurance를 자동화한다.
- **비유**: 5G가 고속도로에 전용차로를 만든 단계라면, 6G는 도로·신호등·차량·드론이 같은 지도를 보고 AI가 통행 전략을 조정하는 단계이다.
- **구체 예시**: 3GPP는 Release 20을 6G study, Release 21을 6G normative work 시작 단계로 계획하며, IMT-2030 제출 일정과 연계된다.
- **흔한 오해·주의점**: 6G는 2026년 현재 상용 확정 서비스가 아니라 연구·표준화 단계이다. THz, AI-native, RIS, NTN은 후보 기술로 한계와 검증 과제가 남아 있다.

## 연결 개념
- THz Communication - 100 GHz 이상 후보 대역과 초대역폭 연구
- AI-native Network - NWDAF, RIC, closed-loop automation의 확장
- Integrated Sensing and Communication - 통신 파형으로 위치·환경 감지

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 6G를 상용 기술처럼 단정하지 않고 IMT-2030, 3GPP Rel-20 study/Rel-21 normative work, THz 한계, AI-native 검증 과제로 답안을 구성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 6G는 IMT-2030을 목표로 THz, AI-native, sensing-communication, NTN, RIS 등을 연구·표준화하는 차세대 이동통신 방향이다.
> 2. **가치**: 초대역폭, 지능형 자원 제어, 통신·센싱 결합, 지상·비지상 통합망을 통해 5G 한계를 보완하려는 접근이다.
> 3. **판단 포인트**: 2026년 기준 확정 상용 서비스가 아니라 표준화·실증 단계이므로 기술 후보와 제약을 함께 써야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 차세대 이동통신 전망 이해 확인 | IMT-2030, 3GPP Rel-20/Rel-21, THz, AI-native | 6G 서비스를 확정된 상용 기능으로 단정 |
| 기술 후보와 한계 판단 확인 | 경로손실, 에너지, 데이터 품질, 표준화 일정 | 장점만 나열 |
| 5G와의 연속성 이해 확인 | 5G-Advanced, NWDAF, NTN, slicing 발전 | 5G와 완전 단절된 기술로 설명 |

> 요약: 이 문제는 6G 후보 기술을 표준화 단계와 제약까지 포함해 균형 있게 설명하는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: IMT-2030 지향 차세대 이동통신
- 배경: 5G 이후 XR, 자율 시스템, 위성 통합, 통신·센싱 결합 요구가 확대
- 필요성: THz, AI-native, NTN, ISAC 후보 기술을 KPI와 상용화 한계 기준으로 평가

---

## Ⅱ. 구조 및 구성요소

```text
6G Candidate System
  / THz Radio -> ultra-wide bandwidth, high path loss
  / AI-native RAN/Core -> closed-loop optimization
  / ISAC -> communication plus sensing
  / NTN -> satellite/HAPS/terrestrial integration
  / RIS -> programmable radio environment
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| THz 통신 | 초대역폭 후보 무선 링크 | 경로손실·차폐·RF 소자 한계 |
| AI-native | RAN/Core/운영 제어 자동화 | 학습 데이터 품질과 설명가능성 필요 |
| ISAC | 통신 파형으로 위치·환경 센싱 | privacy, sensing accuracy 이슈 |
| NTN/RIS | 커버리지 확장과 전파환경 제어 | 위성 지연, RIS phase control |

> 요약: 6G 후보 구조는 THz 무선, AI-native 제어, ISAC, NTN, RIS가 결합되는 연구 방향이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
서비스 요구 도출 -> 후보 주파수/아키텍처 연구 -> 3GPP/ITU 표준화
-> PoC/field trial -> KPI 검증 -> normative specification 반영
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | IMT-2030 use case와 KPI 후보 정의 | peak rate, latency, sensing accuracy |
| 2 | THz, AI-native, ISAC, NTN 후보 기술 연구 | link budget, model accuracy |
| 3 | 3GPP Rel-20 study와 Rel-21 normative work 반영 | study item, work item |
| 4 | 실험망·PoC로 채널·단말·운영 검증 | path loss, energy per bit |
| 5 | 표준 규격과 상용 생태계 성숙도 평가 | interoperability, device readiness |

> 요약: 6G는 요구사항 정의, 후보 기술 연구, 표준화, PoC, 생태계 검증 순서로 진행된다.

---

## Ⅳ. 특징

| 구분 | 5G/5G-Advanced | 6G 후보 방향 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 주파수 | FR1/FR2 중심 | sub-THz/THz 후보 | link budget, blockage |
| 제어 | NWDAF, SON | AI-native closed-loop | model drift, explainability |
| 기능 | 통신 중심 | ISAC, digital twin 연계 | sensing accuracy |
| 커버리지 | 지상망+NTN 확장 | terrestrial/NTN 통합 고도화 | satellite latency |

> 요약: 6G는 초대역폭과 지능형 제어를 지향하지만 RF·AI·표준화 리스크가 동시에 존재한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 6G 후보 기술 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 5G NR/5GC | THz, AI-native, ISAC, NTN | IMT-2030 KPI와 표준 성숙도 |
| 비용/성능 | mmWave 중심 | sub-THz RF, 고밀도 셀 | CAPEX, 전력, backhaul |
| 운영/위험 | 사람이 정책 설계 | AI closed-loop 운영 | 데이터 품질, 책임성, rollback |

> 요약: 6G 후보 기술은 표준 성숙도, RF 경제성, AI 운영 책임성이 확보될 때 단계적으로 적용 가능하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| THz 링크 불안정 | 산소 흡수, 차폐, 빔 정렬 민감 | beam tracking, RIS, dense cell | path loss, outage ratio |
| AI 오작동 | 학습 데이터 편향·drift | MLOps, guardrail, rollback policy | model drift, SLA violation |
| 표준화 불확실성 | Rel-20/Rel-21 진행 중 | PoC와 표준 동향 분리 관리 | 3GPP WI/SI status |

> 요약: 6G 리스크는 RF 물리 한계, AI 운영 책임, 표준화 일정이며 연구·상용 판단을 분리해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 무선 링크 | path loss, throughput, outage | 채널 측정, ray tracing |
| AI 운영 | prediction accuracy, rollback time | MLOps log, A/B test |
| 표준 성숙도 | SI/WI, spec freeze, 상호운용 | 3GPP/ITU 문서 추적 |

> 요약: 6G 검증은 기술 PoC 지표와 표준 성숙도 지표를 분리해 판단해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 연구 과제: THz link budget, RIS 반사 이득, ISAC sensing accuracy를 실험실·필드 시험으로 분리 측정함
2. 운영 준비: AI-native 제어는 NWDAF/RIC 기반 closed-loop PoC부터 시작하고 rollback time과 model drift를 지표화함
3. 표준 추적: 3GPP Rel-20 study, Rel-21 normative work, ITU IMT-2030 문서를 분기별로 점검하고 투자 결정을 단계화함

**결론 (2줄):**
- 기술사 판단: 6G는 2026년 기준 연구·표준화 단계이므로 THz·AI-native 가능성과 RF·AI 리스크를 함께 제시해야 함
- 향후 방향: 5G-Advanced에서 검증된 AI 운영, NTN, slicing 자동화가 6G 표준 후보로 확장되는 흐름임

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "6G 핵심 기술을 설명하시오" | IMT-2030, Rel-20/21, 후보 기술 흐름 | 5G 대비 후보 기능과 한계 |
| 요구사항 명시형 | "6G 도입 전망을 제시하시오" | 표준화 단계, PoC, 투자 게이트 | THz·AI 리스크와 검증 지표 |

> 요약: 설명형은 후보 기술 체계, 전망형은 표준화 일정과 연구 한계를 중심으로 작성한다.
