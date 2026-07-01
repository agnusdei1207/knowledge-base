---
title: "InfiniBand (InfiniBand)"
date: "2026-07-01"
tags:
  - "cspe-hardware"
weight: 57
---

# 📖 【암기용】 개념 완전 이해

> 목적: InfiniBand를 처음 봐도 NVLink·이더넷과 무엇이 다른 계층인지 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: RDMA(Remote Direct Memory Access)를 지원하는 HPC·데이터센터용 개방형 서버 간 네트워크 fabric 표준
- **왜 필요한가**: 다수 서버로 구성된 클러스터(HPC, AI 학습)는 서버 간 데이터 교환이 잦은데, 일반 TCP/IP 이더넷은 커널 개입과 복사 오버헤드로 지연이 크다. InfiniBand는 RDMA로 커널을 우회해 서버 간 메모리를 직접 주고받아 지연을 줄인다.
- **핵심 직관**: 여러 건물(서버)을 잇는 도시 도로망인데, 신호 대기(커널 개입) 없이 통행할 수 있는 전용 급행 차로(RDMA)를 깔아 놓은 구조.

## 깊이 이해
- **배경·문제의식**: HPC 슈퍼컴퓨터와 대규모 AI 학습 클러스터는 수백~수천 대 서버가 all-reduce, MPI(Message Passing Interface) 통신을 주고받으며, 통신 지연이 곧 전체 작업 완료 시간을 좌우한다.
- **작동 원리**: IBTA(InfiniBand Trade Association)가 표준을 정의하며, RDMA로 원격 서버의 메모리에 CPU 개입 최소화된 상태로 직접 읽기/쓰기를 수행한다. 세대는 SDR/DDR/QDR/FDR/EDR/HDR/NDR 등으로 이어지며 세대가 오를수록 링크당 대역폭이 커진다(정확한 Gb/s 수치는 세대·구성에 따라 다르며 공식 스펙 확인이 필요하다).
- **비유**: RDMA는 우체국 창구 직원(커널/CPU)을 거치지 않고 발신자가 수신자의 우편함(메모리)에 직접 편지를 넣는 것과 같다.
- **구체 예시**: NVIDIA는 InfiniBand의 주요 공급사였던 Mellanox를 인수해 InfiniBand 스위치·NIC(HCA, Host Channel Adapter) 제품군을 이어가고 있으며, 이더넷 기반 대안으로 RoCE(RDMA over Converged Ethernet)가 경쟁·병행되고 있다.
- **흔한 오해·주의점**: InfiniBand는 NVLink와 다른 계층이다. NVLink는 한 노드(서버) 내부 GPU 간 직결 인터커넥트(scale-up)이고, InfiniBand는 서버와 서버를 잇는 클러스터 네트워크 fabric(scale-out)이다. 두 기술은 대규모 AI 클러스터에서 함께 쓰이지만 서로 대체재가 아니라 계층이 다른 보완 관계다.

## 연결 개념
- RDMA(Remote Direct Memory Access) — InfiniBand의 핵심 저지연 메커니즘
- NVLink — 노드 내부 GPU 간 인터커넥트, InfiniBand와는 다른 계층(056번 키워드 참고)
- RoCE(RDMA over Converged Ethernet) — 이더넷 기반 RDMA 대안
- MPI(Message Passing Interface) — InfiniBand 위에서 동작하는 대표 HPC 통신 라이브러리

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: InfiniBand 답안은 RDMA 원리, 서버 간(scale-out) 네트워크라는 위치, NVLink·이더넷과의 계층·경쟁 관계를 함께 제시한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: InfiniBand는 RDMA를 지원하는 IBTA 표준 기반 HPC·데이터센터 서버 간 네트워크 fabric이다.
> 2. **가치**: 커널 개입과 데이터 복사를 최소화하는 RDMA로 서버 간 통신 지연을 줄여 대규모 클러스터의 집합 통신 성능을 높인다.
> 3. **판단 포인트**: InfiniBand는 서버 간(scale-out) 통신 계층이고, NVLink는 노드 내부 GPU 간(scale-up) 계층이므로 대규모 AI 클러스터는 두 계층을 함께 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| RDMA 원리 이해 확인 | 커널 우회, 원격 메모리 직접 접근 | RDMA를 단순 "빠른 전송"으로만 서술 |
| 데이터센터 네트워크 위치 이해 확인 | IBTA 표준, 서버 간(scale-out) fabric | InfiniBand를 GPU 전용 기술로 오해 |
| NVLink·이더넷과의 계층 구분 확인 | scale-out(InfiniBand) vs scale-up(NVLink), RoCE와의 경쟁 | NVLink와 InfiniBand를 동일 계층의 경쟁 기술로 혼동 |

