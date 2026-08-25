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

- **USB Type-C**: 상하 대칭형 24핀 물리 폼팩터로 데이터, 비디오, 전력 공급을 단일 케이블로 수용하는 표준 커넥터.
- **Thunderbolt 4/5**: Intel과 Apple이 주도하여 PCIe, DisplayPort, USB 프로토콜을 통합 터널링하고 최소 40~120Gbps 대역폭을 보장하는 고속 직렬 인터페이스 표준.
- **USB PD(Power Delivery)**: Type-C CC 핀 통신을 통해 전압/전류를 동적 협상하여 최대 240W(48V/5A, EPR) 고전력을 공급하는 표준.

</details>

- 정의/개념: 단일 Type-C 커넥터를 통해 데이터, DP 영상, PCIe 터널링, 최대 240W 전력을 통합 전송하는 **고속 직렬 인터페이스**
- 배경/필요성: 주변장치별 포트 파편화로 인해 **단일 케이블 초고속 데이터 전송 및 통합 전력 공급 불가**

#### 한줄 요약
- USB Type-C 폼팩터 상에서 초고속 데이터, 디스플레이 영상, PCIe 터널링, 고전력 충전을 하나로 통합한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Alt Mode(Alternate Mode)**: Type-C 고속 차동 라인을 재할당하여 DisplayPort, HDMI 등 비-USB 영상 신호를 네이티브 전송하는 모드.
- **PCIe 터널링(PCIe Tunneling)**: 외장 그래픽(eGPU)이나 고속 NVMe SSD를 위해 PCIe TLP 패킷을 USB4/TB 프레임 내에 캡슐화하여 전송하는 기술.
- **e-Marker(Electronic Marker)**: 케이블 양 끝 플러그에 내장되어 허용 전류(3A vs 5A)와 지원 대역폭 정보를 호스트에 전달하는 식별 IC.

</details>

- **Alt Mode**를 통해 DisplayPort 비디오 스트림을 별도 변환 없이 네이티브 직결 전송
- **PCIe 터널링** 기반 외장 eGPU 및 초고속 NVMe 독(Dock) 확장성 제공
- **e-Marker** 칩 인증 및 USB PD 3.1 규격을 통한 최대 240W(48V/5A) 동적 전력 공급

#### 한줄 요약
- Alt Mode 영상 출력, PCIe 패킷 터널링, USB PD 고전력 충전을 단일 케이블로 지원한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **CC 핀(Configuration Channel)**: 케이블 삽입 방향 감지, 호스트/디바이스 역할 결정 및 USB PD 전력 프로파일 협상 전용 핀.
- **IOMMU(Kernel DMA Protection)**: 썬더볼트/USB4 포트를 통한 외부 비인가 장치의 직접 메모리 접근(DMA)을 차단하는 하드웨어 보안 모듈.

</details>

```text
[고속 직렬 인터페이스(USB4 / Thunderbolt) 아키텍처]
|-- 호스트 시스템 계층 (CPU·Host DRAM·PCIe 버스)
|-- IOMMU 하드웨어 계층 (Kernel DMA Protection - Thunderspy 방어)
|-- 호스트 컨트롤러 패브릭 (Multiplexing Router)
|   |-- PCIe 패킷 터널링 엔진
|   |-- DisplayPort Alt Mode 비디오 스위치
|   |-- USB3 데이터 터널링 엔진
|   `-- USB PD 및 CC 핀 제어기
`-- Type-C 물리 인터커넥트 (24-Pin e-Marker 인증 케이블)
    `-- 타깃 디바이스 (eGPU·8K 모니터·초고속 NVMe 독)
