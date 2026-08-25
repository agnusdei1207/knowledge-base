---
sidebar:
  order: 21
  label: "021. IDS•IPS"
  badge:
    text: "기출 · 50%"
    variant: note
title: "침입 탐지•방지 시스템 (IDS•IPS)"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 21
extra:
  question_no: "21"
  source_status: "기출"
  source_history: "129회, 134회"
  priority: 50
  priority_note: "미러링 탐지(IDS) 및 인라인 능동 차단(IPS) 아키텍처"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **IDS (Intrusion Detection System)**: 트래픽 미러링(SPAN/TAP)을 통해 네트워크 침입을 수동 모니터링하고 경보(Alert)를 발송하는 수동형 시스템.
- **IPS (Intrusion Prevention System)**: 네트워크 경로 상에 인라인(Inline)으로 배치되어 악성 패킷을 실시간 탐지하고 즉각 폐기(Drop)하는 능동형 보안 시스템.

</details>

- 정의/개념: L4~L7 DPI와 시그니처 및 이상 징후 분석을 통해 **침입 행위를 모니터링·경보하는 IDS와 실시간 인라인 패킷을 차단하는 IPS**
- 배경/필요성: L3/L4 방화벽이 허용한 정상 80/443 포트로 유입되는 **애플리케이션 취약점 익스플로잇, 악성코드 페이로드 침투 방어 불가**

#### 한줄 요약
- 미러링 기반 경보(IDS)와 인라인 실시간 차단(IPS)을 통해 네트워크 심층 위협을 방어한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Signature Detection (오용 탐지)**: 알려진 공격 패턴 지문(CVE 취약점 시그니처)과 일치 여부를 대조하는 방식 (낮은 오탐률, 제로데이 불가).
- **Anomaly Detection (이상 탐지)**: 정상 트래픽 기준선(Baseline)을 학습하고 통계적/행위적 임계치 초과 변칙을 식별하는 방식 (신종 공격 탐지, 오탐 주의).

</details>

- **IDS(경로 외, Out-of-band)**: 원본 패킷 전달 지연이 전무하며 SPAN/TAP 포트로 수동 감시 수행
- **IPS(경로 상, Inline)**: 실시간 패킷 검사 후 즉각 폐기(Drop) 및 TCP Reset 전송으로 능동 차단
- **시그니처 탐지(오용 탐지)**와 **이상 징후 탐지(행위 기반)** 기법의 혼합 적용을 통한 탐지율 극대화

#### 한줄 요약
- Out-of-band 무지연 감시(IDS)와 Inline 실시간 능동 차단(IPS)을 시그니처/이상 탐지로 수행한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Session Normalization (세션 정규화)**: 단편화된 패킷을 재조립하고 인코딩을 디코딩하여 공격자의 우회 기법(Evasion)을 무력화하는 전처리 엔진.
- **Hardware Bypass (Fail-Open)**: IPS 장비 장애 또는 전원 차단 시 트래픽 단절을 방지하기 위해 물리적 릴레이 스위치로 회선을 직결시키는 모듈.

</details>

```text
[IDS / IPS 트래픽 유입 및 검사·대응 아키텍처]
|-- Ingress Network Traffic (TAP / SPAN 미러링 또는 Inline 물리 연결)
`-- Threat Inspection Pipeline
    |-- Session Normalization (패킷 재조립, 프로토콜 디코딩, Evasion 방어)
    |-- Detection Engine (Signature Matching + Anomaly Profiling)
    `-- Policy Decision Engine (위협 스코어링, 허용/차단 정책 매칭)
|-- Output Layer (동작 모드별 분기)
|   |-- IDS Mode (Out-of-band): 보안 이벤트 로깅, SIEM 경보 발송, PCAP 원시 증적 보존
|   `-- IPS Mode (Inline): 패킷 즉시 폐기(Drop), TCP RST 강제 주입 세션 종료
`-- Hardware Bypass Switch (IPS 고장 시 물리적 선로 직결 Fail-Open 보장)
```

선의 의미: 계층 및 인입 트래픽이 세션 정규화와 탐지 엔진을 거쳐 IDS 경보 또는 IPS 인라인 차단으로 분기되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **세션 정규화기** | 패킷 재조립, 디코딩 및 **단편화 우회 공격(Evasion Attack) 패턴 무력화** | 전처리 계층 |
| **탐지 엔진** | Snort/Suricata 시그니처 매칭 및 **통계적/머신러닝 기반 이상 징후 행위 분석** | 핵심 분석 모듈 |
| **정책 판정 엔진** | 탐지된 위협의 위험도와 자산 중요도에 따라 **경보 또는 즉시 차단 여부 결정** | 룰 매칭 |
| **대응 실행기** | IDS 모드 경보(Alert) 발송 또는 **IPS 모드 패킷 폐기(Drop) 및 TCP RST 세션 파기** | 액션 집행 |
| **하드웨어 바이패스**| IPS 하드웨어 고장 시 **물리적 링크를 즉시 단락시켜 서비스 가용성(Fail-Open) 보장** | 고가용성 모듈 |

