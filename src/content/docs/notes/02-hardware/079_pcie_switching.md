---
sidebar:
  order: 79
  label: "079. PCIe 스위칭 아키텍처 (PCIe Switching)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "PCIe 스위칭 아키텍처 (PCIe Switching)"
date: "2026-08-26T16:14:00+09:00"
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

- **PCIe 스위치(PCIe Switch)**: 단일 호스트 업스트림 포트(USP)와 다수의 다운스트림 포트(DSP) 간에 TLP 패킷을 비차단(Non-blocking) 크로스바로 라우팅하는 고속 직렬 인터커넥트 스위칭 IC.
- **루트 컴플렉스(Root Complex, RC)**: 호스트 CPU 코어 및 시스템 메인 메모리와 직결되어 전체 PCIe 트리 토폴로지를 총괄 제어하는 최상위 호스트 브리지 서브시스템.

</details>

- 정의/개념: CPU 레인 한계를 확장하고 엔드포인트 간 호스트 DRAM 우회 P2P 직접 통신을 지원하는 **PCIe 스위칭 패브릭 아키텍처**
- 배경/필요성: CPU의 제한된 **물리 레인 수**와 호스트 DRAM 경유로 인한 **I/O 병목** 및 통신 지연시간 폭증 발생

#### 한줄 요약
- PCIe 스위치는 CPU 레인을 수백 레인으로 확장하고 장치 간 호스트 우회 P2P 직결 통신을 제공하는 서버 I/O 패브릭이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **P2P 직접 전송(Peer-to-Peer Transfer)**: 호스트 CPU와 시스템 DRAM을 전혀 거치지 않고, PCIe 스위치 내부 크로스바 패브릭을 통해 엔드포인트 간(GPU $\leftrightarrow$ NVMe SSD)에 데이터를 직접 DMA 전송하는 기술.
- **액세스 제어 서비스(Access Control Services, ACS)**: 가상화(SR-IOV) 환경에서 비인가 P2P 트랜잭션을 하드웨어적으로 차단하고 IOMMU로 강제 리다이렉트하여 VM 간 보안 격리를 강제하는 규격.

</details>

- 대규모 I/O 레인 확장: 단일 호스트 하단에서 최대 96~144레인 이상의 고밀도 **엔드포인트 확장** 지원
- 호스트 우회 초저지연: **P2P 직접 전송**을 통해 호스트 메모리 대역폭 소모를 배제하고 마이크로초 단위 통신 실현
- 하드웨어 가상화 보안 격리: **ACS(Access Control Services)** 보안 통제를 통해 가상 머신 간 불법 DMA 침범 차단

#### 한줄 요약
- 비차단 크로스바로 호스트 우회 P2P 직결 통신을 지원하고 ACS를 통해 가상화 보안 격리를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **업스트림 포트(Upstream Port, USP)**: 루트 컴플렉스(Host CPU) 방향으로 연결되는 PCIe 스위치의 인입 포트.
- **다운스트림 포트(Downstream Port, DSP)**: GPU 가속기, NVMe SSD, SmartNIC 등 말단 엔드포인트 디바이스와 직결되는 PCIe 스위치의 출력 포트 어레이.

</details>

```text
[PCIe 스위칭 패브릭 서버 아키텍처]
├── 호스트 루트 컴플렉스 (Root Complex): Host CPU 및 시스템 DRAM
├── PCIe 스위치 패브릭 (PCIe Switch IC)
│   ├── 업스트림 포트 (USP): Host CPU 연결 포트
│   ├── 스위칭 패브릭 코어: Non-blocking TLP 크로스바 라우팅 엔진
│   ├── ACS 보안 검증 엔진: P2P 권한 검증 및 IOMMU 리다이렉트 통제
│   └── 다운스트림 포트 어레이 (DSP): x4/x8/x16 물리 레인 인터페이스
└── 엔드포인트 디바이스군: GPU 가속기, NVMe SSD, DPU
```

선의 의미: 가지(`├──`, `└──`)는 계층별 하드웨어 소속 및 패킷 스위칭 구조; GPU와 NVMe가 Host CPU를 거치지 않고 스위치 내부 크로스바에서 P2P로 직접 통신함

| 구성요소 | 책임 |
|:---|:---|
| 루트 컴플렉스 | CPU·PCIe 주소 공간의 **최상위 브리지** |
| 업스트림 포트 | 호스트 방향 **TLP 송수신** |
| 스위칭 패브릭 코어 | 주소 기반 **비차단 라우팅** |
| ACS 보안 엔진 | P2P 권한 검증과 **VM 격리** |
| 다운스트림 포트 | 엔드포인트 연결과 **핫플러그** |

#### 한줄 요약
- PCIe 스위칭 시스템은 Root Complex, USP, 비차단 크로스바 코어, ACS 보안 엔진 및 DSP 어레이로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **TLP(Transaction Layer Packet)**: 64비트 주소, 요청자 ID(Requester ID), 태그 및 데이터 페이로드를 포함하는 PCIe 최상위 계층 표준 패킷.

</details>