```

선의 의미: 계층 및 신호 다중화 전송 구조

| 구성요소 | 책임 |
|:---|:---|
| 호스트 컨트롤러 | USB, PCIe, DP 트래픽을 단일 고속 비트 스트림(40~80Gbps)으로 다중화 |
| **CC 핀** | 플러그 방향 감지 및 USB PD 전력 프로파일(최대 240W) 동적 협상 |
| **e-Marker 칩** | 케이블 허용 전류(3A/5A) 및 최대 대역폭 사양을 호스트에 인증 전달 |
| **IOMMU 방화벽** | 외부 썬더볼트 장비의 무단 DMA 메모리 탈취(Thunderspy) 원천 차단 |
| 엔드포인트 장치 | 외장 GPU, 고해상도 디스플레이, NVMe 스토리지 등 고속 I/O 디바이스 |

#### 한줄 요약
- 호스트 라우터, CC/PD 컨트롤러, e-Marker 케이블, IOMMU DMA 방화벽이 통합된 구조다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **프로토콜 핸드셰이크(Protocol Handshake)**: 케이블 연결 시 호스트와 디바이스 간에 공통 최고 사양(USB 3.2, USB4, TB4)을 결정하는 초기화 시퀀스.

</details>

```text
Type-C 케이블 연결 감지 (CC 핀 전압 강하 측정)
        │
   케이블 삽입 방향 및 전원 공급 역할(Source/Sink) 확정
        │
   SOP' 통신으로 e-Marker 케이블 인증 (대역폭 및 허용 전류 조회)
        │
   USB PD 협상 체결 (예: 20V/5A 100W 또는 48V/5A 240W)
        │
   USB4 / Thunderbolt 프로토콜 핸드셰이크 (최고 공통 속도 확정)
        │
   IOMMU DMA 보안 검증 통과 후 PCIe / DP / USB3 동적 패킷 터널링 개시
```

#### 한줄 요약
- CC 핀 감지 → e-Marker 인증 → USB PD 협상 → 프로토콜 핸드셰이크 → IOMMU 검증 후 터널링 개시 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **PAM3 변조**: Thunderbolt 5에서 3개 전압 레벨로 2사이클당 3비트를 전송하여 최대 120Gbps 비대칭 대역폭을 구현하는 기술.

</details>

| 직렬 인터페이스 규격 | USB 3.2 Gen 2x2 | USB4 (Gen 3x2) | Thunderbolt 4 | Thunderbolt 5 |
|:---|:---|:---|:---|:---|
| 최대 전송 대역폭 | 최대 20 Gbps | 40 Gbps ~ 80 Gbps | 40 Gbps (고정 보장) | 80 Gbps (최대 120 Gbps) |
| 변조 및 신호 방식 | NRZ (듀얼 레인) | NRZ / PAM3 | NRZ (듀얼 레인) | **PAM3** (Bandwidth Boost) |
| PCIe 터널링 | 미지원 (순수 USB 데이터) | 선택 사양 (제조사 재량) | 필수 지원 (PCIe 32Gbps) | 필수 지원 (PCIe 64Gbps) |
| DMA 보안 요구 | 해당 없음 | 권장 사항 | **IOMMU 필수 강제** | **IOMMU 필수 강제** |

#### 한줄 요약
- 단순 데이터는 USB 3.2, 범용 확장은 USB4, 고성능 PCIe 터널링 및 보안 인증은 Thunderbolt 4/5를 채택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Thunderspy**: 외부 포트에 악성 하드웨어를 직결하여 OS 잠금을 우회하고 메모리를 직접 덤프하는 악성 DMA 공격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 외부 포트 직결을 통한 **Thunderspy** DMA 메모리 탈취 | OS **Kernel DMA Protection(IOMMU)** 활성화 | 잠금 상태에서 비인가 외부 장치의 DMA 덤프 원천 차단 |
| 미인증 케이블 사용 시 과전류 인입 및 기기 손상 | **e-Marker** 미탑재 케이블 감지 시 60W(3A)로 강제 제한 | 저품질 케이블로 인한 과전류 발열 및 화재 방지 |
| 초고속 신호 전송 시 긴 케이블 내 신호 감쇄 | 케이블 내 액티브 리타이머(Active Retimer) 칩 내장 | 2미터 이상 장거리에서도 40Gbps 무결성 대역폭 유지 |
| 100W+ 고속 충전 시 커넥터 단자 과열 | USB PD 컨트롤러 실시간 온도 센서 연동 및 전류 스로틀링 | 포트 손상 방지 및 안전한 고속 충전 보장 |

#### 한줄 요약
- IOMMU Kernel DMA Protection, e-Marker 전력 제한, 액티브 리타이머, 온도 스로틀링을 통해 안전성을 확보한다.

## Ⅶ. 결론

- 고성능 모바일 단말 및 워크스테이션은 **Thunderbolt 4/5 및 USB4 표준**을 채택하고, **하드웨어 IOMMU DMA 보호**를 연동하여 초고속 확장성과 보안성 완성

#### 한줄 요약
- 고속 직렬 인터페이스는 단일 Type-C 포트로 데이터, 영상, 전력을 통합하는 동시에 IOMMU 기반 DMA 격리를 갖추는 것이 필수적이다.