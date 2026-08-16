---
sidebar:
  order: 36
  label: "036. 5G 서비스 eMBB•URLLC•mMTC"
  badge: { text: "기출 • 30%", variant: note }
title: "5G 서비스 eMBB•URLLC•mMTC"
date: "2026-08-13T16:48:00+09:00"
tags: ["notes-network"]
weight: 36
extra:
  question_no: "036"
  source_status: "기출"
  source_history: "128회"
  priority: 30
  priority_note: "128회 출제"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **5세대 이동통신 서비스 유형(5G Service Types)**: ITU-R M.2083 표준에서 정의한 요구 성능 지표(대용량 속도, 극저지연, 대규모 접속)별 5G 핵심 서비스 분류 체계이다.
- **초고속 이동통신(Enhanced Mobile Broadband, eMBB)**: 대용량 데이터 전송과 사용자 체감 속도 극대화를 목표로 하는 5G 서비스 유형이다.
- **초신뢰 저지연 통신(Ultra-Reliable and Low-Latency Communications, URLLC)**: 99.999% 신뢰도와 1ms 이하의 극저지연 전송을 목표로 하는 5G 서비스 유형이다.
- **초고밀도 가공형 통신(Massive Machine-Type Communications, mMTC)**: 단위 면적당 수십만 개 이상의 저전력 IoT 단말 접속 수용을 목표로 하는 5G 서비스 유형이다.

</details>

- 정의/개념: **5G 서비스 유형(eMBB·URLLC·mMTC)**은 ITU-R 표준 규격에 따라 초고속 전송(eMBB), 극저지연 및 초신뢰(URLLC), 대규모 저전력 단말 수용(mMTC) 특성별로 네트워크 자원을 맞춤형 할당하는 5G 3대 서비스 기술 체계이다.
- 배경/필요성: 단일 무선 네트워크 품질 정책으로는 UHD 영상, 자율주행 제어, 스마트시티 센서 등 극단적으로 다변화된 산업별 요구 성능(KPI)을 동시에 충족시킬 수 없는 한계를 극복하기 위해 도입되었다.

#### 한줄 요약

- 서비스 요구사항에 맞춰 대용량 속도(eMBB), 극저지연·초신뢰성(URLLC), 대규모 소용량 단말 접속(mMTC) 자원을 특화하여 제공하는 5G 3대 서비스 기술.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **서비스 품질(Quality of Service, QoS)**: 응용별 요구사항에 맞춰 전송 속도, 패킷 손실률, 지연 시간, 우선순위를 차등 제어하는 서비스 품질 체계이다.
- **사용자 평면 기능(User Plane Function, UPF)**: 5G 코어 아키텍처에서 사용자 패킷의 캡슐화, 라우팅, 모바일 에지 컴퓨팅(MEC) 데이터 분기를 담당하는 핵심 엔티티이다.

</details>

- **eMBB (초고속·대용량)**: 3.5GHz/28GHz 광대역 주파수, Massive MIMO 및 Beamforming 기술을 결합하여 최고 20Gbps급 초고속 전송 성능을 제공한다.
- **URLLC (초저지연·초신뢰)**: 짧은 무선 전송 주기(Short TTI), 미니슬롯(Mini-slot) 할당 및 Edge UPF 전진 배치를 통해 무선 지연 1ms 이하 및 99.999% 패킷 전달 성공률을 달성한다.
- **mMTC (대규모 단말 접속)**: Narrowband-IoT/LTE-M 연동, 절전 모드(PSM/eDRX) 기법을 통해 km²당 100만 개 단말 수용 및 10년 이상의 배터리 수명을 보장한다.

#### 한줄 요약

- 대용량 처리량, 초저지연·신뢰성, 대규모 접속 밀도 등 응용 분야별 KPI 목표에 맞춰 무선 및 코어 자원을 상호 독립적으로 최적화.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **5세대 이동통신(Fifth-Generation Mobile Communication, 5G)**: 초고속, 초저지연, 초연결 성능을 기반으로 산업 네트워크를 아우르는 차세대 이동통신 표준 규격이다.

