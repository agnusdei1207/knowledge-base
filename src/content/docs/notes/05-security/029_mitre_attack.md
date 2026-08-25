---
sidebar:
  order: 29
  label: "029. MITRE ATT&CK 프레임워크"
  badge:
    text: "기출 · 50%"
    variant: note
title: "사이버 공격자 TTP 지식 기반 및 보안 검증 : MITRE ATT&CK"
date: "2026-08-25T13:00:00+09:00"
tags:
  - "notes-security"
weight: 29
extra:
  question_no: "29"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "14개 전술(Tactics), 기법/서브기법(Techniques/Sub-techniques), 데이터 소스, 적대적 모의실행(Adversary Emulation)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **MITRE ATT&CK**: 실제 공격자의 전술(Tactics), 기법(Techniques), 절차(Procedures)를 14개 전술과 세부 기법 행렬로 체계화한 지식베이스.
- **Detection Coverage (탐지 커버리지)**: 보안 관제 시스템이 ATT&CK 매트릭스 상의 공격 기법 중 실질적으로 탐지 가능한 비율을 나타내는 보안 지표.

</details>

- 정의/개념: 실제 공격자의 전술(Why), 기법(How), 절차(TTP)를 체계화하여 **보안 탐지 룰을 개발하고 방어 역량을 정량 검증하는 행동 기반 프레임워크**
- 배경/필요성: 단순 IP/해시(IOC) 기반 시그니처 매칭의 **공격자 인프라 변형 시 탐지 무력화, 조직 내 보안 탐지 사각지대 정량 측정 불가**

#### 한줄 요약
- 공격자 행동(TTP) 매트릭스를 기반으로 보안 탐지 룰을 개발하고 적대적 모의실행으로 검증한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Tactics vs Techniques**: 공격자가 달성하려는 전술적 목표(Why)와 이를 실행하는 구체적인 기술 수단(How).
- **Adversary Emulation (적대적 모의실행)**: 실제 공격자 그룹(APT)의 TTP 스크립트를 방어 시스템에서 직접 실행하여 탐지 및 차단 동작을 실증하는 검증.

</details>

- **공격자 행동 양식(TTP) 중심 표준화**: 도구와 해시 변형과 무관하게 **공격자의 본질적 실행 행위(PowerShell 악용 등)를 구조화 분류**
- **정량적 보안 갭(Gap) 분석 제공**: ATT&CK Navigator 매트릭스 시각화를 통해 **조직의 탐지 사각지대 식별 및 보안 투자 우선순위 결정**
- **적대적 모의실행(Atomic Red Team) 연동**: 스크립트 기반 모의 공격을 수행하여 **SIEM/EDR 탐지 규칙의 실효성을 지속적 실증 검증**

#### 한줄 요약
- TTP 중심 표준화, 정량적 갭 분석 시각화, 적대적 모의실행(Atomic Red Team) 실증을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Data Sources (데이터 소스)**: 특정 공격 기법(T-ID)을 탐지하기 위해 반드시 수집해야 하는 엔드포인트/네트워크 원시 이벤트 로그.

</details>

```text
[MITRE ATT&CK 프레임워크 4계층 아키텍처]
|-- 1. Domain Layer (Enterprise / Mobile / ICS Matrix)
`-- 2. Tactics Layer (14대 전술 목표: Recon -> Initial Access -> Lateral Movement -> Impact)
`-- 3. Techniques & Sub-techniques (기법: T1059 / 서브기법: T1059.001 PowerShell)
`-- 4. Detection & Mitigation (필수 데이터 소스 Event ID 4688 & 시스템 완화책 M1038)
`-- SIEM/EDR Rule Implementation -> Atomic Red Team Emulation -> Coverage Validated
```

선의 의미: ATT&CK 매트릭스에서 도메인과 전술/기법을 선정하고 요구되는 데이터 소스를 수집하여 SIEM/EDR 탐지 규칙을 개발한 후 모의실행으로 커버리지를 검증하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **전술 (Tactics / 14종)** | 공격자의 공격 단계별 **전술적 목적(Why) 분류 (TA0001~TA0040)** | 14 Tactics |
| **기법 (Techniques / T-ID)**| 전술 목표를 달성하기 위한 **구체적인 실행 기술(How) 정의** | T1000 Series |
| **서브기법 (Sub-techniques)**| 상위 기법의 **운영체제별 세부 구현 방식 정의 (T1059.001 등)** | Sub-ID |
| **데이터 소스 (Data Sources)**| 해당 기법을 감지하기 위해 **수집해야 하는 필수 이벤트 로그 명시** | Telemetry |
| **완화책 (Mitigations)** | 공격 기법 실행을 **시스템 아키텍처 수준에서 사전 무력화하는 가이드** | M-ID |

#### 한줄 요약
- 전술(Why), 기법(How), 서브기법, 데이터 소스(로그), 시스템 완화책이 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Atomic Red Team**: 수백 개의 MITRE ATT&CK 기법을 1:1로 테스트할 수 있도록 설계된 오픈소스 독립 모의 공격 프레임워크.

</details>

