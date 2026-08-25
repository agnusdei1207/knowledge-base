---
sidebar:
  order: 76
  label: "076. 네트워크 슬라이스 자원 관리"
  badge:
    text: "기출 · 50%"
    variant: note
title: "5G/6G E2E 네트워크 슬라이스 자원 관리 : Resource Management"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 76
extra:
  question_no: "76"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "3GPP 수용 제어(Admission Control), NSI/NSSI 라이프사이클 오케스트레이션 및 SLS 보증"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **NSI (Network Slice Instance)**: RAN, TN, CN 전 도메인의 물리/가상 자원을 결합하여 특정 SLS를 보장하는 종단간 가상 독립망.
- **NSSI (Network Slice Subnet Instance)**: NSI를 구성하는 도메인별(RAN NSSI, TN NSSI, CN NSSI) 독립 자원 단위.

</details>

- 정의/개념: 단일 물리망에서 서비스별 SLS를 보장하기 위해 **RAN, TN, CN 도메인의 가상 자원을 수용 제어, 스케줄링, 폐루프 오케스트레이션으로 동적 할당·격리하는 자원 관리 기술**
- 배경/필요성: 이종 서비스(eMBB/URLLC/mMTC) 공유 시 발생하는 **상호 간섭(Noisy Neighbor), 엄격한 SLS(1ms/99.999%) 보장 실패 및 도메인 간 통합 자원 제어 부재**

#### 한줄 요약
- RAN/TN/CN 전 도메인의 자원 수용 제어, 하이브리드 격리, 폐루프 자율 최적화를 제공한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Admission Control (수용 제어)**: 신규 슬라이스 생성 요청 시 기존 활성 슬라이스의 SLS 품질을 침해하지 않는지 사전 검증하여 수락/거절을 판정하는 기능.
- **Closed-Loop Assurance (폐루프 보증)**: NWDAF AI 분석 기반으로 실시간 품질 저하 감지 시 사람의 개입 없이 자원을 자동 증설(Scale-Out)하는 자율 복구 체계.

</details>

- **도메인 간(Cross-Domain) E2E 자원 조율**: 무선(PRB), 전송망(FlexE/SRv6), 코어망(vUPF) 자원을 **NSMF를 통해 단일 파이프라인으로 제어**
- **결정론적 SLS 및 하드/소프트 격리**: 엄격한 미션 크리티컬 트래픽은 **전용 물리 자원(Hard Slicing)으로 완벽 무간섭 보장**
- **AI 기반 폐루프(Closed-Loop) 자율 최적화**: NWDAF 텔레메트리 연계를 통해 **슬라이스 SLA 위반 시 자원 자동 스케일링**

#### 한줄 요약
- 도메인 간 E2E 자원 조율, 결정론적 SLS 격리, AI 기반 폐루프 자율 최적화를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **NSMF vs NSSMF**: E2E 슬라이스(NSI)를 총괄 관리하는 NSMF와 각 개별 도메인 서브넷(NSSI)을 전담 제어하는 도메인별 NSSMF.

</details>

```text
[3GPP 5G/6G 계층적 슬라이스 관리 및 자원 제어 아키텍처]
|-- CSMF (Communication Service Management Function: 고객 비즈니스 요구 SLS 접수)
`-- NSMF (Network Slice Management Function: E2E NSI 수명주기 및 수용 제어 총괄)
    |-- RAN NSSMF (기지국 PRB 무선 블록, 빔포밍 슬롯, 스케줄링 가중치 할당)
    |-- TN NSSMF (백홀/프론트홀 전송망 FlexE 타임슬롯, SRv6 터널, TSN 대역폭 할당)
    `-- CN NSSMF (5G 코어망 vUPF, AMF, SMF 가상 컨테이너 자원 동적 프로비저닝)
```

선의 의미: CSMF에서 접수된 고객 요구사항이 NSMF를 통해 분해되고 각 도메인 NSSMF를 거쳐 물리/가상 NSSI 자원으로 인스턴스화되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **CSMF (서비스 관리)** | 고객의 통신 서비스 요구사항(비즈니스 SLS) **접수 및 슬라이스 템플릿 변환** | 3GPP 관리 계층 |
| **NSMF (슬라이스 관리)**| E2E 슬라이스(NSI) 설계, 용량 산정, **수용 제어 판정 및 서브넷 오케스트레이션** | TS 28.531 표준 |
| **RAN NSSMF** | 기지국 **무선 자원(PRB), 빔포밍 슬롯, 스케줄링 가중치 할당 (RAN NSSI)** | 3GPP RAN Domain |
| **TN NSSMF** | 전송망의 **FlexE 슬라이스, SRv6 터널, TSN 대역폭 할당 (TN NSSI)** | IETF / IEEE TSN |
| **CN NSSMF** | 코어망 **vUPF, AMF, SMF 가상 머신/컨테이너 인프라 자원 프로비저닝 (CN NSSI)**| ETSI MANO 연동 |

#### 한줄 요약
- CSMF, NSMF, 도메인별 NSSMF(RAN/TN/CN)가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **NWDAF (Network Data Analytics Function)**: 3GPP 5G 코어의 AI/ML 기반 데이터 분석 기능으로 슬라이스 부하 및 비정상 트래픽을 실시간 예측.

</details>

