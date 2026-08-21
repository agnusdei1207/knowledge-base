---
sidebar:
  order: 29
  label: "029. MITRE ATT&CK 프레임워크 (MITRE ATT&CK)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "사이버 공격자 TTP 지식 기반 및 보안 검증 : MITRE ATT&CK (Tactics, Techniques, and Procedures)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-security"
weight: 29
extra:
  question_no: "029"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "14개 전술(Tactics), 기법/서브기법(Techniques/Sub-techniques), 데이터 소스, 적대적 모의실행(Adversary Emulation)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **MITRE ATT&CK(Adversarial Tactics, Techniques, and Common Knowledge)**: 실제 관측된 사이버 침해사고 사례를 바탕으로 공격자가 사용하는 **전술(Tactics: 목적/Why)**, **기법(Techniques: 수단/How)**, **절차(Procedures: 구체적 실행 사례)** 를 14개 전술 카테고리와 수백 개의 세부 기법 행렬(Matrix)로 체계화한 글로벌 개방형 위협 지식 베이스.
- **탐지 커버리지(Detection Coverage)**: 조직이 보유한 보안 모니터링 시스템(SIEM/EDR)이 ATT&CK 매트릭스 상의 공격 기법(Technique ID) 중 몇 개를 실질적으로 탐지 및 방어할 수 있는지를 정량적으로 평가한 보안 방어 역량 지표.

</details>

- 정의/개념: 단편적 침해 지표(IOC: IP, Hash) 중심 방어의 한계를 극복하기 위해, 공격자의 행동 패턴인 **TTP(전술·기술·절차)** 를 행렬 매트릭스로 표준화하고 **데이터 소스(Data Sources)** 및 **적대적 모의실행(Adversary Emulation)** 을 통해 방어 실효성을 검증하는 **위협 중심 보안 아키텍처**
- 배경/필요성: 공격자가 파일 해시나 C2 IP를 지속적으로 변경하더라도 변하지 않는 본질적인 공격 기법(예: LSASS 메모리 덤프, PowerShell 스크립트 실행)을 식별하여 지속 가능한 탐지 룰셋을 개발할 요구

#### 한줄 요약
- 공격자의 목적(전술)과 수단(기법)을 매트릭스로 표준화하여 TTP 기반 위협 헌팅과 방어 커버리지를 검증한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **전술(Tactics) vs 기법(Techniques)**:
  - **전술(Tactics / 14개)**: 공격자의 전술적 목표(예: 초기 접근, 권한 상승, 방어 회피, 횡적 이동).
  - **기법(Techniques / T-ID)**: 해당 전술 목표를 달성하기 위해 사용하는 구체적인 해킹 기술(예: T1059 Command and Scripting Interpreter).
  - **서브기법(Sub-techniques)**: 기법의 세부 구현 기술(예: T1059.001 PowerShell).

</details>

- **3계층 구조화 (Tactics $\rightarrow$ Techniques $\rightarrow$ Sub-techniques)**: 거시적 공격 목적에서 미시적 명령어 수준까지 계층적으로 세분화
- **실제 위협 행위자(Threat Groups) 프로파일링**: APT28, APT29, Lazarus 등 실제 그룹이 사용한 TTP 절차(Procedures)와 매핑
- **환경별 다중 도메인 매트릭스 제공**: Enterprise(Windows, Linux, macOS, Cloud), Mobile(Android, iOS), ICS/OT(산업제어시스템)

#### 한줄 요약
- 3계층 구조화, 실전 APT 그룹 TTP 매핑, 환경별 도메인 매트릭스, 데이터 소스 기반 탐지 설계를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **데이터 소스(Data Sources) & 데이터 컴포넌트(Data Components)**: 특정 공격 기법을 탐지하기 위해 시스템과 네트워크에서 반드시 수집해야 하는 원천 텔레메트리 로그 항목(예: `Process: Process Creation`, `File: File Modification`, `Network Traffic: Network Connection Creation`).