> 요약: 이 문제는 InfiniBand를 NVLink의 대체재가 아니라 서버 간 클러스터 네트워크라는 별도 계층으로 정확히 위치시켜야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: RDMA를 지원하는 IBTA 표준 기반 HPC·데이터센터 서버 간 네트워크 fabric
- 배경: 대규모 클러스터의 서버 간 통신에서 TCP/IP 이더넷의 커널 개입·복사 오버헤드가 지연을 유발함
- 필요성: HPC·AI 학습의 all-reduce, MPI 통신 성능은 서버 간 통신 지연에 좌우되므로 RDMA 기반 저지연 fabric이 필요함

---

## Ⅱ. 구조 및 구성요소

```text
Server A (HCA/NIC) <-> InfiniBand Switch Fabric <-> Server B (HCA/NIC)
  -> RDMA Verbs API -> 원격 메모리 직접 read/write
  -> Subnet Manager -> 경로/QoS 관리
  -> MPI/스토리지 프로토콜(NVMe-oF 등) 상위 계층
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| HCA(Host Channel Adapter) | 서버의 InfiniBand 네트워크 인터페이스 | RDMA 엔진 내장, CPU 개입 최소화 |
| Switch Fabric | 서버 간 패킷 스위칭 | 낮은 지연, 높은 대역폭 토폴로지(팻트리 등, 110번 키워드 참고) |
| Subnet Manager | 네트워크 경로·QoS·파티션 관리 | InfiniBand 특유의 중앙 관리 요소 |
| RDMA Verbs | 원격 메모리 직접 접근 API | 커널 우회로 CPU 오버헤드 감소 |

> 요약: InfiniBand는 HCA와 스위치 fabric으로 서버를 연결하고, Subnet Manager가 경로를 관리하며 RDMA로 저지연 통신을 구현한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
애플리케이션(MPI 등)이 원격 메모리 주소 지정
  -> RDMA Verbs API 호출 -> HCA가 커널 우회 전송 개시
  -> Switch Fabric 경유 -> 수신측 HCA가 원격 메모리에 직접 write/read
  -> 완료 통지(Completion Queue)로 애플리케이션에 전달
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 애플리케이션이 RDMA 대상 메모리 영역 등록 | 메모리 등록 오버헤드 |
| 2 | HCA가 커널 우회하여 전송 개시 | CPU 사용률(전송 중) |
| 3 | 스위치 fabric 경유 전달 | 스위치 홉 수, 큐잉 지연 |
| 4 | 수신측 메모리 직접 기록 후 완료 통지 | end-to-end latency, 처리량 |

> 요약: InfiniBand는 메모리 등록-커널 우회 전송-완료 통지 흐름으로 CPU 개입을 최소화한 저지연 통신을 구현한다.

---

## Ⅳ. 특징

| 구분 | InfiniBand | NVLink(비교, 056번) | 이더넷/RoCE | 수치·표준 포인트 |
|:---|:---|:---|:---|:---|
| 연결 범위 | 서버 간(scale-out) 클러스터 | 노드 내 GPU 간(scale-up) | 서버 간, 범용 데이터센터 네트워크 | 계층이 서로 다름 |
| 표준화 | IBTA 개방 표준 | NVIDIA 독자 규격 | IEEE 802.3 등 개방 표준 | InfiniBand·이더넷은 개방, NVLink는 벤더 종속 |
| 핵심 메커니즘 | RDMA(네이티브) | 전용 point-to-point 링크 | RoCE로 RDMA 구현(오버레이) | RDMA 구현 방식이 다름 |
| 세대 발전 | SDR~NDR 등으로 세대별 대역폭 증가(정확 수치는 공식 스펙 확인) | 세대별 대역폭 증가 | 이더넷 속도 표준(예: 100/200/400GbE)에 맞춰 발전 | 세 규격 모두 지속 진화 중 |

> 요약: InfiniBand는 서버 간 RDMA 네이티브 fabric, NVLink는 노드 내 GPU 전용 링크, 이더넷/RoCE는 범용 네트워크 위에서 RDMA를 구현하는 대안이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 이더넷(RoCE 포함) | InfiniBand | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 범용 TCP/IP 생태계, RoCE로 RDMA 지원 | 네이티브 RDMA, 전용 Subnet Manager | 기존 이더넷 운영 인력·장비 재사용 여부 |
| 비용/성능 | 범용 장비로 비용 유리, RoCE 설정 복잡도 존재 | 저지연·고대역폭에 최적화, 전용 장비 필요 | 극한 저지연 요구 시 InfiniBand 우선 |
| 운영/위험 | 기존 네트워크팀 운영 경험 활용 가능 | 별도 전문 인력·Subnet Manager 운영 필요 | 운영 조직의 InfiniBand 숙련도 |

> 요약: 극한의 저지연·고대역폭 클러스터는 InfiniBand, 범용 인프라 재사용과 운영 편의성은 이더넷/RoCE를 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 운영 복잡도 | Subnet Manager, 파티션 설정 등 전문성 요구 | 전담 인력 확보, 자동화 도구 도입 | 장애 대응 시간(MTTR) |
| 벤더·공급망 편중 | 주요 장비 공급사 편중(Mellanox 계열 등) | 공급망 다변화 검토, 대체 fabric(RoCE) 병행 검토 | 조달 리드타임 |
| 확장 시 토폴로지 설계 오류 | 팻트리 등 토폴로지 미스매치로 병목 발생 | 클러스터 규모별 토폴로지 사전 설계(110번 키워드 참고) | 홉 수, 크로스섹션 대역폭 |

> 요약: InfiniBand 운영 리스크는 전문 인력 의존, 공급망 편중, 토폴로지 설계 오류이며 자동화와 사전 설계로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 지연 | end-to-end latency 목표치 이내 | RDMA 벤치마크(perftest 등) |
| 대역폭 | 링크 대역폭 사용률, 크로스섹션 대역폭 목표 달성 | 스위치 모니터링 |
| 집합 통신 성능 | all-reduce/MPI 벤치마크 처리량 목표 달성 | HPC 벤치마크(OSU 등) |

> 요약: 도입 성과는 end-to-end 지연, 대역폭 사용률, 집합 통신 벤치마크 처리량으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 대규모 HPC·AI 학습 클러스터의 노드 간 통신은 InfiniBand로 구성하고 all-reduce 벤치마크로 성능을 검증함
2. 노드 내부 GPU 간 통신은 NVLink/NVSwitch로 별도 계층을 구성해 scale-up과 scale-out을 분리 설계함
3. 운영 인력·장비 제약이 있는 환경은 RoCE 기반 이더넷을 대안으로 검토하되 지연·손실 튜닝을 사전 검증함

**결론 (2줄):**
- 기술사 판단: 서버 간(scale-out) 클러스터 통신은 InfiniBand(또는 RoCE), 노드 내(scale-up) GPU 통신은 NVLink로 계층을 분리해 설계함
- 향후 방향: 세대별 대역폭 증가와 AI 클러스터 규모 확대에 따라 InfiniBand·이더넷 간 경쟁·병행 구도가 지속되는 방향으로 발전함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "InfiniBand를 설명하시오" | RDMA 통신 흐름, Subnet Manager 구조 | 이더넷 대비 필요성 |
| 비교형 | "InfiniBand와 NVLink를 비교하시오" | 서버 간/노드 내 통신 경로 구분 | scale-out vs scale-up 계층 차이 |

> 요약: 설명형은 RDMA 기반 통신 구조를, 비교형은 NVLink와의 계층·목적 차이를 중심으로 답안 축을 바꾼다.
