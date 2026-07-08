---
title: "RoCE (RDMA over Converged Ethernet)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 254
extra:
  question_no: "254"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- RoCE는 이더넷 환경에서 RDMA를 사용할 수 있게 하는 기술임
- InfiniBand 전용 패브릭 없이도 RDMA 장점을 활용할 수 있다는 점이 핵심임
- 손실 제어와 혼잡 제어가 제대로 설계되지 않으면 성능이 쉽게 흔들릴 수 있음

## Ⅰ. 개요

- **정의/개념**: RoCE는 이더넷 네트워크 위에서 RDMA 기능을 제공하여 CPU 우회형 저지연 고성능 데이터 전송을 가능하게 하는 데이터센터 네트워크 기술임
- **배경/필요성**: 기존 이더넷 인프라를 활용하면서도 AI와 스토리지 워크로드에 필요한 RDMA 성능을 확보하려는 요구가 커지면서 RoCE가 확산됨

## Ⅱ. 특징

- 이더넷 기반이라 기존 데이터센터 환경과의 통합성이 높음
- RDMA를 통해 CPU 부하와 복사 오버헤드를 줄일 수 있음
- 손실 없는 패브릭에 가깝게 운용해야 성능이 안정적임
- 네트워크 설정 품질에 따라 성능 편차가 매우 크게 발생함

## Ⅲ. 종류 및 비교

| 판단 기준 | RoCE | InfiniBand | TCP over Ethernet |
|:---|:---|:---|:---|
| 기반 네트워크 | Ethernet | 전용 IB 패브릭 | Ethernet |
| RDMA 지원 | 지원 | 지원 | 미지원 |
| 통합 용이성 | 높음 | 중간 | 매우 높음 |
| 운영 난도 | 혼잡 제어 튜닝 필요 | 전용 패브릭 운영 | 가장 단순 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| RoCE NIC | 이더넷 환경에서 RDMA 기능을 수행하는 네트워크 어댑터임 |
| Ethernet Switch Fabric | RoCE 트래픽을 운반하며 혼잡 제어와 우선순위 정책이 성능 안정성에 큰 영향을 주는 스위치 패브릭임 |
| Priority Flow Control | 패킷 손실을 줄이기 위해 흐름을 제어해 RDMA 전송 안정성을 유지하는 제어 메커니즘임 |
| ECN and Congestion Control | 혼잡 신호를 감지하고 조정해 대규모 클러스터에서 지연 폭증을 방지하는 운영 계층임 |
| RDMA Stack | 메모리 등록과 큐 관리와 원격 접근을 제공해 애플리케이션이 RDMA 이점을 활용하게 하는 소프트웨어 계층임 |

```text
+--------+    Ethernet / RoCE    +---------+    Ethernet / RoCE    +--------+
| Node A |<--------------------->| Switch  |<--------------------->| Node B |
+--------+                       +---------+                       +--------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| RDMA 버퍼 준비 | -> | 이더넷 경로 설정 | -> | RoCE 전송    | -> | 혼잡 제어 반영 | -> | 완료 처리    |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **RDMA 버퍼 준비**: 호스트가 메모리와 큐를 등록함
2. **이더넷 경로 설정**: 우선순위와 패브릭 정책을 적용함
3. **RoCE 전송**: 이더넷 위에서 RDMA 전송을 수행함
4. **혼잡 제어 반영**: PFC와 ECN 정책으로 혼잡을 제어함
5. **완료 처리**: 수신 결과와 완료 이벤트를 정리함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 손실 제어와 혼잡 제어가 부실하면 RoCE 패브릭이 대규모 통신에서 지연 폭증과 성능 불안정을 일으킬 수 있음
   - 해결방안: PFC tuning과 ECN based congestion control을 적용하고 p99 network latency와 pause storm incidence로 검증함
2. 문제: 이더넷 환경 차이로 장비별 설정 편차가 크면 RDMA 성능 재현성이 낮아질 수 있음
   - 해결방안: fabric standardization과 configuration baseline management를 적용하고 configuration drift count와 rdma performance consistency로 검증함
3. 문제: RDMA 장점을 기대하고 무분별하게 도입하면 운영 복잡도 대비 실효 성능 개선이 제한될 수 있음
   - 해결방안: workload driven adoption policy와 comparative benchmark를 적용하고 cost benefit ratio와 target workload acceleration gain으로 검증함

## Ⅶ. 적용 사례

- AI 클러스터가 PFC와 ECN 튜닝을 적용하며 확인 지표는 p99 network latency와 pause storm incidence임
- 데이터센터 네트워크 팀이 설정 기준선을 관리하며 확인 지표는 configuration drift count와 rdma performance consistency임
- 분산 스토리지 플랫폼이 도입 전 비교 벤치마크를 수행하며 확인 지표는 cost benefit ratio와 target workload acceleration gain임

## Ⅷ. 결론

RoCE는 이더넷 기반 RDMA 확장의 현실적 해법이지만 패브릭 품질과 혼잡 제어가 받쳐주지 않으면 기대 성능을 얻기 어려움.
