---
sidebar:
  order: 76
  label: "076. 네트워크 슬라이스 자원 관리"
  badge:
    text: "기출 · 50%"
    variant: note
title: "5G/6G 종단 간 네트워크 슬라이스 자원 관리 및 제어 (Resource Management)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-network"
weight: 76
extra:
  question_no: "076"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "3GPP 수용 제어(Admission Control), NSI/NSSI 라이프사이클 오케스트레이션 및 SLS 보증"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **네트워크 슬라이스 인스턴스(Network Slice Instance, NSI)**: 무선 접속망(RAN), 전송망(TN), 코어망(CN)의 물리/가상 자원을 결합하여 특정 비즈니스 서비스 요구사항(SLA/SLS)을 충족하도록 격리·생성된 종단 간(End-to-End) 논리적 독립 네트워크.
- **네트워크 슬라이스 서브넷 인스턴스(NSSI)**: E2E NSI를 구성하는 도메인별(RAN NSSI, TN NSSI, CN NSSI) 독립 가상화 자원 조각 단위.
- **서비스 수준 명세(Service Level Specification, SLS)**: 지연 시간($\le 1\text{ms}$), 가용성($99.999\%$), 처리량($\ge 100\text{Mbps}$), 지터 등 개별 슬라이스가 보증해야 하는 정량적 QoS 지표 집합.

</details>

- 정의/개념: 단일 물리 5G/6G 인프라 상에서 고객 및 서비스별 SLS 요구사항을 수용하기 위해 **NSI/NSSI 라이프사이클 관리**, **수용 제어(Admission Control)**, **동적 자원 스케줄링(RAN/TN/CN)** 및 **폐루프 자가 치유(Closed-Loop Assurance)** 를 수행하는 **통합 자원 관리 프레임워크 (3GPP TS 28.530/531 표준)**
- 배경/필요성: eMBB, URLLC, mMTC 등 상이한 트래픽 요구조건을 단일 인프라에서 수용하면서 슬라이스 간 자원 침범을 방지하고 인프라 활용률을 극대화할 요구

#### 한줄 요약
- RAN, 전송, 코어 도메인의 NSSI를 결합하여 NSI를 생성하고 SLS 기반으로 동적 자원을 제어한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **수용 제어(Admission Control)**: 신규 슬라이스 생성 또는 트래픽 인입 시 가용 자원을 사전 계산하여 기존 운영 중인 활성 슬라이스의 SLS 위반 가능성이 있을 경우 신규 요청을 차단하는 자원 보호 메커니즘.
- **슬라이스 격리(Slice Isolation)**: 특정 슬라이스에서 트래픽 폭주나 보안 침해가 발생하더라도 타 슬라이스의 성능 및 데이터에 영향을 주지 않도록 하드웨어/소프트웨어 레벨에서 격리하는 능력.

</details>

- **종단 간(End-to-End) 자원 연계 제어**: 무선 기지국(PRB)뿐만 아니라 유선 백홀(TSN/FlexE 대역폭)과 코어망(NFV vCPU/UPF) 자원을 단일 파이프라인으로 통합 관리
- **SLS 기반 수용 제어 및 성능 보증**: 수학적 용량 산정 모델을 기반으로 기존 슬라이스의 SLA 훼손을 원천 차단하는 엄격한 입장 제어
- **엄격한 물리/논리적 자원 격리**: 하드웨어 전용 큐 및 가상화 파티셔닝을 통해 슬라이스 간 트래픽 간섭(Noisy Neighbor) 배제

#### 한줄 요약
- E2E 자원 연계, SLS 기반 수용 제어, 엄격한 슬라이스 간 격리 및 동적 자원 재조정을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **NSMF(Network Slice Management Function)**: 최상위 E2E 슬라이스 관리자로, 고객의 서비스 요구사항(CSMF)을 받아 전체 NSI의 라이프사이클을 총괄하는 엔진.
- **NSSMF(Network Slice Subnet Management Function)**: RAN, TN, CN 각 개별 도메인의 가상 자원 할당과 슬라이스 서브넷(NSSI) 생성을 전담 제어하는 도메인별 관리자.

</details>

