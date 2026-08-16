---
sidebar:
  order: 79
  label: "079. PCIe 스위칭 아키텍처 (PCIe Switching)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "PCIe 스위칭 아키텍처 (PCIe Switching)"
date: "2026-08-13T12:00:06+09:00"
tags:
  - "notes-hardware"
weight: 79
extra:
  question_no: "079"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "직렬 패브릭의 대역폭•격리 설계 수요가 있음"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **PCIe(Peripheral Component Interconnect Express)**: 고속 직렬 점대점(Point-to-Point) 레인(x1, x4, x8, x16)을 사용하는 대표적인 온보드/서버 인터커넥트 규격.
- **PCIe 스위치(PCIe Switch)**: 1개의 업스트림(Upstream) 포트를 복수의 다운스트림(Downstream) 포트로 패키징 라우팅하여 PCIe 엔드포인트를 확충하는 칩셋.
- **스위칭 패브릭(Switching Fabric)**: PCIe 트랜잭션 패킷(TLP)의 목적지 주소를 기반으로 출력 포트 및 P2P 경로를 동적 디스패치하는 논리 패킷 스위칭 망.

</details>

- 정의/개념: 단일 루트 컴플렉스(Root Complex) 하단에서 복수의 PCIe 엔드포인트를 확충하고 P2P(Peer-to-Peer) 트랜잭션을 디스패치하는 **PCIe 스위치**
- 배경/필요성: CPU 직결 루트 포트 수 한계 극복 및 GPU, NVMe SSD 간 호스트 메모리 경유 없는 직접 P2P 고속 데이터 전송 요구성

#### 한줄 요약

- PCIe 스위치는 루트 측 링크 아래에 여러 엔드포인트와 P2P 경로를 확장하는 패킷 패브릭이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **TLP(Transaction Layer Packet)**: PCIe 상에서 Read/Write, Completion 패킷 정보를 담고 있는 트랜잭션 계층 패킷.
- **P2P(Peer-to-Peer) 전송**: GPU<->NVMe, GPU<->GPU 간 트랜잭션이 CPU/DRAM 호스트 메모리를 거치지 않고 PCIe 스위치 내부에서 직통 전송되는 기술.
- **ACS(Access Control Services)**: P2P DMA 접근 시 보안 검증을 위해 트랜잭션을 IOMMU로 강제 리디렉션하거나 인가하는 액세스 제어 서비스.
- **오버서브스크립션(Oversubscription)**: 다운스트림 포트들의 총 요구 대역폭 합이 업스트림 포트 대역폭을 초과하여 대기 지연이 발생하는 현상.

</details>

![PCIe 스위치 본선 부하율에 따른 대기 지연 차트](/study/diagrams/pcie-oversubscription-delay.svg)

- 호스트 CPU 메모리 경유 없는 초고속 단말 간 **P2P(Peer-to-Peer)** 데이터 전송 지원
- 다운스트림 팬아웃 확장에 따른 **오버서브스크립션** 대기 지연 관리 요구성
- **ACS(Access Control Services)** 및 IOMMU 연동 기반 트랜잭션 보안 격리 및 메모리 보호

$$
\rho = \frac{\sum_{i=1}^{N} B_{i,\mathrm{demand}}}{B_{\mathrm{up,usable}}}
$$

#### 한줄 요약

- 갈래마다 흐름을 따로 조절해도 장치 요구량 합이 본선 용량을 넘으면 대기한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Root Complex**: CPU 및 호스트 DRAM 메모리 하이어라키와 PCIe 버스 패브릭을 결합하는 최상위 노드.
- **Upstream Port**: PCIe 스위치 상에서 Root Complex 또는 상위 스위치를 향해 결합하는 입력 레인 포트.
- **Downstream Port**: NVMe SSD, GPU, NIC 등 실제 엔드포인트(Endpoint)로 분기 출력되는 레인 포트.

</details>

```text
루트 컴플렉스
└─ 업스트림 포트
   └─ 스위칭 패브릭
      ├─ 다운스트림 포트
      │  └─ 엔드포인트
      └─ … 동일 포트•엔드포인트 반복
```

선의 의미: 루트 컴플렉스가 업스트림 포트를 거쳐 스위칭 패브릭 및 다운스트림 포트 상의 엔드포인트들로 연결되는 트리 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| Root Complex | CPU/메모리 계층 연결 및 최상위 PCIe Bus 브릿징 |
| Upstream Port | 상위 Root Complex 레인 결합 및 **TLP** 패킷 수용 |
| 스위칭 패브릭 | **TLP** 주소 디코딩, P2P 라우팅 및 흐름 제어 크레딧(Credit) 관리 |
| Downstream Port | GPU, NVMe SSD 엔드포인트 기기와 물리 레인 바인딩 |
| 엔드포인트(Endpoint) | 트랜잭션 요청자(Requester) 및 응답 처리자(Completer) 역할 수행 |

