---
title: "RDMA 원격직접메모리접근 (Remote Direct Memory Access)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 253
---

# 📖 【암기용】 개념 완전 이해

> 목적: RDMA를 원격 서버 memory에 application이 직접 접근하도록 NIC가 데이터 이동을 대신 수행하는 구조로 이해하게 만든다.

## 한눈에
- **개요**: 원격 host의 등록된 memory buffer를 CPU copy와 kernel network stack 경유 없이 읽고 쓰는 통신 방식
- **왜 필요한가**: 분산 DB, storage, AI 학습은 짧은 지연과 높은 message rate가 필요하며, TCP 처리와 memory copy가 CPU 시간을 소모한다.
- **핵심 직관**: 상대 창고의 허가된 선반에 물건을 직접 놓고 가져오는 자동 운반 장치다.

## 깊이 이해
- **배경·문제의식**: 전통 socket 통신은 user buffer, kernel buffer, NIC buffer 사이 복사가 발생하고, interrupt와 protocol 처리로 CPU overhead가 생긴다.
- **작동 원리**: application은 memory를 등록해 key를 만들고, queue pair에 work request를 올리면 RNIC/HCA가 remote memory read/write/send를 수행한 뒤 completion을 기록한다.
- **비유**: 택배 기사에게 매번 전달 요청을 하는 대신, 인증된 출입카드로 지정 선반에 직접 물건을 놓는 방식이다.
- **구체 예시**: GPUDirect RDMA는 NIC가 GPU memory와 직접 데이터를 교환해 host memory staging copy를 줄인다.
- **흔한 오해·주의점**: RDMA는 아무 memory나 접근하는 기술이 아니다. memory registration, key, protection domain으로 허가된 범위만 접근한다.

## 연결 개념
- InfiniBand — RDMA semantics를 native로 제공하는 대표 fabric
- RoCE — Ethernet 위에서 RDMA를 제공하는 방식
- Zero-Copy — RDMA가 줄이려는 memory copy 비용

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: RDMA는 저지연이라는 결과보다 memory registration, queue pair, RNIC offload, protection을 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: RDMA는 RNIC/HCA가 등록된 원격 memory에 직접 read/write를 수행하는 network offload 구조임.
> 2. **가치**: kernel bypass와 zero-copy로 CPU overhead, context switch, buffer copy를 줄여 AI/HPC/storage 통신 경로를 단축함.
> 3. **판단 포인트**: memory registration 비용, key 보호, congestion control을 함께 설계해야 production 적용이 가능함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| RDMA 동작 원리 확인 | memory registration, QP, CQ, RNIC | 단순 고속 네트워크로 설명 |
| 보안·보호 이해 확인 | lkey/rkey, protection domain | 원격 memory 전체 접근으로 오해 |
| 적용 판단 확인 | InfiniBand/RoCE/iWARP 선택 | TCP를 무조건 대체한다고 단정 |

> 요약: RDMA 문제는 CPU bypass 구조와 memory protection 조건을 동시에 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: 원격 memory 직접 접근
- 배경: socket 기반 통신은 kernel 진입, buffer copy, protocol 처리로 CPU cycle과 지연이 증가함.
- 필요성: AI collective, distributed storage, key-value store에서 통신당 CPU overhead와 p99 latency를 줄여야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Application Buffer -> Memory Registration -> Queue Pair -> RNIC / HCA
RNIC / HCA -> RDMA Fabric -> Remote RNIC / HCA -> Registered Remote Buffer
              +-> Completion Queue / Protection Domain
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Registered Memory | RDMA 접근 허용 buffer | lkey/rkey로 보호 |
| Queue Pair | send/receive/read/write 요청 큐 | QP state 관리 필요 |
| RNIC/HCA | packet 생성과 DMA 수행 | CPU protocol 처리 감소 |
| Completion Queue | 작업 완료와 오류 통지 | polling 또는 event 처리 |