</details>

```text
5G 서비스 자원 아키텍처
└─ 서비스 요구 프로필 (Service Profile)
   └─ 서비스 품질 정책 제어 (QoS Policy Control)
      ├─ 무선 자원 제어 (Radio Resource Management, RRM)
      └─ 전송망 경로 제어 (Transport Path Control)
         └─ 사용자 평면 기능 (User Plane Function, UPF)
```

선의 의미: 산업별 서비스 프로필 요구사항이 QoS 정책 통제하에 무선 자원 관리(RRM) 및 UPF 데이터 전달 경로와 상호 작용하는 아키텍처 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| 서비스 요구 프로필 | 서비스별 최우선 KPI(전송속도, 종단지연, 접속밀도) 정의 및 전달 |
| QoS 정책 제어 | 5QI(5G QoS Identifier) 식별자를 기반으로 트래픽 흐름 우선순위 및 자원 격리 정의 |
| 무선 자원 제어(RRM) | 서비스 프로필에 따라 서브캐리어 스페이싱, Short TTI, Beamforming 등 무선 파라미터 배정 |
| 전송망 경로 제어 | 백홀/프론트홀 전송망의 제어 플레인 및 슬라이싱 라우팅 경로 제어 |
| 사용자 평면 기능(UPF) | 세션 관리 기능(SMF)의 통제를 받아 사용자 트래픽을 최적의 MEC 또는 인터넷망으로 라우팅 |

#### 한줄 요약

- 서비스 프로필 요구사항이 QoS 제어를 통해 무선 자원 배정 및 UPF 데이터 전달 경로로 통합 매핑되는 구조.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **QoS 정책(Quality of Service Policy, QoS Policy)**: 트래픽 특성별 차등화된 서비스 레벨(5QI)을 지정하여 자원 할당 및 패킷 우선순위를 결정하는 정책 체계이다.
- **모바일 에지 컴퓨팅(Mobile Edge Computing, MEC)**: 코어망으로의 트래픽 이동 없이 기지국 단말 인근에서 데이터를 즉시 처리하여 극저지연을 실현하는 에지 컴퓨팅 기술이다.

</details>

```text
1. 서비스 요구사항 판정 및 분류 (eMBB / URLLC / mMTC)
          │
          ▼
2. 서비스 품질 정책 및 슬라이스 프로파일 결정 (QoS / Network Slice Selection)
          │
          ▼
3. 무선 및 전송망 자원 최적 할당 (RRM / Subcarrier & Mini-Slot Assignment)
          │
          ▼
4. 사용자 평면 기능 및 모바일 에지 컴퓨팅 전진 배치 (UPF & MEC Path Setup)
          │
          ▼
5. 엔드투엔드 서비스 품질 모니터링 및 실시간 자원 피드백 (KPI Monitoring)
```

### 동작 원리

1. 서비스 요구사항 판정 및 분류: 데이터 전송 요구 특성을 분석하여 eMBB, URLLC, mMTC 중 적합한 서비스 클래스를 지정한다.
2. 서비스 품질 정책 및 슬라이스 프로파일 결정: 5QI 매핑
3. 무선 및 전송망 자원 최적 할당: 서비스별 자원 배정
4. 사용자 평면 기능 및 모바일 에지 컴퓨팅 전진 배치: 경로 구성
5. 엔드투엔드 서비스 품질 모니터링 및 실시간 자원 피드백: KPI 조정

#### 한줄 요약

- 서비스 분류부터 QoS 설정, 자원 할당, UPF·MEC 전진 배치 및 KPI 모니터링으로 이어지는 엔드투엔드 슬라이싱 흐름.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **처리량(Throughput)**: 단위 시간당 네트워크를 거쳐 성공적으로 전송되는 데이터 양의 크기이다.
- **접속 밀도(Connection Density)**: 단위 면적(km²) 당 네트워크 접속을 유지하며 데이터 전송을 수행할 수 있는 최대 단말 수이다.

