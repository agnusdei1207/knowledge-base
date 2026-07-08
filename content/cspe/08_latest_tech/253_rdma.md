---
title: "RDMA 원격직접메모리접근 (Remote Direct Memory Access)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 253
extra:
  question_no: "253"
  exam_status: "기출"
  exam_history: "138회"
  exam_note: "전망"
---

## 미리 알고가기

- RDMA는 원격 서버 메모리에 CPU 개입을 최소화하고 직접 접근하는 통신 방식임
- 핵심 가치는 복사 횟수와 커널 오버헤드를 줄여 지연과 CPU 사용률을 낮추는 데 있음
- InfiniBand와 RoCE 같은 네트워크 기술 위에서 구현될 수 있음

## Ⅰ. 개요

- **정의/개념**: RDMA는 네트워크를 통해 원격 시스템의 메모리에 직접 읽기와 쓰기를 수행해 CPU 복사와 커널 개입을 줄이고 고성능 저지연 데이터 전송을 가능하게 하는 통신 기법임
- **배경/필요성**: 분산 저장과 AI 학습과 HPC 워크로드에서는 데이터 교환 빈도가 매우 높아 전통적 소켓 통신의 복사와 인터럽트 오버헤드가 큰 병목으로 작용함

## Ⅱ. 특징

- zero copy에 가까운 전송으로 CPU 오버헤드를 줄임
- 짧은 지연과 높은 처리량으로 집단 통신과 스토리지 접근을 가속함
- 메모리 등록과 큐 관리 등 사전 준비가 필요해 설정 복잡도가 높음
- 네트워크와 NIC와 소프트웨어 스택이 함께 맞아야 성능 이점이 살아남

## Ⅲ. 종류 및 비교

| 판단 기준 | RDMA | TCP Socket | Shared Memory IPC |
|:---|:---|:---|:---|
| 적용 범위 | 원격 노드 통신 | 범용 네트워크 통신 | 동일 호스트 내부 통신 |
| CPU 개입 | 낮음 | 높음 | 매우 낮음 |
| 지연 | 낮음 | 높음 | 매우 낮음 |
| 설정 난도 | 높음 | 낮음 | 중간 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| RNIC | RDMA를 처리하는 네트워크 인터페이스 카드로 직접 메모리 접근과 큐 처리를 수행함 |
| Queue Pair | 송신과 수신 요청을 관리해 RDMA 작업 순서를 제어하는 통신 큐 구조임 |
| Memory Region | 원격 접근이 허용되도록 등록된 메모리 구역으로 보호와 성능의 기준점이 됨 |
| Completion Queue | 요청 완료 이벤트를 기록해 애플리케이션이 전송 완료를 효율적으로 확인하게 하는 큐임 |
| RDMA Verbs Layer | 등록과 전송과 동기화 같은 저수준 RDMA 동작을 노출하는 프로그래밍 인터페이스임 |

```text
+---------+    RDMA    +---------+
| App A   |----------->| Memory B|
+---------+            +---------+
    |                      ^
    v                      |
+---------+            +---------+
| RNIC A  |<---------> | RNIC B  |
+---------+            +---------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 메모리 등록  | -> | 큐 연결 설정 | -> | RDMA 읽기쓰기 | -> | 완료 이벤트 수신 | -> | 후속 처리    |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **메모리 등록**: 접근할 버퍼를 RNIC에 등록함
2. **큐 연결 설정**: 통신 대상과 큐 페어를 연결함
3. **RDMA 읽기쓰기 수행**: 직접 메모리 접근 방식으로 전송함
4. **완료 이벤트 수신**: completion queue에서 완료 여부를 확인함
5. **후속 처리**: 다음 통신이나 계산으로 넘어감

## Ⅵ. 문제점 및 해결 방안

1. 문제: 메모리 등록과 큐 설정이 복잡해 애플리케이션 개발과 장애 분석 난도가 크게 높아질 수 있음
   - 해결방안: RDMA abstraction library와 standardized connection template를 적용하고 development lead time과 transport setup error rate로 검증함
2. 문제: 네트워크와 NIC 설정이 맞지 않으면 RDMA 성능 이점이 사라지고 오히려 운용 복잡도만 커질 수 있음
   - 해결방안: end to end fabric validation과 benchmark driven tuning을 적용하고 rdma throughput gain과 tail latency reduction으로 검증함
3. 문제: 등록 메모리 관리가 부실하면 보안과 자원 고갈 위험이 함께 증가할 수 있음
   - 해결방안: bounded memory registration policy와 access control enforcement를 적용하고 registered memory utilization과 unauthorized access incident count로 검증함

## Ⅶ. 적용 사례

- 분산 스토리지 시스템이 RDMA 추상화 라이브러리를 운영하며 확인 지표는 development lead time과 transport setup error rate임
- AI 클러스터가 패브릭 검증 기반 튜닝을 적용하며 확인 지표는 rdma throughput gain과 tail latency reduction임
- 고성능 데이터 플랫폼이 등록 메모리 정책을 강화하며 확인 지표는 registered memory utilization과 unauthorized access incident count임

## Ⅷ. 결론

RDMA는 원격 데이터 이동 오버헤드를 크게 줄이는 핵심 기법이지만 설정 복잡도와 자원 관리까지 포함한 운영 설계가 함께 필요함.
