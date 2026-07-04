---
title: "RoCE (RDMA over Converged Ethernet)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 254
---

# 📖 【암기용】 개념 완전 이해

> 목적: RoCE를 Ethernet 위에서 RDMA semantics를 사용하도록 만든 방식으로 이해하게 만든다.

## 한눈에
- **개요**: RDMA를 Converged Ethernet 환경에서 사용하게 하는 network protocol
- **왜 필요한가**: InfiniBand 전용망 없이 기존 Ethernet 운영 체계와 switch 생태계를 활용하면서 RDMA data path를 쓰려는 요구가 있다.
- **핵심 직관**: 전용 철도인 InfiniBand 대신, 기존 고속도로에 전용 차선과 신호 제어를 붙여 RDMA 차량이 달리게 하는 방식이다.

## 깊이 이해
- **배경·문제의식**: AI cluster와 storage fabric은 RDMA가 필요하지만, 조직에 따라 Ethernet 표준 운영, IP routing, 장비 공용화가 설계 제약으로 작동한다.
- **작동 원리**: RoCEv1은 L2 Ethernet, RoCEv2는 UDP/IP 기반 L3 routing을 사용하고, RNIC가 RDMA verbs를 Ethernet packet으로 캡슐화해 전송한다.
- **비유**: 물류 컨테이너 규격은 RDMA로 유지하되, 운송 도로는 Ethernet 도로망을 쓰는 구조다.
- **구체 예시**: RoCE fabric은 PFC, ECN, DCQCN 같은 혼잡 제어와 lossless 또는 near-lossless 운영 설정으로 tail latency와 packet loss를 통제한다.
- **흔한 오해·주의점**: RoCE는 Ethernet을 쓰므로 설정 없이 동작한다는 생각은 위험하다. PFC misconfiguration은 pause storm, HOL blocking, packet loss를 유발할 수 있다.

## 연결 개념
- RDMA — RoCE가 제공하는 원격 memory 접근 semantics
- PFC/ECN — RoCE lossless fabric 운영의 핵심 제어
- InfiniBand — RoCE와 비교되는 전용 RDMA fabric

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: RoCE는 RDMA over Ethernet의 이점과 PFC/ECN 운영 리스크를 함께 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: RoCE는 Ethernet fabric에서 RDMA read/write/send semantics를 제공하는 protocol임.
> 2. **가치**: Ethernet 장비·IP 운영 체계를 활용하면서 AI/HPC/storage workload의 zero-copy 통신을 구현함.
> 3. **판단 포인트**: PFC, ECN, congestion control 설정이 RoCE 품질을 좌우하므로 network 운영 성숙도가 선택 기준임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| RoCE 구조 이해 확인 | RoCEv1 L2, RoCEv2 UDP/IP, RNIC | Ethernet이면 TCP와 같다고 설명 |
| 운영 조건 확인 | PFC, ECN, QoS, congestion control | 무손실 설정 필요성 누락 |
| 선택 기준 확인 | InfiniBand vs RoCE | RoCE를 비용 절감으로만 단정 |

> 요약: 이 문제는 RDMA semantics와 Ethernet 운영 제어를 동시에 이해하는지를 확인한다.

---

## Ⅰ. 개요 및 필요성

- 개요: Ethernet 기반 RDMA
- 배경: InfiniBand 전용망은 HPC/AI 성능에 맞지만, 많은 데이터센터는 Ethernet 운영 표준과 장비 공용화를 요구함.
- 필요성: Ethernet fabric에서 RDMA를 쓰되 PFC/ECN으로 packet loss와 congestion을 통제해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Application -> RDMA Verbs -> RoCE RNIC -> Ethernet Switch Fabric -> Remote RoCE RNIC
                              +-> PFC / ECN / QoS / Congestion Control
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| RoCE RNIC | RDMA 요청을 Ethernet frame 또는 UDP/IP packet으로 처리 | RoCEv1/v2 지원 확인 |
| Ethernet Switch | RDMA traffic forwarding | PFC, ECN, QoS 필요 |
| DCB/PFC | priority별 pause 제어 | misconfiguration 시 HOL blocking |
| Congestion Control | 혼잡 감지와 rate 조절 | DCQCN 등 구현 |

