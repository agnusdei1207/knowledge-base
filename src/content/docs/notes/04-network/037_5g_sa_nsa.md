---
sidebar:
  order: 37
  label: "037. 5G SA와 NSA (5G SA vs NSA)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "5G 네트워크 구축 아키텍처 : SA(독립형)와 NSA(비독립형)"
date: "2026-08-22T07:15:00+09:00"
tags:
  - "notes-network"
weight: 37
extra:
  question_no: "037"
  source_status: "기출"
  source_history: "135회"
  priority: 70
  priority_note: "Option 3x(NSA) vs Option 2(SA) 비교 및 EPS Fallback/VoNR"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **5G NSA(Non-Standalone, 비독립형)**: 기존 4G LTE 코어망(EPC)과 기지국(eNB)을 제어 평면의 앵커(Anchor)로 활용하면서, 사용자 데이터 평면 전송에 5G 기지국(gNB)을 결합 운용하는 과도기적 구축 방식 (3GPP Option 3x).
- **5G SA(Standalone, 독립형)**: 5G 전용 코어망(5GC)과 5G 무선 접속망(gNB)만으로 제어 평면과 사용자 평면을 독자 구성하는 순수 5G 엔드투엔드 아키텍처 (3GPP Option 2).
- **5G 코어(5GC)**: 서비스 기반 아키텍처(SBA) 및 클라우드 네이티브 가상화 기술을 적용하여 네트워크 슬라이싱과 초저지연 제어를 지원하는 차세대 코어망.

</details>

- 정의/개념: 기존 4G EPC 및 eNB 인프라를 재활용하여 5G 속도를 조기 제공하는 **NSA(비독립형)** 와, 5GC 및 gNB를 완전 구축하여 5G 고유 기능(슬라이싱, 초저지연)을 구현하는 **SA(독립형)** 아키텍처
- 배경/필요성: 5G 도입 초기 막대한 인프라 투자 비용 절감 및 조기 상용화(NSA) 후, B2B 특화망, 완전한 자율주행(URLLC) 및 E2E 슬라이싱 지원을 위한 진정한 5G 인프라(SA)로의 전환 요구

#### 한줄 요약
- NSA는 4G 코어 기반의 조기 상용화 방식이며, SA는 5G 코어 기반의 전 영역 독립 구축 방식이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **EN-DC(E-UTRA NR Dual Connectivity)**: 단말이 4G LTE 기지국(Master Node)과 5G NR 기지국(Secondary Node)에 동시 접속하여 무선 자원을 결합 사용하는 이중 연결 기술.
- **VoNR(Voice over New Radio)**: 4G 망으로의 폴백 없이 5G SA 망 내부에서 전송 지연 없이 고품질 음성 통화를 제공하는 차세대 음성 서비스.

</details>

- **NSA (이중 연결 기반 속도 향상)**: 제어 신호(C-Plane)는 4G eNB/EPC가 처리하고, 데이터(U-Plane)는 5G gNB가 분담하여 기가비트 다운로드 속도 신속 달성
- **SA (서비스 기반 코어 연동)**: 제어 및 데이터 평면 모두 5GC(AMF/SMF/UPF)와 gNB가 직접 처리하여 1ms 초저지연과 E2E 네트워크 슬라이싱 보장
- **단계적 진화 경로**: Option 3x(NSA 초기 투자 최소화) $\rightarrow$ Option 2(SA 완전 독립 코어 전환 및 VoNR 지원)

#### 한줄 요약
- NSA는 LTE 연동을 통해 eMBB를 조기 구현하고, SA는 5GC를 통해 URLLC와 네트워크 슬라이싱을 완전 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **진화된 패킷 코어(Evolved Packet Core, EPC)**: 4G LTE 네트워크의 제어(MME) 및 데이터 전송(SGW/PGW)을 담당하는 레거시 코어망.
- **차세대 노드 B (gNodeB, gNB)**: 5G New Radio(NR) 무선 인터페이스를 통해 단말과 통신하는 5G 기지국 장비.

</details>

```text
[ 5G NSA (Option 3x) 구조 ]                  [ 5G SA (Option 2) 구조 ]

        [ 단말 (UE) ]                                 [ 단말 (UE) ]
         │         │                                        │
 (C-Plane│         │(U-Plane 데이터)                         │ (C/U-Plane)
         ▼         ▼                                        ▼
     [ 4G eNB ] ──▶[ 5G gNB ]                             [ 5G gNB ]
         │ (S1-C)   │ (S1-U 데이터)                          │ (N2/N3)
         ▼          ▼                                        ▼
   [ 4G LTE 코어 (EPC) ]                             [ 5G 전용 코어 (5GC) ]
   (MME / SGW / PGW)                                 (AMF / SMF / UPF / NSSF)
```

선의 의미: NSA는 제어와 데이터가 4G 코어와 5G 기지국으로 분기되는 구조이며, SA는 5G 기지국과 5GC가 직결되어 단일 파이프라인을 형성하는 구조

| 구성요소 | NSA (Option 3x) 역할 | SA (Option 2) 역할 |
|:---|:---|:---|
| **단말 (UE)** | LTE 및 5G NR 라디오를 동시 구동 (EN-DC) | 5G NR 단일 라디오로 제어/데이터 통합 송수신 |
| **무선 접속망 (RAN)** | 4G eNB(Master) + 5G gNB(Secondary) 협력 | **5G gNB 단독 운용 (N2/N3 인터페이스)** |
| **코어 네트워크 (Core)** | **4G EPC (MME, SGW, PGW-U/C)** | **5G 코어 (AMF, SMF, UPF, NSSF, NRF)** |
| **제어 평면 앵커** | 4G LTE 무선 접속망 및 MME | 5G New Radio 및 AMF |

