---
sidebar:
  order: 88
  label: "088. 고속 직렬 인터페이스: USB•Thunderbolt"
  badge:
    text: "미출 · 50%"
    variant: note
title: "고속 직렬 인터페이스: USB•Thunderbolt (High-Speed Serial Interface)"
date: "2026-08-17T09:25:00+09:00"
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

- 정의/개념: 단일 USB Type-C 물리 커넥터를 통해 고속 데이터(USB3/4), 디스플레이 영상(DisplayPort Alt Mode), PCIe 트랜잭션 터널링 및 최대 240W 고전력(USB PD)을 통합 전송하는 범용 고속 직렬 인터페이스 규격 체계
- 배경/필요성: 주변장치 인터페이스 파편화 극복 및 단일 케이블 기반 초고속 데이터 전송(최대 120Gbps)과 통합 전력 공급(USB PD) 필요

#### 한줄 요약

- USB Type-C 기반으로 **고속 데이터, DP Alt Mode 영상, PCIe 터널링, USB PD 240W를 통합 전송하는 규격**

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Alt Mode(Alternate Mode)**: Type-C 고속 차동 라인을 재할당하여 DisplayPort, HDMI 등 비-USB 영상 신호를 네이티브 전송하는 모드.
- **PCIe Tunneling**: 외장 그래픽(eGPU)이나 고속 NVMe SSD를 위해 PCIe TLP 패킷을 USB4/TB 프레임 내에 캡슐화하여 외부로 라우팅하는 기술.
- **e-Marker(Electronic Marker)**: 케이블 양 끝 플러그에 내장되어 허용 전류(3A vs 5A), 지원 대역폭(USB 2.0 vs 40Gbps) 정보를 호스트에 알리는 식별 IC.

</details>

- DisplayPort 영상 신호를 별도 변환기 없이 네이티브 패킷으로 직결 전송하는 **얼터네이트 모드(DP Alt Mode)**
- 외장 데스크톱 가속기 및 NVMe 드라이브를 단일 케이블로 핫플러그 연결하는 **PCIe 프로토콜 터널링**
- 케이블 내장 식별 칩(**e-Marker**)과 실시간 통신하여 화재 위험을 방지하고 최대 240W를 전달하는 **USB PD 3.1 규격**

#### 한줄 요약

- **DisplayPort Alt Mode 영상 출력·PCIe 직결 터널링·e-Marker 및 USB PD 3.1(최대 240W EPR) 전력 협상**

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Host Controller**: PCIe, DisplayPort, USB3 트래픽을 단일 고속 비트 스트림으로 다중화(Multiplexing) 및 라우팅하는 인터페이스 칩셋.
- **CC Pin(Configuration Channel)**: 케이블 삽입 방향(정방향/역방향) 감지, 역할(Host/Device) 협상, USB PD 전력 프로파일 계약을 수행하는 제어 핀.
- **Kernel DMA Protection (IOMMU)**: Thunderbolt 포트를 통한 외부 악성 디바이스의 물리 메모리 무단 탈취(DMA Attack)를 차단하는 하드웨어 방화벽.

</details>

```text
[ 고속 직렬 인터페이스 Type-C 멀티플렉싱 및 보안 아키텍처 ]
┌─────────────────────────────────────────────────────────────┐
│ 1. 호스트 시스템 계층 (CPU / GPU / Memory / PCIe Bus)        │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────┴──────────────────────────────┐
│ 2. IOMMU (Kernel DMA Protection : Thunderspy 공격 원천 차단) │
└──────────────────────────────┬──────────────────────────────┘
                               │ [ 고속 프로토콜 다중화 ]
┌──────────────────────────────┴──────────────────────────────┐
│ 3. USB4 / Thunderbolt 호스트 컨트롤러 (Multiplexing Router) │
│  ├─ PCIe 패킷 터널링 모듈    ├─ DisplayPort 패킷 터널링     │
│  ├─ USB3 데이터 터널링 모듈  └─ 4. CC 로직 및 USB PD 컨트롤러│
└──────────────────────────────┬──────────────────────────────┘
                               │ [ 24-Pin USB Type-C Cable (e-Marker) ]
┌──────────────────────────────┴──────────────────────────────┐
│ 5. 타깃 엔드포인트 디바이스 (eGPU / 8K 모니터 / NVMe Dock)   │
└─────────────────────────────────────────────────────────────┘
```

