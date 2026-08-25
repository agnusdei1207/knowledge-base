---
sidebar:
  order: 88
  label: "088. 고속 직렬 인터페이스: USB•Thunderbolt"
  badge:
    text: "미출 · 50%"
    variant: note
title: "고속 직렬 인터페이스: USB•Thunderbolt (High-Speed Serial Interface)"
date: "2026-08-25T10:25:00+09:00"
tags:
  - "notes-hardware"
weight: 88
extra:
  question_no: "088"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "USB-C 기능 분화•외부 DMA 보호의 실무성"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **USB Type-C**: 상하 대칭형 24핀 물리 커넥터 폼팩터로, 초고속 데이터 전송, 고해상도 디스플레이 영상 출력, 최대 240W 고전력 충전을 단일 케이블로 수용하는 표준 하드웨어 인터페이스.
- **Thunderbolt 4/5**: PCIe 패킷 터널링, DisplayPort 영상, USB3 데이터를 단일 물리 비트 스트림으로 캡슐화하여 40~120Gbps의 초고대역폭을 확정보장하는 고속 직렬 인터페이스 표준.
- **USB PD(Power Delivery)**: Type-C CC 핀 직렬 통신을 통해 호스트와 기기간 전압/전류 프로파일을 동적 협상하여 최대 240W(48V/5A, EPR) 고전력을 공급하는 전력 제어 규격.

</details>

- 정의/개념: 단일 물리 Type-C 커넥터를 매개로 초고속 데이터 전송, DisplayPort 영상, PCIe TLP 패킷 터널링, 최대 240W 전력 공급을 다중화 통합하는 **고속 직렬 인터페이스(USB4 / Thunderbolt) 아키텍처**
- 배경/필요성: 주변장치별(전원선, HDMI, USB, DP, 외장 PCIe) 포트 난립과 파편화로 인한 **케이블 복잡도 해소 및 모바일 단말의 단일 포트 초고속 확장성 확보**

#### 한줄 요약
- USB Type-C 폼팩터 상에서 초고속 데이터, 디스플레이 영상, PCIe 터널링, 고전력 충전을 하나로 통합한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **대체 모드(Alternate Mode, Alt Mode)**: Type-C 케이블 내부의 4개 고속 차동 신호 레인을 재할당하여 DisplayPort, HDMI 등 비-USB 영상 신호를 네이티브 전송하는 기술.
- **PCIe 패킷 터널링(PCIe Tunneling)**: 외장 그래픽 카드(eGPU)나 초고속 NVMe 스토리지를 위해 PCIe TLP 트랜잭션을 USB4/Thunderbolt 프레임 내에 캡슐화하여 전송하는 기술.
- **e-Marker(Electronic Marker)**: Type-C 케이블 플러그 내부에 실장되어 케이블의 허용 전류(3A vs 5A)와 지원 대역폭(20G/40G/80G) 정보를 호스트에 전달하는 식별 IC.

</details>

- 단일 커넥터 멀티 프로토콜 다중화: **Alt Mode**를 통한 8K DisplayPort 영상 출력 및 **PCIe 패킷 터널링** 기반 외장 eGPU/NVMe 완벽 수용
- 지능형 고전력 공급: **e-Marker** 칩 인증을 기반으로 **USB PD 3.1(최대 240W, 48V/5A)** 동적 협상 충전 수행
- 외부 악성 DMA 차단: 고속 PCIe 터널링 포트를 통한 외부 메모리 덤프 공격(Thunderspy)을 방어하기 위해 **IOMMU(Kernel DMA Protection)** 강제 결합

#### 한줄 요약
- Alt Mode 영상 출력, PCIe 패킷 터널링, USB PD 고전력 충전을 단일 케이블로 지원하며 IOMMU로 DMA 보안을 확보한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **CC 핀(Configuration Channel)**: Type-C 커넥터에서 플러그 삽입 방향 감지, 호스트/디바이스 역할(Source/Sink) 결정 및 USB PD 전력 협상을 수행하는 제어 핀.
- **IOMMU(Kernel DMA Protection)**: 썬더볼트 포트에 연결된 외부 장치가 운영체제 잠금 상태에서 시스템 DRAM을 무단 덤프하지 못하도록 메모리 접근을 차단하는 하드웨어 유닛.

</details>

