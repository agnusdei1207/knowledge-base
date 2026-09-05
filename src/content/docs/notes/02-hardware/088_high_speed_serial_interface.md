---
sidebar:
  order: 88
  label: "088. 고속 직렬 인터페이스: USB•Thunderbolt"
  badge:
    text: "미출 · 50%"
    variant: note
title: "고속 직렬 인터페이스: USB•Thunderbolt (High-Speed Serial Interface)"
date: "2026-08-31T09:55:00+09:00"
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

- 정의/개념: 단일 Type-C 커넥터로 데이터·영상·PCIe 터널링 및 전력을 다중화하는 고속 직렬 인터페이스 아키텍처
- 배경/필요성: 데이터 전송, 영상 출력, 외부 버스 확장 및 충전 규격의 파편화로 인한 단말 기구 설계 복잡성 및 인터페이스 호환성 한계

#### 한줄 요약
- **USB Type-C** 폼팩터 상에서 초고속 데이터, 디스플레이 영상, PCIe 터널링, 고전력 충전을 하나로 통합한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **대체 모드(Alternate Mode, Alt Mode)**: Type-C 케이블 내부의 4개 고속 차동 신호 레인을 재할당하여 DisplayPort, HDMI 등 비-USB 영상 신호를 네이티브 전송하는 기술.
- **PCIe 패킷 터널링(PCIe Tunneling)**: 외장 그래픽 카드(eGPU)나 초고속 NVMe 스토리지를 위해 PCIe TLP 트랜잭션을 USB4/Thunderbolt 프레임 내에 캡슐화하여 전송하는 기술.
- **e-Marker(Electronic Marker)**: Type-C 케이블 플러그 내부에 실장되어 케이블의 허용 전류(3A vs 5A)와 지원 대역폭(20G/40G/80G) 정보를 호스트에 전달하는 식별 IC.
- **IOMMU(Kernel DMA Protection)**: 썬더볼트 포트에 연결된 외부 장치가 운영체제 잠금 상태에서 시스템 DRAM을 무단 덤프하지 못하도록 메모리 접근을 차단하는 하드웨어 유닛.

</details>

- 단일 커넥터 멀티 프로토콜 다중화: **Alt Mode** 영상 출력 및 **PCIe 패킷 터널링** 기반 외장 가속기 수용
- 지능형 고전력 공급: **e-Marker** IC 인증 기반 **USB PD** 3.1 동적 협상 전력 공급
- 외부 악성 DMA 차단: 메모리 덤프 방어를 위한 **IOMMU** 기반 **Kernel DMA Protection** 결합

#### 한줄 요약
- Alt Mode 영상 출력, PCIe 패킷 터널링, USB PD 고전력 충전을 단일 케이블로 지원하며 IOMMU로 DMA 보안을 확보한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **CC 핀(Configuration Channel)**: Type-C 커넥터에서 플러그 삽입 방향 감지, 호스트/디바이스 역할(Source/Sink) 결정 및 USB PD 전력 협상을 수행하는 제어 핀.

</details>

```text
[USB4 / Thunderbolt 고속 직렬 인터페이스 아키텍처]
 ├── 호스트 시스템 계층 ───────────── CPU 코어 + 시스템 메인 DRAM + PCIe 루트 컴플렉스
 ├── 하드웨어 IOMMU 보안 계층 ─────── Kernel DMA Protection (Thunderspy 물리 해킹 차단)
 ├── USB4 / TB 호스트 라우터 패브릭
 │   ├── PCIe 패킷 터널링 엔진 ───── PCIe TLP 트랜잭션 캡슐화 (eGPU/NVMe 연결)
 │   ├── DisplayPort Alt Mode 스위치 ─ 비디오 스트림 네이티브 매핑 (8K 모니터)
 │   ├── USB3 데이터 터널링 엔진 ─── 대용량 파일 전송 프로토콜
 │   └── USB PD & CC 핀 제어기 ───── 플러그 방향 감지 + 240W 전력 프로파일 협상
 └── Type-C 물리 인터커넥트 계층 ──── 24-Pin 커넥터 + e-Marker 인증 IC 내장 케이블
```

선의 의미: 가지(`├──`, `└──`)는 하드웨어 소속 및 패킷 다중화 파이프라인; 호스트 라우터가 PCIe/DP/USB3 트래픽을 캡슐화하여 Type-C 케이블로 전송하고 IOMMU가 메모리를 보호함

| 구성요소 | 계층 및 위치 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|:---|
| 호스트 라우터 패브릭 | 칩셋 컨트롤러단 | USB·PCIe·DP 트래픽을 단일 비트스트림으로 다중화 | 프로토콜 터널링 |
| CC 제어 핀 | Type-C 인터페이스 | 플러그 방향 감지 및 **USB PD** 전력 프로파일 협상 | 24-Pin 커넥터 |
| e-Marker 인증 IC | 케이블 플러그 내부 | 케이블 허용 전류 및 대역폭 사양 인증 전달 | 케이블 식별 칩 |
| IOMMU 방화벽 | 시스템 메모리단 | 외부 썬더볼트 장비의 무단 DMA 메모리 접근 차단 | **Kernel DMA Protection** |
| 엔드포인트 디바이스 | 외부 장치단 | eGPU, 8K 디스플레이, 초고속 NVMe 수용 | 복합 장치 수용 |