선의 의미: 호스트 컨트롤러(USB4/TB4), IOMMU 보안 방화벽, Type-C CC 핀 및 e-Marker 인증 케이블 간의 고속 직렬 인터페이스 구조도.

| 구성요소 | 책임 |
|:---|:---|
| 호스트 컨트롤러(Router) | USB3, PCIe, DisplayPort 트래픽을 단일 고속 비트 스트림으로 다중화 및 터널링 라우팅 |
| CC 핀(Configuration Channel) | 케이블 삽입 방향 감지, 호스트/디바이스 역할 결정 및 USB PD 전력 프로파일 협상 |
| 케이블 e-Marker 칩 | 케이블 허용 전류(3A/5A) 및 전송 대역폭(USB 2.0~40Gbps) 사양을 호스트에 전달하는 식별 IC |
| IOMMU (Kernel DMA Protection) | 썬더볼트/USB4 포트를 통한 외부 비인가 장치의 직접 메모리 접근(DMA)을 차단하는 하드웨어 격리 모듈 |

#### 한줄 요약

- **호스트 컨트롤러(Router/Switch)·Type-C 포트 및 CC 핀·e-Marker 인증 케이블·IOMMU/DMA 보안 모듈**

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Protocol Handshake**: 케이블 연결 시 호스트와 디바이스 간에 최고 공통 분모 규격(USB 2.0, USB 3.2, USB4, TB4)을 결정하는 초기화 시퀀스.

</details>

```text
[ Type-C 케이블 연결 및 프로토콜 터널링 협상 시퀀스 ]
                         │
                         ▼
   [ 1. CC 핀 전압 강하 감지 ──> 플러그 방향 및 역할(Source/Sink) 확정 ]
                         │
                         ▼
   [ 2. SOP' 패킷 통신을 통한 e-Marker 케이블 인증 (대역폭/허용전류 조회) ]
                         │
                         ▼
   [ 3. USB PD BMC 통신 ──> 전압/전류 계약 체결 (예: 20V/5A 100W) ]
                         │
                         ▼
   [ 4. USB4 / Thunderbolt 4 프로토콜 핸드셰이크 (기능 교집합 확정) ]
                         │
                         ▼
   [ 5. IOMMU DMA 방화벽 검증 ──> PCIe / DP / USB3 동적 패킷 터널링 개시 ]
```

**동작 원리**

1. **연결 및 방향 감지**: CC 핀의 풀업/풀다운 저항 값을 측정하여 케이블 삽입 방향 및 전원 공급 역할 결정
2. **e-Marker 조회**: 케이블 내부 칩과 VCONN 라인을 통해 통신하여 40Gbps 지원 여부 및 최대 5A 용량 확인
3. **USB PD 협상**: 호스트와 디바이스가 지원 가능한 PDO(Power Data Object)를 교환하여 최적 전력 프로파일 합의
4. **프로토콜 핸드셰이크**: USB4/TB 라우터가 링크 트레이닝을 거쳐 양단이 지원하는 최고 속도(40~80Gbps) 결정
5. **터널링 가동**: IOMMU의 DMA 보안 검증을 통과한 후 PCIe/DP/USB 트래픽을 동적 타임슬롯으로 패킷 전송

#### 한줄 요약

