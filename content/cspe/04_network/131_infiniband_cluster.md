---
title: "InfiniBand 클러스터 인터커넥트 (InfiniBand Cluster)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 131
---

# 📖 【암기용】 개념 완전 이해

> 목적: InfiniBand 클러스터 인터커넥트를 처음 봐도 클러스터 내부 통신 구조와 RDMA 의미를 이해하게 만든다.

## 한눈에
- **개요**: HPC·AI 클러스터 노드를 RDMA로 묶는 저지연 패브릭
- **왜 필요한가**: GPU 학습·MPI 계산은 노드 간 gradient·message 교환이 병목이다. HDR 200Gb/s, NDR 400Gb/s, XDR 800Gb/s급 링크는 계산 장치 대기 시간을 줄인다.
- **핵심 직관**: CPU가 택배를 일일이 포장하지 않고, NIC가 상대 메모리로 물건을 직접 옮기는 전용 물류망이다.

## 깊이 이해
- **배경·문제의식**: TCP/IP 이더넷은 커널 네트워크 스택과 복사 비용이 발생한다. InfiniBand는 RDMA, Queue Pair, Completion Queue로 애플리케이션 버퍼 간 전송을 직접 처리한다.
- **작동 원리**: 애플리케이션은 Verbs API로 Send/Receive·RDMA Read·RDMA Write 작업 요청을 QP에 등록한다. HCA가 패킷화·흐름제어·완료 통지를 수행한다.
- **비유**: 일반 택배가 물류센터를 거친다면, RDMA는 사전 등록된 출입증으로 창고 선반에 직접 입출고하는 방식이다.
- **구체 예시**: 512개 GPU 학습 클러스터에서 NDR 400Gb/s 포트와 SHARP in-network reduction을 적용하면 All-Reduce 일부 연산을 스위치가 집계한다.
- **흔한 오해·주의점**: InfiniBand는 단순 케이블 속도 문제가 아니다. Subnet Manager, lossless fabric, MTU, PFC가 아닌 credit 기반 흐름제어까지 함께 설계해야 한다.

## 연결 개념
- RDMA over Converged Ethernet — 이더넷에서 RDMA를 구현하는 대안
- All-Reduce — AI 학습에서 InfiniBand 대역폭을 많이 쓰는 집합 통신
- Fat-tree / Dragonfly+ — 대규모 클러스터 패브릭 토폴로지

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식이다.
> 핵심: InfiniBand 답안은 속도 나열이 아니라 RDMA 구조, 패브릭 토폴로지, 운영 지표를 연결해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: InfiniBand Cluster는 HCA와 스위치를 통해 노드 메모리 간 RDMA 전송을 제공하는 HPC·AI 전용 클러스터 패브릭이다.
> 2. **가치**: HDR 200Gb/s, NDR 400Gb/s, XDR 800Gb/s급 링크와 SHARP 집계로 MPI·NCCL 통신 병목을 낮춘다.
> 3. **판단 포인트**: 포트 속도보다 bisection bandwidth, oversubscription ratio, job all-reduce time, fabric error counter를 함께 판단한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| HPC·AI 클러스터 네트워크 이해 확인 | RDMA, HCA, QP, CQ, Subnet Manager, SHARP | 단순 400Gb/s 링크로만 설명 |
| 이더넷 대비 선택 기준 확인 | 커널 우회, lossless fabric, fat-tree·Dragonfly+ | TCP/IP와 동일한 패킷망으로 오해 |
| 운영 리스크 판단 확인 | congestion, cable BER, SM 이중화, job 통신시간 | 벤치마크 없이 도입 효과 단정 |

> 요약: 출제자는 InfiniBand를 RDMA 기반 클러스터 패브릭으로 이해하고 설계·운영 지표까지 연결하는지 확인한다.

---

## Ⅰ. 개요 및 필요성

- 개요: RDMA 기반 클러스터 패브릭
- 배경: GPU·MPI 워크로드는 노드 간 통신 지연이 계산 장치 유휴 시간으로 전환됨
- 필요성: NDR 400Gb/s, XDR 800Gb/s 링크로 학습 All-Reduce와 MPI 메시지 교환 병목 통제
- 판단 기준: bisection bandwidth, oversubscription 1:1~2:1, fabric error counter 기준으로 설계 검증

---

## Ⅱ. 구조 및 구성요소

