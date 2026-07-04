---
title: "RoCE RDMA over Converged Ethernet (RoCE)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 130
---

# 📖 【암기용】 개념 완전 이해

> 목적: RoCE를 처음 보는 사람도 Ethernet에서 RDMA를 실행할 때 필요한 무손실 패브릭 조건을 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: RoCE는 Ethernet 네트워크에서 RDMA를 수행하는 프로토콜이며, RoCEv2는 UDP/IP 캡슐화로 L3 라우팅을 지원한다.
- **왜 필요한가**: AI 학습, 분산 스토리지, HPC는 InfiniBand 수준의 저지연 데이터 이동을 기존 Ethernet 운영 모델에서 구현하려 한다.
- **핵심 직관**: 일반 도로인 Ethernet 위에 정차 금지, 혼잡 알림, 전용 차선을 설정해 RDMA 차량이 막히지 않게 하는 방식이다.

## 깊이 이해
- **배경·문제의식**: RDMA는 손실과 재전송에 민감하다. Ethernet은 기본적으로 손실 가능 네트워크이므로 RoCE는 PFC, ECN, DCQCN 같은 데이터센터 혼잡 제어와 함께 설계된다.
- **작동 원리**: RoCEv1은 Ethernet L2에서 동작하고, RoCEv2는 IP/UDP로 캡슐화되어 라우팅 가능한 데이터센터 패브릭에서 사용된다. RoCEv2는 IANA UDP destination port 4791을 사용한다.
- **비유**: 일반 택배망에서 긴급 의료 배송을 하려면 전용 차로, 교통량 감지, 속도 조절 규칙을 함께 둬야 하는 것과 같다.
- **구체 예시**: GPU 클러스터에서 NCCL all-reduce 트래픽이 RoCEv2로 흐르고, 스위치는 ECN 마킹과 PFC pause를 사용하며 호스트는 DCQCN으로 송신률을 조절한다.
- **흔한 오해·주의점**: PFC만 켜면 RoCE가 운영된다고 생각하면 위험하다. PFC는 pause storm과 head-of-line blocking을 만들 수 있어 ECN, DCQCN, 버퍼 설계가 함께 필요하다.

## 연결 개념
- RDMA — RoCE가 Ethernet에서 제공하는 원격 직접 메모리 접근 기술
- PFC — 우선순위별 무손실 Ethernet 흐름 제어
- ECN·DCQCN — RoCEv2 혼잡 완화를 위한 마킹과 송신률 제어

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. RoCEv2 UDP 4791, PFC, ECN, DCQCN, lossless Ethernet을 중심으로 작성한다.
> 핵심: 출제자는 RoCE 프로토콜보다 Ethernet 패브릭에서 RDMA 손실과 혼잡을 어떻게 통제하는지 묻는다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: RoCE는 Ethernet에서 RDMA를 제공하는 프로토콜이고 RoCEv2는 UDP/IP 캡슐화로 L3 라우팅을 지원한다.
> 2. **가치**: AI/HPC/분산 스토리지의 RNIC 간 메모리 접근을 Ethernet 데이터센터 패브릭에서 구현한다.
> 3. **판단 포인트**: RoCEv2 UDP 4791, PFC, ECN, DCQCN, QoS, buffer profile이 맞지 않으면 tail latency와 packet loss가 증가한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| RoCE 구조 이해 확인 | RoCEv1 L2, RoCEv2 UDP/IP, RDMA verbs | RoCE를 TCP 기반 프로토콜로 설명 |
| 무손실 Ethernet 조건 확인 | PFC, ECN, DCQCN, QoS, buffer | PFC만 적용하면 충분하다고 서술 |
| AI 패브릭 운영 판단 확인 | CNP, pause storm, head-of-line blocking | 혼잡·장애 지표 없이 처리량만 언급 |

> 요약: 이 문제는 RoCEv2 캡슐화와 데이터센터 무손실 패브릭 운영 조건을 함께 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: Ethernet에서 RDMA를 실행함.
- 배경: AI 학습과 분산 스토리지는 서버 간 대량 데이터 이동으로 CPU 복사와 커널 경로 비용이 커짐.
- 필요성: RoCEv2는 UDP/IP 캡슐화를 통해 라우팅 가능한 Ethernet에서 RDMA 트래픽을 전달함.
- 판단 기준: UDP 4791, PFC, ECN, DCQCN, buffer profile, p99 latency, packet loss를 확인함.

---

## Ⅱ. 구조 및 구성요소

