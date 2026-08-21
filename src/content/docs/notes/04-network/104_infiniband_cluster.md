---
sidebar:
  order: 104
  label: "104. InfiniBand 클러스터 인터커넥트 (InfiniBand Cluster)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "초고성능 슈퍼컴퓨팅 인터커넥트 : 인피니밴드 클러스터 (InfiniBand Cluster Fabric)"
date: "2026-08-22T08:15:00+09:00"
tags: ["notes-network"]
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

- **인피니밴드(InfiniBand, IB)**: 고성능 컴퓨팅(HPC) 및 대규모 AI 클러스터에서 수천~수만 대의 서버 노드와 GPU 간에 초저지연(Sub-microsecond)과 초대역폭(최대 800Gbps NDR/XDR)을 제공하기 위해 IBTA(InfiniBand Trade Association)가 표준화한 전용 고속 스위칭 패브릭 아키텍처.
- **서브넷 관리자(Subnet Manager, SM)**: 인피니밴드 서브넷 내의 모든 HCA와 스위치를 탐색(Discovery)하여 로컬 식별자(LID)를 부여하고, 최적 포워딩 테이블(LFT) 및 파티션 키(P_Key)를 중앙 집중 연산·배포하는 핵심 두뇌 엔티티.

</details>

- 정의/개념: 서버의 **HCA(Host Channel Adapter)** 와 전용 **InfiniBand 스위치** 를 점대점 직결하여, 하드웨어 레벨의 **크레딧 기반 무손실 흐름 제어(Credit-Based Flow Control)** 와 **네이티브 커널 우회 RDMA** 를 제공하는 **초고성능 클러스터 인터커넥트 패브릭**
- 배경/필요성: 분산 딥러닝 텐서 병렬화(All-Reduce) 및 거대 과학 시뮬레이션에서 이더넷의 소프트웨어 스택 지연, 비결정론적 큐잉 지터 및 패킷 손실 병목을 원천 제거할 요구

#### 한줄 요약
- HCA와 전용 스위치 간 크레딧 기반 무손실 제어와 서브넷 관리자를 통해 극초저지연 고대역폭 전송을 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **크레딧 기반 흐름 제어(Credit-Based Flow Control)**: 송신 노드가 다음 홉 스위치나 수신 HCA로부터 가용한 수신 버퍼 크레딧(Credit)을 사전에 발급받고, 보유한 크레딧 한도 내에서만 패킷을 송출함으로써 버퍼 오버플로우로 인한 패킷 폐기(Drop)를 물리적으로 불가능하게 만드는 기술.
- **가상 레인(Virtual Lane, VL)**: 단일 물리 광섬유 링크 내에서 버퍼와 흐름 제어를 독립적으로 분리하여 트래픽 우선순위(QoS) 및 데드락 방지 경로를 제공하는 논리적 통신 채널 (VL0~VL15).

</details>

- **극초저지연 하드웨어 스위칭 ($\le 100\text{ns}$ 홉 지연)**: 컷스루(Cut-Through) 스위칭과 크레딧 제어를 통해 패킷 버퍼링 지연 최소화
- **완전 무손실(Zero-Loss) 신뢰성 보장**: 패킷 손실이 발생하지 않으므로 TCP와 같은 복잡한 타임아웃 및 재전송 오버헤드 부재
- **중앙 집중식 토폴로지 라우팅 (Subnet Manager)**: 분산 라우팅 프로토콜의 수렴 지연 없이 SM이 Fat-Tree, DragonFly 등 비차단(Non-Blocking) 토폴로지 경로를 일괄 계산

#### 한줄 요약
- 나노초급 초저지연, 크레딧 기반 100% 무손실 전송, 중앙 서브넷 관리자(SM) 경로 최적화를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **로컬 식별자(Local Identifier, LID)**: 인피니밴드 서브넷 내에서 각 포트(HCA, Switch Port)를 유일하게 식별하는 16비트 주소.
- **파티션 키(Partition Key, P_Key)**: 특정 노드 그룹 간의 통신 격리를 보장하기 위해 프레임 헤더에 부착하는 멀티테넌트 가상 격리 토큰.

</details>

