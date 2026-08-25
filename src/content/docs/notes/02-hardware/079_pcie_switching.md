---
sidebar:
  order: 79
  label: "079. PCIe 스위칭 아키텍처 (PCIe Switching)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "PCIe 스위칭 아키텍처 (PCIe Switching)"
date: "2026-08-25T10:25:00+09:00"
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

- **PCIe 스위치(PCIe Switch)**: 단일 업스트림 포트와 다수의 다운스트림 포트 간에 TLP 패킷을 비차단(Non-blocking) 라우팅하는 패브릭 IC.
- **루트 컴플렉스(Root Complex)**: CPU 및 메인 메모리와 직결되어 전체 PCIe 계층 구조를 총괄 제어하는 최상위 호스트 브리지.

</details>

- 정의/개념: CPU PCIe 레인 수를 확장하고 엔드포인트 간 TLP 패킷 라우팅 및 P2P 직접 통신을 지원하는 **PCIe 스위칭** 기술
- 배경/필요성: 고밀도 AI 서버에서 **CPU PCIe 레인 수 한계 및 호스트 메모리 경유 지연시간 폭증 해결 불가**

#### 한줄 요약
- PCIe 스위치는 CPU 레인을 확장하고 장치 간 호스트 우회 P2P 직결 통신을 제공한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **P2P 전송(Peer-to-Peer Transfer)**: 호스트 CPU와 DRAM을 거치지 않고 PCIe 스위치 패브릭을 통해 엔드포인트 간(GPU $\leftrightarrow$ NVMe SSD)에 데이터를 직접 DMA 전송하는 기술.
- **ACS(Access Control Services)**: 가상화 환경에서 비인가 P2P 트랜잭션을 차단하고 IOMMU로 강제 리다이렉트하는 보안 제어 규격.

</details>

- 단일 호스트 하단에서 최대 144레인 이상의 고밀도 엔드포인트 확장
- CPU 개입 없는 **P2P 전송**을 통해 호스트 메모리 대역폭 절약 및 초저지연 실현
- **ACS(Access Control Services)** 보안 통제를 통한 가상 머신 간 DMA 불법 접근 차단

#### 한줄 요약
- 비차단 스위칭으로 P2P 직결 통신을 지원하고 ACS를 통해 가상화 보안 격리를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **USP(Upstream Port)**: 루트 컴플렉스(CPU) 방향으로 연결되는 스위치의 입력 포트.
- **DSP(Downstream Port)**: GPU, NVMe SSD, NIC 등 말단 엔드포인트로 연결되는 스위치의 출력 포트.

</details>

```text
[PCIe 스위칭 패브릭 아키텍처]
|-- 루트 컴플렉스 (Root Complex - CPU 및 Host DRAM)
|-- PCIe 스위치 패브릭 (Switch IC)
|   |-- 업스트림 포트 (USP - Host CPU 연결)
|   |-- 스위칭 패브릭 코어 (TLP 주소 디코딩 및 크로스바 라우팅)
|   |-- ACS 보안 검증 엔진 (P2P 권한 검증 및 IOMMU 리다이렉트)
|   `-- 다운스트림 포트 어레이 (DSP 1~N)
`-- 엔드포인트 디바이스 (GPU·NPU 가속기 및 NVMe SSD 어레이)
```

선의 의미: 계층 및 패킷 스위칭 구조

| 구성요소 | 책임 |
|:---|:---|
| 루트 컴플렉스 | CPU 메모리 공간과 PCIe 공간을 브리징하고 시스템 초기화 수행 |
| **업스트림 포트(USP)** | 호스트 CPU 방향으로 TLP 패킷을 송수신하는 스위치 인입 포트 |
| **스위칭 패브릭 코어** | TLP 헤더의 64비트 주소를 디코딩하여 대상 DSP로 비차단 라우팅 |
| ACS 보안 엔진 | P2P 트랜잭션의 적법성을 검증하여 가상 도메인 간 침해 차단 |
| **다운스트림 포트(DSP)** | GPU, SSD 등 개별 엔드포인트와 물리 레인(x4, x8, x16) 직결 |

#### 한줄 요약
- Root Complex, USP, 크로스바 스위칭 패브릭, ACS 엔진, DSP가 통합되어 대규모 I/O 망을 이룬다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **TLP(Transaction Layer Packet)**: 주소 기반 읽기/쓰기 및 메시지를 전달하는 PCIe 최상위 계층 패킷.

