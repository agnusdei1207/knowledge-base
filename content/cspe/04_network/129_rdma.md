---
title: "RDMA 원격 직접 메모리 접근 (RDMA)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 129
---

# 📖 【암기용】 개념 완전 이해

> 목적: RDMA를 처음 보는 사람도 CPU를 거치지 않는 원격 메모리 접근의 의미를 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 한 서버의 NIC가 다른 서버 메모리에 직접 데이터를 읽고 쓰는 저지연 통신 기술이다.
- **왜 필요한가**: 분산 스토리지, HPC, AI 학습은 서버 간 대량 데이터 이동이 많아 커널 TCP/IP 처리와 CPU 복사 비용이 병목이 된다.
- **핵심 직관**: 택배를 현관에서 다시 포장하지 않고 창고 선반으로 바로 넣는 구조이다.

## 깊이 이해
- **배경·문제의식**: 일반 TCP 통신은 애플리케이션 버퍼, 커널 버퍼, NIC 사이에서 복사와 인터럽트가 발생한다. RDMA는 NIC가 등록된 메모리 영역에 직접 접근해 zero-copy와 kernel bypass를 구현한다.
- **작동 원리**: 애플리케이션은 메모리를 등록하고 Queue Pair를 만든다. RDMA verbs로 send, receive, read, write, atomic 작업을 게시하면 RNIC가 DMA로 원격 메모리와 데이터를 교환하고 Completion Queue에 결과를 남긴다.
- **비유**: 일반 배송은 접수창구와 분류센터를 거치지만, RDMA는 허가된 창고 위치에 지게차가 직접 물건을 넣고 빼는 방식이다.
- **구체 예시**: NVMe-oF over RDMA는 스토리지 서버 메모리와 클라이언트 버퍼 사이의 복사를 줄여 마이크로초 단위 지연 목표를 가진다.
- **흔한 오해·주의점**: RDMA는 자동으로 전체 애플리케이션 성능을 올리는 기술이 아니다. 메모리 등록, flow control, congestion control, NIC·스위치 설정이 맞지 않으면 tail latency가 증가한다.

## 연결 개념
- RDMA Verbs — 애플리케이션이 RNIC에 작업을 요청하는 API
- InfiniBand — RDMA를 위해 설계된 전용 패브릭
- RoCE — Ethernet에서 RDMA를 실행하는 방식

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. zero-copy, kernel bypass, RNIC, Queue Pair, RDMA verbs를 중심으로 작성한다.
> 핵심: 출제자는 RDMA 개념보다 일반 TCP와의 데이터 경로 차이, 메모리 보호, 혼잡 제어 조건을 확인한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: RDMA는 RNIC가 원격 서버의 등록 메모리에 직접 접근해 zero-copy와 kernel bypass를 구현하는 통신 기술이다.
> 2. **가치**: 분산 스토리지, HPC, AI 학습에서 CPU 복사와 커널 경로를 줄여 마이크로초 단위 지연 목표를 지원한다.
> 3. **판단 포인트**: memory registration, Queue Pair, protection key, congestion control, NIC offload 조건을 함께 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| RDMA 동작 구조 확인 | RNIC, registered memory, Queue Pair, Completion Queue | 단순 고속 TCP로 설명 |
| 일반 네트워크 대비 차이 확인 | zero-copy, kernel bypass, one-sided operation | CPU와 커널을 완전히 쓰지 않는다고 단정 |
| 운영 한계 판단 확인 | 메모리 보호, 혼잡 제어, PFC/ECN | 손실 네트워크에서 무조건 동작한다고 서술 |

> 요약: 이 문제는 RDMA 데이터 경로와 메모리 보호, 네트워크 무손실 조건을 함께 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: RNIC가 원격 메모리에 직접 접근함.
- 배경: TCP/IP 경로는 복사, 인터럽트, 커널 처리로 대량 데이터 이동 시 CPU 병목을 만든다.
- 필요성: AI 학습, 분산 스토리지, HPC는 100GbE 이상 패브릭에서 낮은 tail latency와 CPU 사용률 절감이 필요함.
- 판단 기준: RDMA verbs 지원, RNIC, registered memory, congestion control, p99 latency를 확인함.

---

## Ⅱ. 구조 및 구성요소