```text
[ 통신 서비스 관리 기능 (CSMF) ] ── (고객 SLS 요구 접수)
                 │
                 ▼
[ 네트워크 슬라이스 관리 기능 (NSMF) ] ── (종단 간 NSI 라이프사이클 총괄)
                 │
                 ├───────────────────────────────┬───────────────────────────────┐
                 ▼                               ▼                               ▼
[ RAN NSSMF (무선망 관리자) ]    [ TN NSSMF (전송망 관리자) ]    [ CN NSSMF (코어망 관리자) ]
 ├─ RAN NSSI (PRB 무선 블록)      ├─ TN NSSI (FlexE/TSN 대역폭)    ├─ CN NSSI (vCPU/vUPF 인스턴스)
 └─ 기지국 자원 스케줄링          └─ IP/MPLS 광 전송 패브릭       └─ 5G SBA 클라우드 코어
```

선의 의미: CSMF에서 접수된 고객 요구사항이 NSMF를 통해 분해되고, 각 도메인 NSSMF를 거쳐 물리/가상 NSSI 자원으로 인스턴스화되는 계층 관리 구조

| 구성요소 | 책임 및 역할 | 3GPP 표준 엔티티 |
|:---|:---|:---|
| **CSMF (서비스 관리)** | 고객의 통신 서비스 요구사항(비즈니스 SLS) 접수 및 슬라이스 요구로 변환 | 3GPP 3D Management |
| **NSMF (슬라이스 관리)**| E2E 슬라이스(NSI) 설계, 용량 산정, 수용 제어 판정 및 서브넷 오케스트레이션 | TS 28.531 |
| **RAN NSSMF** | 기지국 무선 자원(PRB), 빔포밍 슬롯, 스케줄링 가중치 할당 (RAN NSSI) | 3GPP RAN Domain |
| **TN NSSMF** | 백홀/프론트홀 전송망의 FlexE 슬라이스, SRv6 터널, TSN 대역폭 할당 (TN NSSI) | IETF / IEEE TSN |
| **CN NSSMF** | 코어망 vUPF, AMF, SMF 가상 머신/컨테이너 인프라 자원 프로비저닝 (CN NSSI) | ETSI NFV MANO 연동 |

#### 한줄 요약
- CSMF, NSMF, 도메인별 NSSMF(RAN/TN/CN)가 결합하여 종단 간 슬라이스를 통합 제어한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **폐루프 제어(Closed-Loop Assurance)**: 텔레메트리로 실시간 슬라이스 품질(지연, 처리량)을 측정하고, SLS 임계치 위반 감지 시 AI/ML 엔진이 자동으로 NSSI 자원을 동적 증설(Scale-out/Scale-up)하는 자율 복구 메커니즘.

</details>

```text
1. 고객이 특정 SLS(지연 1ms, 대역폭 500Mbps)를 포함한 슬라이스 생성 요청 제출 ➔ CSMF 접수
            │
            ▼
2. NSMF가 글로벌 인프라 용량 데이터베이스를 조회하여 수용 제어(Admission Control) 알고리즘 실행
            │
            ├─ [가용 자원 부족 시] ➔ 슬라이스 생성 거부 및 협상 실패 반환
            ▼
3. [자원 가용성 확인] ➔ NSMF가 도메인별 NSSMF(RAN, TN, CN)로 서브넷(NSSI) 할당 명령 하달
            │
            ▼
4. 각 도메인 NSSMF가 기지국 PRB, 전송망 FlexE, 코어망 vUPF를 프로비저닝하여 NSI 활성화 개통
            │
            ▼
5. 텔레메트리 기반 E2E SLS 모니터링 ➔ 병목 발생 시 폐루프(Closed-Loop) 자원 동적 재배치
```

**동작 원리**

1. **요구사항 해석**: CSMF가 비즈니스 계약을 3GPP GST(Generic Slice Template) 파라미터로 변환
2. **수용성 연산**: NSMF가 기존 활성 슬라이스의 트래픽 엔지니어링 마진을 침해하지 않는지 검증
3. **서브넷 병렬 배포**: RAN, TN, CN NSSMF가 각 도메인의 오케스트레이터(VIM, SDN Controller)를 구동
4. **종단 간 바인딩**: 단말의 S-NSSAI 식별자와 무선 RB, 전송망 SRv6 터널, 코어망 PDU 세션을 1:1 결합
5. **동적 최적화**: NWDAF(네트워크 데이터 분석 기능)가 슬라이스 부하를 예측하여 선제적 자원 스케일링

