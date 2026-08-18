---
sidebar:
  order: 79
  label: "079. PCIe 스위칭 아키텍처 (PCIe Switching)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "PCIe 스위칭 아키텍처 (PCIe Switching)"
date: "2026-08-17T09:25:00+09:00"
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

- **PCIe(Peripheral Component Interconnect Express)**: 고속 직렬 점대점(Point-to-Point) 차동 링크 기반의 컴퓨터 확장 버스 표준.
- **PCIe Switch(PCIe 스위치)**: 단일 업스트림 포트로부터 수신된 TLP(Transaction Layer Packet)를 다수의 다운스트림 포트로 분배 및 라우팅하는 패브릭 IC.
- **Root Complex(루트 컴플렉스)**: CPU와 시스템 메모리 서브시스템을 PCIe 패브릭 토폴로지의 최상단에서 연결하고 전체 버스를 제어하는 호스트 브리지.

</details>

- 정의/개념: 단일 루트 컴플렉스(Root Complex) 하단에서 제한된 CPU PCIe 레인 수를 확장하고, 다중 엔드포인트(GPU, NVMe SSD, NIC) 간의 고속 패킷 스위칭 및 Peer-to-Peer(P2P) 직결 트랜잭션을 지원하는 직렬 인터커넥트 스위칭 아키텍처
- 배경/필요성: 고밀도 AI/HPC 서버에서 수십 개의 고대역폭 가속기를 연결할 때 발생하는 **CPU 레인 부족 한계를 극복하고 호스트 메모리 경유 없는 초저지연 P2P DMA 통신 제공**

#### 한줄 요약

- 단일 Root Complex 하단에서 **PCIe 레인 확장 및 고속 P2P 트랜잭션 라우팅을 제공하는 스위칭 패브릭**

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **TLP(Transaction Layer Packet)**: 주소 기반 읽기/쓰기 및 메시지를 전달하는 PCIe 최상위 계층 패킷.
- **P2P Transfer(Peer-to-Peer 전송)**: 호스트 CPU나 DRAM을 거치지 않고 PCIe 스위치 내부 패브릭을 통해 엔드포인트 간(GPU $\leftrightarrow$ SSD/NIC)에 데이터를 직접 DMA 전송하는 기술.
- **ACS(Access Control Services)**: P2P 트랜잭션이 허용되지 않은 가상화 VM이나 메모리 영역을 무단 침범하지 못하도록 강제로 루트 컴플렉스나 IOMMU로 리다이렉트하는 보안 통제 표준.
- **Oversubscription(초과 구독)**: 다운스트림 엔드포인트들의 총 요구 대역폭 합계가 업스트림 포트의 가용 대역폭보다 커서 발생하는 대역폭 경합 비율.

</details>

![PCIe 스위치 본선 부하율에 따른 대기 지연 차트](/study/diagrams/pcie-oversubscription-delay.svg)

- 호스트 CPU/메모리 경유 없이 스위치 내부 패브릭에서 직접 패킷을 중계하는 **초저지연 Peer-to-Peer(P2P) DMA 전송**
- 다수의 고속 엔드포인트 동시 송신 시 발생하는 **업스트림 초과 구독(Oversubscription) 대기 지연 통제**
- 가상화 환경(SR-IOV)에서 불법적인 P2P 메모리 접근을 방지하는 **ACS(Access Control Services) 및 IOMMU 격리**

$$
\rho = \frac{\sum_{i=1}^{N} B_{i,\mathrm{demand}}}{B_{\mathrm{up,usable}}}
$$

#### 한줄 요약

- **CPU 우회 P2P DMA 직결·초과 구독(Oversubscription) 대역폭 관리·ACS/IOMMU 하드웨어 격리**

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Upstream Port(USP)**: 루트 컴플렉스(호스트 CPU) 방향을 향하는 스위치 인터페이스 포트.
- **Downstream Port(DSP)**: 가속기, SSD, 네트워크 카드 등 엔드포인트 장비와 연결되는 스위치 출력 포트.
- **Switching Fabric Core**: 수신된 TLP의 목적지 주소를 디코딩하여 대상 DSP 또는 USP로 패킷을 비차단(Non-blocking) 포워딩하는 크로스바 스위치.

</details>

