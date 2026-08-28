---
sidebar:
  order: 104
  label: "104. InfiniBand 클러스터 인터커넥트"
  badge:
    text: "기출 · 50%"
    variant: note
title: "초고성능 슈퍼컴퓨팅 인터커넥트 : 인피니밴드 클러스터"
date: "2026-08-26T14:13:38+09:00"
tags:
  - "notes-network"
weight: 104
extra:
  question_no: "104"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "IBTA 표준, HCA, 서브넷 관리자(Subnet Manager), 크레딧 기반 흐름 제어(Credit-Based), Fat-Tree 토폴로지"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **InfiniBand (인피니밴드)**: HPC 및 초대형 AI 클러스터에서 서브 마이크로초 지연과 테라비트 대역폭을 제공하는 IBTA 표준 인터커넥트.
- **Subnet Manager (서브넷 관리자, SM)**: 서브넷 내의 모든 HCA와 스위치를 탐색하여 16비트 LID를 할당하고 최적 포워딩 테이블(LFT)을 배포하는 중앙 제어기.

</details>

- 정의/개념: HCA·전용 스위치의 **크레딧 무손실·컷스루** 인터커넥트
- 배경/필요성: 이더넷 스택은 노드 간 통신마다 **소프트웨어 처리와 버퍼 대기에서 오는 테일 지연**을 반복하므로, 링크 계층에서 크레딧으로 수신 여유를 미리 확인하고 컷스루로 흘려보내 버퍼 대기와 손실 재전송을 함께 제거

#### 한줄 요약
- 하드웨어 크레딧 기반 무손실 흐름 제어, 컷스루 스위칭, 중앙 서브넷 관리자를 통해 극한의 클러스터 성능을 보장한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Credit-Based Flow Control**: 수신단 버퍼에 여유 공간이 있을 때만 송신단에 토큰(Credit)을 부여하여 하드웨어 레벨에서 패킷 드롭을 원천 차단하는 흐름 제어.
- **Cut-Through Switching**: 패킷 전체를 수신할 때까지 기다리지 않고 헤더의 목적지 LID만 확인하는 즉시 100ns 내에 출력 포트로 밀어내는 고속 포워딩.

</details>

- **크레딧 무손실 제어**: 수신 버퍼 범위에서만 송신
- **컷스루 스위칭**: LID 확인 후 즉시 포워딩
- **서브넷 관리자**: LID·LFT와 Fat-Tree 경로 주입

#### 한줄 요약
- 크레딧 기반 무손실, 컷스루 초저지연 스위칭, 서브넷 관리자 중앙 최적 경로 제어를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **HCA (Host Channel Adapter)**: 호스트의 PCIe Gen5 버스와 인피니밴드 광 링크를 연결하여 RDMA 전송을 가속하는 전용 어댑터 (Mellanox ConnectX).
- **Fat-Tree Topology**: 스파인 계층으로 갈수록 링크 대역폭을 비례 확장하여 모든 노드 간 1:1 전대역폭(Non-Blocking) 통신을 보장하는 구조.

</details>

```text
[InfiniBand 정적 구성]
|-- HCA
|-- 인피니밴드 스위치
|-- 서브넷 관리자
|-- 가상 레인
`-- 파티션 키
```

선의 의미: 컴퓨트 노드와 스토리지 노드가 Fat-Tree 인피니밴드 스위치를 통해 연결되고 서브넷 관리자가 패브릭 전체의 주소와 경로를 중앙 제어하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| HCA | **RDMA 통신 가속** | ConnectX-7 |
| 인피니밴드 스위치 | **컷스루·LFT·크레딧 처리** | Quantum-2 |
| 서브넷 관리자 | **LID 할당·경로 주입** | OpenSM |
| 가상 레인 | **우선순위 큐·버퍼 격리** | 8~16 VLs |
| 파티션 키 | **노드 풀 가상 격리** | 16bit P_Key |

#### 한줄 요약
- 서브넷 관리자가 전체 경로표를 중앙에서 계산해 주입하므로, 개별 스위치는 분산 라우팅 수렴 시간을 치르지 않고 결정된 경로만 집행한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **LFT (Linear Forwarding Table)**: SM이 각 스위치 ASIC에 프로그래밍하는 정적 포워딩 테이블로, 패킷의 16비트 LID를 기반으로 출력 포트를 즉시 결정함.

</details>

```text
패브릭 초기화
    |
1. SM 토폴로지 탐색
    |
2. LID 할당·LFT 주입
    |
3. 버퍼 크레딧 획득
    |
4. 컷스루 RDMA 송출
    |
5. 크레딧 반환
    |
무손실 완료
```

- 1. SM 토폴로지 탐색
- 2. LID 할당·LFT 주입
- 3. 버퍼 크레딧 획득
- 4. 컷스루 RDMA 송출
- 5. 크레딧 반환

#### 한줄 요약
- 크레딧 확보 여부가 전송과 대기를 가르며, 송신 전에 수신 여유를 확인하는 대가로 손실과 재전송 비용이 원천적으로 발생하지 않는다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **HDR vs NDR vs XDR vs GDR**: 대역폭 진화에 따른 4X 링크 전송 속도 표준 규격.

</details>

| 속도 세대 (Generation) | 레인당 속도 (Lane Rate) | 4X 링크 총 대역폭 | 인코딩 방식 | 상용화 시점 |
|:---|:---|:---|:---|:---|
| HDR | **50 Gbps·PAM4** | **200 Gbps** | 64b/66b | 2018년 |
| NDR | **100 Gbps·PAM4** | **400 Gbps** | PAM4·RS-FEC | 2022년 |
| XDR | **200 Gbps·PAM4** | **800 Gbps** | PAM4·RS-FEC | 2024~2025년 |
| GDR | **400 Gbps·광** | **1.6 Tbps** | 차세대 광 | 로드맵 |

#### 한줄 요약
- HDR 200G, NDR 400G, XDR 800G로 진화하며 고밀도 PAM4 변조와 FEC 기술을 통해 대역폭을 극대화한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **SHARP (Scalable Hierarchical Aggregation and Reduction Protocol)**: All-Reduce 집계 연산을 GPU가 아닌 인피니밴드 스위치 ASIC 하드웨어에서 직접 수행하여 통신 트래픽을 50% 절감하는 인네트워크 컴퓨팅 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 단일 SM 장애로 제어 평면 마비 | **OpenSM HA·하트비트** | 자동 페일오버 |
| All-Reduce의 스파인 병목 | **1:1 Fat-Tree·SHARP** | 집계 부하 분산 |
| 광모듈 BER·링크 플래핑 | **BER 감시·포트 자동 격리** | 테일 지연 방어 |
| 오결선에 따른 토폴로지 불균형 | **ibnetdiscover·ibdiagnet** | 결선 오류 검출 |

#### 한줄 요약
- SM 이중화로 제어 가용성을 확보하고, 1:1 Fat-Tree로 병목을 제거하며, BER 모니터링으로 불량 링크를 격리한다.

## Ⅶ. 결론

- 최고 성능 HPC는 **InfiniBand·Fat-Tree**, 집계 병목은 **SHARP** 적용

#### 한줄 요약
- InfiniBand는 크레딧 기반 무손실 제어와 Fat-Tree 토폴로지 및 SM 이중화를 통해 초고성능 AI 클러스터를 실현하는 표준 인터커넥트다.
