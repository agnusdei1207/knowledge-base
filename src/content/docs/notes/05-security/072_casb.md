---
sidebar:
  order: 72
  label: "072. CASB 클라우드 접근 보안 브로커 (Cloud Access Security Broker)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "CASB 클라우드 접근 보안 브로커 (Cloud Access Security Broker)"
date: "2026-08-13T20:26:00+09:00"
tags:
  - "notes-security"
weight: 72
extra:
  question_no: "072"
  source_status: "기출"
  source_history: "122회, 137회"
  priority: 70
  priority_note: "122•137회 반복된 SaaS 데이터•접근 통제 핵심임"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **클라우드 접근 보안 브로커(Cloud Access Security Broker, CASB)**: 온프레미스와 클라우드 인프라 또는 사용자 단말과 클라우드 애플리케이션 사이에 위치하여 중앙 보안 정책을 인라인/API 기반으로 중계•집행하는 보안 솔루션이다.
- **서비스형 소프트웨어(Software as a Service, SaaS)**: 클라우드 공급자가 운영하는 완성형 소프트웨어 서비스(Salesforce, M365 등) 모델이다.

</details>

- 정의/개념: SaaS 접근•데이터를 중계 통제하는 **CASB**
- 배경/필요성: SaaS 확산은 **그림자 IT•민감정보 유출** 유발

#### 한줄 요약

- 사내외 사용자와 SaaS 서비스 사이에서 가시성, DLP, 위협 방어, 규정 준수 정책을 통합 집행하는 중계 보안 제어 솔루션이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **클라우드 발견(Cloud Discovery)**: 네트워크 방화벽/SWG 로그 분석을 통해 사내에서 사용 중인 수천 개 SaaS의 종류와 위험도를 자동 탐지하는 기능이다.
- **그림자 IT(Shadow IT)**: 중앙 IT/보안 부서의 승인 없이 사용자들이 임의로 구독•사용하는 위험 클라우드 앱 및 자산이다.
- **프록시(Proxy / Forward & Reverse Proxy)**: 클라이언트와 SaaS 간 패킷 통로에 위치해 SSL/TLS 트래픽을 복호화하고 실시간 트래픽을 중계•차단하는 기술이다.
- **응용 프로그래밍 인터페이스(Application Programming Interface, API)**: SaaS 제공자가 공개한 REST API를 활용해 저장된 데이터, 설정, 외부 공유 권한을 비대면 백그라운드 탐지하는 연동 기술이다.
- **데이터 유출 방지(Data Loss Prevention, DLP)**: 개인정보, 금융정보, 핵심 자산의 클라우드 업로드 및 외부 공유를 식별해 암호화•격리•차단하는 기술이다.

</details>

- **클라우드 발견**으로 사내 **그림자 IT** 사용 현황을 자동 가시화하고 서비스 위험도(Risk Rating)를 정량 평가한다.
- 실시간 트래픽 차단용 **프록시**(Forward/Reverse)와 저장 데이터 탐지용 **API** 연동 기술을 혼합(Hybrid)하여 적용한다.
- 인라인 **DLP**를 통해 단말 환경(BYOD vs 관리 단말) 및 트래픽 맥락에 따라 실시간 다운로드 차단, 암호화, DRM 연동 조치를 실행한다.

#### 한줄 요약

- 그림자 IT 자동 발견, 프록시/API 하이브리드 배치, 맥락 기반 DLP 조치를 통해 클라우드 데이터 유출을 차단한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **정책 엔진(Policy Engine)**: 신원, 기기 무결성, 접속 위치, 데이터 민감도, 사용 행위를 대조해 통제 조치를 결정하는 중앙 판단 모듈이다.
- **서비스 위험(Service Risk Rating)**: SaaS 서비스의 규정 준수, 데이터 암호화 지원 여부, 보안 사고 이력을 기반으로 계산한 위험 점수이다.
- **예외 증적(Exception Audit Log)**: 업무상 허용된 예외 정책 적용 건에 대해 승인 사유, 만료일, 사용 이력을 암호화 보존한 감사 기록이다.

