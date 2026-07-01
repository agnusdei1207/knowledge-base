---
title: "5G 네트워크 슬라이싱 (5G Network Slicing)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 46
---

# 📖 【암기용】 개념 완전 이해

> 목적: 5G 네트워크 슬라이싱을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 하나의 물리 5G 인프라를 서비스별 논리 네트워크로 분리해 SLA를 다르게 적용하는 기술
- **왜 필요한가**: 영상 서비스, 공장 제어, 대량 센서망은 지연시간·대역폭·신뢰도 요구가 다르다. 하나의 평균 QoS로는 서비스별 요구를 만족하기 어렵다.
- **핵심 직관**: 같은 철도 선로 위에 고속열차, 화물열차, 통근열차를 분리된 운행 규칙과 우선순위로 운용하는 방식이다.

## 깊이 이해
- **배경·문제의식**: 4G의 APN/QCI 중심 QoS는 산업별 전용망 수준의 격리와 자동화 요구를 처리하기 어렵다. 5G는 slice 단위로 RAN, transport, core 자원을 묶고 서비스별 정책을 적용한다.
- **작동 원리**: 단말은 S-NSSAI를 통해 필요한 slice를 요청한다. AMF는 허용 NSSAI를 확인하고, NSSF·PCF·SMF와 연계해 해당 slice의 PDU Session과 QoS Flow를 설정한다.
- **비유**: 건물의 같은 전기·수도 설비를 쓰지만 병원, 사무실, 데이터센터 층마다 전력 우선순위와 보안 구역을 다르게 설정하는 것과 같다.
- **구체 예시**: SST 1은 eMBB, SST 2는 URLLC, SST 3은 MIoT 계열로 사용되며 SD는 사업자별 세부 slice를 구분하는 24-bit 값이다.
- **흔한 오해·주의점**: 슬라이싱은 VLAN처럼 단순 분리만 의미하지 않는다. 무선 자원, 코어 NF, 전송망, SLA 관측성이 함께 설계되어야 한다.

## 연결 개념
- S-NSSAI - SST와 SD로 slice를 식별
- NSSF - 단말 요청에 맞는 slice selection 지원
- 5QI - slice 내부 QoS Flow의 지연·손실 특성 지정

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 슬라이싱을 가상망 분리로만 쓰지 않고 S-NSSAI, NSSF, QoS Flow, RAN/Core/Transport 자원 격리와 SLA 검증으로 답안을 구성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 5G Network Slicing은 하나의 물리 인프라에서 S-NSSAI 기준 논리 네트워크 인스턴스를 구성해 서비스별 SLA를 제공하는 구조이다.
> 2. **가치**: eMBB·URLLC·mMTC와 기업 전용 서비스를 slice별 자원, 정책, 보안 구간으로 분리 운영한다.
> 3. **판단 포인트**: slice 식별, 자원 격리, QoS Flow, 오케스트레이션, SLA 관측성, 장애 전파 차단을 함께 검증해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 5G slicing 구조 이해 확인 | S-NSSAI, NSSF, AMF/SMF/UPF, 5QI | VLAN·VPN 수준으로만 설명 |
| 서비스별 SLA 판단 확인 | eMBB·URLLC·mMTC별 KPI와 자원 격리 | slice와 QoS Flow 혼동 |
| 운영 리스크 인식 확인 | slice lifecycle, 관측성, 장애 격리 | 오케스트레이션·지표 누락 |

> 요약: 이 문제는 slice 식별자와 5GC 절차를 바탕으로 논리망 격리와 SLA 운영을 설명하는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

5G 네트워크 슬라이싱은 물리망을 서비스별 논리망으로 분리하는 5G 핵심 기능이다. 산업망, XR, IoT는 서로 다른 지연·대역폭·접속밀도 요구를 가지므로 slice별 자원 예약과 정책 제어가 필요하다. 답안은 RAN·Transport·Core를 함께 다루어야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
UE -> S-NSSAI Request -> AMF -> NSSF
NSSF -> Allowed NSSAI -> AMF/SMF
SMF -> UPF Selection -> QoS Flow -> Data Network
RAN/Transport/Core -> Slice Resource Isolation
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| S-NSSAI | slice 식별자 | SST + SD, SST 1/2/3 |
| NSSF | slice selection 지원 | Allowed NSSAI 결정 |
| AMF/SMF/UPF | 등록, 세션, 사용자 평면 처리 | slice별 NF 또는 공유 NF 선택 |
| NSSMF/NSMF | slice lifecycle 오케스트레이션 | 생성, 변경, 종료, SLA 관리 |