```text
[USB4 / Thunderbolt 고속 직렬 인터페이스 아키텍처]
 ┌─ [1. 호스트 시스템 계층] ──────────── CPU 코어 + 시스템 메인 DRAM + PCIe 루트 컴플렉스
 │                                                    │
 ├─ [2. 하드웨어 IOMMU 보안 계층] ────── [Kernel DMA Protection (Thunderspy 물리 해킹 차단)]
 │                                                    │
 ├─ [3. USB4 / TB 호스트 라우터 패브릭]
 │   ├─ [PCIe 패킷 터널링 엔진] ──────── PCIe TLP 트랜잭션 캡슐화 (eGPU/NVMe 연결)
 │   ├─ [DisplayPort Alt Mode 스위치] ── 비디오 스트림 네이티브 매핑 (8K 모니터)
 │   ├─ [USB3 데이터 터널링 엔진] ────── 대용량 파일 전송 프로토콜
 │   └─ [USB PD & CC 핀 제어기] ──────── 플러그 방향 감지 + 240W 전력 프로파일 협상
 │                                                    │
 └─ [4. Type-C 물리 인터커넥트 계층] ── [24-Pin 커넥터] + [e-Marker 인증 IC 내장 케이블]
                                                      │
                                           [타깃 디바이스: eGPU / 모니터 / NVMe 독]
```

선의 의미: 가지(`├─`, `└─`)는 하드웨어 소속 및 패킷 다중화 파이프라인; 호스트 라우터가 PCIe/DP/USB3 트래픽을 캡슐화하여 Type-C 케이블로 전송하고 IOMMU가 메모리를 보호함

| 구성요소 | 계층 및 위치 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|:---|
| **호스트 라우터 패브릭**| 칩셋 컨트롤러단 | USB, PCIe, DisplayPort 트래픽을 단일 고속 비트 스트림(40~80Gbps)으로 다중화 | 프로토콜 터널링 |
| **CC 제어 핀** | Type-C 인터페이스| 플러그 삽입 방향(정/역) 감지 및 **USB PD 전력 프로파일(최대 240W) 동적 협상** | 24-Pin 커넥터 |
| **e-Marker 인증 IC** | 케이블 플러그 내부 | 케이블 허용 전류(3A/5A) 및 최대 대역폭 사양(Gen3/4)을 호스트에 인증 전달 | 케이블 식별 칩 |
| **IOMMU 방화벽** | 시스템 메모리단 | 외부 썬더볼트 장비의 **무단 DMA 메모리 탈취(Thunderspy 공격) 원천 차단** | Kernel DMA Protection |
| **엔드포인트 디바이스**| 외부 장치단 | eGPU 가속기, 8K 디스플레이 모니터, 초고속 NVMe 독(Dock) 등 | 복합 장치 수용 |

#### 한줄 요약
- 고속 직렬 인터페이스는 호스트 라우터, CC/PD 컨트롤러, e-Marker 케이블, IOMMU DMA 방화벽 및 Type-C 24핀 커넥터로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **프로토콜 핸드셰이크(Protocol Handshake)**: 케이블 결착 직후 호스트와 외장 장치 간에 지원 가능한 최상위 프로토콜(USB 3.2, USB4, Thunderbolt 4/5)을 협상하여 링크를 수립하는 과정.

</details>

```text
1. Type-C 케이블 결착 감지 (CC 핀 전압 강하 측정 ➔ 플러그 삽입 방향 확정)
                      │
                      ▼
2. 전원 공급 역할(Source vs Sink) 결정 및 SOP' 통신으로 e-Marker 케이블 사양 인증
                      │
                      ▼
3. USB PD 3.1 협상 체결 (예: 28V/5A 140W 또는 48V/5A 240W EPR 충전 개시)
                      │
                      ▼
4. USB4 / Thunderbolt 프로토콜 핸드셰이크 ➔ 최고 공통 전송 속도(40Gbps / 80Gbps) 확정
                      │
                      ▼
5. 외부 디바이스가 PCIe 패킷 터널링(eGPU / NVMe)을 요청했는가?
   ┌──────────────────┴──────────────────┐
[ 단순 USB/DP 디스플레이 요청 ]       [ PCIe 터널링 요청 (eGPU / 독) ]
   │                                     │
   ▼                                     ▼
6. DP Alt Mode 및 USB3 패킷 스트리밍   6. OS IOMMU(Kernel DMA Protection) 보안 검증 수행
   │                                     ┌──────────┴──────────┐
   │                                   [ 승인 (인가 장치) ]   [ 거부 (비인가 장치/잠금) ]
   │                                     │                     │
   │                                     ▼                     ▼
   │                                   7. PCIe TLP 캡슐화     7. DMA 접근 차단
   │                                      초고속 터널링 개시      (Thunderspy 방어)
   └──────────────────┬──────────────────┴─────────────────────┘
                      │
                      ▼
8. 단일 Type-C 케이블을 통한 데이터, 영상, 전력 전송 동시 가동
```

