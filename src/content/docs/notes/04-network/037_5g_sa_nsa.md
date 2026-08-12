---
sidebar:
  order: 37
  label: "037. 5G SA와 NSA"
  badge: { text: "기출 • 70%", variant: note }
title: "5G SA와 NSA"
date: "2026-08-06T23:27:50+09:00"
tags: ["notes-network"]
weight: 37
extra:
  question_no: "037"
  source_status: "기출"
  source_history: "135회"
  priority: 70
  priority_note: "135회 출제"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **독립형(Standalone, SA)**: 5G 무선기지국(gNB)과 5G 전용 코어망(5GC)만을 결합하여 단독으로 구축하는 5G 통신망 방식이다.
- **비독립형(Non-Standalone, NSA)**: 기존 LTE 코어망(EPC) 및 제어 기지국(eNB)을 활용하면서 5G 무선망(gNB)을 데이터 확장 전용으로 연결하는 방식이다.
- **장기 진화(Long Term Evolution, LTE)**: 4세대 이동통신의 대표적인 무선 및 패킷 코어 통신 표준 규격이다.
- **5세대 이동통신(Fifth-Generation Mobile Communication, 5G)**: 초고속, 초저지연, 대규모 연결을 제공하는 차세대 이동통신 기술 표준이다.
- **5세대 코어(5G Core, 5GC)**: 서비스 기반 아키텍처(SBA)를 적용하여 세션 제어, 가입자 관리, 네트워크 슬라이싱을 총괄하는 5G 전용 코어 시스템이다.

</details>

- 정의/개념: **5G 구축 방식(SA/NSA)**은 5G 코어(5GC)의 단독 운용 여부에 따라 구별되며, **NSA**는 LTE 패킷 코어(EPC) 및 제어망을 공유하는 비독립 구조이고 **SA**는 5GC와 5G 무선(NR)만을 결합한 완전 독립 구조이다.
- 배경/필요성: 초기 5G 도입 시 천문학적 코어망 투자 비용(CAPEX) 절감과 신속한 상용화 커버리지 확보를 위해 NSA가 채택되었으나, E2E 네트워크 슬라이싱, URLLC, VoNR 등 5G 본연의 기능을 완벽히 수용하기 위해 SA로의 전환이 요구된다.

#### 한줄 요약

- LTE 코어망(EPC) 및 제어 신호 의존 여부에 따라 신속 도입 중심의 NSA와 5G 코어(5GC) 중심의 완전 독립형 SA로 구분되는 망 구축 구조.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **진화형 패킷 코어(Evolved Packet Core, EPC)**: LTE 시스템의 가입자 인증, 세션 관리 및 패킷 라우팅을 제어하는 4세대 패킷 코어망이다.
- **신규 무선(New Radio, NR)**: 3GPP에서 정의한 5G 이동통신 전용 무선 접속 기술(RAT) 규격이다.
- **신규 무선 기반 음성(Voice over New Radio, VoNR)**: 5G SA 환경에서 LTE망 우회(Fallback) 없이 5G 코어와 5G 무선망을 통해 직접 음성 통화를 제공하는 규격이다.

</details>

- **NSA (EN-DC 기반 비독립형)**: LTE 제어 기지국(eNB)이 제어 플레인을 담당하고, 5G 기지국(gNB)이 데이터 플레인을 전담하는 이중 연결(EN-DC) 방식으로 기존 EPC 코어망과 연동한다.
- **SA (5GC 기반 완전 독립형)**: 5G 무선(NR)이 제어 및 사용자 플레인을 모두 처리하며, SBA 구조의 5GC에 직접 연결되어 서비스별 자원 격리가 가능한 독립망을 형성한다.
- **기능 제공 차별성**: SA는 E2E 네트워크 슬라이싱, 1ms 이하 초저지연(URLLC), VoNR을 지원하며, NSA는 이중 연결을 통한 전송 속도 향상에 집중한다.

#### 한줄 요약

- NSA는 LTE 망 기반 이중 연결(EN-DC)로 빠른 서비스 제공, SA는 5GC 기반의 E2E 네트워크 슬라이싱 및 저지연 구현.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **이중 연결(Dual Connectivity, EN-DC)**: 단말이 LTE 기지국(Master Node)과 5G NR 기지국(Secondary Node)에 동시 접속하여 데이터를 송수신하는 기술이다.

