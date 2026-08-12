---
sidebar:
  order: 69
  label: "069. PDH•SDH•SONET 디지털 계위 (PDH SDH SONET)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "PDH•SDH•SONET 디지털 계위 (PDH SDH SONET)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-network"
weight: 69
extra:
  question_no: "069"
  source_status: "기출"
  source_history: "134회"
  priority: 30
  priority_note: "비교형: 134회 PDH•SDH•SONET 서술"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **준동기식 디지털 계위(Plesiochronous Digital Hierarchy, PDH)**: 독립적인 국부 클럭(Local Clock)을 사용하여 신호 전송 속도 편차를 비트 채움(Bit Stuffing) 방식으로 흡수 및 단계별 다단 다중화하는 1세대 디지털 전송 계위이다.
- **동기식 디지털 계위(Synchronous Digital Hierarchy, SDH)**: 망 전체에 단일 절대 세슘 마스터 클럭(Network Synchronization)을 공급하여, 포인터(Pointer)와 STM 프레임 기반으로 하위 신호를 직접 분기·결합(Add-Drop)하는 ITU-T 국제 표준 광전송 계위이다.
- **동기식 광 네트워크(Synchronous Optical Network, SONET)**: ANSI 북미 전송 표준으로, 51.84Mbps의 기본 STS-1/OC-1 속도를 기준으로 동기 페이로드 봉투(SPE) 구조를 적용하여 다중화하는 광 네트워크 규격이다.

</details>

- 정의/개념: **PDH**, **SDH**, **SONET**은 광통신 및 유선 기간망에서 저속의 T1/E1 신호들을 대용량 백본 계위(Gbps)로 다중화(Multiplexing)하고 정밀 프레임 포맷 및 OAM 관리 오버헤드를 규정하는 디지털 시분할 전송 계위(TDM Hierarchy) 표준들이다.
- 배경/필요성: 기존 **PDH**는 다단 다중화(Multiplexing Hierarchy) 구조로 인해 중간의 64Kbps/E1 신호를 인출하기 위해 전체 대용량 프레임을 완전 역다중화(Demux)해야 하는 비효율성과 벤더 간 호환성 부재를 겪었으며, 이를 해결하기 위해 절대 동기 프레임 기반 **SDH/SONET**이 도입되었다.

#### 한줄 요약

- 망 전체 절대 클럭 동기화와 포인터 기반 직접 분기결합(Add-Drop)을 구현하는 디지털 광전송 계위 체계 적용.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **비트 채움(Bit Stuffing / Positive Stuffing)**: PDH 각 수발신 장치 간 국부 클럭의 미세한 주파수 편차를 흡수하기 위해 비유효 다미 비트를 인위적으로 끼워 넣어 프레임 속도를 맞추는 기술이다.
- **포인터(Pointer)**: SDH/SONET 동기 프레임 헤더 영역에서 페이로드(VC/SPE)의 실제 시작 바이트 위치를 동적으로 지시하여, 클럭 위상 변동 수용 및 직접 분기결합을 가능케 하는 바이트 지표이다.
- **운용·관리·유지보수(Operations, Administration and Maintenance, OAM)**: 전송 프레임의 섹션/경로 오버헤드(Overhead) 영역을 활용하여 비트 오류(BIP-8), 경로 추적 및 자동 보호 절체(APS)를 지능적으로 수행하는 네트워크 관리 체계이다.

</details>

- **PDH**는 클럭 편차를 **비트 채움**으로 수용하여 중간 회선 인출 시 복잡한 다단 역다중화(Demux Chain)가 필요하다.
- **SDH/SONET**은 절대 망 동기 상태에서 **포인터**(Pointer) 기법을 사용하여, 다중화 프레임을 해체하지 않고도 특정 하위 채널(E1/DS3 등)을 1-Step으로 직접 **분기결합**(Add-Drop)한다.
- 프레임 헤더 전면에 충분한 **OAM** 전용 바이트(SOH/POH)를 할당하여 50ms 이내의 자동 보호 절체(APS) 및 종단 간 원격 모니터링 체계를 보장한다.

#### 한줄 요약