```text
[ PCIe 스위칭 아키텍처 및 P2P 직결 데이터 흐름도 ]
┌─────────────────────────────────────────────────────────────┐
│ 1. 루트 컴플렉스 (Root Complex : 호스트 CPU + Host DRAM)     │
└──────────────────────────────┬──────────────────────────────┘
                               │ [ PCIe Gen5 x16 Upstream Link ]
┌──────────────────────────────┴──────────────────────────────┐
│ 2. PCIe 스위치 (PCIe Switch Fabric)                          │
│  ├─ 업스트림 포트 (Upstream Port, USP)                      │
│  ├─ 3. 스위칭 패브릭 코어 (TLP 주소 라우팅 & ACS 검증)       │
│  ├─ 다운스트림 포트 1 (DSP 1)    ├─ 다운스트림 포트 2 (DSP 2)│
└──────────────┬───────────────────────────────┬──────────────┘
               │ [ P2P 직결 통신 경로 ]         │
┌──────────────▼──────────────┐        ┌──────▼──────────────┐
│ 4. 엔드포인트 1 (GPU / NPU) │ ◄────► │ 4. 엔드포인트 2 (NVMe)│
└─────────────────────────────┘        └─────────────────────┘
```

선의 의미: Root Complex, 업스트림 포트(USP), 스위칭 패브릭 코어, 다운스트림 포트(DSP) 및 엔드포인트(GPU/NVMe) 간의 PCIe 스위칭 아키텍처 구조도.

| 구성요소 | 책임 |
|:---|:---|
| 루트 컴플렉스 | CPU와 메모리가 있는 본진으로, 전체 PCIe 고속도로망을 통제하는 절대 권력의 최상위 노드 |
| 업스트림 포트 | 본진(루트) 쪽을 향해 뚫려 있는 스위치의 윗방향 포트로, 트랜잭션(**TLP**)을 빨아들이는 입구 |
| 스위칭 패브릭 | 들어온 TLP의 주소표를 까보고 "넌 본진으로 가라", "넌 GPU로 가라" 하고 냅다 던져버리는 라우팅 코어 |
| 다운스트림 포트 | GPU, NVMe SSD 같은 실제 장비(엔드포인트)들과 물리적인 선(레인)으로 묶여있는 아랫방향 출구 포트 |
| 엔드포인트 | 실제로 계산하거나 데이터를 저장하는 말단 노가다 장비들로, 명령을 던지거나 응답을 뱉어냄 |

#### 한줄 요약

- **루트 컴플렉스(Root Complex)·업스트림 포트(USP)·스위칭 패브릭 코어·다운스트림 포트(DSP)·엔드포인트(EP)**

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Requester ID / Tag**: TLP 요청을 발행한 장치 번호(Bus:Device:Function)와 트랜잭션 고유 태그로 완료 패킷(Completion) 라우팅에 사용.

</details>

```text
[ PCIe 스위치 TLP 패킷 수신 및 P2P 라우팅 시퀀스 ]
                         │
                         ▼
   [ 1. DSP 1 에서 GPU 로부터 TLP 요청 패킷 수신 (Requester ID & Tag 기록) ]
                         │
                         ▼
   [ 2. 스위칭 패브릭 주소 디코딩 : 목적지 메모리 매핑 확인 ]
        /                                               \
   [ 호스트 메모리 영역 ]                              [ 타겟 엔드포인트 (DSP 2 NVMe) ]
        │                                               │
   [ USP 를 통해 루트 컴플렉스로 포워딩 ]         [ 3. ACS 보안 검증 (P2P 허용 여부 판정) ]
                                                        /                 \
                                                   [ 허용 ]             [ 차단 ]
                                                      │                    │
                                            [ 4. DSP 2 로 직결 전송 ]  [ USP 로 리다이렉트 ]
```

**동작 원리**

1. **TLP 수신**: 엔드포인트 GPU가 발행한 메모리 읽기/쓰기 TLP가 다운스트림 포트 1(DSP 1)로 인입
2. **주소 디코딩**: 스위칭 패브릭이 TLP 헤더의 64비트 주소를 분석하여 목적지 포트 판별
3. **ACS 검증**: P2P 트랜잭션일 경우 ACS 레지스터를 조회하여 해당 가상 도메인 간의 직접 통신 권한 확인
4. **P2P 직결 포워딩**: 권한이 유효하면 호스트 CPU 개입 없이 DSP 2(NVMe SSD)로 패킷을 즉시 크로스바 스위칭
5. **완료 반환**: 데이터 전송 후 대상 장비가 생성한 CplD(Completion with Data) 패킷을 원래 Requester ID로 역방향 반환