```text
[ GPU 컴퓨트 노드 (Compute HCA) ]                 [ 고성능 분산 스토리지 (Storage HCA) ]
 ├─ RDMA User Space Buffer                          ├─ NVMe-oF Storage Target
 └─ Queue Pair (QP: RC / UC / UD)                  └─ Queue Pair (QP)
         │                                                  │
         ▼ (1. 하드웨어 크레딧 기반 직결 링크)             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 인피니밴드 스위치 패브릭 (Fat-Tree Non-Blocking Topology) ]           │
│  ├─ Leaf Switch ──── Spine Switch ──── Core Switch (QSFP/OSFP 800G)     │
│  ├─ 크레딧 기반 버퍼링 & 컷스루 포워딩 (Cut-Through Forwarding)           │
│  └─ 가상 레인 (Virtual Lanes: VL0~VL15) QoS 격리                         │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (2. 서브넷 관리 패킷: SMP / MAD)
                                     ▼
                      [ 마스터 서브넷 관리자 (Subnet Manager) ]
                       ├─ 토폴로지 자동 탐색 (Discovery Engine)
                       ├─ 포워딩 테이블 연산 (Up/Down, Fat-Tree Routing)
                       └─ P_Key 기반 보안 파티셔닝
```

선의 의미: 컴퓨트 노드와 스토리지 노드가 Fat-Tree 인피니밴드 스위치를 통해 연결되고, 서브넷 관리자가 패브릭 전체의 주소와 경로를 중앙 제어하는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **HCA (Host Channel Adapter)** | PCIe Gen5 버스와 인피니밴드 광 링크를 연결하는 RDMA 통신 가속기 | ConnectX-7 / BlueField |
| **인피니밴드 스위치** | 컷스루 기반 고속 패킷 스위칭, LFT 기반 LID 포워딩, 크레딧 반환 처리 | Quantum-2 (64 Port 400G) |
| **서브넷 관리자 (SM)** | 패브릭 내 모든 노드 탐색, 16bit LID 할당, 비차단 최적 라우팅 경로 주입 | OpenSM / Embedded SM |
| **가상 레인 (VL)** | 물리 링크를 복수의 논리적 큐로 분할하여 우선순위 지정 및 버퍼 격리 | 8~16 VLs |
| **파티션 키 (P_Key)** | 멀티 테넌트 간 통신 차단 및 특정 연산 노드 풀 격리 (Full/Limited Membership) | 16bit P_Key |

#### 한줄 요약
- HCA 어댑터, Fat-Tree 스위치 패브릭, 서브넷 관리자(SM), 가상 레인(VL), 파티션 키(P_Key)가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **서브넷 관리 패킷(Subnet Management Packet, SMP)**: SM이 패브릭 내 스위치와 HCA를 초기 탐색하고 포워딩 테이블을 프로그래밍하기 위해 사용하는 특수 관리 프레임.

</details>

```text
1. 인피니밴드 패브릭 부팅 ➔ 마스터 서브넷 관리자(SM)가 SMP 패킷을 송출하여 전체 토폴로지 자동 탐색
            │
            ▼
2. SM이 Fat-Tree 라우팅 알고리즘을 연산하여 각 HCA 포트에 LID를 할당하고 스위치 LFT에 포워딩 룰 주입
            │
            ▼
3. 컴퓨트 노드가 송신 전 대상 스위치 포트로부터 가용 버퍼 크레딧(Flow Control Credit) 수신
            │
            ▼
4. 보유한 크레딧 범위 내에서 RDMA 패킷 송출 ➔ 스위치가 컷스루 방식으로 100ns 내 목적지 포워딩
            │
            ▼
5. 목적지 노드가 패킷을 버퍼에서 처리 후 송신단으로 신규 크레딧 반환 ➔ 패킷 손실 제로 통신 완수
```

**동작 원리**

1. **자동 탐색 및 구성**: SM이 브로드캐스트 없이 지향성 라우팅(Directed Route)으로 전 장비 스캔
2. **비차단 경로 최적화**: Up/Down 또는 D-Mod-K 알고리즘을 적용하여 루프와 병목 없는 LFT 배포
3. **크레딧 동기화**: 송수신 양단이 링크 초기화 시 버퍼 블록 크기 단위로 크레딧을 상호 교환
4. **컷스루 스위칭**: 패킷 전체를 수신하기 전 헤더의 LID만을 보고 즉시 출력 포트로 데이터 스트리밍
5. **무손실 흐름 완결**: 크레딧이 0이 되면 물리적으로 송신을 멈추므로 패킷 드롭이 원천 발생하지 않음