- 포인터 기법을 활용한 Direct Add-Drop 및 SOH/POH 기반 OAM 50ms 미만 자동 보호 절체 원칙 준수.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **가상 컨테이너(Virtual Container, VC)**: SDH에서 하위 저속 신호(C-12, C-3, C-4 등)에 경로 오버헤드(POH)를 결합하여 프레임 내부에서 독립 관리되는 논리적 수용 단위(e.g. VC-12, VC-4)이다.
- **동기 페이로드 봉투(Synchronous Payload Envelope, SPE)**: SONET에서 사용자 데이터 페이로드와 POH를 포함하여 STS-1 프레임 내부를 부유(Floating)하는 실물 데이터 영역이다.
- **동기 전송 모듈(Synchronous Transport Module, STM)**: SDH의 기본 광 전송 프레임 단위로, STM-1(155.52 Mbps)을 기본 단위로 4배수($N=4, 16, 64, 256$) 확장(STM-4: 622M, STM-16: 2.5G, STM-64: 10G)된다.
- **동기 전송 신호(Synchronous Transport Signal, STS)**: SONET의 기본 전기적 신호 단위(STS-1: 51.84 Mbps, STS-3: 155.52 Mbps)이다.
- **광 반송파(Optical Carrier, OC)**: SONET의 광파장 물리 신호 계위로 OC-3(155.52M), OC-12(622M), OC-48(2.5G), OC-192(10G)로 맵핑된다.
- **분기결합 다중화기(Add-Drop Multiplexer, ADM)**: 통신 링(Ring) 상에서 상위 STM/OC 광 신호로부터 원하는 저속 신호만을 직접 빼내거나(Drop) 보충 주입(Add)하는 전송 장비이다.
- **디지털 교차 연결기(Digital Cross-Connect, DXC)**: 대규모 전송 국사에서 다수의 STM/OC 신호 간 VC 단위 경로를 전자적으로 수용 및 스위칭 재배치하는 핵심 제어 노드이다.

</details>

- 하위 신호는 **VC** 및 **SPE** 구조로 캡슐화되고, **STM** (SDH) 및 **STS/OC** (SONET) 프레임 오버헤드와 결합되어 전송된다.
- 광 전송 링 노드에 **ADM** 및 **DXC** 장비를 배치하여 고속 트래픽의 유연한 회선 스위칭과 망 장애 수복을 제어한다.

```text
[하위 T1/E1 신호] ──► [Container (C-12/C-4)] ──► [VC / SPE 매핑 + POH]
                                                         │
[STM-N / OC-N 광신호] ◄── [ADM / DXC 분기] ◄── [STM-1 / STS-1 프레임 + SOH + Pointer] ◄┘
```

| 구성요소 | 역할 및 핵심 기능 |
|:---|:---|
| **가상 컨테이너 (VC / SPE)** | 하위 클럭 신호를 정형화하고 종단 간 관리를 위한 경로 오버헤드(POH) 부가 수용 |
| **포인터 (Pointer)** | 프레임 내 VC/SPE의 시작 위치 바이트 주소를 실시간 추적 지시 |
| **구간 오버헤드 (Section/Line Overhead, SOH)** | RSOH/MSOH 영역을 통해 노드 간 프레임 동기, BIP-8 오류 감시, APS 절체 제어 |
| **분기결합 다중화기 (ADM)** | 링 토폴로지 상에서 프레임 풀 해체 없이 특정 VC 채널의 Add/Drop 수행 |
| **디지털 교차연결기 (DXC)** | 국사 대용량 광선로 간 VC-12/VC-4 단위의 전자적 Cross-Connect 회선 재배치 |

#### 한줄 요약