#### 한줄 요약

- TLP 패킷 인입 $\to$ **Requester ID/Tag 장부 기록 $\to$ 목적지 메모리 주소 디코딩 $\to$ ACS/IOMMU 보안 검증 $\to$ 다운스트림 DSP 직결 라우팅 / 완료(CplD) TLP 반환**

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Switching Topology vs Direct Attachment**:
  - Switching: 스위치 IC를 통한 문어발 레인 확장, 대규모 GPU/SSD 클러스터링, P2P 직결
  - Direct Attach: CPU PCIe 레인에 1:1 직결, 최소 지연, 장치 수 확장 엄격히 제한

</details>

| 비교 항목 | PCIe 스위칭 토폴로지 (Switching) | PCIe 직접 직결 토폴로지 (Direct Attach) |
|:---|:---|:---|
| 확장성 및 포트 수 | 수십~수백 개 엔드포인트 확장 (단일 스위치 96~144 레인) | CPU SoC 내장 레인 수(보통 64~128 레인)에 엄격히 제한 |
| P2P 통신 및 호스트 부하 | 스위치 내부에서 P2P 패킷 직결 처리, 호스트 CPU 개입 0 | 호스트 CPU/루트 컴플렉스를 경유하여 왕복 지연 발생 |
| 한계 및 추가 오버헤드 | 업스트림 초과 구독(Oversubscription) 병목 및 스위치 홉 지연 | 장치 수 확장 한계 및 복합 가속기 클러스터링 불가 |

#### 한줄 요약

- 고밀도 가속기 P2P는 **PCIe 스위칭**, 소수 장치 초저지연은 **직접 직결(Direct Attach)**

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Retimer(리타이머)**: PCIe Gen5/Gen6 초고속 신호가 긴 PCB 배선을 지나면서 감쇄될 때 신호를 복원(CDR)하고 지터를 제거하여 링크 다운트레이닝(Downtraining)을 방지하는 IC.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 밑에 달린 GPU들이 동시에 급격히 데이터를 쏴서 업스트림 본선이 꽉 막혀버리는 **초과 구독** 재앙 터짐 | 최대 부하량을 계산해 업스트림 용량을 넉넉하게 뚫고 뼈 깎는 대역폭 트래픽 제어(QoS) 강력 도입 | 패브릭이 막혀서 시스템이 뻗어버리는 병목 현상과 꼬리 지연을 효과적으로 완화 |
| 선로 노이즈가 심해서 최고 속도(Gen5)로 못 달리고, 강제로 속도가 반토막 나는 **다운트레이닝** 발생 | 중간중간에 신호 증폭기(리타이머)를 충분히 적용하고 신호 무결성(SI/PI) 빡세게 시뮬레이션 돌림 | 속도 반토막 나는 굴욕 없이 목표로 한 PCIe 레인 폭과 세대(Gen) 최고 성능 절대 사수 |
| GPU가 남의 메모리나 다른 가상 머신(VM) 영역을 허락도 없이 쑤셔버리는 악성 P2P 해킹 공격 발발 | 스위치에서 **ACS** 기능을 강제 활성화하고 **아이오엠엠유**(IOMMU)로 가상 주소 멱살 잡아 완벽 격리 | 가상 머신 간 불법 DMA 데이터 탈취 공격을 철저히 차단해 극강의 보안 아키텍처 완성 |

#### 한줄 요약

- **업스트림 대역폭 초과 구독(Oversubscription) 통제·리타이머(Retimer) 신호 무결성 확보·ACS/IOMMU P2P 보안 격리**

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **CXL(Compute Express Link) 스위치로의 진화**: 단순 PCIe 블록 전송을 넘어 CXL.mem/CXL.cache 프로토콜을 스위칭하여 풀링된 메모리 및 가속기 간 캐시 일관성 공유 지원.

</details>

- AI 가속 서버(8x GPU) 및 NVMe-oF 스토리지 어레이에서 **PCIe Gen5/Gen6 스위칭 패브릭(Broadcom, Microchip) 및 CXL 스위칭 표준 채택**

#### 한줄 요약

- **엔드포인트 밀집도와 P2P 트래픽 비율**에 최적화된 PCIe 스위칭 패브릭 설계