</details>

```text
5G 망 구축 아키텍처
├─ 비독립형 경계 (NSA Boundary)
│  ├─ 이중 연결 단말 (NSA Dual-Connectivity UE)
│  ├─ 이-유트라 신규무선 이중 연결 (EN-DC)
│  └─ 진화형 패킷 코어 (LTE EPC)
└─ 독립형 경계 (SA Boundary)
   ├─ 단독 접속 단말 (SA Dedicated UE)
   ├─ 5G 신규무선 단독 연결 (NR SA)
   └─ 5G 코어망 (5G Core, 5GC)
```

선의 의미: LTE 코어망(EPC) 의존성 여부에 따라 NSA와 SA의 단말, 무선 접속 링크, 코어 망간 매핑 구조를 명시한다.

| 구성요소 | 책임 |
|:---|:---|
| 이중 연결 단말 (NSA UE) | LTE 및 5G NR 신호를 동시에 수신하고 제어 신호는 LTE 경로로 전송 |
| EN-DC (E-UTRA NR Dual Connectivity) | LTE 기지국을 제어 노드(MN)로 지정하고 5G 기지국을 데이터 확장 노드(SN)로 결합 |
| 진화형 패킷 코어 (EPC) | NSA 환경에서 가입자 식별, 이동성 제어(MME) 및 패킷 세션(SGW/PGW) 처리 |
| 단독 접속 단말 (SA UE) | 5G NR 제어 신호 및 5GC 무선 인터페이스(N1/N2/N3) 직접 연결 지원 |
| 5G NR 단독 연결 | 5G 무선 채널(gNB)을 통해 제어 및 사용자 트래픽을 5GC로 직접 전달 |
| 5G 코어망 (5GC) | AMF, SMF, UPF, NRF 등 NF(Network Function) 기반의 서비스 기반 세션/슬라이싱 관리를 전담 |

#### 한줄 요약

- NSA는 EPC 제어망과 EN-DC를 사용하고, SA는 5GC 및 서비스 기반 아키텍처(SBA)를 통한 독립 라우팅을 수행하는 구성.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **NR 단독 연결(NR Standalone Connectivity, NR SA)**: LTE 지원 없이 5G NR 무선망과 5GC만을 이용하여 가입자 제어 및 데이터 세션을 설정하는 절차이다.

</details>

```text
1. 사업자 구축 목표 및 CAPEX 판정 (NSA vs SA Decision)
      │
      ├─ LTE 자산 활용 및 신속 도입 ── 2a. NSA 방식 (EN-DC Dual Connectivity)
      │                                   │
      │                                   ├─ LTE Control Plane 제어
      │                                   └─ EPC 기반 가입자/세션 관리
      │
      └─ 슬라이싱·저지연·VoNR 구현 ── 2b. SA 방식 (5GC Standalone)
                                          │
                                          ├─ 5G NR Control Plane 독립 제어
                                          └─ 5GC SBA 기반 가입자/세션/슬라이스 제어
```

### 동작 원리

1. **구축 정책 의사결정**: 초기 CAPEX 및 자산 활용(NSA)과 네트워크 슬라이싱/URLLC 구현(SA) 중 요구사항을 선정한다.
2. **NSA 가입자 접속 (EN-DC)**: NSA 단말 접속 시 LTE 기지국에서 RRC 연결을 생성하고 EPC 가입자 인증을 완료한 후, 5G NR을 데이터 전송 보조 채널로 추가 할당한다.
3. **SA 가입자 접속 (5GC)**: SA 단말 접속 시 5G NR 무신 채널을 통해 5GC AMF(접속·이동성 관리)로 제어 신호를 직접 전달하여 인증 및 인가를 완료한다.
4. **세션 및 자원 제어**: NSA는 PGW/SGW가 트래픽을 처리하며, SA는 SMF/UPF가 가상 네트워크 슬라이스별 특화 세션을 생성한다.
5. **음성 서비스 처리**: NSA는 LTE CSFB/VoLTE로 음성을 처리하고, SA는 5G VoNR 또는 SA 초기 미지원 시 EPS Fallback 기술로 음성을 보장한다.

#### 한줄 요약