```text
Application -> RDMA Verbs -> Queue Pair -> RNIC
RNIC -> DMA -> Local Registered Memory
RNIC -> Network Fabric -> Remote RNIC -> Remote Registered Memory
Completion Queue -> Application Notification
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| RDMA Verbs | send, receive, read, write 작업 요청 | libibverbs, provider |
| Registered Memory | NIC가 접근 가능한 메모리 영역 | memory region, lkey, rkey |
| Queue Pair | 송수신 작업 큐 제공 | SQ, RQ, QP state |
| RNIC | DMA와 프로토콜 오프로딩 수행 | NIC offload, completion |
| Completion Queue | 작업 완료 이벤트 제공 | polling 또는 interrupt |

> 요약: RDMA는 애플리케이션이 verbs로 작업을 게시하고 RNIC가 등록 메모리 사이의 데이터 이동을 수행하는 구조이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
메모리 등록 -> QP 생성 -> 연결 설정 -> Work Request 게시
-> RNIC DMA 전송 -> 원격 메모리 접근 -> Completion Queue 확인 -> 버퍼 재사용
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 애플리케이션이 메모리 영역 등록 | lkey, rkey, page pinning |
| 2 | Queue Pair와 Completion Queue 생성 | QP state, MTU |
| 3 | RDMA read/write/send 작업 게시 | Work Request, SGE |
| 4 | RNIC가 네트워크와 DMA 처리 | packet loss, CNP, retry |
| 5 | 완료 이벤트를 확인하고 버퍼 회수 | completion status, latency |

> 요약: RDMA는 사전 등록된 메모리와 큐 기반 작업 게시를 통해 RNIC가 데이터 이동을 수행한다.

---

## Ⅳ. 특징

| 구분 | TCP/IP 소켓 | RDMA | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 데이터 경로 | user -> kernel -> NIC | user -> RNIC DMA | zero-copy, kernel bypass |
| CPU 사용 | 복사·인터럽트 비용 발생 | RNIC offload 중심 | CPU utilization |
| 동작 방식 | two-sided send/recv | one-sided read/write 가능 | RDMA verbs |
| 한계 | 범용성 높음 | 메모리 등록과 패브릭 설정 필요 | p99 latency, retry count |

> 요약: RDMA는 데이터 경로를 줄이는 대신 메모리 보호와 네트워크 패브릭 설정을 엄격히 요구한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | RDMA | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | TCP 소켓, 커널 네트워크 스택 | RNIC, verbs, registered memory | 대량 데이터 이동과 낮은 CPU 사용률 필요 시 |
| 비용/성능 | 일반 NIC 사용 | RNIC와 RDMA 지원 스위치 필요 | 100GbE 이상, p99 지연 목표 |
| 운영/위험 | 운영 단순 | PFC/ECN, MTU, buffer 설정 민감 | 전문 운영과 모니터링 가능 시 |

> 요약: RDMA는 저지연·고처리량 워크로드에 적합하지만, 패브릭 운영 능력이 선택 조건이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 메모리 침범 | rkey 관리 오류 | protection domain, access flag 제한 | access violation count |
| tail latency 증가 | 혼잡과 packet loss | ECN, PFC, congestion control | p99 latency, retry count |
| 운영 복잡도 | MTU·QoS·펌웨어 불일치 | 표준 프로파일, 호환성 테스트 | link error, firmware matrix |

> 요약: RDMA 위험은 메모리 보호, 혼잡 제어, 장비 호환성 지표로 관리해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 지연 | p99 지연 목표 충족 | rdma_lat, 애플리케이션 계측 |
| 처리량 | 링크 사용률 80% 이상 | ib_write_bw, NIC counter |
| 오류 | retry·RNR·access violation 0건 | RNIC counter, dmesg |

> 요약: RDMA 도입 효과는 평균 처리량보다 p99 지연, retry, access violation으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. 애플리케이션은 RDMA verbs 또는 검증된 라이브러리를 사용하고 memory registration, QP lifecycle, rkey 관리를 명확히 구현함.
2. 패브릭은 MTU, QoS, ECN, PFC, buffer profile을 워크로드 기준으로 검증하고 장비 펌웨어 조합을 고정함.
3. 운영 지표는 p99 latency, retry count, CNP, RNR, access violation을 수집해 배포 전후로 비교함.

**결론 (2줄):**
- 기술사 판단: RDMA는 AI/HPC/분산 스토리지처럼 데이터 이동 비용이 병목인 구간에 적용하고 일반 웹 트래픽에는 TCP 기반 운영을 유지함.
- 향후 방향: RoCEv2, NVMe-oF, GPU Direct RDMA가 AI 데이터센터 패브릭의 핵심 데이터 경로로 확대됨.

### 🔀 문제 유형별 목차 전환

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "RDMA를 설명하시오" | 메모리 등록, QP, RNIC 데이터 흐름 | TCP/IP와 데이터 경로 차이 |
| 요구사항 명시형 | "저지연 통신 방안을 제시하시오" | RNIC, congestion control, p99 검증 | 메모리 보호·혼잡·운영 리스크 대응 |

> 요약: 설명형은 데이터 경로를, 방안형은 패브릭 조건과 운영 지표를 중심으로 작성한다.