</details>

```text
                        [정책 엔진·신호]
                         /            \
                 [클라우드 발견]  [프록시·API 집행] -- [SaaS]
                         \            /                 /
                         [위협·운영 분석]
```

선의 의미: 클라우드 발견과 위협 분석 신호를 정책 엔진으로 전달하고, 인라인 프록시/API 집행 모듈이 SaaS 패킷 및 데이터를 통제하는 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| 클라우드 발견 | **클라우드 발견**엔진을 통해 네트워크 로그를 수집하고 SaaS 앱 식별 및 **서비스 위험** 평가 |
| 정책 엔진·신호 | **정책 엔진**이 IAM, 단말 무결성, 트래픽 콘텍스트를 수집하여 허용/차단/암호화/MFA 결정 |
| 프록시·API 집행 | Forward/Reverse 프록시를 통한 인라인 차단 및 API 커넥터를 통한 백그라운드 스토리지 정밀 검사 |
| SaaS | 정책 집행 대상인 멀티테넌트 SaaS 애플리케이션 |
| 위협·운영 분석 | UEBA 기반 사용자 이상 행위 탐지, 봇 공격 차단 및 **예외 증적** 무결성 보존 |

#### 한줄 요약

- 정책 엔진의 맥락 평가에 따라 프록시의 실시간 인라인 패킷 차단과 API 기반 저장 데이터 감시를 병행 집행한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **인라인 검사(Inline Inspection)**: Forward/Reverse 프록시 패스를 통해 트래픽을 실시간 인터셉트하여 업로드/다운로드 트래픽을 즉시 제어하는 방식이다.
- **API 사후 점검(API Out-of-band Inspection)**: SaaS 서비스 API를 연계하여 이미 저장된 파일의 공유 상태, 맬웨어 감염, 오설정을 주기적으로 검사하는 방식이다.
- **보호 조치 결정(Protection Action Determination)**: 사용자 환경, 단말 상태, 데이터 등급에 맞춰 차단, 허용, 암호화, Watermarking, MFA를 선택 부여하는 단계이다.
- **다중 요소 인증(Multi-Factor Authentication, MFA)**: 미관리 BYOD 단말에서 접속 시 2차 추가 인증을 강제 구동하는 처리 과정이다.
- **신원•기기•데이터 맥락 확인(Identity, Device & Data Context Verification)**: 주체 신원, 단말 백신/OS 무결성, 파일 내 개인정보 포함 여부를 파악하는 단계이다.
- **인라인 DLP•접근 정책 집행(Inline DLP & Access Policy Enforcement)**: 실시간 데이터 흐름 상에서 차단 및 암호화 동작을 집행하는 단계이다.
- **저장 데이터•공유 정책 평가(Stored Data & Sharing Policy Evaluation)**: API로 SaaS 내 저장된 파일의 외부 전체 공유(Public Share) 정책 위반을 대조하는 단계이다.
- **위반 조치•정책 환류(Violation Remediation & Policy Feedback)**: 비인가 공유 권한을 회수하고 맬웨어 격리 후 탐지 시그니처를 업데이트하는 단계이다.

</details>

```text
실시간 요청 통제

[로그인·업로드·공유 요청]
          |
          v
1. 신원·기기·데이터 맥락 확인
          |
          v
2. 보호 조치 결정
          |
          v
3. 인라인 DLP·접근 정책 집행
          |
          v
[SaaS 응답]

저장 상태 사후 점검

[주기·사건 기반 API 점검]
          |
          v
[저장 데이터·공유 정보 조회]
          |
          v
4. 저장 데이터·공유 정책 평가
          |
          v
5. 위반 조치·정책 환류
          |
          v
[공유 회수·격리 결과]
```

### 동작 원리