- CC 핀 연결 감지 $\to$ **e-Marker 케이블 인증 $\to$ USB PD 전력 협상 $\to$ USB4/TB4 터널링 프로토콜 핸드셰이크 $\to$ IOMMU 보안 검증 및 동적 패킷 전송**

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **USB 3.2 vs USB4 vs Thunderbolt 4/5**:
  - USB 3.2: 20Gbps, 단순 데이터, 터널링 불가, 구형 표준
  - USB4: 40~80Gbps, 동적 대역폭, PCIe 터널링 선택 사양(제조사 파편화)
  - Thunderbolt 4/5: 40~120Gbps, PCIe 터널링 필수, Intel 인증 및 IOMMU DMA 보호 강제

</details>

| 구분 | USB 3.2 Gen 2x2 | USB4 (Gen 3x2 / Gen 4) | Thunderbolt 4 / 5 |
|:---|:---|:---|:---|
| 최대 전송 대역폭 | 최대 20 Gbps (단순 데이터) | 40 Gbps ~ 80 Gbps (동적 대역폭 공유) | 40 Gbps (TB4) / 80~120 Gbps (TB5 Bandwidth Boost) |
| PCIe 터널링 및 영상 지원 | 지원 불가 (순수 USB 데이터만 전송) | 선택적 지원 (제조사 구현에 따라 상이) | 필수 지원 (PCIe 32~64Gbps, 듀얼 4K/단일 8K 필수) |
| 인증 및 최소 요구조건 | USB-IF 기본 인증 | 기본 사양 최소화 (기능 파편화 존재) | Intel 엄격한 인증 및 IOMMU DMA 보호 필수화 |

#### 한줄 요약

- 단순 데이터는 **USB 3.2**, 범용 확장은 **USB4**, 최고성능 풀옵션 인증은 **Thunderbolt 4/5**

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Thunderspy(DMA 공격)**: 외부 포트에 악성 하드웨어를 직접 연결하여 OS 로그인 잠금을 우회하고 메모리를 직접 덤프하는 취약점.
- **EPR(Extended Power Range)**: USB-C 전력을 기존 100W(20V/5A)에서 최대 240W(48V/5A)로 확장한 최신 USB PD 3.1 규격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 외부 썬더볼트 포트에 악성 하드웨어 연결 시 발생하는 Thunderspy 다이렉트 DMA 메모리 탈취 공격 | OS 레벨 **Kernel DMA Protection(IOMMU 활성화)** 강제 적용 | 시스템 잠금 상태에서 비인가 외부 장치의 메모리 덤프 완벽 차단 |
| 미인증 저품질 케이블 사용 시 과전류 인입으로 인한 발열 및 기기 손상 위험 | **e-Marker 칩 부재 케이블 감지 시 60W(20V/3A) 및 기본 대역폭으로 강제 제한** | 규격 미달 케이블로 인한 과전류 손상 및 화재 방지 |
| 대용량 전력 공급(100W+) 및 고속 데이터 동시 전송 시 포트 단자 과열 위험 | **USB PD 컨트롤러 온도 센서 연동 및 동적 전류 스로틀링(Thermal Throttling)** 적용 | 커넥터 과열 방지 및 안전한 고속 충전 보장 |

#### 한줄 요약

- **Intel VT-d/Kernel DMA Protection 기반 Thunderspy 차단·e-Marker 미인증 케이블 60W 제한·USB PD 온도 센서 스로틀링**

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **PAM3 변조 및 비대칭 대역폭**: Thunderbolt 5에서 PAM3 변조를 도입하고 비대칭 모드(Transmit 120Gbps / Receive 40Gbps)를 지원하여 초고해상도 디스플레이 구동.

</details>

- 차세대 워크스테이션 및 모바일 랩톱 설계 시 **Thunderbolt 4/5 및 USB4 2.0 표준 채택과 IOMMU DMA 보호 하드웨어 표준 활성화**

#### 한줄 요약

- **대역폭 확장과 엄격한 DMA 하드웨어 격리**를 통한 고속 직렬 인터페이스 구축