- VC/SPE 하위 매핑과 포인터 연산, SOH/POH 오버헤드 및 ADM/DXC 노드 기반 통합 전송 구조 적용.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **신호 매퍼(Signal Mapper)**: PDH, 이더넷, ATM 등 다양한 하위 사용자 신호를 규격화된 가상 컨테이너(VC-12/VC-3/VC-4)에 수용 매핑하는 변환기이다.
- **경로 오버헤드(Path Overhead, POH)**: VC/SPE 신호가 생성되는 지점부터 최종 해제되는 수신 노드까지 유지되며 End-to-End 품질과 오류를 추적하는 헤더이다.
- **보호 절체(Protection Switching)**: 주 회선(Working Path)의 광케이블 절단 시 예비 회선(Protection Path)으로 50ms 이내에 회선 경로를 즉각 우회시키는 고가용성 기술이다.
- **VC·SPE 매핑(VC/SPE Mapping)**: 하위 데이터를 표준 규격 가상 컨테이너로 패킹하는 단계이다.
- **포인터 위치 조정(Pointer Adjustment)**: 클럭 위상 오차 발생 시 포인터 바이트 값을 증가/감소(Positive/Negative Stuffing) 조정하는 단계이다.
- **동기 프레임 전송(Synchronous Frame Transmission)**: SOH를 결합하여 STM-N / OC-N 광파형으로 송출하는 단계이다.
- **오류·품질 감시(Error & Quality Monitoring)**: BIP-8 parity 오버헤드를 연산하여 회선 훼손을 실시간 진단하는 단계이다.
- **경로 처리 지시(Path Action Instruction)**: 정상 트래픽 분기결합 또는 링 장애 시 APS 절체를 집행하는 단계이다.

</details>

```text
하위 PDH / Ethernet 데이터 주입 (PDH/Ethernet Ingress)
      │
      ▼
1. 가상 컨테이너 VC/SPE 캡슐화 & POH 결합 (VC/SPE Mapping & POH Insertion)
      │
      ▼
2. 절대 망동기 기준 포인터(Pointer) 주소 설정 (Pointer Address Assignment)
      │
      ▼
3. SOH 오버헤드 결합 및 STM-N / OC-N 광송출 (SOH Insertion & Optical Tx)
      │
      ▼
4. ADM 노드 상에서 SOH/POH 기반 BIP-8 오류 감시 (OAM & Quality Monitoring)
      ├─ [정상] 5. ADM Direct Add-Drop 분기결합 수행
      └─ [선로 절단 장애] 5. 50ms 이내 MS-SPRING / UPSR 자동 보호 절체 (APS Switching)
```

### 동작 원리

1. **VC·SPE 매핑**: **신호 매퍼**가 저속 회선 데이터를 가져와 **경로 오버헤드**(POH)와 함께 **VC/SPE** 컨테이너에 매핑한다.
2. **포인터 위치 조정**: 망 절대 클럭과의 미세 지터 편차를 **포인터** 바이트 증가/감소 연산으로 정밀 보정한다.
3. **동기 프레임 전송**: 재생기 오버헤드(RSOH) 및 다중화기 오버헤드(MSOH)를 통합하여 **STM-N/OC-N** 광 신호로 전송한다.
4. **오류·품질 감시**: **ADM** 및 **DXC** 전송 노드가 SOH의 BIP-8 바이트를 검증하여 품질 저하 및 단선 여부를 진단한다.
5. **경로 처리 지시**: 정상 시 특정 VC를 **Add-Drop** 하고, 선로 장애 감지 시 50ms 이내 **보호 절체**(APS)를 발동한다.

#### 한줄 요약

- VC 매핑 및 포인터 지시 연산, SOH 품질 모니터링과 50ms 이내 APS 보호 절체 프로세스 준수.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **상호 연동(Interworking)**: ANSI 속도 체계(SONET OC-n)와 ITU-T 속도 체계(SDH STM-n) 및 기존 PDH E1/T1 회선 간의 상호 매핑 변환 통신 연동 기술이다.

</details>

- **PDH**는 미세 속도 차이를 비트 채움으로 처리하여 다단 역다중화가 불가피하다.
- **SDH**와 **SONET**은 절대 망 동기 상에서 포인터를 활용하여 특정 하위 신호를 1-Step으로 분기결합하고 강력한 OAM 인프라를 제공한다.