#### 한줄 요약

- 루트 컴플렉스·업스트림 포트·스위칭 패브릭·다운스트림 포트·엔드포인트를 계층형 PCIe로 연결한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Requester ID & Tag**: 완료 TLP를 원래 요청과 대응시키는 요청자 식별자와 태그.
- **Credit-Based Flow Control**: 수신 측 버퍼 공간 수치(Credit)를 송신 측이 사전 확인하여 패킷 드롭을 방지하는 흐름 제어.

</details>

```text
[요청 엔드포인트의 요청 TLP]
              │
              ▼
1. 포트 수신•태그 추적
              │
              ▼
2. 주소 디코딩•중재
              │
       ┌──────┴────────┐
       │ 루트 방향     │ P2P 방향
       ▼               ▼
[루트 컴플렉스]   [대상 엔드포인트]
       └──────┬────────┘
              ▼
3. 접근 경계 검증
              │
              ▼
4. 완료자 요청 처리
              │
              ▼
[완료 TLP를 원 요청자에 반환]
```

### 동작 원리

1. 포트 수신·태그 추적: 스위치 포트가 **TLP**를 수신하고 Requester ID와 Tag 추적 정보 기록.
2. 주소 디코딩·중재: 스위치 패브릭 상에서 TLP 주소를 파악하여 루트 컴플렉스 또는 **P2P** 다운스트림 포트로 디스패치.
3. 접근 경계 검증: **ACS**로 P2P 경로를 통제하고 **IOMMU**로 DMA 주소 권한 검증.
4. 완료자 요청 처리: 대상 장치가 TLP 요청을 수행하고 완료 TLP 생성.

#### 한줄 요약

- 요청을 완료자에게 보내고 요청자 ID•태그로 완료 TLP를 원 요청자에게 반환한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Direct Attachment**: PCIe 스위치 없이 CPU/Root Complex 레인에 엔드포인트를 1:1 직접 결합하는 토폴로지.

</details>

| 비교 항목 | PCIe 스위칭 (Switching Topology) | 직접 연결 (Direct Attachment) |
|:---|:---|:---|
| 적용 기준 | 다수 GPU·NVMe의 팬아웃과 P2P 경로가 필요할 때 | 소수 장치와 최소 홉 연결이 중요할 때 |
| 확장성/기능 | 팬아웃 확장과 **P2P 전송** 경로 지원 | 루트 컴플렉스의 포트·레인 수에 따라 제한 |
| 대역폭/지연 | **오버서브스크립션**과 스위치 홉 지연 가능 | 스위치 홉이 없으나 루트 자원 공유 가능 |

#### 한줄 요약

- 스위치는 장치 확장·P2P 경로에 유리하고, 직접 연결은 장치별 전용 업링크 대역폭에 유리하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Downtraining**: 신호 잡음이나 레이아웃 결함으로 인해 Gen5 x16 레인이 Gen4 또는 x4/x8로 물리 하향 동작하는 현상.
- **IOMMU(Input-Output MMU)**: 가상 머신(VM) 및 P2P DMA 연산 시 메모리 주소 변환 및 영역 침범을 격리하는 하드웨어.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 업스트림 본선 초과로 인한 **오버서브스크립션** 지연 | 동시 부하 기준 업링크 용량과 QoS 설계 | 패브릭 병목과 **꼬리 지연** 완화 |
| 신호 무결성 손상으로 인한 PCIe **Downtraining** | 리타이머 배치 및 SI/PI 시뮬레이션 | 목표 링크 폭·세대 유지 가능성 향상 |
| P2P DMA 간 악성 메모리 침범 공격 | **ACS** 활성화 및 **IOMMU** 가상화 결합 | VM 간 DMA 보안 격리 |

> 사례: 8-GPU 서버 상의 **PCIe Gen5 스위치** 기반 P2P GPUDirect Storage 아키텍처 구축

#### 한줄 요약

- 가속기를 배치할 때 P2P 경로와 업스트림 용량 및 스위치 홉을 함께 산정해야 병목과 꼬리 지연을 예측할 수 있다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **PCIe 선택 기준(PCIe Architecture Selection Criteria)**: 엔드포인트 팬아웃 수량, P2P 전송 수요 및 오버서브스크립션 비율에 기초한 설계 체계.

</details>

- 다수 장치·P2P는 **PCIe 스위칭**, 소수 장치·최소 홉은 **직접 연결** 선택

#### 한줄 요약

- 다수 장치·P2P는 스위칭, 소수 장치·최소 홉은 직접 연결을 선택한다.
