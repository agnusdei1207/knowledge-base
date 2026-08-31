---
sidebar:
  order: 151
  label: "151. InfiniBand"
  badge:
    text: "기출 · 60%"
    variant: note
title: "InfiniBand"
date: "2026-08-31T15:08:00+09:00"
tags:
  - "notes-latest_tech"
weight: 151
extra:
  question_no: "151"
  source_status: "기출"
  source_history: "138회"
  priority: 60
  priority_note: "인피니밴드 지연•혼잡 제어가 138회 출제됨"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **인피니밴드(InfiniBand, IB)**: 고성능 컴퓨팅(HPC) 및 AI 클러스터에서 노드 간 초저지연, 고대역폭, 무손실 원격 직접 메모리 접근(RDMA)을 제공하는 전용 스위치 패브릭 기술.
- **원격 직접 메모리 접근(Remote Direct Memory Access, RDMA)**: CPU 및 운영체제 커널 개입 없이 호스트 메모리 데이터를 네트워크상에서 직접 읽고 쓰는 고성능 통신 기술.
- **인공지능(Artificial Intelligence, AI)**: 학습•추론을 수행하는 컴퓨팅 시스템
- **중앙처리장치(Central Processing Unit, CPU)**: 범용 연산•제어 프로세서

</details>

- 정의: RDMA•서브넷 관리•혼잡 제어의 **InfiniBand 패브릭**이다.
- 배경/필요성: 수만 대의 GPU가 결합된 현대 AI 슈퍼컴퓨터와 고성능 컴퓨팅(HPC) 클러스터에서 전통적인 이더넷 TCP/IP 스택은 OS 커널 개입에 따른 컨텍스트 스위칭, 다중 메모리 복사 오버헤드, 혼잡 시 패킷 드롭 및 재전송으로 인한 마이크로초 단위 지연 시간(Tail Latency) 급증과 처리량 저하를 유발함에 따라, 링크 계층 크레딧 기반 흐름 제어(Credit-based Flow Control)로 패킷 손실을 원천 방지하고 OS 커널을 우회하여 초고속 직접 전송을 구현하는 InfiniBand(InfiniBand Architecture: HDR, NDR, XDR / Ultra-low Latency RDMA, Centralized Subnet Manager: SM, Adaptive Routing, Hardware Congestion Control, Virtual Lane: VL, P_Key Isolation) 인터커넥트 패브릭을 도입하여 **노드 간 왕복 지연 1마이크로초($\mu s$) 미만의 결정적 초저지연 및 포트당 400G/800Gbps 이상의 초고대역폭 보장, 서브넷 관리자(SM)를 통한 Fat-Tree 토폴로지 중앙 경로 최적화 및 적응형 라우팅(Adaptive Routing)을 통한 핫스폿 혼잡 제거, GPU Direct RDMA를 통한 호스트 CPU 메모리 경유 없는 GPU VRAM 간 무손실 직접 통신**을 달성할 필요

#### 한줄 요약
- 중앙 경로 관리와 **서버 간 직접 메모리 통신** 결합

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **서비스 수준(Service Level, SL)**: 트래픽 우선순위와 가상 통로(Virtual Lane, VL) 매핑을 통해 트래픽을 분류하고 관리하는 논리적 속성.
- **적응형 경로(Adaptive Routing, AR)**: 네트워크 혼잡 상태를 실시간 탐지하여 다중 경로 중 최적 경로를 동적 선택하는 전달 방식.
- **호스트 채널 어댑터(Host Channel Adapter, HCA)**: RDMA 프로토콜을 구현하여 메모리 작업을 패킷화하고 전송/수신을 전담하는 하드웨어 인터페이스.

</details>

- 서브넷 관리자 기반 **주소•경로•분할 정책** 제어
- HCA 등록 메모리 기반 **저지연 RDMA 전송**
- SL•VL•적응형 경로 기반 **혼잡 제어•부하 분산**

#### 한줄 요약
- 중앙 경로 제어•직접 메모리 전송•**동적 혼잡 우회**

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **인피니밴드 스위치(InfiniBand Switch)**: 목적지 주소 및 서브넷 경로 정보를 기반으로 패킷을 고속 전달하는 저지연 패브릭 하드웨어.
- **서브넷 관리자(Subnet Manager, SM)**: 패브릭 내 장치 탐색(Discovery), 주소 할당, 경로 및 분할 정책을 중앙 집중적으로 제어하는 관리 주체.
- **전송 및 큐 계층(Transport and Queue Layer)**: 큐 페어(Queue Pair, QP), 완료 큐(Completion Queue, CQ) 기반의 신뢰성 있는 RDMA 데이터 전송 계층.
- **혼잡 및 서비스 계층(Congestion and Service Layer)**: 서비스 수준(SL), 가상 통로(VL), 혼잡 제어를 통해 트래픽 격리 및 무손실 전달을 보장하는 계층.
- **분할 키(Partition Key, P_Key)**: 통신 가능한 노드 집단을 논리적으로 분리하고 보안을 강화하기 위한 접근 식별값.

</details>

```text
                     [서브넷 관리자]
                            │
                     [인피니밴드 스위치]
                      ┌─────┴─────┐
            [호스트 채널 어댑터]  [혼잡 및 서비스 계층]
                    │
            [전송 및 큐 계층]
```
| 구성요소 | 책임 |
|:---|:---|
| 호스트 채널 어댑터(HCA) | **RDMA 요청 패킷화•호스트 종단** 처리 |
| 인피니밴드 스위치 | **경로표 기반 패킷** 전달 |
| 서브넷 관리자(SM) | **장치 발견•주소•분할 정책** 관리 |
| 전송•큐 계층 | **연결•순서•송수신 큐** 관리 |
| 혼잡•서비스 계층 | **SL•가상 통로•혼잡 제어**와 손실 방지 |