1. 신원•기기•데이터 맥락 확인: 신원•단말•민감도 추출
2. 보호 조치 결정: 허용•차단•암호화•MFA 선택
3. 인라인 DLP•접근 정책 집행: 민감정보 전송 실시간 차단
4. 저장 데이터•공유 정책 평가: 저장 파일•공개 공유 대조
5. 위반 조치•정책 환류: 공유 회수•맬웨어 격리

#### 한줄 요약

- 인라인 프록시 기반의 실시간 트래픽 차단과 API 연동 기반의 저장 데이터 사후 공유 권한 회수 절차로 보안을 완성한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **전송 계층 보안 검사 부담(Transport Layer Security Inspection Overhead, TLS Inspection Overhead)**: SSL/TLS 대용량 트래픽의 복호화 및 재암호화 처리에 따른 CASB 프록시 인프라 지연 및 성능 부하 현상이다.
- **로그 기반 발견(Log-based Discovery)**: 방화벽, SWG 로그를 오프라인/SIEM으로 수신하여 사내 SaaS 사용 현황 및 위험도만 측정하는 비간섭 분석 방식이다.

</details>

| CASB 구현 형태 | 로그 기반 발견 (Log-based) | Forward Proxy | Reverse Proxy | API 연동 (Out-of-band) |
|:---|:---|:---|:---|:---|
| 배치 방식 | 방화벽/SWG 로그 분석 | 사용자 단말 에이전트/PAC 설정 | SaaS DNS CNAME 변경 배치 | SaaS 제공자 REST API 연동 |
| 주요 기능 | 그림자 IT 시각화, 위험도 측정 | 전체 Web/SaaS 실시간 DLP | 인가된 SaaS 접근 실시간 DLP | 저장 파일 검사, 공유 권한 회수 |
| 핵심 장점 | 네트워크 영향 제로, 빠른 도입 | 미인가 SaaS 실시간 차단 가능 | 단말 에이전트 미설치(BYOD) 지원 | 네트워크 지연 zero, 무마찰 |
| 주요 한계 | 실시간 차단 불가능 | 에이전트 설치 필수, **TLS 검사 부담** | 미인가 SaaS 통제 불가 | 실시간 차단 불가(사후 조치) |

#### 한줄 요약

- 실시간 차단을 위한 Forward/Reverse 프록시와 지연 없는 저장을 탐지하는 API 방식을 혼합 적용(Hybrid CASB)한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **ISO/IEC 27017:2015**: 클라우드 서비스 환경의 거버넌스 및 고객/제공자의 보안 통제 요구사항 지침이다.
- **CSA CCM v4.1 (Cloud Security Alliance Cloud Controls Matrix v4.1)**: 17개 도메인의 197개 통제 항목으로 구성된 글로벌 클라우드 보안 프레임워크이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 클라우드 데이터 통제 기준 미비 | **ISO/IEC 27017:2015** 준용 | 클라우드 접근 및 암호화 통제 기준 정합성 확보 |
| SaaS 보안 평가 프레임워크 부재 | **CSA CCM v4.1** 매핑 | SaaS 서비스 위험도(Risk Rating)의 객관적 산출 |
| 프록시/API 방식 단일 배치의 한계 | Hybrid CASB (Proxy + API) 아키텍처 | 실시간 차단과 저장 데이터 감시의 **집행 사각지대** 제거 |

#### 한줄 요약

- ISO 27017 및 CSA CCM 프레임워크를 기반으로 SaaS 위험도를 평가하고, Hybrid CASB를 배치하여 집행 사각지대를 해소한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **집행 사각지대(Enforcement Blind Spot)**: 미인가 단말(BYOD), 모바일 앱, 비인가 SaaS 접속 시 프록시나 API 통제를 벗어나는 보안 가시성 공백 영역이다.

</details>

- **집행 사각지대**를 근본 제거하기 위해 **로그 기반 발견**, 인라인 **프록시**, 사후 **API 연동** 기법을 통합 구성한다.

#### 한줄 요약

- 실시간은 **프록시**, 저장 데이터는 **API 연동** 적용
