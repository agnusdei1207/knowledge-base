---
title: "5G 핵심 기술 - eMBB·URLLC·mMTC (5G Core Technologies)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 43
---

# 📖 【암기용】 개념 완전 이해

> 목적: 5G 핵심 기술을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 5G는 eMBB·URLLC·mMTC 3대 서비스 축을 만족하도록 무선·코어·엣지를 함께 설계한 이동통신 시스템
- **왜 필요한가**: 4G는 모바일 인터넷 중심이었지만, 5G는 초고화질 미디어, 공장 제어, 대규모 센서처럼 서로 다른 요구사항을 하나의 시스템에서 수용해야 한다.
- **핵심 직관**: eMBB는 대용량 도로, URLLC는 구급차 전용 차선, mMTC는 수많은 저속 자전거 통행을 동시에 처리하는 구조이다.

## 깊이 이해
- **배경·문제의식**: 모바일 트래픽은 영상·XR로 커지고, 산업 제어는 ms 단위 지연과 높은 신뢰도를 요구하며, IoT는 저전력 단말 수만 개를 수용해야 한다. 5G는 한 가지 속도 경쟁이 아니라 요구조건별 네트워크 설계 문제이다.
- **작동 원리**: 5G NR은 numerology, massive MIMO, beamforming으로 무선 용량을 확보한다. 5G Core는 SBA, network slicing, MEC 연계를 통해 서비스별 QoS와 트래픽 경로를 분리한다.
- **비유**: 한 도시 안에 고속도로(eMBB), 응급차 우선 신호(URLLC), 우편함 센서망(mMTC)을 동시에 운영하는 교통 시스템과 같다.
- **구체 예시**: IMT-2020 목표는 eMBB peak 20 Gbps, URLLC radio latency 1 ms, mMTC 1 km2당 100만 단말 수준을 제시한다.
- **흔한 오해·주의점**: 5G가 모든 서비스에서 항상 1 ms를 보장하는 것은 아니다. URLLC는 제한된 커버리지·대역·스케줄링 조건에서 설계 목표로 다룬다.

## 연결 개념
- 5G SA/NSA - 5G Core 도입 여부에 따른 구축 방식
- Network Slicing - 서비스별 논리 네트워크 분리
- MEC - URLLC·XR 지연시간을 줄이기 위한 엣지 처리

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 5G를 속도 향상으로만 쓰지 않고 eMBB·URLLC·mMTC 요구사항별 구조·지표·한계를 구분해 답안을 구성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 5G는 eMBB, URLLC, mMTC 요구사항을 5G NR·5GC·MEC·Slicing으로 수용하는 3GPP 이동통신 시스템이다.
> 2. **가치**: 대용량, 저지연·고신뢰, 초연결 서비스를 같은 인프라에서 논리적으로 분리 운영한다.
> 3. **판단 포인트**: 서비스별 KPI가 다르므로 peak rate, latency, reliability, connection density, battery life를 각각 제시해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 5G 서비스 요구사항 구분 확인 | eMBB·URLLC·mMTC 정의가 아니라 KPI 차이 | 5G를 속도 중심으로만 설명 |
| 3GPP 구조 이해 확인 | 5G NR, 5GC SBA, slicing, MEC 연결 | 무선 기술만 나열하고 코어 누락 |
| 적용 판단 확인 | 제조·XR·IoT별 SLA와 제약 | URLLC 1 ms를 모든 환경 보장처럼 단정 |

> 요약: 이 문제는 5G의 3대 서비스 축과 이를 구현하는 무선·코어·엣지 구조를 연결하는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

5G는 eMBB·URLLC·mMTC 3대 요구사항을 수용하는 3GPP 이동통신 시스템이다. 트래픽 대용량화, 산업 제어 저지연, IoT 대량 접속을 하나의 인프라에서 처리하기 위해 무선·코어·엣지 아키텍처가 함께 진화했다. 답안은 서비스별 KPI와 구조 요소를 함께 제시해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
UE -> 5G NR gNB -> 5G Core SBA -> Data Network
  / eMBB: Massive MIMO, wide bandwidth
  / URLLC: low latency scheduling, MEC
  / mMTC: massive access, power saving
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| 5G NR | OFDM, numerology, beamforming 기반 무선 접속 | FR1/FR2, subcarrier spacing 15~120 kHz |
| 5G Core | AMF·SMF·UPF 등 SBA 기반 제어·사용자 평면 | 서비스 기반 인터페이스, UPF 분산 |
| Network Slicing | 서비스별 논리망 분리 | SST 1 eMBB, SST 2 URLLC, SST 3 MIoT |
| MEC | 사용자 가까운 위치에서 애플리케이션 처리 | URLLC·XR 지연시간 감소 |