</details>

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ [ MITRE ATT&CK 지식 체계 (Knowledge Architecture) ]                     │
│  ├─ 1. 대상 도메인 선정: Enterprise Matrix (OS, Cloud, Identity)        │
│  │                                                                      │
│  ├─ 2. 전술 계층 (Tactics / 14대 목표: TA0001 ~ TA0040)                 │
│  │     └─ [ Recon ➔ Initial Access ➔ ... ➔ Lateral Movement ➔ Impact ]   │
│  │                                                                      │
│  ├─ 3. 기법 및 서브기법 (Techniques: T1059 / Sub-techniques: T1059.001)│
│  │                                                                      │
│  └─ 4. 탐지 및 완화 가이드 (Detection & Mitigation)                      │
│       ├─ 필수 데이터 소스 (Data Sources: Process Creation / Event ID 4688)│
│       └─ 시스템 완화 대책 (Mitigations: PowerShell Constrained Language)│
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (실제 환경 탐지 룰 구현 및 검증)
                                     ▼
[ SIEM / EDR 탐지 룰셋 구현 ] ──▶ [ Atomic Red Team 모의실행 ] ──▶ [ 커버리지 검증 완료 ]
```

선의 의미: ATT&CK 매트릭스에서 도메인과 전술/기법을 선정하고, 요구되는 데이터 소스를 수집하여 SIEM/EDR 탐지 규칙을 개발한 후 모의실행으로 커버리지를 검증하는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **전술 (Tactics / 14종)** | 공격자의 공격 단계별 전술적 목적(Why) 분류 (TA0001~TA0040) | 14 Tactics |
| **기법 (Techniques / T-ID)** | 전술 목표를 달성하기 위한 구체적인 실행 기술(How) 정의 (T1000 시리즈) | Techniques |
| **서브기법 (Sub-techniques)** | 상위 기법의 운영체제별 세부 구현 방식 정의 (T1059.001 등) | Sub-ID |
| **데이터 소스 (Data Sources)**| 해당 기법을 감지하기 위해 수집해야 하는 필수 이벤트 로그 명시 | Telemetry |
| **완화책 (Mitigations)** | 공격 기법 실행을 시스템 아키텍처 수준에서 사전에 무력화하는 설정 가이드 | M-ID |

#### 한줄 요약
- 전술(Why), 기법(How), 서브기법, 데이터 소스(로그), 시스템 완화책이 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **적대적 모의실행(Adversary Emulation / Atomic Red Team)**: 특정 APT 공격 그룹이 사용하는 실제 TTP 스크립트를 자동화 도구를 통해 방어 대상 시스템에서 직접 실행함으로써, 보안 장비(EDR/SIEM)의 탐지 경보 및 차단 동작이 정상적으로 작동하는지 실증하는 보안 검증 프랙티스.

</details>

```text
1. [위협 인텔리전스 분석] 자사 산업군을 표적으로 하는 주요 APT 그룹의 공격 기법(T-ID) 우선순위 도출
            │
            ▼
2. [데이터 소스 식별 및 수집] 해당 T-ID 탐지에 필요한 엔드포인트 로그(Sysmon/Windows Event ID) 수집 파이프라인 구성
            │
            ▼
3. [탐지 규칙 개발] SIEM/EDR 상에 Sigma/YARA-L 기반의 행위 탐지 상관분석 룰셋 구현
            │
            ▼
4. [적대적 모의실행 검증] Atomic Red Team 프레임워크를 사용하여 대상 시스템에서 해당 T-ID 공격 스크립트 실행
            │
            ├─ [경보 미발생 / 탐지 실패] ➔ 데이터 소스 누락 보완 및 탐지 룰셋 튜닝
            ▼
