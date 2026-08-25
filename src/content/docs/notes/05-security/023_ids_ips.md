---
sidebar:
  order: 23
  label: "023. IDS•IPS 탐지 vs 차단"
  badge:
    text: "기출 · 85%"
    variant: note
title: "네트워크 침입 탐지 및 방지 시스템 : IDS vs IPS"
date: "2026-08-25T13:00:00+09:00"
tags:
  - "notes-security"
weight: 23
extra:
  question_no: "23"
  source_status: "기출"
  source_history: "129회, 134회, 137회"
  priority: 85
  priority_note: "미러링(SPAN/TAP) vs 인라인(Inline), 오탐/미탐 딜레마, 패킷 정규화(Normalization), 하드웨어 바이패스(Bypass)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **IDS (Intrusion Detection System)**: 미러링(SPAN/TAP) 트래픽을 수동 분석하여 공격 탐지 시 경보를 발행하는 사후 모니터링 시스템.
- **IPS (Intrusion Prevention System)**: 네트워크 경로에 직렬(Inline) 배치되어 악성 패킷을 실시간 폐기(Drop)하는 능동 방어 시스템.

</details>

- 정의/개념: 비인가 침입을 수동 감시하는 미러링 IDS와 악성 패킷을 실시간 능동 폐기하는 인라인 IPS로 구성된 **네트워크 침입 탐지 및 방지 시스템**
- 배경/필요성: 단순 방화벽의 정상 포트(80/443) 통과 후 발생하는 **패킷 페이로드 내 취약점 익스플로잇 침투 및 실시간 침입 차단 불가**

#### 한줄 요약
- 미러링 기반 수동 감시(IDS)와 인라인 기반 실시간 차단(IPS)을 통해 네트워크 침입을 무력화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Signature vs Anomaly Detection**: 알려진 공격 패턴과 대조하는 시그니처 기반 탐지와 정상 트래픽 기준선을 벗어나는 변종을 탐지하는 이상행위 탐지.
- **Hardware Bypass (Fail-Open)**: IPS 장비의 전원 이상이나 장애 시 물리 릴레이 스위치를 직결하여 회선 단절을 방지하는 안전장치.

</details>

- **배치 방식에 따른 통제력 분리**: 무지연 가용성 중심의 **미러링(IDS)과 실시간 능동 차단 중심의 인라인(IPS) 분업**
- **시그니처 및 이상행위 복합 탐지**: CVE 기반 **패턴 매칭과 통계적 베이스라인 이상 행위 분석을 결합하여 변종 위협 탐지**
- **패킷 정규화(Normalization)를 통한 우회 차단**: IP 단편화 조각을 **메모리에서 재조합하여 Evasion 공격 원천 무력화**

#### 한줄 요약
- 미러링 vs 인라인 분업, 시그니처/이상행위 복합 분석, 패킷 정규화 기반 우회 차단을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Stream Reassembler (패킷 정규화기)**: 조각난 IP 패킷과 비순차 TCP 세그먼트를 원본 스트림으로 재조합하여 시그니처를 검사하는 모듈.

</details>

```text
[IDS 미러링 vs IPS 인라인 네트워크 배치 구조]
|-- Inline IPS Architecture (직렬 연결: 실시간 패킷 드롭)
|   `-- External Internet -> Hardware Bypass Switch -> [ Inline IPS Engine (DPI & Drop) ] -> Internal LAN
`-- Mirroring IDS Architecture (병렬 연결: 수동 모니터링 및 경보)
    `-- External Internet -> Backbone Switch (SPAN/TAP) -> Internal LAN
                             `-- Mirror Traffic Copy -> [ Passive IDS Engine (Alert & SIEM) ]
```

선의 의미: IPS는 실제 네트워크 경로 중간에 직렬로 연결되어 악성 패킷을 직접 폐기하고 IDS는 스위치 미러링 포트를 통해 복사본을 수동 분석하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **트래픽 수집 센서** | 인라인 인터페이스(IPS) 또는 **TAP/SPAN 포트(IDS)로부터 패킷 캡처** | Sensor Interface |
| **패킷 정규화기 (Decoder)**| IP 단편화 재조합 및 **TCP 스트림 리어셈블리, 난독화 디코딩 수행** | Normalizer |
| **탐지 분석 엔진** | Snort/Suricata 룰 기반 **시그니처 매칭 및 이상 행위 통계 분석** | Inspection Engine |
| **능동 대응 제어기** | 위협 탐지 시 **패킷 드롭(Drop), TCP RST 주입 또는 경보 발행** | Action Controller |
| **하드웨어 바이패스 모듈**| IPS 장비 장애 시 **물리 릴레이 스위치를 직결하여 회선 유지(Fail-Open)** | Bypass Module |

#### 한줄 요약
- 트래픽 수집 센서, 패킷 정규화기, 탐지 분석 엔진, 능동 대응기, 하드웨어 바이패스가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **TCP Reset Injection**: IDS가 미러링 망에서 공격 탐지 시 공격자와 피해자 양단에 위조된 TCP RST 패킷을 주입하여 세션을 강제 종료시키는 기법.

</details>

