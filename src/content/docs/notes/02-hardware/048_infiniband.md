---
sidebar:
  order: 48
  label: "048. InfiniBand (InfiniBand)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "InfiniBand (InfiniBand)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-hardware"
weight: 48
extra:
  question_no: "048"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "RDMA•집단 통신의 단일 기출 핵심"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **InfiniBand**: RDMA와 저지연 스위칭을 제공하는 고성능 컴퓨팅용 네트워크 패브릭이다.
- **원격 직접 메모리 접근(Remote Direct Memory Access, RDMA)**: 사전 등록한 원격 메모리에 상대 CPU의 복사 개입 없이 직접 접근하는 통신 방식이다.
- **커널 우회(Kernel Bypass)**: 통신 데이터 경로에서 운영체제 커널의 반복적인 처리와 문맥 전환을 줄이는 방식이다.
- **중앙 처리 장치(Central Processing Unit, CPU)**: 일반 네트워크에서 데이터 복사와 커널 프로토콜 처리를 수행하는 프로세서이다.

</details>

- 정의/개념: HCA·스위치와 RDMA 전송으로 컴퓨팅 노드의 등록 메모리를 연결하는 **저지연 고성능 네트워크 패브릭**이다.
- 배경/필요성: 커널 네트워크 경로와 CPU 데이터 복사를 반복하면 **통신 지연·CPU 사용량이 증가한다**.

#### 한줄 요약

- InfiniBand는 RDMA와 커널 우회로 노드 간 데이터 복사와 문맥 전환을 줄여 집단 통신 지연을 낮춘다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **메모리 등록(Memory Registration)**: HCA가 접근할 메모리 주소 범위와 권한 키를 미리 등록하는 절차이다.
- **호스트 채널 어댑터(Host Channel Adapter, HCA)**: 호스트 메모리와 InfiniBand 패브릭 사이에서 RDMA 전송을 처리하는 어댑터이다.
- **크레딧 기반 흐름 제어(Credit-based Flow Control)**: 수신 버퍼의 여유만큼만 전송하여 버퍼 초과 손실을 방지하는 제어 방식이다.
- **집단 통신(Collective Communication)**: 여러 계산 노드가 데이터를 합산•분배•교환하는 다자간 통신이다.
- **인피니밴드(InfiniBand)•원격 직접 메모리 접근(Remote Direct Memory Access, RDMA)**: 저지연 패브릭과 원격 메모리 직접 접근 방식이다.

</details>

- 원격 CPU•커널을 거치지 않는 **등록 메모리•HCA 전송**이 핵심이다.
- 무손실 링크를 만드는 **크레딧 흐름 제어**가 핵심이다.
- **혼잡 증가•비효율 토폴로지**에서 집단 통신 처리량 저하된다.

#### 한줄 요약

- 등록 메모리와 HCA는 CPU 복사 없이 데이터를 전송하고, 링크별 크레딧 흐름 제어는 수신 버퍼 초과 손실을 막는다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **큐 페어(Queue Pair, QP)**: 송신 큐와 수신 큐로 구성되어 원격 직접 메모리 접근(Remote Direct Memory Access, RDMA) 작업을 게시하는 통신 종단점이다.
- **완료 큐(Completion Queue, CQ)**: 게시한 RDMA 작업의 성공이나 오류 완료 상태를 응용에 전달하는 큐이다.
- **서브넷 관리자(Subnet Manager)**: InfiniBand의 주소와 경로, 파티션 및 포트 상태를 설정하는 관리자이다.
- **호스트 채널 어댑터(Host Channel Adapter, HCA)•직접 메모리 접근(Direct Memory Access, DMA)**: 큐 작업을 처리하고 호스트 메모리를 직접 전송하는 어댑터와 방식이다.

</details>

```text
[HCA•QP•CQ 엔드포인트 집합] -- [스위치 패브릭]
                                       |
                                 [서브넷 관리자]
```

선의 의미: 엔드포인트 집합이 스위치 패브릭에 접속하고 서브넷 관리자가 해당 패브릭의 주소•경로•접근 경계를 관리하는 정적 연결 관계다.