- 사업자 구축 환경에 따라 NSA(EN-DC/EPC) 또는 SA(5GC/VoNR) 제어 경로와 가입자 등록 및 세션을 실행하는 흐름.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **네트워크 슬라이싱(Network Slicing)**: 단일 5G 물리망을 독립적인 가상 네트워크로 분할하여 서비스 품질(eMBB, URLLC, mMTC)을 맞춤 보장하는 기술이다.

</details>

| 비교 항목 | **5G NSA (Non-Standalone)** | **5G SA (Standalone)** |
|:---|:---|:---|
| 핵심 코어망 | 4G LTE EPC (Evolved Packet Core) | 5G 전용 5GC (5G Core) |
| 무선 접속 및 제어 | LTE 기지국(제어) + 5G NR 기지국(데이터) | 5G NR 기지국 (제어 및 데이터 독점) |
| 연결 기술 | EN-DC (E-UTRA NR Dual Connectivity) | Standalone 5G NR |
| 핵심 지원 서비스 | eMBB (초고속 대용량 데이터 전송) | eMBB, URLLC, mMTC, E2E 네트워크 슬라이싱 |
| 음성 통화 방식 | VoLTE (4G LTE 망으로 제어 전환) | VoNR (5G 망 직접 음성 처리) / EPS Fallback |
| 구축 장단점 | 초기 투자비(CAPEX) 절감, 초저지연 구현 불가 | 코어망 투자비 증가, 5G 전용 고성능 서비스 완벽 지원 |

> 요약: 신속한 커버리지 확대에는 NSA, E2E 네트워크 슬라이싱 및 URLLC 초저지연 구현에는 SA 적용.

#### 한줄 요약

- NSA는 초기 커버리지 구축과 CAPEX 절감에 유리하며, SA는 E2E 슬라이싱, URLLC, VoNR을 구현하는 차세대 표준.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **통화 연속성(Call Continuity, EPS Fallback)**: SA 음성 통화(VoNR) 미지원 및 약전계 이동 시 LTE 망(VoLTE)으로 자동 세션을 전환하여 끊김을 방지하는 기술이다.
- **과금 기록(Charging Data Record, CDR)**: 코어망이 데이터 사용량, 세션 시간, 접속 슬라이스 정보를 수집하여 과금을 부과하는 원시 데이터 세트이다.

</details>

| 문제점 | 발생 원인 | 실무 대응 대책 | 기대 효과 |
|:---|:---|:---|:---|
| SA 전환 시 음성 커버리지 음영 | 초기 SA 음성(VoNR) 품질 불안정 및 커버리지 부족 | EPS Fallback 기술 적용 및 VoLTE 연동 전환 | 음성 통화 연속성 보장 및 통화 끊김 차단 |
| NSA 신호 과다 소모 (Battery) | LTE와 5G 무선 신호를 동시 처리하여 단말 전력 소모 폭증 | 무선 데이터 송수신 비활성화 시 5G NR 무신 릴리스 | 단말 배터리 소모 절감 및 전력 효율 향상 |
| 이중 코어 정산 과금 오차 | EPC와 5GC 간 과금 기록(CDR) 포맷 및 인덱스 불일치 | 5GC CHF(Charging Function) 및 과금 중계 시스템 연동 | 정산 오류 예방 및 과금 데이터 일관성 확보 |
| SA 기지국 간 로밍 지연 | SA 핸드오버 시 N2/N3 세션 재설정 지연 발생 | Xn 인터페이스 기반 기지국 간 직접 핸드오버 적용 | 로밍 지연 시간 단축 및 끊김 없는 데이터 전달 |

#### 한줄 요약

- EPS Fallback 기술 적용, EN-DC 셀 수용량 최적화, EPC/5GC 과금 데이터(CDR) 연동을 통해 통화 연속성 및 운용 품질 보장.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **전환 기준(Migration Strategy Criteria)**: 5G 서비스 확장에 맞춰 NSA 구조에서 SA 코어 구조로의 단계별 투자 및 전환 시점을 결정하는 기준이다.

</details>

- 이동통신 및 사설 5G 망 구축 시 **단계적 SA 전환 로드맵**, **EPS Fallback 연동 통화 연속성 확보**, **E2E 네트워크 슬라이싱 체계 구축 필수**.

#### 한줄 요약

- NSA 중심 구축에서 5GC 기반 SA로의 단계적 고도화 및 EPS Fallback 기반 통화 연속성 구현 필수.