</details>

```text
엔드포인트 GPU가 NVMe SSD로 메모리 읽기 TLP 송출
        │
   스위치 DSP 1이 TLP 헤더의 목적지 주소를 디코딩
        │
   목적지가 호스트 메모리인가, 타 엔드포인트인가?
   ┌────┴─────┐
[호스트 메모리]   [타 엔드포인트 (P2P)]
   │             │
USP를 통해      ACS(Access Control Services) 보안 검증 수행
루트 컴플렉스     ┌──┴───┐
전송            [허용]   [차단/미인가]
   │             │        │
   │        스위칭 패브릭  USP로 강제 리다이렉트
   │        크로스바 직결   (IOMMU 위반 처리)
   │             │        │
   │        DSP 2(NVMe)로 └───────┐
   │        직접 DMA 패킷 전송     │
   └────┬────────┴────────────────┘
        │
   완료 응답(CplD) TLP를 원래 요청자(GPU)로 역방향 반환
```

#### 한줄 요약
- TLP 인입 → 주소 디코딩 → ACS 보안 검증 → 스위칭 패브릭 P2P 직결 라우팅 → 완료 응답 반환 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **초과 구독(Oversubscription)**: 다운스트림 엔드포인트들의 총 대역폭 합계가 업스트림 호스트 링크 대역폭을 초과하는 상태.

</details>

| 연결 구조 | PCIe 스위칭 토폴로지 | PCIe 직접 직결 (Direct Attach) | CXL 스위칭 토폴로지 |
|:---|:---|:---|:---|
| 확장성 | 단일 스위치 96~144 레인 확장 | CPU 내장 레인(64~128)에 엄격 제한 | 수천 개 노드 메모리 풀링 확장 |
| P2P 통신 특성 | 스위치 내부 P2P 직결 (CPU 개입 0) | 루트 컴플렉스 경유 지연 발생 | 캐시 일관성(CXL.cache/mem) 공유 |
| 한계점 | 업스트림 초과 구독 및 홉 지연 | 장치 수 확장 한계 및 AI 클러스터링 불가 | 칩셋 단가 및 CXL 3.0 인프라 성숙도 |

#### 한줄 요약
- 고밀도 GPU/NVMe P2P 클러스터에는 PCIe 스위칭이, 초저지연 단일 장비에는 직접 직결이 쓰인다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **리타이머(Retimer)**: PCIe Gen5/Gen6 초고속 신호의 감쇄 및 지터를 제거하고 신호를 완전 복원(CDR)하는 액티브 IC 소자.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 다중 GPU 동시 버스트로 업스트림 초과 구독 병목 | 가중치 기반 라운드로빈(WRR) QoS 및 가상 채널(VC) 적용 | 특정 포트 기아 방지 및 트래픽 공정 분배 |
| 긴 PCB 배선 신호 감쇄로 링크 다운트레이닝 발생 | 신호 경로에 **PCIe 리타이머(Retimer)** 전진 배치 | 지터 제거 및 Gen5 32GT/s 최대 링크 속도 유지 |
| 가상화(SR-IOV) 환경에서 비인가 P2P 무단 침범 | 스위치 레벨 **ACS 활성화** 및 IOMMU 주소 격리 | VM 간 무단 DMA 침해 및 메모리 오염 원천 차단 |
| 핫플러그(Hot-Plug) 시 스위치 링크 순시 리셋 | DPC(Downstream Port Containment) 에러 격리 적용 | 불량 장비만 국소 차단 및 전체 시스템 가동 유지 |

#### 한줄 요약
- QoS 트래픽 중재, 리타이머 신호 복원, ACS 가상화 격리, DPC 핫플러그 안전성을 확보한다.

## Ⅶ. 결론

- AI 가속 서버 및 NVMe 스토리지 어레이는 **PCIe Gen5/Gen6 스위칭 패브릭**을 구축하고, **ACS 보안 및 CXL 스위칭**으로 확장하여 초저지연 인프라 완성

#### 한줄 요약
- PCIe 스위칭은 호스트 우회 P2P 직결과 대규모 레인 확장을 가능하게 하는 현대 고성능 AI 서버의 핵심 패브릭이다.