```text
Compute Node / GPU -> HCA -> Leaf Switch -> Spine Switch -> HCA -> Peer Node
                         +-> Subnet Manager / Telemetry / SHARP
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| HCA | Verbs 요청을 패킷 전송으로 변환 | RDMA Read/Write, Send/Receive 처리 |
| InfiniBand Switch | 포트 간 무손실 패브릭 구성 | HDR 200Gb/s, NDR 400Gb/s, XDR 800Gb/s |
| Subnet Manager | LID·라우팅·파티션 관리 | SM 이중화와 장애 전환 필요 |
| SHARP | 스위치 내부 집합 연산 수행 | All-Reduce 일부 연산을 네트워크에서 집계 |

> 요약: InfiniBand는 HCA·스위치·SM·SHARP가 RDMA 전송과 클러스터 집합 통신을 분담하는 구조이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Buffer 등록 -> QP 생성 -> Work Request 등록 -> HCA DMA 전송
-> Switch 라우팅 -> CQ 완료 통지 -> Telemetry 수집
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 애플리케이션 버퍼를 메모리 등록 | MR key, page pinning 오류 0건 |
| 2 | QP·CQ 생성 후 RDMA 작업 등록 | QP state RTS 도달 |
| 3 | HCA가 DMA와 패킷화를 수행 | retransmit, symbol error 확인 |
| 4 | 스위치가 LID 기반으로 패킷 전달 | congestion counter, VL 사용률 확인 |
| 5 | CQ가 완료 이벤트를 반환 | p99 latency, job communication time 측정 |

> 요약: InfiniBand는 애플리케이션 버퍼 등록부터 HCA DMA, 스위치 라우팅, CQ 완료 통지까지 커널 복사 없이 처리한다.

---

## Ⅳ. 특징

| 구분 | 일반 이더넷 클러스터 | InfiniBand 클러스터 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 전송 방식 | TCP/IP 스택 경유 | RDMA 커널 우회 | CPU copy 감소, verbs 기반 전송 |
| 흐름제어 | 손실 후 재전송 중심 | credit 기반 무손실 패브릭 | congestion counter로 확인 |
| 클러스터 연산 | 호스트가 집계 수행 | SHARP가 네트워크 집계 지원 | All-Reduce 시간 측정 |
| 적용 영역 | 범용 서비스망 | HPC·AI 학습망 | HDR/NDR/XDR 포트 선택 |

> 요약: InfiniBand는 범용 네트워크가 아니라 RDMA와 무손실 패브릭을 전제로 한 HPC·AI 클러스터 전용 설계이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | InfiniBand | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Ethernet + TCP/RoCE | Native IB + SM | 운용 조직의 RDMA·SM 역량 |
| 비용/성능 | 범용 스위치 활용 | 전용 HCA·스위치 필요 | GPU idle time 감소액과 장비 비용 비교 |
| 운영/위험 | IP 운영 도구 성숙 | Fabric counter 중심 운영 | 케이블·펌웨어·SM 장애 대응 체계 |

> 요약: InfiniBand 선택은 포트 단가가 아니라 학습 작업 통신시간 절감과 전용 패브릭 운영 역량으로 결정한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 혼잡 확산 | leaf-spine oversubscription 과다 | 1:1 non-blocking 또는 job 배치 제약 | port xmit wait, VL stall |
| 링크 오류 | DAC/AOC 품질·온도 문제 | 케이블 인증, BER 모니터링 | symbol error, link down count |
| SM 장애 | 단일 Subnet Manager 구성 | active/standby SM 이중화 | SM failover time, routing convergence |

> 요약: 운영 리스크는 혼잡·물리 링크·SM 장애로 나누고 fabric counter와 failover 지표로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 대역폭 | 포트별 HDR 200Gb/s·NDR 400Gb/s 근접 | ib_write_bw, NCCL test |
| 지연 | 마이크로초 단위 RTT 유지 | ib_send_lat, MPI ping-pong |
| 운영 품질 | error counter 0 유지, job 실패율 1% 이하 | UFM, ibdiagnet, scheduler log |

> 요약: 도입 효과는 링크 속도보다 RDMA 벤치마크, NCCL/MPI 작업 시간, error counter로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. GPU 학습 클러스터는 leaf-spine 1:1 non-blocking 기준으로 NDR 400Gb/s 이상 포트를 배치한다.
2. MPI·NCCL 워크로드는 SHARP, GPUDirect RDMA, NCCL topology file을 함께 검증한다.
3. 운영 단계는 ibdiagnet, UFM, switch telemetry로 congestion·symbol error·SM 상태를 상시 점검한다.

**결론 (2줄):**
- 기술사 판단: GPU 유휴 시간이 통신 병목에서 발생하면 InfiniBand를 우선 검토하고, 범용 서비스망이면 이더넷·RoCE와 비교한다.
- 향후 방향: XDR 800Gb/s와 in-network computing 확대로 AI 클러스터 네트워크는 계산 장치 일부처럼 설계된다.

### 🔀 문제 유형별 목차 전환

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "InfiniBand를 설명하시오" | RDMA 전송 흐름과 HCA/QP/CQ | 이더넷 대비 구조 차이 |
| 요구사항 명시형 | "AI 클러스터망을 설계하시오" | NDR/XDR 토폴로지와 SHARP 적용 | oversubscription, error counter, job time |

> 요약: 설명형은 RDMA 원리를 넓게 쓰고, 설계형은 토폴로지와 운영 지표를 중심으로 목차를 전환한다.