> 요약: 5G는 5G NR, 5GC SBA, slicing, MEC를 결합해 서비스별 KPI를 분리 제어한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
서비스 요구 식별 -> slice/QoS 선택 -> 5G NR 무선 자원 배정
-> 5GC 세션 제어 -> UPF 경로 설정 -> MEC/Data Network 처리
-> KPI 측정과 SLA 피드백
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 서비스가 eMBB·URLLC·mMTC 중 요구 유형 지정 | 5QI, SST, SLA |
| 2 | AMF/SMF가 PDU Session과 QoS Flow 설정 | 5QI, ARP, GBR |
| 3 | gNB가 numerology·MCS·beam을 선택 | SINR, BLER 10% 목표 |
| 4 | UPF가 데이터 경로를 MEC 또는 DN으로 분기 | user plane latency |
| 5 | PM 카운터로 KPI 측정 후 정책 조정 | throughput, latency, reliability |

> 요약: 5G는 요구사항을 slice와 QoS로 변환하고, 무선 자원·코어 경로·엣지 위치를 함께 제어한다.

---

## Ⅳ. 특징

| 구분 | 4G LTE 중심 | 5G 핵심 기술 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 대용량 | LTE-A CA, MIMO | eMBB, massive MIMO, FR2 | peak 20 Gbps 목표 |
| 저지연 | EPC 중앙 경로 | URLLC, MEC, short TTI | radio latency 1 ms 목표 |
| 초연결 | NB-IoT/LTE-M | mMTC, 대량 접속 제어 | 1 km2당 100만 단말 목표 |
| 운영 | 단일망 QoS | slicing, SBA, UPF 분산 | SST, 5QI, SLA 매핑 |

> 요약: 5G의 차별점은 대용량·저지연·초연결을 KPI별로 나누고 slicing과 MEC로 운영 제어까지 포함한다는 점이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 5G 핵심 기술 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | LTE EPC 중앙집중 | 5GC SBA, UPF 분산 | 서비스별 지연·트래픽 경로 |
| 비용/성능 | 단일망 증설 | slice별 자원 예약 | SLA 위반 비용과 자원 점유율 |
| 운영/위험 | APN/QCI 중심 | S-NSSAI, 5QI, NWDAF | slice 격리와 관측성 |

> 요약: 5G 적용은 세대 교체가 아니라 서비스 KPI별 무선·코어·엣지 자원 설계 문제이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| URLLC 미달 | 백홀·코어 경로 지연 | MEC 배치, UPF local breakout | E2E latency, jitter |
| mMTC 접속 폭주 | 랜덤 액세스 충돌 | access barring, RACH 파라미터 조정 | RACH success rate |
| eMBB 품질 저하 | 셀 부하·빔 간섭 | beam optimization, CA, load balancing | cell throughput, BLER |

> 요약: 5G 리스크는 서비스별 병목이 다르므로 지연·접속 성공률·셀 처리량을 분리 측정해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| eMBB | peak/user throughput, BLER 10% 이하 | gNB PM, drive test |
| URLLC | 1 ms radio latency, 99.999% reliability 목표 | probe, MEC 로그 |
| mMTC | connection density, battery life | RACH 통계, 단말 전력 측정 |

> 요약: 5G KPI는 서비스별로 다르며 하나의 평균 처리량 지표로 평가하면 출제 의도를 놓친다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. eMBB: FR1/FR2, massive MIMO, carrier aggregation을 셀 트래픽 분포와 BLER 10% 기준으로 설계함
2. URLLC: MEC, local UPF, preemption scheduling을 조합해 E2E latency와 99.999% reliability 목표를 시험함
3. mMTC: RACH 파라미터, access barring, DRX/PSM을 적용해 접속 성공률과 단말 전력 소모를 측정함

**결론 (2줄):**
- 기술사 판단: 5G는 eMBB·URLLC·mMTC 중 목표 KPI를 먼저 정하고 5QI·S-NSSAI·UPF 위치를 설계해야 함
- 향후 방향: 5G-Advanced는 AI 기반 RAN 제어, RedCap, NTN, slicing 자동화로 서비스별 SLA 제어 범위를 넓히는 방향임

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "5G 핵심 기술을 설명하시오" | eMBB·URLLC·mMTC 요구사항과 5GC 흐름 | 4G 대비 KPI·구조 비교 |
| 요구사항 명시형 | "산업 적용 방안을 제시하시오" | 5QI·S-NSSAI·MEC 경로 설계 | SLA별 리스크와 점검 지표 |

> 요약: 설명형은 3대 서비스 축, 방안형은 서비스 KPI를 네트워크 구조로 변환하는 절차를 강조한다.