5. [탐지 성공 실증] 실제 관제 화면에서 SIEM/EDR 알람 발생 확인 ➔ ATT&CK Navigator 매트릭스에 방어 성공 검증 등록
```

**동작 원리**

1. **위협 기반 스코핑**: CTI 보고서를 통해 조직 위험도가 높은 핵심 TTP 목록 도출
2. **로그 인프라 정렬**: Sysmon Event ID 1(프로세스 생성), ID 3(네트워크 연결) 등 필수 데이터 확보
3. **규칙 정밀화**: 오탐(False Positive)을 억제하고 이상 행위를 포착하는 정밀 상관분석 룰 작성
4. **실행 기반 실증**: 공격 코드를 안전한 파라미터로 격리 실행하여 탐지 센서의 동작 여부 판정
5. **정량적 갭 분석**: 미탐지 영역을 시각화(ATT&CK Navigator)하여 차기 보안 투자 및 정책 개선에 반영

#### 한줄 요약
- 위협 T-ID 선정, 데이터 소스 수집, 탐지 규칙 구현, Atomic 모의실행 검증, 커버리지 매트릭스 등록 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **ATT&CK 3대 도메인 매트릭스 비교**: 기업 IT 및 클라우드(Enterprise), 모바일 기기(Mobile), 산업제어망(ICS/OT)의 비교.

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

- **관찰 편향(Observation Bias)과 룰 개수 지표의 오류**: ATT&CK 매트릭스를 채우기 위해 구현하기 쉬운 단순 룰(예: `whoami` 실행 탐지)만 대량으로 등록하여 매트릭스를 인위적으로 색칠하고, 정작 실제 고위험 TTP(LSASS 덤프 등)에 대한 실질적 탐지 검증을 누락하는 보안 운영 오류.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 수천 개의 SIEM 탐지 룰을 배포했으나 실제 공격 발생 시 **경보 미발생으로 인한 침해 탐지 실패** | **Atomic Red Team 기반 자동화된 적대적 모의실행(Continuous Emulation) 상시 검증** | 탐지 룰의 실효성 100% 실증 및 탐지 실패 사각지대 즉각 제거 |
| 단순 기법 중심 매트릭스 채우기에 치중하여 **자사 위협 환경에 부합하지 않는 룰만 양산하는 오류** | **사이버 위협 인텔리전스(CTI) 기반 표적 공격 그룹(APT) 맞춤형 TTP 우선순위화** | 자사 위협에 직결된 핵심 공격 경로에 보안 리소스 100% 집중 |
| 엔드포인트 보안 툴 간 공격 명칭 파편화로 인한 **보안 관제(SOC) 및 사고대응(IR) 협업 지연** | **전사 보안 이벤트 및 인시던트 티켓에 ATT&CK Technique ID(T-ID) 태깅 의무화** | 보안 조직 간 표준화된 커뮤니케이션 확립 및 대응 속도 극대화 |

#### 한줄 요약
- 모의실행으로 룰 실효성을 검증하고, CTI로 TTP 우선순위를 정하며, T-ID 표준화로 대응 속도를 극대화한다.

## Ⅶ. 결론

- 글로벌 사이버 보안의 표준 언어로 자리잡은 **MITRE ATT&CK 프레임워크 아키텍처**는 단편적 정적 방어에서 벗어나 공격자의 행위 중심 능동 방어를 실현하는 핵심 인프라이며, 실무 구현 시 **위협 인텔리전스(CTI) 기반 주요 T-ID 도출**, **필수 데이터 소스 수집 및 정밀 탐지 룰 개발**, **적대적 모의실행(Adversary Emulation) 기반 실증 커버리지 검증**을 통합 추진하여 정량적이고 신뢰할 수 있는 엔터프라이즈 위협 방어 체계를 완성

#### 한줄 요약
- 전술(Why)과 기법(How)의 매트릭스 분류 및 모의실행 검증을 통해 TTP 기반 능동 보안 커버리지를 완성한다.