#### 한줄 요약
- HCA•스위치•서브넷 관리자의 **전용 전송 구조**

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **가상 통로(Virtual Lane)**: 한 물리 링크에서 트래픽 종류별 흐름과 버퍼를 논리적으로 분리하는 통신 경로로 정의된다.
- **경로표**: 목적지 주소에 따라 스위치가 선택할 출력 포트를 기록한 전달 정보로 정의된다.

</details>

```text
서브넷 관리자 ── 1. 장치 발견, 주소, 분할 설정 ──▶ 호스트 채널 어댑터
서브넷 관리자 ── 2. 경로, 서비스 수준, 가상 통로 구성 ──▶ 스위치
호스트 채널 어댑터 ── 3. RDMA 작업 패킷 전송 ──▶ 스위치
스위치 ── 4. 경로표 기반 패킷 전달 ──▶ 목적지 호스트 채널 어댑터
호스트 채널 어댑터 ◀── 완료 및 혼잡 신호 ────────────── 목적지 HCA
```

### 동작 원리

1. 장치 발견, 주소, 분할 설정: 통신 종단과 **P_Key 경계** 확정
2. 경로, 서비스 수준, 가상 통로 구성: **목적지•SL 경로** 게시
3. RDMA 작업 패킷 전송: HCA의 **메모리 요청** 패킷화
4. 경로표 기반 패킷 전달: **주소•가상 통로** 기반 전달

#### 한줄 요약
- 서브넷 정책 후 **RDMA 직접 통신•동적 경로** 운영

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **융합 이더넷 기반 RDMA(RDMA over Converged Ethernet, RoCE)**: 기존 이더넷 인프라 위에서 무손실 혼잡 제어를 통해 RDMA를 지원하는 프로토콜.
- **NVLink•NVSwitch**: GPU 메모리 간 초고속 데이터 전송 및 다수 GPU의 다대다 연결을 지원하는 전용 인터커넥트 기술.
- **그래픽 처리장치(Graphics Processing Unit, GPU)**: 대규모 병렬 연산에 최적화된 프로세서.

</details>

| 구분 | InfiniBand | RoCE | NVLink•NVSwitch |
|:---|:---|:---|:---|
| 적용 기준 | **전용 다중 노드 클러스터** | **이더넷 기반 기존망** | **단일 서버 내부 GPU** |
| 핵심 특징 | 관리형 **RDMA 통합 패브릭** | 이더넷 기반 **RDMA** | GPU 메모리 **고속 직접 연결** |
| 한계 | **고비용 전용 장비** 필요 | 복잡한 **무손실 환경** 구성 | **노드 간 연결 확장성** 제한 |

#### 한줄 요약
- 전용 클러스터•이더넷 RDMA•**GPU 내부 연결** 비교

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **핫스폿 혼잡**: 다수 흐름이 특정 스위치나 링크에 몰려 완료 지연이 증가하는 현상이다.
- **경로 텔레메트리**: 링크별 트래픽•지연•오류를 관측해 배치와 우회 경로를 조정하는 정보이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 잘못된 P_Key의 **테넌트 통신 노출** | **분할 정책•HCA 멤버십** 상호 검증 | 패브릭 격리 **확보** |
| 집단 통신의 **핫스폿 혼잡** | **SL•가상 통로•적응형 경로** 적용 | 완료 지연 **완화** |
| 비대칭 토폴로지의 **느린 링크 집중** | **경로 텔레메트리** 기반 순위•경로 재배치 | 대역폭 활용률 **향상** |

#### 한줄 요약
- P_Key 격리와 **적응형 경로•가상 통로** 최적화

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **전용 패브릭**: 장치•스위치•관리 체계를 고성능 클러스터 통신에 맞춰 함께 구성한 네트워크로 정의된다.
- **패브릭 격리**: P_Key 등으로 통신 가능한 종단 집단을 나누어 상호 접근을 제한하는 통제이다.

</details>

- 엑사스케일 AI 슈퍼컴퓨팅 및 분산 딥러닝 인프라의 표준 백본으로서 최고의 전송 효율을 보장하는 **초저지연 무손실 고성능 스위치 패브릭의 최고 핵심 표준(InfiniBand / NVIDIA Quantum-2 NDR & Quantum-X800 XDR / Hardware RDMA Engine / Centralized Subnet Manager & Adaptive Routing / GPUDirect RDMA / Lossless Credit Flow Control)의 확고한 표준**으로 확고히 자리 잡았으며, 차세대 XDR(1.6Tbps) 및 코패키지드 옵틱스(CPO) 기반 광 스위칭으로 진화하는 가운데, 실무 클러스터 인프라 설계 시에는 **극도의 지연 시간 민감성과 대규모 GPU All-Reduce가 요구되는 프론트엔드/백엔드 AI 학습망에는 InfiniBand 레일 최적화 토폴로지(Rail-optimized Fat-Tree)를 구축하고, 적응형 라우팅과 혼잡 알림(ECN)을 활성화하며, P_Key 기반 멀티테넌트 보안 격리**를 결합하여 완벽한 네트워크 처리량과 무손실 분산 훈련 성능을 완성

#### 한줄 요약

- 초저지연•중앙 관리가 필요하면 **InfiniBand**, 기존망은 RoCE
