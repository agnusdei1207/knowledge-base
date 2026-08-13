---
sidebar:
  order: 48
  label: "048. InfiniBand (InfiniBand)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "InfiniBand (InfiniBand)"
date: "2026-08-13T12:00:06+09:00"
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

- **인피니밴드(InfiniBand)**: 초고속·저지연 Switched Fabric 기반 고성능 컴퓨팅(HPC) 및 AI 클러스터용 상호연결망 기술.
- **원격 직접 메모리 접근(Remote Direct Memory Access, RDMA)**: OS 커널 및 CPU 개입 없이 원격 메모리에 직접 읽기·쓰기를 수행하는 기술.
- **커널 우회(Kernel Bypass)**: 네트워크 I/O 시 OS 프로토콜 스택 처리 및 잦은 Context Switch를 방지하는 제어 구조.
- **중앙 처리 장치(Central Processing Unit, CPU)**: 일반 네트워크 프로토콜 스택(TCP/IP) 처리 및 패킷 소켓 버퍼 복사를 총괄하는 중앙 연산 장치.

</details>

- 정의/개념: HCA 어댑터, 전용 스위치 및 **RDMA** 하드웨어 전송 기법을 통해 노드 간 메모리를 고속 연결하는 **InfiniBand** 패브릭
- 배경/필요성: 기존 소켓 기반 커널 TCP/IP 네트워크의 데이터 복사 오버헤드, 커널 문맥 전환 지연 및 높은 CPU 점유율 극복

#### 한줄 요약

- InfiniBand는 RDMA와 커널 우회로 노드 간 데이터 복사와 문맥 전환을 줄여 집단 통신 지연을 낮춘다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **메모리 등록(Memory Registration)**: RDMA 전송 대상 메모리 영역을 HCA에 핀(Pin) 고정하고 가상-물리 주소 변환 및 접근 키(rkey/lkey)를 할당하는 사전 작업.
- **호스트 채널 어댑터(Host Channel Adapter, HCA)**: 호스트 메모리 버스(PCIe)와 InfiniBand 패브릭을 연결하는 전용 네트워크 하드웨어 인라인 카드.
- **크레딧 기반 흐름 제어(Credit-Based Flow Control)**: 수신 버퍼의 여유 크레딧(Credit) 수량만큼만 송신하여 버퍼 오버플로우 패킷 드랍을 원천 차단하는 무손실 제어.
- **집단 통신(Collective Communication)**: 분산 클러스터 간 All-Reduce, All-Gather 등 대용량 데이터 축소 및 공유 연산 패브릭 통신.

</details>

- **메모리 등록** 기반 원격 메모리 직결 및 **커널 우회** 구현
- 수신 버퍼 오버플로우에 따른 신호 손실을 방지하는 **크레딧 기반 흐름 제어**
- HPC 및 AI 분산 클러스터링의 **집단 통신** 대역폭 극대화

#### 한줄 요약

- 등록 메모리와 HCA는 CPU 복사 없이 데이터를 전송하고, 링크별 크레딧 흐름 제어는 수신 버퍼 초과 손실을 막는다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **큐 쌍(Queue Pair, QP)**: RDMA 작업을 요청하는 송신 큐(SQ)와 수신 큐(RQ)의 쌍으로 구성된 통신 종단점.
- **완료 큐(Completion Queue, CQ)**: QP에 등록된 요청 작업의 완료 상태(Work Completion) 결과를 비동기 통지받는 큐.
- **서브넷 관리자(Subnet Manager, SM)**: InfiniBand 서브넷 내의 노드 탐색, 주소(LID) 할당, 라우팅 테이블 및 QoS 구성을 관리하는 제어 소프트웨어.

</details>

```text
[HCA•QP•CQ 엔드포인트 집합] -- [스위치 패브릭]
                                       |
                                 [서브넷 관리자]
```

선의 의미: 엔드포인트 집합이 스위치 패브릭에 물리 연결되고 서브넷 관리자가 해당 패브릭의 토폴로지 및 라우팅 경로를 총괄 제어하는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| HCA•QP•CQ 엔드포인트 집합 | RDMA 요청 생성, 하드웨어 DMA 전송 및 **CQ** 작업 완료 통지 |
| 스위치 패브릭 | 무손실 패킷 라우팅, **크레딧 기반 흐름 제어** 및 패킷 스위칭 |
| 서브넷 관리자 | LID 주소 관리, 파티셔닝 정책 설정 및 최적 경로 구축 |

#### 한줄 요약

- 서브넷 관리자가 경로를 정하고 HCA와 스위치가 등록 메모리 사이를 직접 전송한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **작업 요청(Work Request, WR)**: 애플리케이션이 QP의 SQ/RQ에 제출하는 RDMA Read/Write 명령 객체.
- **등록 키(Registration Key, rkey/lkey)**: HCA가 원격/로컬 메모리 영역의 접근 권한 및 물리 주소를 검증하는 인증 키.
- **직접 메모리 접근(Direct Memory Access, DMA)**: CPU 조율 없이 HCA가 호스트 메모리와 패브릭 간 데이터를 직접 이동시키는 기술.

</details>