#### 한줄 요약
- NSA는 EPC와 eNB가 제어 앵커를 맡고, SA는 5GC와 gNB가 제어 및 데이터를 전담한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **EPS 폴백(EPS Fallback)**: 5G SA 네트워크 초기 음성 통화(VoNR) 커버리지가 미흡할 때, 통화 연결 시점에 단말을 4G LTE(VoLTE) 망으로 즉시 핸드오버시키는 음성 연속성 보장 기술.

</details>

```text
[ 5G SA 음성 통화 (VoNR vs EPS Fallback) 흐름 ]

1. 단말이 5G SA 망에서 음성 호 발신 (SIP INVITE 전송)
            │
            ├─ [VoNR 커버리지 양호] ──▶ 2a. 5G SA 망 내 gNB/UPF 기반 즉시 음성 통화 수립
            │
            └─ [VoNR 품질 미흡] ─────▶ 2b. gNB가 4G 셀로 리다이렉트 지시 (EPS Fallback)
                                             │
                                             ▼
                                        3. 4G eNB/EPC로 세션 핸드오버 ➔ VoLTE 음성 통화 연결
```

**동작 원리**

1. **서비스 요청**: 단말이 5GC의 AMF로 PDU 세션 수립 또는 음성 호 설정 요청
2. **품질 판정**: 5G 무선 채널 품질 및 gNB의 VoNR 지원 여부 판정
3. **VoNR 처리**: 5G 전용 QCI(5QI 1)를 할당하여 5G 코어 경로 내에서 지연 없이 고품질 음성 통화 수립
4. **EPS Fallback 핸드오버**: 음성 채널이 불안정할 경우 4G LTE로 리디렉션하여 통화 단절 방지

#### 한줄 요약
- 서비스 요청 수신 후 VoNR 가용성에 따라 5G 내 직접 처리 또는 4G EPS Fallback으로 분기한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **3GPP 구축 옵션**: 무선망과 코어망의 조합에 따른 표준 분류로, 대표적으로 Option 3/3a/3x(NSA)와 Option 2(SA)가 존재.

</details>

| 비교 항목 | 5G NSA (Option 3x) | 5G SA (Option 2) |
|:---|:---|:---|
| **코어 네트워크** | **4G EPC (레거시 하드웨어 코어)** | **5G 5GC (클라우드 네이티브 SBA 코어)** |
| **제어 평면 앵커** | **4G LTE eNB** | **5G NR gNB** |
| **E2E 네트워크 슬라이싱** | 지원 불가 (코어망 가상화 부재) | **완전 지원 (E2E 논리적 망 분리)** |
| **전송 지연 시간** | 4G EPC 경유로 약 10~20ms | **MEC 연계 1~5ms 초저지연 달성** |
| **단말 배터리 소모** | 이중 무선 수신(EN-DC)으로 높음 | 단일 무선 인터페이스 운용으로 최적화 |
| **음성 통화 방식** | 기존 VoLTE 활용 | **VoNR 지원 (필요 시 EPS Fallback)** |

#### 한줄 요약
- NSA는 4G 코어 기반의 속도 증대 중심이며, SA는 5GC 기반의 E2E 슬라이싱과 초저지연을 실현한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **과금 기능(Charging Function, CHF)**: 5G 코어에서 온라인/오프라인 과금을 통합 처리하는 SBA 기반 과금 노드.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 5G SA 전환 초기 VoNR 커버리지 부족으로 인한 음성 통화 단절 | **EPS Fallback(4G VoLTE 망 핸드오버)** 기술 적용 | 음성 통화의 중단 없는 연속성 및 안정성 보장 |
| NSA 이중 연결(EN-DC) 구동 시 단말 배터리 급격한 소모 | 트래픽 유무에 따른 **보조 셀(Secondary Cell) 동적 수면 제어** | 유휴 상태 배터리 소모 절감 및 발열 억제 |
| NSA 환경에서 4G EPC와 5G gNB 간 이원화된 과금 기록(CDR) 불일치 | **통합 과금 게이트웨이(CHF)** 연동 및 표준 패킷 계량 적용 | 데이터 과금 누락 방지 및 정산 정합성 확보 |

#### 한줄 요약
- EPS Fallback으로 음성 연속성을 지키고, 동적 셀 제어로 배터리를 절감하며, 통합 CHF로 과금 정합성을 유지한다.

## Ⅶ. 결론

- 초기 5G 상용화는 기구축된 4G 망을 활용한 **NSA(Option 3x)** 방식으로 eMBB 서비스를 신속히 개시하되, 향후 B2B 특화망, 자율주행, 스마트 팩토리 등 초저지연(URLLC)과 E2E 슬라이싱이 요구되는 환경을 위해 **5GC 기반 SA(Option 2)** 로 전면 전환하고, 과도기에는 **EPS Fallback**을 적용하여 서비스 품질을 안정화

#### 한줄 요약
- NSA 조기 런칭 후 5GC 기반 SA로 전환하여 5G 본연의 초저지연 및 슬라이싱 가치를 완성한다.
