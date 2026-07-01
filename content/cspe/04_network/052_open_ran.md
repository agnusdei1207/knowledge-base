---
title: "Open RAN·O-RAN (Open RAN)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 52
---

# 📖 【암기용】 개념 완전 이해

> 목적: Open RAN과 O-RAN을 처음 보는 사람도 기지국이 왜 분해되고 개방 인터페이스가 왜 필요한지 이해하게 만든다.

## 한눈에
- **개요**: Open RAN은 RAN 장비를 RU·DU·CU로 분리하고 개방 인터페이스로 다중 벤더 연동을 지향하는 구조다.
- **왜 필요한가**: 기존 RAN은 단일 벤더 통합 장비 의존도가 높아 교체 비용, 공급망 리스크, 기능 혁신 주기가 제한된다.
- **핵심 직관**: 기지국을 하나의 닫힌 상자로 사는 대신, 안테나·무선처리·제어 SW를 표준 포트로 조립하는 방식이다.

## 깊이 이해
- **배경·문제의식**: 5G RAN은 셀 수와 기능이 늘면서 장비 비용과 운영 복잡도가 증가했다. O-RAN Alliance는 Open Fronthaul, RIC, xApp/rApp으로 RAN 지능화를 표준화한다.
- **작동 원리**: RU는 RF와 하위 PHY, DU는 MAC/RLC/상위 PHY, CU는 PDCP/RRC를 담당한다. Near-RT RIC은 10ms~1s 제어 루프, Non-RT RIC은 1s 이상 정책·학습을 맡는다.
- **비유**: 완제품 PC만 사던 방식에서 메인보드·CPU·GPU를 표준 슬롯으로 조립하는 방식으로 바뀐 것과 유사하다.
- **구체 예시**: O-RAN Split 7.2x는 RU-DU 사이 Open Fronthaul을 정의하고, E2 인터페이스는 Near-RT RIC이 DU/CU 상태를 관측해 xApp 정책을 적용하게 한다.
- **흔한 오해·주의점**: Open RAN은 무조건 비용 절감이 아니다. 통합 검증, 동기화, 프론트홀 지연, 벤더 책임 경계 비용을 함께 계산해야 한다.

## 연결 개념
- O-RAN RIC — Near-RT RIC, Non-RT RIC, xApp/rApp
- C-RAN/vRAN — RAN 기능 가상화와 중앙집중 처리
- 5G Network Slicing — RAN 자원 정책과 SLA 연계

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: Open RAN 문제에서 개방성 구호가 아니라 구조 분해, 인터페이스, RIC 기반 제어, 운영 리스크를 답안화한다.
> 핵심: 출제자는 다중 벤더 연동의 가치와 검증 부담을 동시에 보는지 확인한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Open RAN은 RU·DU·CU 분리와 O-RAN 개방 인터페이스로 RAN 공급망과 기능 제어를 분산하는 아키텍처다.
> 2. **가치**: Open Fronthaul, E2, A1, O1 인터페이스와 RIC/xApp으로 벤더 종속을 낮추고 RAN 제어 자동화를 구현한다.
> 3. **판단 포인트**: 프론트홀 지연, IEEE 1588v2/PTP 동기화, 다중 벤더 IOT, 장애 책임 경계가 도입 판단의 핵심이다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| O-RAN 구조 이해 확인 | RU/DU/CU, Open Fronthaul, RIC, xApp/rApp | Open RAN을 단순 오픈소스로 설명 |
| 다중 벤더 장단점 판단 | 공급망 분산, 통합검증, 동기화 | 비용 절감만 단정 |
| 운영 자동화 역량 확인 | E2/A1/O1, Near-RT/Non-RT 제어 루프 | RIC 역할과 시간 범위 누락 |

> 요약: Open RAN 답안은 개방 인터페이스와 RIC 제어 구조, 통합 검증 리스크를 같이 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: RAN 기능을 개방 인터페이스로 분리
- 배경: 단일 벤더 RAN은 장비 교체와 기능 도입 시 벤더 로드맵에 종속
- 필요성: RU, DU, CU 분리와 RIC 제어로 공급망 선택지와 RAN 자동화 범위를 늘림

---

## Ⅱ. 구조 및 구성요소