```text
                [등록 메모리 RDMA 쓰기 게시]
                               |
                   1. 송신 버퍼 DMA 읽기
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

### 동작 원리

1. **송신 버퍼 DMA 읽기**: 애플리케이션의 RDMA Write **작업 요청** 인가 시, 송신 HCA가 **DMA**로 로컬 등록 메모리 데이터 인출.
2. **QP 패킷·패브릭 전달**: **QP** 및 하드웨어 흐름 제어 조건 검증 후 InfiniBand 패브릭으로 패킷 분할 송출.
3. **수신 등록 키·권한 검증**: 수신 노드 HCA가 패킷 내 포함된 원격 **등록 키** 및 가상 주소 접근 권한 검증.
4. **원격 등록 메모리 DMA 쓰기**: 수신 HCA가 등록 메모리에 **DMA** 쓰기를 수행하고 **CQ** 이벤트 기록.

#### 한줄 요약

- RDMA 쓰기에서는 송신 HCA가 등록 버퍼를 읽어 전송하고, 수신 HCA가 원격 키를 검증한 뒤 등록 메모리에 직접 기록한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **RoCE(RDMA over Converged Ethernet)**: 표준 이더넷 망 상에서 UDP/IP 캡슐화를 통해 RDMA Verbs를 구동하는 통신 기술.
- **RDMA 버브(RDMA Verbs)**: 원격 메모리 접근을 위해 애플리케이션에 제공되는 표준 API 인터페이스.
- **TCP/IP(Transmission Control Protocol/Internet Protocol)**: OS 커널 스택을 경유하여 계층적 데이터 전송을 수행하는 범용 인터넷 프로토콜.

</details>

| 원격 통신 방식 | InfiniBand | RoCE (RoCEv2) | TCP/IP |
|:---|:---|:---|:---|
| 적용 기준 | 미션크리티컬 HPC/AI **집단 통신** 환경 | 기존 이더넷 기반 데이터센터 **RDMA** 구축 시 | 범용 서버 간 네트워크 및 인프라 통신 시 |
| 핵심 특징 | **InfiniBand** 전용 패브릭 및 HCA 하드웨어 | **RoCE** 무손실 이더넷(PFC/ECN) 활용 | 범용 **TCP/IP** OS 커널 프로토콜 스택 |
| 한계 | 전용 하드웨어 도입 단가 및 관리 복잡성 | PFC 튜닝 복잡성 및 쇄도 동결(Pause Flood) 위험 | CPU 커널 복사 및 높은 대기 지연시간 |

> 요약: 극초저지연은 InfiniBand, 이더넷 재활용은 RoCE, 범용은 TCP/IP 선택.

#### 한줄 요약

- 전용 HPC·AI 패브릭은 InfiniBand, 기존 이더넷 환경에서 RDMA 가속이 필요하면 RoCE, 범용 호환성이 우선이면 TCP/IP 선택이 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **키 폐기(Key Revocation)**: RDMA 전송 완료 후 할당된 rkey/lkey를 무효화하여 무단 메모리 접근을 차단하는 보안 절차.
- **QP 오류 상태(QP Error State)**: 전송 타임아웃 또는 미인가 접근 발생 시 해당 QP가 잠김 처리되는 예외 상태.
- **GPUDirect RDMA(GPU Direct Remote Direct Memory Access)**: CPU 메인 메모리 복사를 제거하고 GPU VRAM과 HCA를 직접 연결하는 RDMA 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 낡은 **등록 키** 노출에 따른 원격 메모리 무단 침범 위험 | RDMA 전송 완료 후 즉시 **키 폐기** 및 영역 해제 | 메모리 경계 오염 및 세그먼트 오류 방지 |
| 네트워크 순간 패킷 에러에 의한 **QP 오류 상태** 전환 | 에러 복구 핸들러 구축 및 자동 QP 리셋/재연결 | 시스템 세션 가용성 확보 |
| 특정 스위치 링크로 트래픽이 쏠려 혼잡 발생 | Adaptive Routing 및 **다중 경로 부하 분산** 적용 | 트래픽 핫스폿 방지 및 대역폭 균등화 |
| CPU-GPU 간 데이터 전송 복사로 인한 병목 | **GPUDirect RDMA** 기술 기반 VRAM-HCA 직결 | CPU 점유율 제어 및 통신 지연시간 최소화 |

> 사례: 대규모 GPU 클러스터 간 **GPUDirect RDMA** 기반 All-Reduce 통신 가속

#### 한줄 요약

- GPUDirect RDMA는 GPU 메모리와 HCA를 직접 연결해 CPU 복사와 집단 통신 대기를 줄인다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **패브릭 선택 기준(Fabric Selection Criteria)**: 지연시간 상한, 네트워크 구축 예산, 기존 인프라 호환성을 평가하여 최적 패브릭을 결정하는 기준.

</details>

- **패브릭 선택 기준**에 따라 최고 성능의 초저지연망은 **InfiniBand**, 기존 이더넷 인프라 활용 시 **RoCE** 적용

#### 한줄 요약

- 초저지연 전용망은 InfiniBand, 기존 이더넷 재활용은 RoCE를 선택한다.
