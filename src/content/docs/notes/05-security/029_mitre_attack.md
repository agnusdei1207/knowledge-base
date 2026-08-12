---
sidebar:
  order: 29
  label: "029. MITRE ATT&CK 프레임워크 (MITRE ATT&CK)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "MITRE ATT&CK 프레임워크 (MITRE ATT&CK)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-security"
weight: 29
extra:
  question_no: "029"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "137회 기출이며 탐지규칙•헌팅 운영으로 확장 가능함"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **적대적 전술•기술•공통 지식(Adversarial Tactics, Techniques, and Common Knowledge, ATT&CK)**: 실제 발생한 사이버 공격자들의 전술(Tactics), 기술(Techniques), 절차(Procedures)를 기반으로 위협 행위를 매트릭스 형태로 체계화한 MITRE의 공개 지식 프레임워크.
- **커버리지(Coverage)**: 조직의 보안 모니터링 환경에서 특정 ATT&CK 기법(Technique)을 실제 데이터 소스(Log) 및 탐지 규칙(Rule)으로 검증 감지할 수 있는 방어 범위 및 유효 비율.

</details>

- 정의/개념: 실제 발생한 사이버 공격자들의 전술(Tactics), 기술(Techniques), 절차(Procedures)를 기반으로 위협 행위를 매트릭스 형태로 체계화한 MITRE의 공개 **ATT&CK 프레임워크**
- 배경/필요성: 시그니처 및 단순 IOC(Hash, IP) 기반 모니터링 한계 극복, 실제 공격자 행동(TTP) 기반의 객관적 방어 **커버리지(Coverage)** 측정 및 위협 헌팅 가이드 요구

#### 한줄 요약

- 실제 공격자의 TTP(Tactics, Techniques, Procedures)를 행렬 매트릭스로 체계화하여 위협 헌팅 및 탐지 커버리지를 검증하는 지식 지침

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **전술(Tactics)**: 공격자가 해당 행동을 수행하는 목적(Why)을 나타내는 고차원적 14개 단계 (예: Initial Access, Persistence 등).
- **기법(Techniques)**: 전술적 목적을 달성하기 위한 수단(How)을 정의한 공격 기술 (예: Phishing, Process Injection 등).
- **서브기법(Sub-techniques)**: 기법을 특정 OS, 애플리케이션 및 환경 기술 수준으로 세분화한 하위 공격 기법 (예: Spearphishing Attachment 등).
- **절차 사례(Procedures)**: 특정 APT 그룹(APT29, Lazarus 등)이나 악성코드가 해당 기법을 실제로 적용하여 악용한 구체적 관찰 사례.
- **기업 도메인(Enterprise Domain)**: Windows, Linux, macOS, Cloud(AWS, Azure, GCP, SaaS), Identity 환경을 망라한 기업 IT 분석 매트릭스.
- **모바일 도메인(Mobile Domain)**: Android 및 iOS 디바이스 특화 위협 및 권한 오용을 분석하는 매트릭스.
- **산업 제어 시스템 도메인(ICS Domain)**: SCADA, PLC 및 OT 산업 제어 프로세스 특화 위협을 분석하는 매트릭스.

</details>

- **전술(Tactics)** → **기법(Techniques)** → **서브기법(Sub-techniques)**으로 계층화된 구조적 위협 체계 제공
- **절차 사례(Procedures)**를 통해 기법별 완화 통제(Mitigations) 및 데이터 소스(Data Sources) 기반 탐지 전략 제시
- **Enterprise**, **Mobile**, **ICS** 도메인을 구분하여 환경별 위협 기법 매트릭스 수립

#### 한줄 요약

- Tactics, Techniques, Sub-techniques의 계층구조, Enterprise/Mobile/ICS 도메인 구별 및 실세계 위협 시나리오(Procedures) 제공

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **완화(Mitigation)**: 해당 ATT&CK 기법 공격 성공률 및 피해 노출을 줄이기 위해 적용하는 보안 정책 및 시스템 통제 설정 (M1042 등).
- **탐지 전략(Detection Strategy)**: 기법 실행 증적(Process, Network, Registry 등)을 감지하기 위해 수집해야 할 필수 데이터 소스(Data Sources).
- **분석 규칙(Analytic / Detection Rules)**: 수집된 데이터 소스에서 특정 TTP 행위를 식별하기 위해 작성된 쿼리 및 상관분석 데이터 논리 (Sigma, YARA, SIEM Rules).

</details>

`	ext
MITRE ATT&CK 지식 구조
└─ 도메인•행렬
   └─ 전술
      └─ 기법•서브기법
         ├─ 절차 사례•검증
         └─ 완화•탐지 전략
`

가지의 의미: 도메인 매트릭스, 전술 목적, 세부 기법, 실제 사례 및 완화/탐지 전략 연동 책임을 표현한 구조

| 구성요소 | 책임 |
|:---|:---|
| 도메인•행렬 | Enterprise, Mobile, ICS 환경별 전술 및 기법 행렬 매트릭스 구성 |
| 전술 | 14개 전술(Tactics) 단계를 통한 공격 목적 분류 가이드 |
| 기법•서브기법 | 세부 공격 기술(Techniques/Sub-techniques) 단위의 고유 식별자(T-ID) 정의 |
| 절차 사례•검증 | 실제 APT 그룹의 악용 절차(Procedures) 사례 및 레드팀 시뮬레이션 증적 제공 |
| 완화•탐지 전략 | Mitigations 통제 정책 및 Data Source 중심의 분석 규칙(Detection Rule) 매핑 |


#### 한줄 요약

