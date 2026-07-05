---
title: "NVLink (NVLink)"
date: "2026-07-05"
tags:
  - "cspe-hardware"
weight: 56
---

## Ⅰ. 개요
- **정의**: NVIDIA GPU 간 고대역폭 직접 연결을 제공하는 점대점 인터커넥트 기술
- **배경/필요성**: 멀티 GPU 학습에서 PCIe 대역폭이 GPU 간 데이터 교환 병목이 되므로, PCIe를 우회하는 전용 고속 링크가 필요함
- **비유**: PCIe가 일반 도로라면, NVLink는 GPU 전용 고속 전용차선임

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| GPU 간 인터커넥트 구조 이해 | PCIe 대비 대역폭 배율과 토폴로지 | NVLink와 NVSwitch의 역할을 구분할 것 |

> 요약: PCIe를 대체하여 GPU 간 고대역폭 직접 통신을 제공하는 전용 인터커넥트임

## Ⅱ. 구성요소
```text
GPU 0 ---NVLink--- GPU 1
  |                  |
NVLink             NVLink
  |                  |
GPU 2 ---NVLink--- GPU 3
  |                  |
  +--- NVSwitch ----+
       (All-to-All)
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| NVLink | GPU 간 점대점 고속 시리얼 링크로 양방향 데이터 전송을 수행함 | 전용 고속도로 차선 |
| NVSwitch | 다수 GPU 간 All-to-All 연결을 제공하는 크로스바 스위치 칩 | 고속도로 인터체인지 |
| NVLink Bridge | 2개 GPU를 물리적으로 연결하는 보드 레벨 커넥터 | 고가도로 연결 구간 |
| NCCL | NVLink 위에서 집합 통신(AllReduce 등)을 수행하는 통신 라이브러리 | 교통 관제 시스템 |

> 요약: NVLink 링크와 NVSwitch 스위치로 GPU 간 고대역폭 메시 토폴로지를 구성함

## Ⅲ. 절차
```text
GPU 토폴로지 구성 --> 메모리 주소 매핑 --> 데이터 전송 --> 집합 통신 완료
       |                    |                  |                |
       v                    v                  v                v
  NVSwitch 연결       Unified Memory      NVLink 패킷전송    AllReduce 동기화
```
- 1단계: NVLink Bridge 또는 NVSwitch로 GPU 간 물리 토폴로지를 구성함
- 2단계: Unified Virtual Addressing(UVA)으로 GPU 간 메모리 주소 공간을 통합 매핑함
- 3단계: GPU가 원격 GPU 메모리에 NVLink를 통해 직접 읽기·쓰기(RDMA 방식)를 수행함
- 4단계: NCCL이 NVLink 토폴로지를 인식하여 AllReduce 등 집합 통신을 최적 경로로 수행함

> 요약: 물리 연결 후 UVA 매핑, RDMA 전송, 집합 통신의 순서로 GPU 간 데이터를 교환함

## Ⅳ. 문제점
- 확장성 한계: 노드 내 GPU 수가 증가하면 NVLink 포트 수 부족으로 풀메시 구성이 어려움
- 비용 부담: NVSwitch 탑재 시스템(DGX 등)의 도입 비용이 PCIe 기반 대비 수 배 높음
- 벤더 종속: NVIDIA GPU 전용 기술이어서 타사 가속기와의 상호 운용이 불가함

> 요약: 확장성 한계, 높은 도입 비용, 벤더 종속이 주요 제약임

## Ⅴ. 개선방안
1. 단기: NVSwitch 세대 업그레이드(NVLink 5세대 등)로 포트당 대역폭과 포트 수를 확장함
2. 중기: NVLink과 InfiniBand(057 참조)를 계층적으로 조합하여 노드 내·노드 간 대역폭을 균형 있게 설계함
3. 장기: UALink 등 개방형 GPU 인터커넥트 표준 참여로 벤더 종속을 완화함

> 요약: 대역폭 확장, 계층적 인터커넥트 설계, 개방형 표준 참여로 개선이 필요함

## Ⅵ. 전망
- 발전 방향: NVLink 세대별 대역폭이 1.8TB/s 이상으로 확대되며 수천 GPU 클러스터의 핵심 인터커넥트로 자리잡음
- 기술사적 판단: 초대규모 모델 학습에서 GPU 간 통신 대역폭이 학습 효율을 결정하는 핵심 요소가 됨
- 기술사 제언: 클러스터 설계 시 NVLink(노드 내)과 InfiniBand(노드 간) 대역폭 비율을 워크로드에 맞게 설정해야 함