```text
1. 엔드포인트 GPU가 NVMe SSD 접근을 위한 메모리 읽기 TLP 송출
                      │
                      ▼
2. 스위치 DSP: 수신된 TLP 헤더의 목적지 주소 디코딩
                      │
                      ▼
3. 대상 주소 영역(호스트 메모리 vs 타 엔드포인트) 판정
   ├── [호스트 메모리]: USP를 통해 루트 컴플렉스로 전달
   └── [타 엔드포인트]: ACS 보안 검증 수행
          ├── [P2P 허용]: 스위치 크로스바 P2P 직결 라우팅 후 DSP로 전달
          └── [P2P 차단]: USP로 강제 리다이렉트하여 IOMMU 위반 처리
                      │
                      ▼
4. 완료 데이터(CplD) TLP가 스위치 크로스바를 통해 요청자(GPU)로 전달
                      │
                      ▼
[통신 완료]: TLP 핸드셰이크 완료 및 크레딧 반환
```

분기 결과: 동일 가상화 도메인의 **P2P 트랜잭션**은 호스트 CPU 개입 없이 스위치 내부에서 **직결 라우팅**됨

**동작 원리**

1. 엔드포인트 GPU가 NVMe SSD 접근을 위한 메모리 읽기 TLP 송출
2. 스위치 DSP: 수신된 TLP 헤더의 목적지 주소 디코딩
3. 대상 주소 영역(호스트 메모리 vs 타 엔드포인트) 판정
4. 완료 데이터(CplD) TLP가 스위치 크로스바를 통해 요청자(GPU)로 전달

#### 한줄 요약
- TLP 인입 ➔ 주소 디코딩 ➔ ACS 보안 검증 ➔ 스위칭 패브릭 P2P 직결 라우팅 ➔ 완료 데이터 반환 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **초과 구독(Oversubscription)**: 스위치에 연결된 다운스트림 장치들의 대역폭 총합이 호스트 업스트림 링크 대역폭을 초과하는 구조.

</details>

| 상호연결 토폴로지 | PCIe 스위칭 토폴로지 | PCIe 직접 직결 (Direct Attach) | CXL 스위칭 토폴로지 |
|:---|:---|:---|:---|
| 시스템 확장성 | **단일 스위치당 96~144레인** 확장 | CPU 내장 레인에 엄격 제한 | 수천 개 노드 **메모리 풀링** |
| P2P 통신 특성 | **스위치 내부 P2P 직결** | 루트 컴플렉스 경유 지연 발생 | **캐시 일관성** 공유 지원 |
| 호스트 메모리 부하 | 호스트 DRAM 부하 0 (P2P) | 호스트 버퍼 경유 복사 | 완전 메모리 공간 공유 |
| 주요 적용 분야 | **AI GPU 클러스터**, NVMe JBOF | 단일 GPU 워크스테이션 | 차세대 분산 메모리 풀링 |

#### 한줄 요약
- 고밀도 GPU/NVMe P2P 클러스터에는 PCIe 스위칭이, 단일 워크스테이션에는 직접 직결이, 분산 메모리 풀링에는 CXL 스위칭이 쓰인다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **리타이머(Retimer)**: PCIe Gen5(32GT/s)/Gen6(64GT/s) 초고주파 신호 전송 시 PCB 배선에서 감쇄된 신호를 수신하여 지터를 제거하고 클록을 완전 복원(CDR)하는 액티브 IC.
- **다운스트림 포트 격리(Downstream Port Containment, DPC)**: 특정 엔드포인트에서 치명적 에러 발생 시 해당 포트만 하드웨어로 즉시 차단하여 스위치 전체 다운을 방지하는 안전 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| PCB 배선 길이에 따른 고주파 신호 감쇄 및 링크 다운 | 신호 경로 상에 **PCIe 리타이머(Retimer)** 전진 배치 | 지터 제거 및 Gen5 32GT/s 전송 품질 유지 |
| 다중 GPU 버스트 전송 시 업스트림 링크 대역폭 병목 | **가중치 라운드로빈(WRR)** QoS 및 가상 채널(VC) 적용 | 특정 포트 기아 방지 및 트래픽 공정 분배 |
| 가상화 환경에서 비인가 P2P 무단 메모리 침범 | 스위치 레벨 **ACS(Access Control Services)** 활성화 | 가상 머신 간 무단 DMA 침해 및 메모리 오염 차단 |
| 엔드포인트 핫플러그(Hot-Plug) 시 스위치 링크 순시 리셋 | **DPC(Downstream Port Containment)** 결함 격리 실장 | 불량 장비 국소 차단 및 전체 시스템 가동 유지 |

#### 한줄 요약
- 실무에서는 리타이머로 신호를 복원하고, ACS로 가상화를 격리하며, DPC로 핫플러그 결함을 차단한다.

## Ⅶ. 결론

- 다중 장치 P2P는 **PCIe 스위치**, 단일 장치는 **직접 연결** 선택

#### 한줄 요약
- PCIe 스위칭은 호스트 우회 P2P 직결과 대규모 레인 확장을 가능하게 하는 현대 고성능 AI 서버의 핵심 패브릭이다.
