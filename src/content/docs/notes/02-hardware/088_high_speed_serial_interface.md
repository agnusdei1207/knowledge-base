---
sidebar:
  order: 88
  label: "088. 고속 직렬 인터페이스: USB•Thunderbolt (High-Speed Serial Interface)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "고속 직렬 인터페이스: USB•Thunderbolt (High-Speed Serial Interface)"
date: "2026-08-10T10:00:00+09:00"
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

<details><summary>핵심 용어</summary>

- **USB-C(Type-C)**: 24-Pin 가반형 상하 대칭 구조를 가지며, USB 3.2/4, Thunderbolt, DisplayPort Alt-Mode 및 USB PD 전력 수용을 표준화한 범용 인터페이스 폼팩터.
- **Thunderbolt 4/5**: Intel과 Apple이 협력 수립한 고속 시리얼 인터커넥트 규격으로, PCIe, DisplayPort 및 USB4 패킷을 멀티플렉싱(40Gbps~120Gbps) 전송하는 프로토콜.
- **USB PD(Power Delivery)**: USB-C 케이블을 통하여 단말 간 양방향 최대 240W(48V/5A, EPR 규격) 전력 전송을 제어하는 규격.

</details>

- 정의/개념: 차동 시리얼 레인 매핑 및 전력/영상/PCIe 터널링 멀티플렉싱을 단일 Type-C 커넥터 폼팩터 상에 통합 제공하는 **USB & Thunderbolt 고속 직렬 인터페이스**
- 배경/필요성: 영상(DisplayPort), 대용량 데이터(PCIe), 고전력(USB PD) 단자의 파편화 해소 및 통합 범용 억세스 요구성

#### 한줄 요약

- USB-C는 호스트•장치•케이블이 공통으로 지원하는 기능만 활성화한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Alt Mode(Alternate Mode)**: USB-C 물리 레인을 DisplayPort, HDMI 등 타 고속 직렬 프로토콜 신호 전송선으로 재할당하는 동작 모드.
- **PCIe Tunneling**: 외장 GPU, NVMe 등 PCIe 트랜잭션 TLP 패킷을 USB4/Thunderbolt 프레임 내에 캡슐화하여 40Gbps 이상 전송하는 패브릭 기술.
- **e-Marker(Electronic Marker)**: USB-C 케이블 커넥터 내부에 내장되어 허용 전류(3A/5A), 전송 대역폭(20Gbps/40Gbps) 정보를 전달하는 식별 칩셋.

</details>

- DisplayPort 영상 신호를 전송선에 맵핑하는 **Alt Mode(Alternate Mode)** 지원
- 외장 그래픽 카드(eGPU) 및 초고속 스토리지를 연동하는 **PCIe Tunneling** 수용
- **e-Marker** IC 기반 케이블 스펙 자동 판독 및 **USB PD** 기반 최대 240W 스마트 전력 가변 제어

#### 한줄 요약

- 기능 탐색과 Thunderbolt 외부 DMA 격리가 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Host Controller**: xHCI(USB) 및 Thunderbolt/USB4 매핑 터널링 라우터 패브릭 칩셋.
- **CC Pin(Configuration Channel)**: USB-C 포트 단자의 삽입 방향, 역할(Host/Device), 전력 계측(USB PD) 및 Alt-Mode 진입을 협상하는 제어 핀.
- **IOMMU(VT-d/AMD-Vi)**: Thunderbolt PCIe 터널링 인가 시 외부 악성 DMA 접근을 메모리 차원에서 차단하는 하드웨어 격리 장치.

</details>

```text
[IOMMU] -- [호스트 컨트롤러] -- [USB-C 포트]
                                      |
                          [케이블•e-Marker] -- [장치 컨트롤러]
```

선의 의미: 호스트 컨트롤러가 USB-C 포트 및 e-Marker 케이블을 통해 디바이스와 통신하며, IOMMU가 호스트 측 DMA 보안을 관장하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| 호스트 컨트롤러 | USB4/Thunderbolt 패킷 라우팅 및 **PCIe Tunneling** 멀티플렉싱 |
| CC Pin(Config Channel) | 케이블 방향성, **USB PD** 전력 협상 및 **Alt-Mode** 핸드셰이크 |
| 케이블•e-Marker | 허용 대역폭(40Gbps) 및 최고 전축 전류(5A) 메타데이터 전달 |
| IOMMU | Thunderbolt PCIe 직결 시 외부 디바이스 **DMA 덤프 공격** 방어 차단 |

#### 한줄 요약

