---
sidebar:
  order: 104
  label: "104. InfiniBand 클러스터 인터커넥트 (InfiniBand Cluster)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "InfiniBand 클러스터 인터커넥트 (InfiniBand Cluster)"
date: "2026-08-05T16:32:08+09:00"
tags: ["notes-network"]
weight: 104
extra:
  question_no: "104"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "비교•설계형: 138회 InfiniBand 직접 요구"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **InfiniBand 패브릭**: HCA와 스위치를 연결해 RDMA와 크레딧 기반 무손실 전송을 제공하는 인터커넥트
- **호스트 채널 어댑터(Host Channel Adapter, HCA)**: 서버를 InfiniBand 패브릭에 연결하는 장치
- **원격 직접 메모리 접근(Remote Direct Memory Access, RDMA)**: 호스트 간 등록 메모리를 직접 연결하는 전송 기술

</details>

- 정의/개념: HCA와 스위치를 잇는 **RDMA•크레딧 제어 패브릭**
- 배경/필요성: 범용망의 복사와 손실로 인한 **지연 변동**

#### 한줄 요약

- 서버 사이 대량 자료를 빠르게 보내도록 주소와 경로, 버퍼 여유를 패브릭 전체에서 함께 관리하는 전용망이다.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **링크 무손실 흐름 제어**: HCA가 수신 버퍼의 여유 크레딧 범위에서 RDMA 자료를 보내는 방식
- **서브넷 관리자**: 패브릭 토폴로지를 발견하고 주소•경로•파티션을 계산•배포하는 중앙 제어 기능

</details>

- HCA 기반 **RDMA 전송**
- 크레딧 기반 **링크 무손실 흐름 제어**
- 서브넷 관리자 기반 **주소•경로 관리**

#### 한줄 요약

- 각 링크는 받을 공간이 있다는 신호만큼 보내 패킷을 잃지 않지만 중앙 경로 관리가 잘못되면 많은 서버가 함께 영향을 받는다.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **컴퓨트 HCA**: 서버 메모리의 RDMA 작업을 실행하는 장치
- **InfiniBand 스위치 패브릭**: HCA 간 무손실 패킷 경로를 제공하는 전송망
- **저장 HCA**: 저장 장치의 RDMA 종단을 제공하는 장치
- **서브넷 관리자**: 토폴로지를 발견하고 주소•경로•파티션을 배포하는 기능
- **패브릭 관측기**: 포트•링크•오류•혼잡 상태를 수집하는 구성요소
- **로컬 식별자(Local Identifier, LID)**: 서브넷 내부 포트를 식별하는 주소
- **가상 레인(Virtual Lane, VL)**: 링크에서 트래픽을 논리적으로 분리하는 전송 통로
- **파티션 키(Partition Key, P_Key)**: 통신 가능한 종단 그룹을 구분하는 격리 키

</details>

```text
InfiniBand 클러스터
├─ 컴퓨트 HCA
├─ InfiniBand 스위치 패브릭
├─ 저장 HCA
├─ 서브넷 관리자
└─ 패브릭 관측기
```

가지의 의미: 연산•전달•저장•경로 관리•관측 책임을 분리한 구조다.

| 구성요소 | 책임 |
|:---|:---|
| 컴퓨트 HCA | 서버 메모리의 **RDMA 작업** 실행 |
| InfiniBand 스위치 패브릭 | **LID•VL 경로**로 무손실 패킷 전달 |
| 저장 HCA | 저장 장치의 **RDMA 종단** 제공 |
| 서브넷 관리자 | **LID•경로•P_Key** 관리 |
| 패브릭 관측기 | **포트•링크•오류•혼잡 상태** 수집 |

#### 한줄 요약

- 서버와 저장장치의 HCA를 스위치들이 연결하고 서브넷 관리자가 모든 포트의 주소와 경로, 격리 그룹을 정한다.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **크레딧 RDMA 전송**: HCA와 스위치가 다음 홉의 수신 버퍼 여유 안에서 RDMA 패킷을 보내는 방식
- **큐 페어(Queue Pair, QP)**: 송수신 작업 요청을 HCA에 게시하는 큐 쌍

