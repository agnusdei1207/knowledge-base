---
sidebar:
  order: 37
  label: "037. 5G SA와 NSA"
  badge:
    text: "기출 · 70%"
    variant: note
title: "5G SA(독립형)와 NSA(비독립형) (5G SA vs NSA)"
date: "2026-08-26T13:46:19+09:00"
tags:
  - "notes-network"
weight: 37
extra:
  question_no: "37"
  source_status: "기출"
  source_history: "135회"
  priority: 70
  priority_note: "Option 3x(NSA) vs Option 2(SA) 비교 및 EPS Fallback/VoNR"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **5G NSA (Non-Standalone, 비독립형)**: 기존 4G 코어(EPC)와 기지국(eNB)을 제어 앵커로 활용하고 5G gNB를 데이터 전송에 결합하는 방식 (Option 3x).
- **5G SA (Standalone, 독립형)**: 5G 전용 코어망(5GC)과 5G 기지국(gNB)만으로 제어와 데이터를 단독 처리하는 순수 5G E2E 아키텍처 (Option 2).

</details>

- 정의/개념: 4G 인프라를 연동해 조기 상용화하는 **NSA(Option 3x)**와 5GC/gNB 전용망으로 슬라이싱과 초저지연을 실현하는 **SA(Option 2)** 아키텍처
- 배경/필요성: 4G 인프라 연동 방식(NSA)의 한계로 인한 **진정한 5G 초저지연(1ms), E2E 네트워크 슬라이싱 격리 및 VoNR 고품질 음성 독립 처리 불가**

#### 한줄 요약
- NSA는 4G 코어 기반의 조기 상용화 방식이며, SA는 5GC 기반의 전 영역 독립 구축 방식이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **EN-DC (E-UTRA NR Dual Connectivity)**: 단말이 4G LTE eNB(Master)와 5G NR gNB(Secondary)에 동시 접속하여 무선 자원을 결합 사용하는 기술.
- **VoNR (Voice over New Radio)**: 4G 망 폴백 없이 5G SA 코어와 기지국 경로 내에서 직접 처리하는 차세대 고품질 음성 서비스.

</details>

- **NSA (이중 연결 기반 속도 조기 확보)**: 제어는 4G eNB/EPC, 데이터는 5G gNB가 분담하여 기가비트 다운로드 달성
- **SA (서비스 기반 코어 연동)**: 제어 및 데이터 평면 모두 5GC(AMF/SMF/UPF)와 gNB가 직접 처리하여 1ms 초저지연 보장
- **단계적 진화 경로**: Option 3x(NSA 초기 투자 최소화) $\to$ Option 2(SA 완전 독립 코어 전환 및 VoNR 지원)

#### 한줄 요약
- NSA는 LTE 연동을 통해 eMBB를 조기 구현하고, SA는 5GC를 통해 URLLC와 네트워크 슬라이싱을 완전 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **EPC (Evolved Packet Core)**: 4G LTE 네트워크의 제어(MME) 및 데이터 전송(SGW/PGW)을 담당하는 레거시 코어망.
- **5GC (5G Core Network)**: 서비스 기반 아키텍처(SBA) 및 클라우드 네이티브 가상화 기술을 적용한 5G 전용 코어망.

</details>

```text
[5G NSA (Option 3x) vs 5G SA (Option 2) 아키텍처 비교]
|-- NSA Mode (Option 3x)
|   |-- UE -> Dual Radio (EN-DC: 4G C-Plane + 5G U-Plane)
|   |-- 4G eNB (Master Node: S1-C 제어 신호 앵커)
|   |-- 5G gNB (Secondary Node: S1-U 고속 데이터 포워딩)
|   `-- 4G EPC Core (MME / SGW / PGW 레거시 하드웨어 코어)
`-- SA Mode (Option 2)
    |-- UE -> Single NR Radio (통합 C/U-Plane)
    |-- 5G gNB (Standalone Node: N2 C-Plane / N3 U-Plane 직결)
    `-- 5G 5GC Core (AMF / SMF / UPF / NSSF 클라우드 네이티브 SBA 코어)