- 호스트 컨트롤러, USB-C 포트, 전자 마커, 장치 컨트롤러 경로와 IOMMU의 외부 DMA 격리가 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **USB4 / TB4 Protocol Handshake**: CC 핀 전압 래칭 후 호스트와 디바이스 간 터널링 모드(DisplayPort / PCIe / USB3)를 자동 선택 체결하는 과정.

</details>

```text
[USB-C 연결 감지]
        │
        ▼
1. 케이블 능력 확인
        │
        ▼
2. 전력•기능 협상
        │
        ▼
3. 공통 기능 확정
        │
        ▼
4. 외부 DMA 경계 설정
        │
        ▼
5. 데이터•영상 링크 활성화
        │
        ▼
 [협상 기능 제공]
```

### 동작 원리

1. **케이블 능력 확인**: **CC Pin**을 통한 연결 감지 및 **e-Marker** 통신으로 허용 전류/대역폭 체크.
2. **전력·기능 협상**: **USB PD** 계약 체결(VBUS 전압 결정) 및 **Alt-Mode / Tunneling** 기능 협상.
3. **공통 기능 확정**: 호스트/디바이스/케이블이 매칭되는 최고 프로토콜(Thunderbolt 4 등) 래칭.
4. **외부 DMA 경계 설정**: **PCIe Tunneling** 구동 시 **IOMMU(VT-d)** 활성화로 호스트 메모리 접근 권한 제한.
5. **데이터·영상 링크 활성화**: 데이터, DisplayPort, PCIe 패킷 멀티플렉싱 전송 수행.

#### 한줄 요약

- 공통 기능 확정과 외부 DMA 경계 적용을 마친 뒤 데이터·영상 링크 활성화를 수행한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **USB 3.2 Gen 2x2**: 2개 차동 레인을 사용하여 최대 20Gbps를 보장하는 USB 데이터 인터페이스.
- **Thunderbolt 4**: 40Gbps 전송, 듀얼 4K 디스플레이, PCIe 32Gbps 실효 대역폭 및 DMA 보안(IOMMU)을 의무화한 규격.

</details>

| 비교 항목 | USB 3.2 Gen 2x2 | USB4 Gen 3x2 | Thunderbolt 4 |
|:---|:---|:---|:---|
| 최고 대역폭 | 20 Gbps | 40 Gbps | 40 Gbps (동일 대역폭) |
| PCIe 터널링 | 미지원 | 옵션 지원 (Optional) | **필수 지원** (PCIe 32Gbps 최저 인가) |
| 외부 디스플레이 | Alt-Mode 한정 | DisplayPort 터널링 | **Dual 4K / Single 8K** 필수 지원 |
| DMA 보안 (IOMMU) | 해당 없음 | 옵션 사양 | **IOMMU(VT-d) 필수 요구** (Security Level) |

#### 한줄 요약

- 범용 장치•충전은 USB, 외장 고속 주변장치 상호연결•다중 화면은 Thunderbolt가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **DMA Attack (Thunderspy)**: 외부 Thunderbolt PCIe 레인을 통해 호스트 메모리를 무단 덤프/위변조하는 하드웨어 보안 위협.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Thunderbolt 포트를 통한 **DMA Attack (Thunderspy)** 위협 | **IOMMU (VT-d)** 활성화 및 SL5(Secure DMA) 설정 | 메모리 직접 덤프 원천 차단 |
| 저품질 비인증 케이블 사용 시 **Downtraining** 및 발열 | **e-Marker** 검증 및 USB-IF 공식 인증 케이블 사용 | 40Gbps / 240W 안정 전송 |
| USB-C 동시 충전/디스플레이 출력 시 과열 | **USB PD** 온도 센서 텔레메트리 연동 | VBUS 전류 제어로 포트 용융 방지 |

> 사례: **Thunderbolt 4** 독(Dock) 연동 시 **IOMMU** 기반 DMA 덤프 방어 및 듀얼 4K 디스플레이 구축

#### 한줄 요약

- 업무용 도크는 호스트 컨트롤러와 장치 및 케이블이 모두 필요한 화면 수와 해상도 및 충전 전력을 지원하는지 확인한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **직렬 인터페이스 선택 기준(High-Speed Serial Selection Criteria)**: 요구 대역폭, PCIe 터널링 필요성, 전력 용량 및 IOMMU 보안에 근거한 규격 선정 체계.

</details>

- **직렬 인터페이스 선택 기준**에 따라 대용량 eGPU/외장 NVMe 및 듀얼 4K 출력 시 **Thunderbolt 4/5**, 단순 데이터/충전 시 **USB 3.2/USB4** 채택

#### 한줄 요약

- Type-C 폼팩터 상의 전력/영상/PCIe 터널링 멀티플렉싱 및 IOMMU 기반 DMA 보호 통합 고속 직렬 인터페이스 구축 체계 적용.