#### 한줄 요약
- 세션 정규화, 탐지 엔진, 정책 판정기, 대응 실행기, 하드웨어 바이패스가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **TCP RST 주입**: 탐지된 악성 TCP 세션을 강제 종료시키기 위해 공격자와 피해자 양측으로 위조된 TCP RST 플래그 패킷을 송출하는 기법.

</details>

```text
IDS / IPS 패킷 인입 및 탐지·차단 파이프라인
        │
   1. [트래픽 수집] TAP/SPAN 미러링(IDS) 또는 인라인 직렬 수신(IPS)
        │
   2. [세션 정규화] 패킷 재조립 및 디코딩을 통한 우회 시도 차단
        │
   3. [시그니처 대조] CVE 취약점 룰셋 및 이상 징후 프로파일링 매칭
   ┌────┴───────────────────────────┐
  정상 트래픽                      악성 공격 식별
   │                                 │
4A. [인라인 정상 통과]              ┌─┴─────────────────────────────┐
   지연 없이 대상 포워딩             │                               │
                                   [IDS 환경]                      [IPS 환경]
                                   4B. 경보(Alert) 전송            4C. 패킷 폐기(Drop)
                                       SIEM 원시 증적 보존             TCP RST 세션 종료
```

#### 한줄 요약
- 트래픽 수집 → 세션 정규화 → 시그니처 대조 → 정상 통과 또는 IDS 경보 / IPS 차단 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **False Positive (오탐)** vs **False Negative (미탐)**: 정상 트래픽을 공격으로 오인하여 차단하는 오류(오탐)와 실제 공격을 놓치는 오류(미탐).

</details>

| 비교 항목 | 침입 탐지 시스템 (IDS) | 침입 방지 시스템 (IPS) |
|:---|:---|:---|
| **네트워크 배치 방식** | **경로 외 (Out-of-band / SPAN, TAP 미러링)**| **경로 상 (Inline / 물리적 직렬 연결)** |
| **서비스 가용성 영향** | **지연 전무 (Zero Latency), 장애 시 영향 없음** | **패킷 검사 지연 발생, 장비 장애 시 망 단절 위험** |
| **위협 대응 메커니즘** | 사후 분석, 관리자 경보, PCAP 증적 저장 | **실시간 인라인 패킷 차단(Drop), TCP RST 세션 파기** |
| **오탐(False Positive) 영향**| 경보 피로(Alert Fatigue) 유발에 그침 | **정상 고객 비즈니스 서비스 차단 장애 유발** |

#### 한줄 요약
- IDS는 서비스 영향 없는 무지연 사후 모니터링을 제공하고, IPS는 실시간 차단을 수행한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Fail-Open (Bypass)**: IPS 장애 시 트래픽을 차단하지 않고 무조건 통과시켜 가용성을 보장하는 모드.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 과도한 오탐(False Positive)으로 인한 정상 비즈니스 서비스 차단 장애 | **초기 `IDS 모드(Alert-only) 검증` 후 단계적 인라인 IPS 전환** | 오탐 차단 방지 및 룰셋 신뢰도 확보 |
| 패킷 분할/변조를 통한 침입 탐지 우회(Evasion Attack) 시도 | **`세션 정규화(Normalization)` 및 재조립 타임아웃 튜닝** | 파편화 우회 공격 완전 무력화 |
| 인라인 IPS 장비의 전원/하드웨어 고장 시 전체 네트워크 마비 | **광/구리선 `하드웨어 바이패스(Hardware Bypass / Fail-Open)` 장착** | 장비 장애 시에도 물리 링크 직결 가용성 보증 |
| 암호화(HTTPS) 트래픽 급증으로 L7 악성 페이로드 탐지 불가 | **IPS 전단에 `SSL 가시성 어플라이언스(SSL Offloader)` 연동** | 암호화 트래픽 복호화 및 위협 가시성 확보 |

#### 한줄 요약
- 단계적 IDS/IPS 전환, 세션 정규화, 하드웨어 바이패스, SSL 가시성 연동으로 운영한다.

## Ⅶ. 결론

- 진화하는 지능형 네트워크 공격을 선제 차단하기 위해 **신규 시그니처는 IDS 모드로 충분한 오탐 검증을 거친 후 인라인 IPS 차단 모드로 단계적 승격**하고, **하드웨어 Fail-Open 바이패스 모듈과 SSL 복호화 가시성 시스템**을 결합하여 가용성과 보안성을 동시에 만족하는 고신뢰 침입 방어 인프라 완성

#### 한줄 요약
- IDS/IPS는 DPI와 시그니처/이상 탐지를 기반으로 위협을 식별·차단하며, 하드웨어 바이패스와 SSL 가시성을 결합하여 무중단 능동 보안을 실현하는 핵심 네트워크 보안 기술이다.