```

선의 의미: 계층 및 NSA는 제어와 데이터가 4G 코어와 5G 기지국으로 분기되고 SA는 5G 기지국과 5GC가 직결되는 구조

| 구성요소 | NSA (Option 3x) 역할 | SA (Option 2) 역할 |
|:---|:---|:---|
| **단말 (UE)** | LTE 및 5G NR 라디오를 동시 구동 (**EN-DC 이중 무선**) | **5G NR 단일 라디오로 제어/데이터 통합 송수신** |
| **무선 접속망 (RAN)**| 4G eNB(Master) + 5G gNB(Secondary) 협력 | **5G gNB 단독 운용 (N2 제어 / N3 데이터 직결)** |
| **코어 네트워크** | **4G EPC (MME, SGW, PGW-U/C 레거시 코어)** | **5G 5GC (AMF, SMF, UPF, NSSF 가상화 코어)** |
| **제어 평면 앵커** | 4G LTE 무선망 및 MME (4G 앵커) | **5G New Radio 및 AMF (5G 앵커)** |

#### 한줄 요약
- NSA는 EPC와 eNB가 제어 앵커를 맡고, SA는 5GC와 gNB가 제어 및 데이터를 전담한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **EPS Fallback**: 5G SA 초기 음성 통화(VoNR) 커버리지가 미흡할 때, 통화 연결 시점에 단말을 4G LTE(VoLTE) 망으로 즉시 핸드오버시키는 기술.

</details>

```text
5G SA 음성 통화 (VoNR vs EPS Fallback) 처리 흐름
        │
   1. [음성 호 발신] 5G SA 단말이 SIP INVITE 메시지 발송
        │
   2. [VoNR 무선 품질 판정] 5G NR 무선 채널 품질 및 gNB 음성 지원 여부 판정
   ┌────┴───────────────────────────┐
  5G 커버리지 양호 (VoNR 가용)     5G 음영 또는 품질 미흡
   │                                 │
3A. [5G SA VoNR 호 수립]            3B. [EPS Fallback 리다이렉트 지시]
   5G UPF 경로 내 즉각 음성 연결         gNB가 단말을 4G LTE 셀로 핸드오버
   │                                 │
   ▼                                 ▼
[초고음질 무지연 통화 유지]          [4G VoLTE 망 기반 음성 통화 연결]
```

#### 한줄 요약
- 서비스 요청 수신 후 VoNR 가용성에 따라 5G 내 직접 처리 또는 4G EPS Fallback으로 분기한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Option 3x vs Option 2**: 무선/코어망 조합에 따른 표준 분류로 4G 코어 연동(Option 3x)과 순수 5G 전용망(Option 2).

</details>

| 비교 항목 | 5G NSA (Option 3x) | 5G SA (Option 2) |
|:---|:---|:---|
| **코어 네트워크** | **4G EPC (레거시 하드웨어 코어)** | **5G 5GC (클라우드 네이티브 SBA 코어)** |
| **제어 평면 앵커** | **4G LTE eNB** | **5G NR gNB** |
| **E2E 네트워크 슬라이싱**| **지원 불가 (코어망 가상화 부재)** | **완전 지원 (E2E 논리적 가상망 분리)** |
| **전송 지연 시간** | 4G EPC 경유로 약 10~20ms | **MEC 연계 1~5ms 초저지연 달성** |
| **단말 배터리 효율** | 이중 무선 수신(EN-DC)으로 소모량 큼 | **단일 무선 운용으로 배터리 수명 최적화** |
| **음성 통화 방식** | 기존 4G VoLTE 활용 | **VoNR 지원 (과도기 EPS Fallback)** |

#### 한줄 요약
- NSA는 4G 코어 기반의 속도 증대 중심이며, SA는 5GC 기반의 E2E 슬라이싱과 초저지연을 실현한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **CHF (Charging Function)**: 5G 코어에서 온라인/오프라인 과금을 통합 처리하는 SBA 기반 클라우드 과금 노드.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 5G SA 전환 초기 VoNR 커버리지 부족으로 인한 통화 단절 | **`EPS Fallback (4G VoLTE 망 핸드오버)` 기술 적용** | 음성 통화의 무중단 연속성 및 가용성 보장 |
| NSA 이중 연결(EN-DC) 구동 시 단말 배터리 급격한 소모 | 트래픽 유무에 따른 **`보조 셀(Secondary Cell) 동적 수면 제어`** | 유휴 상태 배터리 소모 절감 및 발열 억제 |
| NSA 환경에서 4G EPC와 5G gNB 간 이원화된 과금 기록(CDR) 불일치 | **통합 과금 게이트웨이(`CHF`) 연동 및 표준 패킷 계량** | 데이터 과금 누락 방지 및 정산 정합성 확보 |
| 5G SA 전환 시 기존 4G 가입자 인증 데이터(HSS) 마이그레이션 | **`UDM / UDR 클라우드 네이티브 통합 가입자 DB` 구축** | 무중단 가입자 프로파일 전환 및 서비스 연속성 |

#### 한줄 요약
- EPS Fallback 음성 보장, 동적 보조 셀 절전, 통합 CHF 과금, UDM 가입자 DB 통합으로 운영한다.

## Ⅶ. 결론

- 조기 상용화는 **NSA**, 초저지연·E2E 슬라이싱은 **SA** 선택

#### 한줄 요약
- 5G SA/NSA는 인프라 진화 단계별 핵심 아키텍처이며, 5GC 기반 SA 전환을 통해 5G 본연의 초저지연과 네트워크 슬라이싱 가치를 완성한다.