> 요약: 슬라이싱은 S-NSSAI 식별, NSSF 선택, SMF/UPF 세션 제어, 자원 격리 오케스트레이션으로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
서비스 SLA 정의 -> S-NSSAI 설계 -> UE slice 요청
-> AMF/NSSF slice 선택 -> SMF PDU Session 생성
-> UPF/QoS Flow 설정 -> SLA 측정 -> 정책 조정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 서비스별 SLA를 latency, throughput, reliability로 정의 | SLA catalog |
| 2 | SST/SD와 DNN, 5QI 매핑 설계 | S-NSSAI 정책 일관성 |
| 3 | UE 등록 시 Requested/Allowed NSSAI 처리 | slice attach success |
| 4 | SMF가 slice별 PDU Session과 QoS Flow 생성 | PDU success, 5QI 매핑 |
| 5 | RAN/Core/Transport KPI 측정 후 자원 조정 | SLA violation count |

> 요약: 슬라이싱은 SLA를 S-NSSAI와 QoS Flow로 변환하고, 접속·세션·자원 지표로 지속 제어한다.

---

## Ⅳ. 특징

| 구분 | 기존 QoS/APN | 5G Network Slicing | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 식별 | APN, QCI | S-NSSAI, DNN, 5QI | SST 1/2/3, SD |
| 격리 범위 | 코어 중심 | RAN·Transport·Core 논리 격리 | PRB, VLAN/SR, UPF |
| 운영 | 수동 프로비저닝 | slice lifecycle orchestration | NSMF/NSSMF |
| SLA | 평균 품질 중심 | slice별 SLA 측정 | latency, reliability, throughput |

> 요약: 5G slicing은 식별자, 자원 격리, 생명주기 관리, SLA 측정을 결합한 논리망 운영 기술이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 5G Network Slicing | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | APN/VPN 분리 | S-NSSAI 기반 end-to-end slice | 산업별 SLA와 격리 요구 |
| 비용/성능 | 공유망 증설 | slice별 자원 예약·우선순위 | 자원 점유율과 SLA 위반 비용 |
| 운영/위험 | 개별 장비 설정 | NSMF/NSSMF 자동화 | lifecycle, rollback, 관측성 |

> 요약: 슬라이싱은 전용망 수준 SLA가 필요하고 물리망 공유가 사업상 필요한 경우 적용 가치가 크다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| slice 격리 실패 | 공유 NF·전송망 자원 경합 | admission control, resource quota | SLA violation, PRB usage |
| 설정 불일치 | S-NSSAI, DNN, 5QI 매핑 오류 | 정책 카탈로그, CI 검증 | attach/PDU failure |
| 장애 전파 | 공유 AMF/SMF/UPF 장애 | NF redundancy, slice-aware routing | slice incident scope |

> 요약: 슬라이싱 리스크는 격리·정책·장애 범위이며, SLA 위반과 세션 실패 지표로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 접속 품질 | slice attach/PDU success 99% 이상 | AMF/SMF PM |
| SLA 품질 | latency, reliability, throughput | probe, NWDAF, SLA dashboard |
| 격리 수준 | slice별 자원 사용량·장애 범위 | RAN/Core/Transport counter |

> 요약: 도입 후 평가는 slice 접속 성공률, SLA 달성률, 자원 격리 수준을 분리해 측정한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 설계: 서비스별 SLA를 eMBB, URLLC, MIoT로 분류하고 SST/SD, DNN, 5QI, UPF 위치를 카탈로그화함
2. 구축: NSSF, AMF/SMF policy, UPF routing, RAN PRB quota, transport QoS를 end-to-end로 연결함
3. 운영: slice attach, PDU success, latency, reliability, SLA violation count를 NWDAF/OSS에서 모니터링함

**결론 (2줄):**
- 기술사 판단: 단순 논리 분리이면 VPN/APN으로 충분하나, 5G SLA와 자원 격리가 필요하면 S-NSSAI 기반 slicing을 선택함
- 향후 방향: 5G-Advanced는 AI 기반 slice assurance와 closed-loop automation으로 slice lifecycle 자동화를 확대함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "네트워크 슬라이싱을 설명하시오" | S-NSSAI, NSSF, PDU Session 흐름 | 기존 QoS/APN 대비 차이 |
| 요구사항 명시형 | "산업망 slicing 방안을 제시하시오" | SLA 정의에서 slice 생성까지 절차 | 격리 실패·SLA 위반 리스크와 지표 |

> 요약: 설명형은 구조·절차, 방안형은 SLA 카탈로그와 end-to-end 격리 검증 중심으로 작성한다.