> 요약: RoCE는 RDMA endpoint와 Ethernet switch fabric, DCB/PFC/ECN 설정이 함께 맞아야 production traffic을 처리한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Memory 등록 -> RDMA Work Request -> RNIC가 RoCE packet 생성
-> Ethernet QoS/PFC 적용 -> Remote RNIC 수신 -> Remote buffer 반영 -> Completion 확인
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | RDMA buffer와 queue pair 구성 | QP ready |
| 2 | RNIC가 RoCEv2 UDP/IP packet으로 캡슐화 | packet format |
| 3 | switch가 priority와 ECN에 따라 forwarding | PFC/ECN counter |
| 4 | remote RNIC가 memory에 직접 반영 | completion status |

> 요약: RoCE는 RDMA 처리 흐름을 유지하면서 Ethernet QoS와 congestion control로 packet loss를 억제한다.

---

## Ⅳ. 특징

| 구분 | InfiniBand | RoCE | 판단 기준 |
|:---|:---|:---|:---|
| 물리/링크 | 전용 fabric | Ethernet fabric | 기존망 활용 여부 |
| 라우팅 | subnet manager 기반 | RoCEv2는 IP routing 가능 | L3 확장 요구 |
| 운영 제어 | IB fabric counter | PFC, ECN, QoS, DCQCN | 네트워크 운영 역량 |
| 리스크 | 전용 장비 의존 | pause storm, loss 설정 오류 | 장애 격리 절차 |

> 요약: RoCE는 Ethernet 통합 이점이 있지만 lossless Ethernet 운영 설계가 InfiniBand보다 더 세밀하게 요구될 수 있다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | TCP/IP Ethernet | RoCE RDMA over Ethernet | CPU overhead와 p99 latency |
| 비용/성능 | 장비 공용화 | RNIC, DCB switch, 설정 검증 | 기존 Ethernet 자산 활용 |
| 운영/위험 | 일반 L3 운영 | PFC/ECN/QoS 운영 | pause storm 대응 역량 |

> 요약: RoCE는 Ethernet 운영 표준을 유지하면서 RDMA가 필요한 조직에 적합하지만, 무손실 fabric 설정 검증이 선행되어야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| pause storm | PFC priority 범위 오류 | RDMA class만 PFC 적용 | pause frame counter |
| packet loss | buffer, ECN threshold 설정 미흡 | ECN/DCQCN tuning | retransmit, drop counter |
| tenant 간 영향 | RDMA traffic이 일반 traffic 압박 | QoS queue 분리, rate limit | queue occupancy |

> 요약: RoCE 운영 리스크는 PFC, ECN, QoS 설정으로 통제하며 counter 기반 검증이 필수다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| RDMA 품질 | p99 latency와 bandwidth baseline 충족 | perftest, NCCL test |
| 손실/혼잡 | drop, ECN mark, pause frame 추적 | switch telemetry |
| 격리 | RDMA queue와 일반 queue 영향 분리 | QoS counter |

> 요약: RoCE 성과는 RDMA benchmark뿐 아니라 Ethernet switch counter로 무손실 운영 상태를 확인해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. RoCEv2, PFC, ECN, QoS class, MTU, DSCP 값을 표준 profile로 정의하고 server/switch 양끝에 동일 적용함.
2. 배포 전 perftest와 NCCL test로 latency, bandwidth, pause frame, ECN mark baseline을 저장함.
3. RDMA traffic과 일반 service traffic을 queue와 VLAN/VRF로 분리해 pause 전파 범위를 제한함.

**결론 (2줄):**
- 기술사 판단: Ethernet 운영 통합이 중요하면 RoCE, 전용 AI/HPC fabric 예측 가능성이 중요하면 InfiniBand를 우선 검토함.
- 향후 방향: RoCE는 AI data center의 Ethernet 표준화 요구와 함께 telemetry 기반 congestion control 중심으로 확대됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "RoCE를 설명하시오" | RoCEv2 packet 처리와 RDMA completion | InfiniBand 대비 Ethernet 운영 차이 |
| 요구사항 명시형 | "RDMA 네트워크 구축 방안을 제시하시오" | PFC/ECN/QoS 설정 검증 절차 | pause storm, loss, tenant 영향 |

> 요약: 설명형은 RDMA over Ethernet 원리를, 구축형은 무손실 Ethernet 운영 통제를 중심으로 작성한다.