| 비교 항목 | PDH (Plesiochronous) | SDH (Synchronous - ITU-T) | SONET (Synchronous - ANSI) |
|:---|:---|:---|:---|
| **동기 방식** | 개별 국부 클럭 (비트 채움 기술) | 망 전체 절대 세슘 마스터 클럭 동기 | 망 전체 절대 세슘 마스터 클럭 동기 |
| **기본 프레임 속도** | 이원화 (북미 DS1: 1.544M / 유럽 E1: 2.048M) | **STM-1** (155.52 Mbps) 기본 | **STS-1 / OC-1** (51.84 Mbps) 기본 |
| **하위 신호 추출** | 다단 역다중화 (Demux Chain) 필수 | **포인터** 기법 기반 Direct Add-Drop | **포인터** 기법 기반 Direct Add-Drop |
| **OAM & 절체 성능** | 미흡 (오버헤드 최소화 구조) | **강력** (SOH/POH 지원, 50ms APS 절체) | **강력** (SOH/POH 지원, 50ms APS 절체) |
| **벤더/지역 호환성** | 벤더 및 지역 간 호환 불능 | 국제 표준 준수로 완전 호환 | 북미 표준 준수로 완전 호환 |

> 요약: 레거시 개별 회선에는 **PDH**, 글로벌 광 전송 백본 망 구축에는 **SDH**, 북미 계위 백본 및 국사 연동에는 **SONET** 표준을 채택한다.

#### 한줄 요약

- PDH 비트 채움 방식과 SDH/SONET의 절대 동기, 포인터 기반 Direct Add-Drop 계위 특성 비교 모델 수용.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **지터(Jitter)**: 전송 노드의 포인터 조정(Pointer Adjustment) 연산 시 발생하는 디지털 신호 에지의 미세한 타이밍 흔들림 현상이다.
- **클럭 품질(Clock Quality)**: 망동기(Network Sync) 제공 장치(SSU/PRC)의 주파수 정확도로, 품질 저하 시 포인터 조정 폭증 및 지터 훼손이 발생한다.

</details>

| 실무 문제점 | 발생 원인 | 해결 대책 | 기대 효과 |
|:---|:---|:---|:---|
| **포인터 지터 폭증** | **클럭 품질** 저하 및 주파수 동기 이탈로 Pointer Adjustment 빈번 | Primary Reference Clock (PRC 세슘) 마스터 동기 강화 및 De-jitter 버퍼 적용 | 디지털 신호 지터 억제 및 무손실 transmission 구현 |
| **이종 계위 연동 오류** | 북미 SONET(OC-3)과 유럽 SDH(STM-1) 간 페이로드 매핑 불일치 | **상호 연동**(Interworking) 매퍼(VC-3/VC-4 Gateway) 교차 설정 | 북미-유럽 간 국가 광 백본 상호운용성 완전 확보 |
| **보호 절체 실패** | 링 토폴로지 상에서 APS 패킷 미동기 또는 예비 선로 수용량 부족 | Dual Ring(MS-SPRING) 50ms **보호 절체** 주기적 시뮬레이션 및 예비 선로 점유율 관리 | 케이블 절단 장애 시 서비스 무단절 50ms 복구 달성 |
| **레거시 TDM 수용** | 광 백본 패킷망(IP/MPLS) 전환 시 기존 SDH E1/DS3 회선 수용 필요 | Circuit Emulation Service (CESoPSN / SAToP) 기술 연동 | 기존 SDH/PDH 전송 자산 보호 및 유연한 패킷망 이관 |

#### 한줄 요약

- PRC 세슘 망동기 강화, 포인터 지터 수용 버퍼링, 50ms APS 절체 검증 및 CESoPSN 이관을 통한 광전송망 가동성 확보 체계 구축.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **전송 계위 선택(Transmission Hierarchy Selection)**: 전송 회선의 규모, 망 동기화 요구 수준, OAM 제어성 및 국제 호환성을 다각도로 검토하여 PDH, SDH, SONET, WDM/OTN 기술을 선정하는 의사결정 체계이다.

</details>

- 유선 전송 망 수립 시 **전송 계위 선택** 기준을 체계화하여, 기존 회선 수용에는 **PDH**, 글로벌 대용량 동기 백본에는 **SDH/SONET**, 향후 초고속 백본에는 DWDM 연동 OTN(Optical Transport Network) 기술을 유연하게 수용하는 차세대 광전송 인프라 구축 체계 적용.

#### 한줄 요약

- 망 절대 동기화 및 포인터 기반 Direct Add-Drop, SOH OAM 절체 성능을 결합한 차세대 SDH/SONET 광전송 아키텍처 구현 필수.