```text
T-ID 선정, 데이터 소스 수집, 탐지 룰 구현 및 모의실행 검증 파이프라인
        │
   1. [위협 인텔리전스 분석] 자사 산업군 표적 APT 그룹의 공격 기법(T-ID) 우선순위 도출
        │
   2. [데이터 소스 수집] T-ID 탐지에 필요한 엔드포인트 로그(Sysmon/Event ID) 수집 파이프라인 구성
        │
   3. [탐지 규칙 개발] SIEM/EDR 상에 Sigma/YARA-L 기반 행위 탐지 상관분석 룰셋 구현
        │
   4. [적대적 모의실행] Atomic Red Team 프레임워크로 대상 시스템에서 T-ID 공격 스크립트 실행
        │
   ├─ [경보 미발생 / 탐지 실패] ➔ 데이터 소스 누락 보완 및 탐지 룰셋 튜닝
   ▼
5. [탐지 성공 실증] 관제 화면에서 SIEM/EDR 알람 발생 확인 ➔ ATT&CK Navigator 방어 검증 등록
```

#### 한줄 요약
- 위협 T-ID 선정 → 데이터 소스 수집 → 탐지 규칙 구현 → Atomic 모의실행 검증 → 커버리지 매트릭스 등록 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Enterprise Matrix** vs **Mobile Matrix** vs **ICS Matrix**.

</details>

| 도메인 영역 | Enterprise Matrix (기업 IT/Cloud) | Mobile Matrix (스마트폰) | ICS Matrix (산업제어시스템) |
|:---|:---|:---|:---|
| **적용 대상 인프라** | **Windows, Linux, macOS, AWS, M365, AD**| **Android, iOS 모바일 운영체제** | **SCADA, PLC, DCS, 발전/제조 제어망** |
| **핵심 위협 전술** | **권한 상승, 방어 회피, 횡적 이동, 유출** | **디바이스 접근 권한 획득, 네트워크 도청** | **제어 명령 조작, 안전 시스템(SIS) 무력화**|
| **핵심 탐지 데이터** | **EDR 프로세스 생성, 인증 이벤트, API 로그**| **MDM 로그, 앱 권한 요청, 기기 샌드박스** | **공학 워크스테이션 로그, 산업 프로토콜 패킷**|
| **대표 위협 행위자** | **Lazarus, APT29 (Cozy Bear), FIN7** | APT-C-23, Pegasus 스파이웨어 그룹 | **Sandworm (Industroyer), Volt Typhoon** |

#### 한줄 요약
- Enterprise는 기업 IT/클라우드, Mobile은 스마트폰 OS, ICS는 제조/발전 산업제어망에 특화된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Observation Bias (관찰 편향)**: 단순 룰(whoami 등)만 대량 등록하여 매트릭스를 인위적으로 채우고 실제 고위험 TTP 탐지 검증을 누락하는 보안 운영 오류.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 수천 개의 룰 배포에도 실제 공격 시 **경보 미발생으로 인한 침해 탐지 실패** | **`Atomic Red Team 기반 자동화된 적대적 모의실행(Continuous Emulation)` 상시 검증** | 탐지 룰 실효성 100% 실증 및 사각지대 제거 |
| 단순 기법 중심 매트릭스 채우기로 **자사 환경에 부합하지 않는 룰 양산** | **사이버 위협 인텔리전스(CTI) 기반 `표적 공격 그룹 맞춤형 TTP 우선순위화`** | 자사 위협에 직결된 핵심 공격 경로에 집중 |
| 보안 툴 간 공격 명칭 파편화로 인한 **보안 관제(SOC) 협업 지연** | **전사 보안 이벤트 및 인시던트 티켓에 `ATT&CK Technique ID(T-ID) 태깅 의무화`** | 보안 조직 간 표준 커뮤니케이션 확립 |
| 정상 관리 도구(PowerShell 등) 모니터링 시 과도한 오탐 경보 발생 | **`정상 업무 스크립트 화이트리스트 튜닝 및 부모-자식 프로세스 상관분석`** | 오탐 경보 80% 감축 및 관제 효율 극대화 |

#### 한줄 요약
- 모의실행으로 룰 실효성을 검증하고, CTI로 TTP 우선순위를 정하며, T-ID 표준화로 대응 속도를 극대화한다.

## Ⅶ. 결론

- 글로벌 사이버 보안의 표준 언어로 자리잡은 **MITRE ATT&CK 프레임워크 아키텍처는 단편적 정적 방어에서 벗어나 공격자의 행위 중심 능동 방어를 실현하는 핵심 인프라**이며, 실무 구현 시 **위협 인텔리전스(CTI) 기반 주요 T-ID 도출, 필수 데이터 소스 수집 및 정밀 탐지 룰 개발, 적대적 모의실행(Adversary Emulation) 기반 실증 커버리지 검증**을 통합 추진하여 정량적이고 신뢰할 수 있는 엔터프라이즈 위협 방어 체계 완성

#### 한줄 요약
- MITRE ATT&CK은 전술(Why)과 기법(How)의 매트릭스 분류 및 모의실행 검증을 통해 TTP 기반 능동 보안 커버리지를 완성하는 핵심 지식베이스다.