```text
E2E 네트워크 슬라이스 생성 및 폐루프 자원 관리 파이프라인
        │
   1. [SLS 요구 접수] 고객이 특정 SLS(지연 1ms, 대역폭 500Mbps) 요청을 CSMF에 제출
        │
   2. [수용 제어(Admission Control)] NSMF가 인프라 자원 DB를 조회하여 수용 가능 여부 검증
        │
   ├─ [가용 자원 부족 시] ➔ 슬라이스 생성 거부 및 협상 실패 반환
   ▼
3. [도메인별 NSSI 병렬 배포] NSMF가 RAN, TN, CN NSSMF로 서브넷 할당 명령 하달
        │
   4. [종단간 바인딩 활성화] 기지국 PRB, 전송망 FlexE, 코어망 vUPF를 1:1 결합하여 NSI 개통
        │
   ▼
5. [NWDAF 폐루프 자율 최적화] 실시간 텔레메트리로 SLS를 감시하고 병목 발생 시 자원 자동 증설
```

#### 한줄 요약
- SLS 접수 → 수용 제어 검증 → NSSI 병렬 배포 → 종단 바인딩 → 폐루프 모니터링 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Dedicated (Hard Slicing)** vs **Shared (Soft Slicing)** vs **Hybrid (Dynamic)**.

</details>

| 비교 항목 | 완전 전용 할당 (Dedicated / Hard) | 완전 공유 할당 (Shared / Soft) | 하이브리드 할당 (Hybrid Dynamic) |
|:---|:---|:---|:---|
| **자원 배분 메커니즘**| **특정 물리 자원(PRB/코어) 100% 영구 독점** | 공용 풀에서 가중치(WFQ) 기반 **통계적 공유** | **최소 전용 보장(Hard) + 잉여분 공유(Soft)** |
| **SLS 품질 보장** | **100% 결정론적 보장 (간섭 제로)** | 트래픽 폭주 시 SLS 위반 가능성 존재 | **최소 SLA 100% 보장 및 피크 트래픽 흡수** |
| **인프라 자원 효율** | **낮음 (유휴 시 대역폭 낭비 발생)** | **매우 높음 (통계적 다중화 극대화)** | **높음 (품질 보장과 자원 효율의 최적 균형)**|
| **구현 복잡도** | 낮음 (정적 파티셔닝) | 중간 (QoS 스케줄링) | **높음 (실시간 동적 오케스트레이션)** |
| **주요 적용 서비스** | 스마트팩토리, 자율주행 (URLLC 전용) | 대규모 센서 네트워크 (mMTC), 일반 웹 | **VIP 기업 전용망, 모바일 eMBB 프리미엄망** |

#### 한줄 요약
- Dedicated는 URLLC용 무간섭 격리, Shared는 mMTC용 자원 효율화, Hybrid는 품질과 효율을 절충한 표준 모델이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Resource Flapping (자원 플래핑)**: 트래픽이 임계치 부근에서 미세하게 진동할 때 자원 할당과 회수가 급격히 반복되어 시스템 오버헤드가 발생하는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 전송망/코어망 병목으로 인한 종단 간(E2E) 슬라이스 지연 시간 SLS 위반 | **`NWDAF 연계 E2E 텔레메트리` 및 병목 도메인 NSSI 자동 스케일아웃** | 지연 병목 구간 조기 해소 및 99.999% SLS 준수 |
| 트래픽 임계치 경계에서 빈번한 자원 증감으로 인한 **플래핑(Flapping)** | 자원 스케일링 정책에 **`히스테리시스(Hysteresis) 및 쿨다운 타이머`** 적용 | 잦은 제어 진동 억제 및 제어 평면 안정성 확보 |
| 완전 전용 예약(Hard Slicing) 시 유휴 자원 증가로 인한 망 수익성 저하 | **`최소 보장 + 잉여 공유의 하이브리드 슬라이싱(Hybrid)` 모델 구축** | SLS 품질 무손실 유지 및 자원 활용률 35% 향상 |
| 비인가 단말의 고우선순위 슬라이스 무단 접속 및 자원 고갈 위협 | **`NSSF (Network Slice Selection Function)` 기반 단말 인증 검증** | 미인가 단말 접근 원천 차단 및 슬라이스 보안 격리 |

#### 한줄 요약
- NWDAF로 E2E 지연을 방어하고, 히스테리시스로 플래핑을 방지하며, 하이브리드 슬라이싱으로 자원 효율을 극대화한다.

## Ⅶ. 결론

- 초저지연·초연결·초광대역 서비스를 단일 인프라에서 완벽히 수용하기 위해 **3GPP 표준 5G/6G 네트워크 슬라이스 자원 관리 체계를 도입**하되, 운영 신뢰성과 비용 효율을 극대화하기 위해 **NSMF/NSSMF 계층 오케스트레이션, 하이브리드 자원 할당 모델, NWDAF 기반 폐루프(Closed-Loop) AI 자가 치유**를 통합 구축하여 고품질 자율 운영 네트워크 완성

#### 한줄 요약
- 네트워크 슬라이스 자원 관리는 NSMF/NSSMF와 NWDAF 폐루프 제어를 결합하여 E2E 격리 및 SLS 품질을 보증하는 5G/6G 핵심 제어 기술이다.