```text
UE -> O-RU -> Open Fronthaul -> O-DU -> F1 -> O-CU -> 5GC
                         / E2 -> Near-RT RIC -> xApp
SMO/Non-RT RIC -> A1/O1 -> 정책, 관측, 구성관리
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| O-RU | RF, Low-PHY 처리 | Split 7.2x, PTP 동기화 |
| O-DU | High-PHY, MAC, RLC | 프론트홀 지연·처리량 민감 |
| O-CU | PDCP, SDAP, RRC | CU-CP/CU-UP 분리 가능 |
| RIC | RAN 지능 제어 | Near-RT 10ms~1s, Non-RT 1s 이상 |
| SMO | 서비스 관리·오케스트레이션 | O1 기반 구성·장애·성능 관리 |

> 요약: Open RAN은 RU-DU-CU 데이터 경로와 RIC/SMO 제어 경로를 분리해 RAN을 조립형 구조로 전환한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
무선 트래픽 수신 -> O-RU RF 처리 -> O-DU MAC/RLC 처리
-> O-CU PDCP/RRC 처리 -> 5GC 전달
-> E2 KPI 수집 -> RIC xApp 정책 계산 -> RAN 파라미터 조정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | O-RU가 무선 신호를 디지털화 | EVM, RF 출력, PTP lock |
| 2 | O-DU가 스케줄링·HARQ 처리 | fronthaul latency, DU CPU 사용률 |
| 3 | O-CU가 세션·무선자원 제어 | F1-C/F1-U 정상 상태 |
| 4 | Near-RT RIC이 KPI 기반 제어 | E2 node 연결, xApp 응답 10ms~1s |
| 5 | SMO가 정책·구성을 배포 | O1 구성 성공률, rollback 시간 |

> 요약: Open RAN은 사용자 트래픽 처리와 RIC 기반 제어 루프를 동시에 운영해야 한다.

---

## Ⅳ. 특징

| 구분 | 기존 통합 RAN | Open RAN | 판단 포인트 |
|:---|:---|:---|:---|
| 장비 구조 | 벤더 통합 DU/RU | O-RU/O-DU/O-CU 분리 | O-RAN Split 7.2x 지원 |
| 제어 방식 | 벤더 EMS 중심 | RIC xApp/rApp 정책 | E2/A1/O1 인터페이스 |
| 검증 범위 | 단일 벤더 책임 | 다중 벤더 IOT 필요 | lab IOT, field trial |
| 운영 지표 | 셀 KPI 중심 | 셀 KPI+앱 정책 KPI | PRB, BLER, handover rate |

> 요약: Open RAN은 개방성과 자동화 범위를 넓히지만 프론트홀·동기화·IOT 검증이 도입 조건이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | Open RAN | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 단일 벤더 RAN | 다중 벤더 RU/DU/CU | 공급망 분산·지역망·특화망 |
| 비용/성능 | 통합 최적화 | COTS/vRAN+가속기 | DU CPU, FPGA/NIC offload 필요 |
| 운영/위험 | 책임 경계 단순 | 통합 책임 분산 | SI 역량·IOT 테스트 체계 |

> 요약: Open RAN은 벤더 다변화 가치가 IOT와 운영 자동화 비용을 초과할 때 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 프론트홀 지연 | RU-DU 분리와 패킷화 | eCPRI QoS, PTP, SyncE | one-way latency, PTP offset |
| 상호연동 실패 | 벤더별 구현 차이 | O-RAN PlugFest, IOT 시나리오 | attach success, handover success |
| xApp 장애 | 제어 정책 충돌 | policy sandbox, rollback | xApp error rate, KPI drift |

> 요약: Open RAN 리스크는 무선 품질보다 동기화, 다중 벤더 연동, 정책 충돌 검증에서 발생한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 무선 품질 | BLER 10% 이하, RSRP/SINR 기준 충족 | drive test, RAN KPI |
| 프론트홀 | PTP offset 허용 범위, packet loss 0.01% 이하 목표 | PTP log, eCPRI capture |
| 운영 자동화 | O1 구성 성공률 99% 이상 목표 | SMO audit, change log |

> 요약: 도입 효과는 RAN KPI, 프론트홀 동기화, O1 자동화 성공률로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 특화망·농어촌·실험망부터 O-RU/O-DU/O-CU 벤더 조합을 제한해 IOT 범위를 정의하고 PlugFest 결과를 반영함
2. Open Fronthaul에 eCPRI QoS, IEEE 1588v2 PTP, SyncE를 적용하고 RU-DU 지연·jitter 기준을 사전 측정함
3. Near-RT RIC xApp은 handover optimization, traffic steering 등 1~2개 정책부터 적용하고 rollback 절차를 SMO에 등록함

**결론 (2줄):**
- 기술사 판단: 전국망 핵심 셀은 통합 RAN 검증성을 우선하고, 특화망·신규 지역은 Open RAN으로 공급망 다변화를 추진함
- 향후 방향: AI RAN, RIC 앱 생태계, 클라우드 네이티브 DU가 확산되며 RAN 운영은 KPI 기반 자동 제어로 전환됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Open RAN을 설명하시오", "O-RAN을 기술하시오" | RU-DU-CU 처리 흐름과 RIC 제어 루프 | 통합 RAN 대비 구조·운영 차이 |
| 요구사항 명시형 | "비교하시오", "도입 방안을 제시하시오", "설계하시오" | 프론트홀·동기화·RIC 요구사항 매핑 | IOT 리스크, 선택 기준, 검증 지표 |

> 요약: Open RAN은 설명형이면 구조 분해를, 설계형이면 다중 벤더 검증과 동기화 지표를 중심으로 전환한다.