#### 한줄 요약
- SLS 접수, 수용 제어 검증, NSSI 병렬 배포, 종단 바인딩, 폐루프 모니터링 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **정적 예약(Dedicated) vs 동적 공유(Shared) vs 하이브리드(Hybrid)**: 물리 자원을 100% 독점 할당하는 방식, 모든 자원을 풀링하여 공유하는 방식, 최소 대역폭을 보장하고 잉여 자원을 탄력 공유하는 방식.

</details>

| 비교 항목 | 완전 전용 할당 (Dedicated / Hard Slicing) | 완전 공유 할당 (Shared / Soft Slicing) | 하이브리드 할당 (Hybrid Dynamic Slicing) |
|:---|:---|:---|:---|
| **자원 배분 메커니즘** | 특정 물리 자원(PRB/코어)을 **100% 영구 독점 예약** | 공용 자원 풀에서 가중치(WFQ) 기반 **통계적 공유** | **최소 전용 보장(Hard) + 잉여분 탄력 공유(Soft)** |
| **SLS 품질 보장** | **100% 결정론적 보장 (간섭 제로)** | 트래픽 폭주 시 SLS 위반 가능성 존재 | **최소 SLA 100% 보장 및 피크 트래픽 흡수** |
| **인프라 자원 효율** | **낮음 (유휴 시 대역폭 낭비 발생)** | **매우 높음 (통계적 다중화 이득 극대화)** | **높음 (품질 보장과 자원 효율의 최적 균형)** |
| **구현 복잡도** | 낮음 (정적 파티셔닝) | 중간 (QoS 스케줄링) | **높음 (실시간 동적 오케스트레이션 요구)** |
| **주요 적용 서비스** | 스마트팩토리, 자율주행 (URLLC 미션 크리티컬) | 대규모 센서 네트워크 (mMTC), 단순 웹 서핑 | **VIP 기업 전용망, 모바일 eMBB 프리미엄망** |

#### 한줄 요약
- Dedicated는 URLLC용 무간섭 격리, Shared는 mMTC용 자원 효율화, Hybrid는 품질과 효율을 절충한 표준 모델이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **플래핑(Flapping / Resource Churn)**: 트래픽 부하가 임계치 부근에서 미세하게 진동할 때 자원 할당과 회수가 초 단위로 급격히 반복되어 시스템 오버헤드를 유발하는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 특정 도메인(TN/CN) 병목으로 인한 종단 간(E2E) 슬라이스 지연 시간 SLS 위반 | **NWDAF 연계 E2E 텔레메트리** 및 병목 도메인 NSSI 핀포인트 자동 스케일아웃 | 지연 병목 구간 조기 해소 및 99.999% SLS 준수율 달성 |
| 트래픽 임계치 경계에서 빈번한 자원 증감으로 인한 오케스트레이터 **플래핑(Flapping) 발생** | 자원 스케일링 정책에 **히스테리시스(Hysteresis 마진) 및 쿨다운 타이머** 적용 | 잦은 제어 진동 억제 및 슬라이스 제어 평면 안정성 확보 |
| 완전 전용 예약(Hard Slicing) 적용 시 유휴 자원 증가로 인한 통신망 수익성 저하 | **최소 보장 + 잉여 공유의 하이브리드 슬라이싱(Hybrid Slicing)** 모델 구축 | SLS 품질 무손실 유지 및 전체 인프라 자원 활용률 35% 향상 |

#### 한줄 요약
- NWDAF로 E2E 지연을 방어하고, 히스테리시스로 플래핑을 방지하며, 하이브리드 슬라이싱으로 자원 효율을 극대화한다.

## Ⅶ. 결론

- 초저지연·초연결·초광대역 서비스를 단일 인프라에서 완벽히 수용하기 위해 **3GPP 표준 5G/6G 네트워크 슬라이스 자원 관리 체계**를 도입하되, 운영 신뢰성과 비용 효율을 극대화하기 위해 **NSMF/NSSMF 계층 오케스트레이션**, **하이브리드 자원 할당 모델**, **NWDAF 기반 폐루프(Closed-Loop) AI 자가 치유**를 통합 구축하여 고품질 자율 운영 네트워크를 완성

#### 한줄 요약
- NSMF/NSSMF와 NWDAF 폐루프 자원 제어를 결합하여 고신뢰 5G/6G 네트워크 슬라이싱을 구현한다.