#### 한줄 요약
- 호스트 라우터가 프로토콜마다 따로 두던 포트를 하나의 비트스트림으로 대신 받아 내고, 그 한 커넥터가 감당할 전류와 대역폭의 상한은 규격으로 고정되는 대신 **CC 핀**과 케이블 속 e-Marker가 연결할 때마다 협상해 정한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **프로토콜 핸드셰이크(Protocol Handshake)**: 케이블 결착 직후 호스트와 외장 장치 간에 지원 가능한 최상위 프로토콜(USB 3.2, USB4, Thunderbolt 4/5)을 협상하여 링크를 수립하는 과정.

</details>

```text
[외부 장치 연결 및 전원 인입]
                │
                ▼
1. Type-C CC 핀 결착 감지 및 플러그 방향 확정
                │
                ▼
2. e-Marker 케이블 인증 및 전원 공급 역할(Source/Sink) 결정
                │
                ▼
3. USB PD 3.1 전력 프로파일 동적 협상 및 공급 개시
                │
                ▼
4. USB4 / Thunderbolt 프로토콜 핸드셰이크 및 전송 속도 확정
                │
                ▼
5. IOMMU 보안 검증 및 PCIe 터널링·DP Alt Mode 다중화 전송
                │
                ▼
[데이터·영상·전력 동시 전송 가동]
```

분기 결과: IOMMU 보안 검증 승인 장치는 PCIe 터널링을 즉시 가동하며 비인가 장치는 DMA 접근이 차단됨

#### 한줄 요약
- 전력과 데이터, 영상 협상을 커넥터 하나로 모아 케이블 수를 줄이는 대신, PCIe 터널링이 열리는 순간 외부 장치가 DMA 경로에 올라서므로 IOMMU 검증이 그 대가로 따라붙는다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **PAM3 변조**: Thunderbolt 5에서 3개 전압 레벨(-1, 0, +1)을 사용하여 2클록당 3비트를 전송함으로써 최대 120Gbps 비대칭 대역폭을 구현하는 신호 변조 기술.

</details>

| 직렬 인터페이스 규격 | USB 3.2 Gen 2x2 | USB4 (Gen 3x2) | Thunderbolt 4 | Thunderbolt 5 |
|:---|:---|:---|:---|:---|
| 최대 전송 대역폭 | 20 Gbps | 40~80 Gbps | 40 Gbps | 80~120 Gbps |
| 신호 변조 방식 | NRZ (듀얼 레인) | NRZ / PAM3 | NRZ (듀얼 레인) | PAM3 |
| PCIe 터널링 | 미지원 | 선택 사양 | 32 Gbps 필수 | 64 Gbps 필수 |
| 외부 디스플레이 지원 | DP Alt Mode (선택) | DP 1.4a 터널링 | 듀얼 4K 또는 8K | 트리플 4K 또는 8K |
| DMA 보안 요구조건 | 해당 없음 | 권장 사항 | **IOMMU** 필수 | **IOMMU** 필수 |

#### 한줄 요약
- 단순 데이터는 USB 3.2, 범용 확장은 USB4, 고성능 PCIe 터널링 및 보안 인증은 Thunderbolt 4/5를 채택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Thunderspy 공격**: 썬더볼트 포트에 악성 하드웨어 장치를 직결하여 OS 잠금 화면과 로그인 인증을 우회하고 시스템 메모리를 직접 덤프하는 악성 DMA 공격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Thunderspy 악성 DMA 메모리 탈취 | **IOMMU** 기반 **Kernel DMA Protection** 활성화 | 비인가 외장 장치의 메모리 덤프 차단 |
| 비인증 케이블 사용 시 과전류 발열 | **e-Marker** 미탑재 감지 시 **60W(3A)** 이하로 전류 제한 | 포트 손상 방지 및 기기 보호 |
| 고속 신호 전송 시 긴 케이블 감쇄 | 케이블 내부 **액티브 리타이머(Retimer)** IC 실장 | 신호 지터 제거 및 최대 대역폭 유지 |

#### 한줄 요약
- 실무에서는 IOMMU로 악성 DMA를 차단하고, e-Marker로 전류를 제어하며, 액티브 리타이머로 신호 감쇄를 극복한다.

## Ⅶ. 결론

- USB Type-C 단일 폼팩터 상에서 데이터·영상·전력(최대 240W PD) 및 PCIe 패킷 터널링을 통합하는 글로벌 표준 인터커넥트(USB4/**Thunderbolt 4/5**)로 확립되었으며, 향후 **PAM3 변조 기반 120Gbps 초고대역폭 전송 및 IOMMU 결합 하드웨어 DMA 보안(Kernel DMA Protection)**이 고성능 모바일·워크스테이션 생태계의 핵심 요건

#### 한줄 요약
- 고속 직렬 인터페이스는 단일 Type-C 포트로 데이터, 영상, 전력을 통합하는 동시에 IOMMU 기반 DMA 격리를 갖추는 것이 필수적이다.