분기 결과: **안전한 장치는** IOMMU 승인 후 초고속 PCIe 터널링을 수행하며, **비인가 장치는** DMA가 차단되어 시스템 메모리를 지킴

#### 한줄 요약
- CC 핀 감지 ➔ e-Marker 인증 ➔ USB PD 협상 ➔ 프로토콜 핸드셰이크 ➔ IOMMU 검증 후 PCIe/DP 터널링 개시 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **PAM3 변조**: Thunderbolt 5에서 3개 전압 레벨(-1, 0, +1)을 사용하여 2클록당 3비트를 전송함으로써 최대 120Gbps 비대칭 대역폭을 구현하는 신호 변조 기술.

</details>

| 직렬 인터페이스 규격 | USB 3.2 Gen 2x2 | USB4 (Gen 3x2) | Thunderbolt 4 | Thunderbolt 5 |
|:---|:---|:---|:---|:---|
| 최대 전송 대역폭 | **최대 20 Gbps** | **40 Gbps ~ 80 Gbps** | **40 Gbps (최소 보장)** | **80 Gbps (최대 120 Gbps)** |
| 신호 변조 방식 | NRZ (듀얼 레인) | NRZ / PAM3 | NRZ (듀얼 레인) | **PAM3 (Bandwidth Boost)** |
| PCIe 터널링 지원 | **미지원 (순수 USB 데이터)** | 선택 사양 (제조사 재량) | **필수 지원 (PCIe 32Gbps)** | **필수 지원 (PCIe 64Gbps)** |
| 외부 디스플레이 지원 | DP Alt Mode (선택) | DP 1.4a 터널링 | **듀얼 4K 또는 8K 모니터** | **트리플 4K 144Hz 또는 8K** |
| DMA 보안 요구조건 | 해당 없음 | 권장 사항 | **IOMMU 필수 강제** | **IOMMU 필수 강제** |

#### 한줄 요약
- 단순 데이터는 USB 3.2, 범용 확장은 USB4, 고성능 PCIe 터널링 및 보안 인증은 Thunderbolt 4/5를 채택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Thunderspy 공격**: 썬더볼트 포트에 악성 하드웨어 장치를 직결하여 OS 잠금 화면과 로그인 인증을 우회하고 시스템 메모리를 직접 덤프하는 악성 DMA 공격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 외부 포트 직결을 통한 **Thunderspy** 악성 DMA 메모리 탈취 | **OS 수준 Kernel DMA Protection(IOMMU 활성화) 강제 정책** | 시스템 잠금 상태에서 비인가 외장 장치의 DMA 덤프 원천 차단 |
| 저품질 비인증 케이블 사용 시 과전류로 인한 포트 손상 및 화재 | **e-Marker 미탑재 케이블 감지 시 충전 전류를 60W(3A)로 강제 제한** | 과전류 발열 차단 및 하드웨어 기기 보호 |
| 초고속 신호 전송 시 2미터 이상 긴 케이블 내 심각한 신호 감쇄 | **케이블 내부에 액티브 리타이머(Active Retimer) IC 실장** | 신호 지터 제거 및 40~80Gbps 최대 대역폭 무결성 유지 |

#### 한줄 요약
- 실무에서는 IOMMU로 악성 DMA를 차단하고, e-Marker로 전류를 제어하며, 액티브 리타이머로 신호 감쇄를 극복한다.

## Ⅶ. 결론

- 초고속 데이터 전송, 8K 영상 출력, 240W 고전력 충전을 단일 폼팩터로 수용하기 위해 **Thunderbolt 4/5 및 USB4 표준을 채택**하고, 외부 물리 해킹을 차단하기 위해 **하드웨어 IOMMU 기반 Kernel DMA Protection**을 필수 연동하며, 장거리 신호 무결성을 위해 **e-Marker 인증 및 액티브 리타이머 케이블**을 적용하는 고신뢰 고속 직렬 I/O 인프라 확립

#### 한줄 요약
- 고속 직렬 인터페이스는 단일 Type-C 포트로 데이터, 영상, 전력을 통합하는 동시에 IOMMU 기반 DMA 격리를 갖추는 것이 필수적이다.