| 구성요소 | 책임 |
|:---|:---|
| HCA•QP•CQ 엔드포인트 집합 | DMA 송수신•**완료 처리** |
| 스위치 패브릭 | 전달•흐름 제어•**경로 선택** |
| 서브넷 관리자 | 주소•경로•**접근 경계 설정** |

#### 한줄 요약

- 서브넷 관리자가 경로를 정하고 HCA와 스위치가 등록 메모리 사이를 직접 전송한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **작업 요청(Work Request)**: 응용이 큐 페어(Queue Pair, QP)에 게시하는 송수신 또는 원격 직접 메모리 접근(Remote Direct Memory Access, RDMA) 읽기•쓰기 명령이다.
- **등록 키(Registration Key)**: 호스트 채널 어댑터(Host Channel Adapter, HCA)가 원격 메모리의 주소 범위와 접근 권한을 검증하는 값이다.
- **직접 메모리 접근(Direct Memory Access, DMA)**: HCA가 CPU 복사 없이 호스트 메모리와 장치 사이에서 데이터를 전송하는 방식이다.

</details>

```text
                [등록 메모리 RDMA 쓰기 게시]
                               |
                   1. 송신 HCA 버퍼 DMA 읽기
                               |
              +----------------------------------+
              | 반복: 링크 전송 패킷            |
              | 2. QP 패킷•패브릭 전달         |
              | 3. 수신 등록 키•권한 검증      |
              | 4. 원격 등록 메모리 DMA 쓰기    |
              +----------------------------------+
                               |
                     [전송 확인 응답]
                               |
                       [CQ 완료 상태]
```

**동작 원리**

1. **송신 버퍼 DMA 읽기**: 송신 HCA가 작업 요청의 로컬 등록 메모리에서 CPU 복사 없이 데이터를 회수한다.
2. **QP 패킷·패브릭 전달**: QP 전송 상태와 링크 크레딧을 확인해 스위치 경로로 패킷을 전달한다.
3. **원격 키·권한 검증**: 수신 HCA가 등록 키, 원격 주소 범위와 쓰기 권한을 확인한다.
4. **원격 메모리 기록·완료**: 수신 HCA가 등록 메모리에 DMA 기록하고 확인 응답을 보내 송신 측 CQ에 완료 상태를 생성한다.

#### 한줄 요약

- RDMA 쓰기에서는 송신 HCA가 등록 버퍼를 읽어 전송하고, 수신 HCA가 원격 키를 검증한 뒤 등록 메모리에 직접 기록한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **융합 이더넷 기반 원격 직접 메모리 접근(RDMA over Converged Ethernet, RoCE)**: 이더넷에서 RDMA Verbs와 네트워크 어댑터로 원격 메모리에 접근하는 방식이다.
- **원격 직접 메모리 접근 동작(Remote Direct Memory Access Verbs, RDMA Verbs)**: 메모리 등록과 큐 생성, 작업 게시 및 완료 회수를 응용에 제공하는 표준 인터페이스이다.
- **전송 제어 프로토콜•인터넷 프로토콜(Transmission Control Protocol•Internet Protocol, TCP/IP)**: 신뢰 전송과 주소 및 라우팅을 제공하는 범용 인터넷 프로토콜 모음이다.
- **고성능 컴퓨팅(High-Performance Computing, HPC)•인공지능(Artificial Intelligence, AI)**: 대규모 병렬 계산과 신경망 학습을 수행하는 워크로드이다.
- **원격 직접 메모리 접근 네트워크 인터페이스 카드(RDMA Network Interface Card, RNIC)•우선순위 기반 흐름 제어(Priority Flow Control, PFC)•명시적 혼잡 알림(Explicit Congestion Notification, ECN)**: RoCE 전송과 무손실•혼잡 제어를 담당하는 장치 및 기능이다.

</details>

| 원격 통신 방식 | InfiniBand | RoCE | TCP/IP |
|:---|:---|:---|:---|
| 적용 기준 | HPC•AI **집단 통신** | 기존 이더넷 기반 **RDMA** | 범용 연결•**호환성** |
| 핵심 특징 | 전용 스위치•**HCA•Verbs** | 이더넷•**RNIC•Verbs** | 이더넷•IP•**커널 소켓** |
| 한계 | 전용 장비•**운영 비용** | PFC•ECN **조정 복잡도** | CPU•커널 **경로 오버헤드** |

