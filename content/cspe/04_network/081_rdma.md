---
title: "RDMA (Remote Direct Memory Access)"
date: "2026-07-05"
tags:
  - "cspe-network"
weight: 81
---

## Ⅰ. 개요
- **정의**: 원격 호스트 메모리에 CPU 개입 없이 직접 데이터를 읽고 쓰는 네트워크 전송 기술임
- **배경/필요성**: 고성능 컴퓨팅·분산 스토리지 환경에서 커널 경유 TCP 복사 오버헤드가 지연과 CPU 부하의 병목이 됨
- **비유**: 택배 기사가 수신자 창고에 직접 물건을 놓고 가는 것과 유사함

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 커널 바이패스와 제로카피 원리 이해 | Zero-copy, Kernel Bypass, OS Offload | InfiniBand vs RoCE vs iWARP 차이 혼동 주의 |

> 요약: RDMA는 CPU·커널 개입 없이 원격 메모리에 직접 접근하여 지연과 CPU 부하를 줄이는 기술임

## Ⅱ. 구성요소
```text
App (Verb API)
    |
    v
RDMA NIC (RNIC) ---> Network Fabric ---> Remote RNIC
                                             |
                                             v
                                      Remote Memory
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Verb API | 응용이 RDMA 연산을 요청하는 표준 인터페이스임 | 택배 접수 창구 |
| RNIC | 프로토콜 처리·DMA를 하드웨어에서 수행하는 네트워크 어댑터임 | 자동 분류 로봇 |
| Queue Pair (QP) | Send/Receive 큐 쌍으로 연결 단위를 구성함 | 양방향 우편함 |
| Completion Queue | 연산 완료를 응용에 통지하는 큐임 | 배송 완료 알림 |
| Memory Region (MR) | 등록된 메모리 영역으로 원격 접근 권한을 제어함 | 허가된 창고 구역 |

> 요약: RNIC가 QP 기반으로 등록된 메모리 영역에 직접 데이터를 전송하는 구조임

## Ⅲ. 절차
```text
MR 등록 --> QP 생성/연결 --> RDMA Write/Read 요청 --> CQ 완료 통지
```
- 1단계: 응용이 Memory Region을 RNIC에 등록하여 DMA 가능 영역을 확보함
- 2단계: 양측 호스트가 Queue Pair를 생성하고 연결 정보를 교환함
- 3단계: 송신 측이 RDMA Write/Read 요청을 QP에 게시하면 RNIC가 직접 전송함
- 4단계: 연산 완료 시 Completion Queue에 이벤트가 게시되어 응용이 확인함

> 요약: MR 등록 후 QP로 연결하고 RNIC가 직접 전송한 뒤 CQ로 완료를 통지하는 흐름임

## Ⅳ. 문제점
- 메모리 고정 부담: MR 등록 시 pinned memory가 필요하여 대용량 환경에서 메모리 낭비가 발생함
- 연결 확장성 한계: QP당 상태를 RNIC 캐시에 유지하므로 수천 노드 시 캐시 미스가 증가함
- 장애 격리 어려움: 원격 메모리 직접 접근으로 한 노드 오류가 상대 메모리를 오염시킬 수 있음

> 요약: 메모리 고정, 연결 확장성, 장애 전파가 대규모 환경에서 병목으로 작용함

## Ⅴ. 개선방안
1. 단기: On-Demand Paging(ODP) 적용으로 메모리 고정 없이 동적 MR 관리함
2. 중기: Scalable QP·DCT(Dynamically Connected Transport) 도입으로 연결 상태 오버헤드 감소함
3. 장기: 하드웨어 기반 메모리 보호 키·격리 메커니즘으로 원격 접근 안전성 확보함

> 요약: ODP, DCT, 하드웨어 격리를 단계적으로 적용하여 확장성과 안전성을 확보함

## Ⅵ. 전망
- 발전 방향: CXL·GPU Direct RDMA 등 이기종 메모리 패브릭과 통합 확대됨
- 기술사적 판단: AI 학습 클러스터·초저지연 금융 시스템에서 사실상 표준 전송 기술로 자리잡음
- 기술사 제언: RoCEv2 기반 데이터센터 설계 시 PFC/ECN 등 무손실 네트워크 설정 역량이 필요함