```text
패킷 인입, 정규화 재조합, 위협 분석 및 IDS/IPS 대응 파이프라인
        │
   1. [원시 패킷 캡처] 네트워크 인터페이스로 인입되는 패킷 수신 (IPS: 직렬 / IDS: 미러링 복사본)
        │
   2. [패킷 정규화] IP 단편화 조각 재조합, TCP 시퀀스 정렬 및 다중 URL 인코딩 해제
        │
   3. [위협 시그니처 대조] Snort 룰셋 대조 및 통계적 프로파일링 이상 행위 판정
        │
   ├─ [정상 패킷으로 판정] ➔ 목적지 포트로 무지연 포워딩
   ▼
4. [악성 위협 탐지 시 정책 집행]
    ├─ [IDS 모드]: 침입 로그 생성 ➔ SIEM/SOC 관제 전송 및 필요 시 TCP RST 주입
    └─ [IPS 모드]: 해당 악성 패킷 즉각 폐기(Drop) ➔ 공격지 IP 임시 블랙리스트 차단
```

#### 한줄 요약
- 패킷 캡처 → 정규화 스트림 복원 → 시그니처/이상 탐지 → IDS 로깅 또는 IPS 실시간 드롭 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **IDS (침입 탐지)** vs **IPS (침입 방지)**.

</details>

| 비교 항목 | 침입 탐지 시스템 (IDS: Detection) | 침입 방지 시스템 (IPS: Prevention) |
|:---|:---|:---|
| **물리적 배치 방식** | **수동적 병렬 배치 (Out-of-Band / TAP, SPAN)** | **능동적 직렬 배치 (In-Line)** |
| **주요 동작 방식** | 패킷 복사본 분석 후 **로그 기록 및 경보(Alert) 발생** | 실제 패킷 검사 후 **악성 트래픽 실시간 폐기(Drop/Reject)** |
| **네트워크 지연 (Latency)**| **지연 없음 (0ms, 라이브 경로 외부 동작)** | **수 밀리초 검사 지연 발생 (1~5ms)** |
| **장비 장애 시 영향** | **가용성 무영향 (네트워크 정상 가동 유지)** | **통신 단절 위험 (단일 장애점 SPOF 발생 가능)** |
| **오탐(False Positive) 영향**| 보안 관제사의 경보 피로도(Alert Fatigue) 증가 | **정상 고객 서비스 트랜잭션 차단 및 서비스 마비 장애**|
| **주요 권장 구축 영역** | **고가용성이 절대적인 금융 거래 코어망, 모니터링망** | **외부 침입 위협에 노출된 인터넷 경계망, DMZ 전면** |

#### 한줄 요약
- IDS는 가용성이 중요한 백본망 수동 감시용, IPS는 경계망 실시간 능동 방어용이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Phased Deployment (단계적 차단 배포)**: 신규 IPS 룰셋 적용 시 2~4주간 모니터링(Detection-Only) 모드로 선운영하여 오탐을 정제한 후 차단으로 전환하는 운영 프랙티스.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 신규 IPS 시그니처 과도 매칭으로 인한 **정상 비즈니스 트래픽 오탐(False Positive) 차단** | **신규 룰셋 적용 시 `2주간 모니터링(Alert-Only) 선운영 후 단계적 차단 전환`** | 오탐 서비스 다운타임 0% 달성 및 시그니처 정밀 튜닝 |
| 패킷 단편화 및 인코딩 조작을 통한 **IPS 시그니처 우회(Evasion) 공격** | **`세션 스트림 재조합 및 다중 인코딩 복원 정규화(Normalization) 엔진 강화`** | 단편화 우회 공격 100% 탐지 및 검사 사각지대 소거 |
| 인라인 IPS 하드웨어 고장/크래시로 인한 **사내망 전체 통신 단절(SPOF 장애)** | **전원/시스템 장애 시 물리 광스위치를 강제 직결하는 `하드웨어 바이패스(Fail-Open)`** 장착 | 인라인 보안 장비 고장 시에도 네트워크 가용성 100% 보장 |
| 암호화된 HTTPS 트래픽 내부의 공격 페이로드 미탐지 | **`SSL 복호화 장비(SSL Decryption Proxy)`와 IPS 연동** | 암호화 통신 내 익스플로잇 및 C2 시그니처 100% 가시화 |

#### 한줄 요약
- 단계적 배포로 오탐을 방지하고, 스트림 정규화로 Evasion을 막으며, 하드웨어 바이패스로 SPOF를 방지한다.

## Ⅶ. 결론

- 네트워크 경계 및 내부망 침입 위협을 차단하는 **IDS 및 IPS 아키텍처는 가용성(Availability)과 보안성(Security)의 균형을 유지하는 핵심 통제 수단**이며, 실무 구현 시 **외부 경계망의 인라인 IPS 및 코어 백본망의 미러링 IDS 이원화, 하드웨어 바이패스(Fail-Open) 안전망 확보, 패킷 정규화 및 모니터링 기반 단계적 차단(Phased Deployment) 거버넌스**를 통합 구축하여 무결점 네트워크 침입 방어 환경 완성

#### 한줄 요약
- IDS와 IPS는 가용성 모니터링과 실시간 인라인 차단 및 바이패스 안전망을 결합하여 고신뢰 네트워크 침입 방어를 실현하는 핵심 시스템이다.