</details>

```text
1. 토폴로지 발견
        │
        ▼
2. 경로•파티션 계산
        │
        ▼
3. LID•P_Key 할당
        │
        ▼
RDMA 작업 요청
        │
        ▼
4. QP•키 연결 설정
        │
        ▼
5. 크레딧 RDMA 전송
        │
        └── 완료 상태 반환
```

**동작 원리**

1. **토폴로지 발견**: 링크•스위치•HCA 상태 수집
2. **경로•파티션 계산**: 목적지 경로와 통신 그룹 결정
3. **LID•P_Key 할당**: LID와 P_Key 배포
4. **QP•키 연결 설정**: QP와 원격 메모리 정보 공유
5. **크레딧 RDMA 전송**: 수신 버퍼 여유 안에서 전달
#### 한줄 요약

- 관리자가 주소와 길을 정하면 서버들이 작업 큐를 연결하고 각 링크가 받을 공간만큼만 자료를 보낸다.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **RoCEv2(RDMA over Converged Ethernet version 2)**: IP 이더넷에서 RDMA를 제공하는 전송 방식
- **인터넷 프로토콜(Internet Protocol, IP)**: 주소 기반 패킷 라우팅을 제공하는 프로토콜
- **전송 제어 프로토콜(Transmission Control Protocol, TCP)**: 신뢰성 있는 바이트 흐름을 제공하는 전송 프로토콜
- **중앙처리장치(Central Processing Unit, CPU)**: 범용 명령 실행과 연산을 담당하는 처리장치

</details>

| 클러스터 인터커넥트 | InfiniBand | RoCEv2 | TCP 이더넷 |
|:---|:---|:---|:---|
| 적용 기준 | **최고 성능 연산 클러스터** | 기존 이더넷 기반 **대규모 RDMA** | **범용 호환•운영 단순성** 우선 |
| 핵심 특징 | **전용 RDMA•크레딧 제어** | **IP 이더넷 기반 RDMA** | **커널 기반 신뢰 전송** |
| 한계 | **전용 장비•관리자 의존** | **혼잡•무손실 조정 복잡성** | **복사•CPU•지연 부담** |

#### 한줄 요약

- 최고 성능 전용망은 InfiniBand, 이더넷 RDMA는 RoCEv2, 범용성과 쉬운 운영은 TCP 이더넷이 알맞다.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **서브넷 관리자 단일 장애**: 토폴로지•주소•경로•파티션 변경 제어를 멈춰 패브릭 전체 운영에 영향을 주는 위험
- **InfiniBand 무역협회(InfiniBand Trade Association, IBTA)**: InfiniBand 규격과 상호운용을 관리하는 협회
- **InfiniBand 아키텍처(InfiniBand Architecture, IBA)**: InfiniBand 장치•링크•전송 동작을 규정한 규격

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 집단 통신의 **상위 링크 병목** | **비차단 용량•경로 분산** | **반복 시간 단축** |
| 서브넷 관리자의 **단일 장애** | **관리자 이중화•상태 동기화** | **제어 가용성** 확보 |
| 장비 간 **상호운용 차이** | **IBTA IBA 규격 준수 시험** | **패브릭 호환성** 확보 |

#### 한줄 요약

- 집단 통신 부하로 비차단 용량을 산정하고 서브넷 관리자 장애 전환과 장비 상호운용을 사전 검증한다.

## Ⅶ. 결론

- 전용 최고 성능은 **InfiniBand**, 이더넷 재사용은 **RoCEv2** 선택

#### 한줄 요약

- InfiniBand는 링크 속도뿐 아니라 서브넷 관리 이중화와 경로 용량, 파티션 격리를 함께 운영할 수 있을 때 선택해야 한다.