```text
Application -> RDMA Verbs -> RNIC -> RoCEv2 UDP/IP Packet
RoCEv2 Packet -> Lossless Ethernet Fabric -> Remote RNIC -> Remote Memory
Switch -> PFC / ECN Marking -> CNP -> DCQCN Rate Control
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| RNIC | RDMA 오프로딩과 RoCE 패킷 처리 | RDMA verbs, QP |
| RoCEv2 | RDMA payload를 UDP/IP로 캡슐화 | UDP destination port 4791 |
| PFC | 우선순위별 pause로 손실 억제 | pause storm 위험 |
| ECN | 혼잡 시 패킷에 마킹 | 스위치 threshold 설정 |
| DCQCN | CNP 기반 송신률 조절 | AI collective 트래픽에 사용 |

> 요약: RoCE는 RNIC와 Ethernet 패브릭이 함께 동작하며, PFC·ECN·DCQCN이 손실과 혼잡을 통제한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
메모리 등록 -> RDMA Work Request -> RNIC RoCEv2 캡슐화
-> Ethernet Fabric 전달 -> ECN/PFC 혼잡 제어 -> Remote RNIC 처리 -> Completion 확인
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 애플리케이션이 RDMA 작업을 게시 | QP state, memory key |
| 2 | RNIC가 RoCEv2 UDP/IP 패킷 생성 | UDP 4791, MTU |
| 3 | 스위치가 QoS 큐로 전달 | PFC priority, buffer |
| 4 | 혼잡 시 ECN 마킹과 CNP 전달 | ECN mark, CNP count |
| 5 | DCQCN이 송신률을 조절하고 완료 확인 | p99 latency, retry count |

> 요약: RoCEv2는 RNIC의 RDMA 작업을 UDP/IP 패킷으로 운반하고, 스위치와 호스트가 혼잡 신호를 교환해 손실을 줄인다.

---

## Ⅳ. 특징

| 구분 | InfiniBand | RoCEv2 | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 패브릭 | 전용 RDMA 네트워크 | Ethernet 기반 RDMA | UDP 4791 |
| 운영 모델 | 전용 스위치·관리 | 기존 DC Ethernet 활용 | QoS, PFC, ECN |
| 혼잡 제어 | IB credit 중심 | PFC + ECN + DCQCN | CNP count, ECN mark |
| 한계 | 별도 생태계 | 설정 민감, pause storm 가능 | p99 latency, packet loss |

> 요약: RoCEv2는 Ethernet 운영 모델을 활용하지만, 무손실과 혼잡 제어 설정 품질이 지연과 장애를 결정한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | RoCEv2 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | TCP/IP 또는 InfiniBand | UDP/IP 기반 RDMA over Ethernet | Ethernet 표준 운영과 RDMA 성능이 모두 필요 시 |
| 비용/성능 | TCP는 CPU 비용, IB는 전용망 비용 | RNIC와 lossless Ethernet 필요 | 100/200/400GbE AI 패브릭 |
| 운영/위험 | 운영 단순 또는 전용관리 | PFC·ECN·DCQCN 튜닝 필요 | 전문 운영, 자동 검증 가능 시 |

> 요약: RoCEv2는 Ethernet 기반 AI 패브릭에 적합하지만, 설정 검증 없는 도입은 tail latency와 장애를 만든다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| pause storm | PFC 과다 발생 | PFC watchdog, buffer tuning | PFC pause duration |
| HOL blocking | 우선순위 큐 정체 | QoS 분리, ECN threshold 조정 | queue occupancy |
| tail latency 증가 | 혼잡 제어 미조정 | DCQCN 파라미터 검증 | p99 latency, CNP count |

> 요약: RoCE 운영 리스크는 PFC, 큐 점유율, CNP, p99 지연을 함께 감시해 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 무손실 조건 | RDMA packet loss 0건 | switch/RNIC counter |
| 혼잡 제어 | ECN mark와 CNP 추이 정상 | telemetry, switch counter |
| 애플리케이션 품질 | all-reduce p99 지연 목표 충족 | NCCL test, APM |

> 요약: RoCE 성공 여부는 처리량보다 packet loss, ECN/CNP, all-reduce p99 지연으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. RoCEv2 패브릭은 UDP 4791, MTU, QoS priority, PFC, ECN threshold, DCQCN 파라미터를 표준 프로파일로 고정함.
2. 배포 전 `ib_write_bw`, `ib_write_lat`, NCCL test로 처리량, p99 지연, CNP, PFC pause를 측정함.
3. 운영 중 PFC watchdog, switch buffer telemetry, RNIC retry counter를 수집하고 설정 변경은 canary 랙에서 먼저 검증함.

**결론 (2줄):**
- 기술사 판단: Ethernet 운영 체계와 AI/HPC RDMA 요구가 동시에 있으면 RoCEv2를 선택하고, 패브릭 튜닝 역량이 없으면 전용 InfiniBand 또는 TCP 기반 구조를 검토함.
- 향후 방향: AI 데이터센터는 RoCEv2, DCQCN, telemetry 기반 자동 튜닝, GPU Direct RDMA를 결합한 패브릭으로 진화함.

### 🔀 문제 유형별 목차 전환

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "RoCE를 설명하시오" | RoCEv2 캡슐화와 혼잡 제어 흐름 | InfiniBand·TCP와 차이 |
| 요구사항 명시형 | "AI 패브릭 설계 방안을 제시하시오" | PFC, ECN, DCQCN, telemetry 검증 | pause storm·HOL·tail latency 대응 |

> 요약: 설명형은 프로토콜 구조를, 설계형은 무손실 Ethernet 운영 조건과 검증 지표를 중심으로 작성한다.