> 요약: RDMA는 등록 memory, queue pair, RNIC offload, completion 확인으로 원격 buffer 간 직접 전송을 수행한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Memory 등록 -> QP 연결 -> Remote key 교환
-> Work Request 게시 -> RNIC DMA 전송 -> Remote buffer 반영 -> Completion 확인
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 송수신 buffer 등록과 key 생성 | registration 성공 |
| 2 | QP를 INIT/RTR/RTS 상태로 전환 | QP state |
| 3 | RDMA read/write/send work request 게시 | work queue depth |
| 4 | completion queue에서 성공·오류 확인 | completion status |

> 요약: RDMA는 사전 등록과 연결 설정 이후 RNIC가 데이터 이동을 수행하고 application은 completion만 확인한다.

---

## Ⅳ. 특징

| 구분 | TCP Socket | RDMA | 판단 기준 |
|:---|:---|:---|:---|
| 데이터 경로 | user/kernel buffer copy | registered buffer direct DMA | copy 횟수 |
| CPU 처리 | kernel protocol stack 처리 | RNIC offload | CPU utilization |
| 보호 방식 | process/socket 권한 | protection domain, key | key 관리 |
| 적용 난이도 | 일반 API | verbs, registration 관리 | 개발 역량 |

> 요약: RDMA는 CPU와 copy 비용을 줄이지만 buffer 등록, key 보호, queue 관리 복잡도가 추가된다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | TCP/IP stack | RNIC offload + registered memory | latency budget |
| 비용/성능 | 범용성과 운영 편의 | NIC, switch, 개발 복잡도 추가 | CPU 절감 효과 |
| 운영/위험 | 일반 network monitoring | RDMA counter와 queue depth 관리 | 운영 가시성 |

> 요약: RDMA는 microservice 일반 API보다 AI/HPC/storage data path에 우선 적용해야 효과가 명확하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| memory 노출 | rkey 유출 또는 범위 과다 등록 | protection domain 분리, key rotation | access violation |
| registration 비용 | buffer 등록·해제 반복 | memory pool, pinned buffer 재사용 | registration rate |
| 혼잡 | lossless fabric 설정 미흡 | congestion control, PFC/ECN 검증 | retry, drop counter |

> 요약: RDMA 리스크는 보호, 등록 비용, 혼잡이며 key 관리와 fabric telemetry가 필요하다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| latency | 목표 workload p99 기준 충족 | rdma_lat, application trace |
| CPU overhead | network thread CPU 사용률 감소 | perf, cgroup metric |
| 오류 | retry, RNR, access error 추적 | RNIC counter |

> 요약: RDMA 효과는 synthetic benchmark와 application p99 trace를 함께 측정해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. AI collective, storage replication, cache get/put처럼 데이터 이동이 빈번한 hot path를 RDMA 후보로 분리함.
2. 등록 memory pool과 protection domain을 tenant, job, process 단위로 분리해 rkey 범위를 최소화함.
3. RNIC retry, completion error, congestion counter를 SLO dashboard에 포함해 fabric 문제를 application 장애와 연결함.

**결론 (2줄):**
- 기술사 판단: CPU copy와 kernel 처리 비용이 병목이면 RDMA를 선택하고, 개발 복잡도와 protection 요구가 크면 TCP/gRPC 경로를 유지함.
- 향후 방향: RDMA는 GPUDirect, NVMe-oF, disaggregated memory와 결합해 AI infrastructure의 data path offload 계층으로 확대됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "RDMA를 설명하시오" | memory registration과 QP 처리 흐름 | TCP socket 대비 차이 |
| 요구사항 명시형 | "저지연 분산 시스템 설계 방안을 제시하시오" | hot path 선정과 protection 절차 | registration, key, congestion 리스크 |

> 요약: 설명형은 RDMA 원리를, 설계형은 적용 범위와 운영 통제 기준을 중심으로 작성한다.