> 요약: 전용망은 InfiniBand, 이더넷은 RoCE가 적합하다.

#### 한줄 요약

- 전용 HPC·AI 패브릭은 InfiniBand, 기존 이더넷에서 RDMA가 필요하면 RoCE, 범용 호환성이 우선이면 TCP/IP가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **키 폐기(Key Revocation)**: 등록 메모리의 사용이 끝난 뒤 기존 접근 권한이 다시 쓰이지 못하도록 무효화하는 절차이다.
- **QP 오류 상태(QP Error State)**: 전송 실패나 시간 초과 후 해당 큐 페어가 정상 작업을 수행할 수 없는 상태이다.
- **핫스폿(Hotspot)**: 특정 통신 경로나 스위치 포트에 트래픽이 집중되어 대기와 지연이 커지는 병목 지점이다.
- **상류 전파(Upstream Propagation)**: 하류 버퍼의 크레딧 부족이 앞선 링크들의 송신 정지와 대기로 연쇄 확산되는 현상이다.
- **그래픽 처리 장치 직접 원격 메모리 접근(GPUDirect Remote Direct Memory Access, GPUDirect RDMA)**: 그래픽 처리 장치(Graphics Processing Unit, GPU) 메모리와 원격 호스트 채널 어댑터(Host Channel Adapter, HCA)가 중앙 처리 장치(Central Processing Unit, CPU) 복사 없이 직접 통신하는 방식이다.
- **인공지능(Artificial Intelligence, AI)**: 다중 가속기의 집단 통신을 요구하는 학습 워크로드이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 등록 키·버퍼 수명이 맞지 않아 **허용 범위 밖 메모리 접근** | 필요한 범위만 등록하고 사용 후 **키 폐기·버퍼 소유권 검증** | 오래된 키 재사용 차단으로 **원격 메모리 보호 강화** |
| 링크·노드 장애 후 QP가 오류 상태에 남아 **통신 재개 불가** | 오류·타임아웃 원인을 분류하고 **QP와 대체 경로 재생성** | 실패 연결을 새 경로로 복구해 **통신 복구성 향상** |
| 집단 통신 경로가 특정 스위치 포트에 몰려 **핫스폿 발생** | 통신 토폴로지에 맞춘 작업 배치와 **다중 경로 부하 분산** | 포트별 트래픽 균등화로 **혼잡·꼬리 지연 완화** |
| 하류 크레딧 부족이 앞선 링크에 전파되어 **패브릭 전체 대기 증가** | 포트별 크레딧·대기와 집단 통신 지연을 감시해 **경로·전송률 조정** | 병목 포트 부하 완화로 **상류 전파 제한** |

> **GPUDirect RDMA**로 CPU 복사•집단 통신 대기 감소

#### 한줄 요약

- GPUDirect RDMA는 GPU 메모리와 원격 HCA를 직접 연결해 CPU 복사와 집단 통신 대기를 줄인다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **고성능 컴퓨팅(High-performance Computing, HPC)**: 여러 계산 노드로 대규모 과학•공학 연산을 병렬 처리하는 컴퓨팅이다.
- **전용 패브릭(Dedicated Fabric)**: 특정 고성능 통신을 위해 전용 어댑터와 스위치 및 관리 체계를 사용하는 연결망이다.
- **기존 이더넷(Existing Ethernet)**: 범용 네트워크 인프라를 유지하면서 원격 직접 메모리 접근 등의 기능을 추가해 사용하는 환경이다.
- **인공지능(Artificial Intelligence, AI)•융합 이더넷 기반 원격 직접 메모리 접근(RDMA over Converged Ethernet, RoCE)**: 대규모 집단 통신 워크로드와 기존 이더넷에서 사용하는 원격 메모리 접근 방식이다.

</details>

- **전용 HPC•AI 망**은 InfiniBand, **기존 이더넷**은 RoCE을 선택한다.

#### 한줄 요약

- 노드 간 통신 시간이 연산 시간을 지배하고 전용 장비·운영 비용을 상쇄할 때 InfiniBand 패브릭을 검토한다.