#### 한줄 요약
- SM 토폴로지 탐색, LID/LFT 주입, 크레딧 획득, 컷스루 무손실 전송, 크레딧 반환 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **InfiniBand 대역폭 진화 규격**: SDR(10G)부터 HDR(200G), NDR(400G), XDR(800G)로 진화하는 전송 속도 표준.

</details>

| 속도 세대 (Generation) | 레인당 속도 (Lane Rate) | 4X 링크 총 대역폭 (4X Link Bandwidth) | 인코딩 방식 | 상용화 시점 |
|:---|:---|:---|:---|:---|
| **HDR (High Data Rate)** | **50 Gbps (PAM4)** | **200 Gbps** | 64b/66b | 2018년 |
| **NDR (Next Data Rate)** | **100 Gbps (PAM4)** | **400 Gbps (스위치 800G 포트 분기)**| PAM4 + RS-FEC | 2022년 (H100 표준) |
| **XDR (eXtreme Data Rate)**| **200 Gbps (PAM4)** | **800 Gbps** | PAM4 + RS-FEC | 2024~2025년 (B200) |
| **GDR (Giga Data Rate)** | **400 Gbps (PAM4/Optical)** | **1,600 Gbps (1.6 Tbps)** | 차세대 광인터커넥트 | 차세대 로드맵 |

#### 한줄 요약
- HDR 200G, NDR 400G, XDR 800G로 진화하며 고밀도 PAM4 변조와 FEC 기술을 통해 대역폭을 극대화한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **서브넷 관리자 이중화(SM High Availability)**: 마스터 SM 장애 시 서브넷 내의 스탠바이(Standby) SM이 1초 내에 마스터십을 승계하여 토폴로지 재구성 마비를 방지하는 고가용성 메커니즘.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 단일 서브넷 관리자(SM) 장애 시 신규 노드 인식 불가 및 패브릭 토폴로지 제어 마비 | **마스터-스탠바이 SM 이중화(OpenSM HA)** 구성 및 주기적 하트비트 감시 | 마스터 장애 시 1초 내 자동 페일오버 및 100% 제어 평면 가용성 확보 |
| 대규모 All-Reduce 통신 시 상위 스파인 스위치 오버서브스크립션으로 인한 성능 저하 | **Fat-Tree 1:1 Non-Blocking(비차단) 풀 바이섹션 대역폭** 토폴로지 구축 | 스파인 병목 제거 및 초대규모 GPU 클러스터 통신 효율 100% 보장 |
| 광케이블 마이크로 벤딩 또는 광모듈 열화로 인한 비트 에러(BER) 발생 및 링크 플래핑 | **스위치 포트 BER 모니터링 및 자동 링크 다운(Port Auto-Disable)** 연동 | 불량 링크 조기 격리 및 전체 클러스터 동기화 지연(Tail Latency) 방어 |

#### 한줄 요약
- SM 이중화로 제어 가용성을 확보하고, 1:1 Fat-Tree로 병목을 제거하며, BER 모니터링으로 불량 링크를 격리한다.

## Ⅶ. 결론

- 글로벌 최상위 슈퍼컴퓨터 및 초대형 프론티어 AI 학습 인프라 구축을 위해 **InfiniBand 아키텍처**는 가장 신뢰할 수 있는 사실상의 표준(De-facto Standard) 인터커넥트이며, 실무 구축 시 **1:1 비차단 Fat-Tree 토폴로지 설계**, **서브넷 관리자(SM) 고가용성 이중화**, **NVIDIA GPUDirect RDMA 및 SHARP(인네트워크 컴퓨팅)** 기술을 통합 적용하여 극한의 연산 가속 인프라를 완성

#### 한줄 요약
- InfiniBand의 크레딧 무손실 제어와 Fat-Tree 토폴로지 및 SM 이중화를 통해 초고성능 AI 클러스터를 구현한다.