- 도메인/매트릭스, 전술(Tactics), 기법(Techniques), 절차 사례(Procedures), 완화 통제(Mitigations) 및 탐지 전략 아키텍처

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **위협 헌팅(Threat Hunting)**: ATT&CK 기법 매트릭스 기반 가설을 수립하여 SIEM/EDR 로그를 능동 탐색하고 미탐 지점을 발견하는 활동.
- **모의공격 검증(Adversary Emulation / Red Teaming)**: Atomic Red Team 등 도구를 통해 특정 TTP 공격을 실제 실행하고 EDR/SIEM이 탐지하는지 검증하는 시뮬레이션.
- **위협 행동 선택**: 자산 및 위협 시나리오 기반 우선 대응 대상 Technique(T-ID)선정 단계.
- **데이터•분석 규칙 구현**: 해당 기법을 감지하기 위한 필수 Data Source 수집 및 탐지 규칙(Rule) 개발 단계.
- **모의공격•헌팅 검증**: 모의공격 실행을 통해 EDR 알람 발생 및 SOC 대응 실효성 입증 단계.
- **증적•커버리지 갱신**: 검증 완료된 T-ID를 조직의 탐지 **커버리지(Coverage)** 지도에 실증 등록하는 단계.

</details>

`	ext
자산•위협 시나리오
        │
        ▼
1. 위협 행동 선택
        │
        ▼
2. 데이터•분석 규칙 구현
        │
        ▼
3. 모의공격•헌팅 검증
        ├─ 미탐•지연 ── 데이터•규칙 보완
        └─ 탐지•대응 성공
                │
                ▼
4. 증적•커버리지 갱신
        └─ 위협 변화 시 행동 재선정
`

### 동작 원리

1. **위협 행동 선택**: 타깃 인프라 위협 시나리오에 부합하는 ATT&CK 주요 기법(T-ID) 선정
2. **데이터•분석 규칙 구현**: 필요한 데이터 소스(Process Creation, Network Flow 등) 수집 및 SIEM/EDR 탐지 규칙 구현
3. **모의공격•헌팅 검증**: Atomic Red Team 모의공격 실행을 통한 룰 탐지 유효성 및 미탐/지연 구간 식별
4. **증적•커버리지 갱신**: 실제 감지 입증된 기법에 대해 조직의 ATT&CK 탐지 커버리지 매트릭스 업데이트 완결


#### 한줄 요약

- 위협 기법 선정, 데이터 소스 및 탐지 분석 규칙(Rule) 개발, 에뮬레이션/헌팅 검증 및 탐지 커버리지(Coverage) 최신화 흐름

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **운영 기술(Operational Technology, OT)**: 산업 공정, 에너지, 제조 시설을 제어하는 실시간 제어 인프라.

</details>

| ATT&CK 도메인 | **Enterprise Domain** | **Mobile Domain** | **ICS Domain (OT)** |
|:---|:---|:---|:---|
| 주요 대상 환경 | OS (Windows, Linux, Mac), Cloud, Identity | Android, iOS 이동통신 단말 | SCADA, PLC, HMI, OT 제어망 |
| 특화 전술/기법 | Privilege Escalation, Lateral Movement, Exfiltration | Network Effects, Device Access, App Analysis | Inhibit Response Function, Impair Process Control |
| 주요 데이터 소스 | Syslog, EDR, CloudTrail, Active Directory Logs | Mobile Device Management (MDM), App Logs | Network Passive TAP, Modbus/DNP3 Logs |

> 요약: 대상 시스템 환경(Enterprise vs Mobile vs ICS)에 부합하는 ATT&CK 도메인 선택 및 적용

#### 한줄 요약

- 기업 IT/클라우드용 Enterprise, 모바일 기기/앱용 Mobile, 산업 제어 시스템용 ICS 도메인의 영역별 기법 매트릭스 비교

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **ATT&CK 기법 ID(Technique ID)**: T1059(Command and Scripting Interpreter) 등 기법별로 부여된 글로벌 공통 식별 기호.
- **관찰 편향(Observation Bias)**: 매트릭스의 특정 인기 기법에만 매몰되어 실제 자사 환경에 특화된 위협 및 비인기 TTP를 간과하는 분석적 오류.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 보안 커뮤니케이션 혼선 | **ATT&CK Technique ID (T-ID) 기반 용어 표준화** | SOC, 분석팀, 레드팀 간 명확한 공유 언어 확립 |
| 단순 체크리스트형 커버리지 | **모의공격 에뮬레이션(Adversary Emulation) 실증 검증** | 단순 룰 존재가 아닌 실질적 탐지/차단 작동 입증 |
| 특정 인기 TTP **관찰 편향** | **위협 인텔리전스(CTI) 기반 우선순위 산정** | 실제 타깃 위협 그룹(APT) TTP 위주 효율적 대응 |

#### 한줄 요약

- ATT&CK Technique ID 기반 공유, 체크리스트 채우기식 극복을 위한 모의공격 에뮬레이션 검증 및 데이터 소스 기반 우선순위 통제

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **커버리지 인정 기준(Coverage Validation Criteria)**: 탐지 규칙의 양적 수량이 아닌, 실제 모의공격 및 수집 데이터 소스를 통해 실증 감지된 기법만을 커버리지로 승인하는 기준.

</details>

- 단순 탐지 룰 존재가 아닌 실제 수집 데이터 및 모의공격(Adversary Emulation) 실전 검증으로 실효 **커버리지** 인정

#### 한줄 요약

- ATT&CK Technique ID 통일, 모의공격 에뮬레이션 검증, 데이터 소스 확보 및 위협 헌팅 연동 기반 실증적 보안 체계 구축 필수