</details>

| 비교 항목 | **eMBB (Enhanced Mobile Broadband)** | **URLLC (Ultra-Reliable & Low-Latency)** | **mMTC (Massive Machine-Type Comms)** |
|:---|:---|:---|:---|
| 목표 KPI | 최고 속도 20Gbps, 체감 속도 100Mbps | 신뢰도 99.999%, 무선 지연 1ms 이하 | 접속 밀도 1,000,000 devices/km² |
| 주요 응용 | 4K/8K UHD, AR/VR, 홀로그램 서비스 | 자율주행, 원격 의료 수술, 스마트 공장 | 스마트 그리드, 스마트시티 센서, 원격 검침 |
| 핵심 무선 기술 | 광대역 주파수, Massive MIMO, Beamforming | Short TTI, Mini-slot, Grant-free 전송 | NB-IoT, eDRX, PSM, Narrowband 주파수 |
| 네트워크 관건 | 광대역 대역폭 확보 및 백본 유선 처리량 | Edge UPF/MEC 배치 및 E2E 지연 예산 관리 | 제어 채널 Paging 수용 및 단말 전력 절감 |

> 요약: 초고용량 전송은 eMBB, 실시간 안전 제어는 URLLC, 초대규모 IoT 접속은 mMTC 기술 적용.

#### 한줄 요약

- eMBB는 초고속 대용량, URLLC는 초저지연·초신뢰성, mMTC는 초대규모 저전력 단말 접속을 목표로 자원 분화.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **서비스 수준 협약(Service Level Agreement, SLA)**: 발주자와 사업자 간 합의된 네트워크 처리량, 지연 시간, 가용성 보장 계약 수치이다.
- **종단 지연 예산(End-to-End Latency Budget, E2E Latency Budget)**: 전체 시스템 허용 지연 시간을 무선 구간, 전송 구간, 애플리케이션 처리 구간으로 분할 할당한 관리 기준이다.

</details>

| 문제점 | 발생 이유 | 실무 대응 대책 | 기대 효과 |
|:---|:---|:---|:---|
| 자원 충돌 및 SLA 위반 | eMBB 대용량 트래픽이 URLLC 대역 수용 침범 | 5G Network Slicing 기반 자원 완전 물리/논리 격리 | 서비스별 독립적 SLA 보장 및 자원 interference 방지 |
| URLLC 지연 예산 초과 | 코어망 라우팅 지연 및 백홀 전송 병목 발생 | UPF 및 MEC 기지국 인근 전진 배치(Edge Offloading) | 엔드투엔드 반응 지연 시간 1ms 내 달성 |
| mMTC 제어 채널 폭주 | 수십만 개 IoT 단말의 동시 접속 시도 | 3GPP Paging Throttle 및 eDRX/PSM 최적화 | 제어 평면 과부하 예방 |
| 서비스 간 자원 효율 저하 | 고정 자원 할당으로 인한 비활성 시간 자원 낭비 | AI/ML 기반 동적 자원 스케줄링(Dynamic Slicing) 적용 | 망 운용 효율성 향상 및 자원 활용률 극대화 |

#### 한줄 요약

- SLA 기반 QoS 파라미터 설계, MEC 전진 배치를 통한 E2E 지연 예산 준수, 네트워크 슬라이싱 적용으로 5G 서비스 품질 확보.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **최우선 품질 지표(Key Performance Indicator, KPI)**: 네트워크 구축 시 서비스의 성공 기준이 되는 최우선 품질 지표(처리량, 지연시간, 접속밀도)이다.

</details>

- 처리량은 **eMBB**, 실시간 제어는 **URLLC**, 센서는 **mMTC** 선택

#### 한줄 요약

- 서비스별 요구 KPI 기반 네트워크 자원 분화 및 모바일 에지 컴퓨팅 기반 초저지연 제어 체계 구현 필수.
