---
sidebar:
  order: 92
  label: "092. CASB 클라우드 접근 보안 브로커 (CASB)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "CASB 클라우드 접근 보안 브로커 (CASB)"
date: "2026-08-13T18:22:00+09:00"
tags: ["notes-network"]
weight: 92
extra:
  question_no: "092"
  source_status: "기출"
  source_history: "122회, 137회"
  priority: 70
  priority_note: "설계•비교형: 122•137회 CASB 반복"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **클라우드 접근 보안 중개(CASB, Cloud Access Security Broker)**: 온프레미스 사용자와 클라우드 서비스(SaaS/IaaS) 사이에 위치하여 접근 가시성 확보, DLP, 위협 방어, 규정 준수 정책을 통합 집행하는 보안 솔루션.
- **섀도 IT(Shadow IT)**: 중앙 IT 부서 승인과 통제 없이 사용자가 임의로 사용하는 클라우드 서비스 및 소프트웨어.
- **서비스형 소프트웨어(SaaS, Software as a Service)**: 클라우드 기반으로 응용 소프트웨어를 구독형 서비스로 제공하는 모델.
- **CASB 보안 중개 체계(CASB Security Brokerage Framework)**: 가시성, 데이터 보안, 위협 방어, 컴플라이언스의 4대 핵심 Pillar를 기반으로 통제하는 체계.
- **계정/자료 유출 비가시성(Account & Data Leakage Invisibility)**: 미승인 클라우드 사용으로 인해 기업 기밀 및 계정 정보 유출 현황을 모니터링하지 못하는 보안 사각지대 문제.

</details>

- 정의/개념: 온프레미스와 클라우드 전단에서 가시성 및 보안 정책을 집행하는 **CASB 보안 중개 체계(CASB Security Brokerage Framework)**.
- 배경/필요성: **섀도 IT(Shadow IT)** 범람 및 미승인 **SaaS** 사용 확대에 따른 **계정/자료 유출 비가시성(Account & Data Leakage Invisibility)** 해결.

#### 한줄 요약

- 멀티 클라우드 및 SaaS 이용 시 인가/미인가 서비스의 접근 모니터링, DLP 통제 및 보안 정책 통합 집행.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **데이터 유출 방지(DLP, Data Loss Prevention)**: 콘텐츠 식별 및 정규표현식 매칭을 통해 중요 기밀의 무단 외부 전송 및 공유를 차단하는 기술.
- **순방향 프록시(Forward Proxy)**: 사용자 단말에서 클라우드로 나가는 아웃바운드 트래픽을 중계하여 실시간 트래픽을 감시/통제하는 방식.
- **응용 프로그래밍 인터페이스(API, Application Programming Interface)**: CASB가 클라우드 사업자의 API를 직접 호출하여 저장된 데이터와 공유 설정을 사후 점검하는 연동 방식.
- **행위별 정책(Behavior-based Policy)**: 사용자 신원, 접속 단말 상태, 데이터 민감도, 사용 서비스 등 Context를 결합하여 차등적 접근 권한을 부여하는 정책.
- **프록시 연동(Proxy Integration)**: 세션 통로에 인라인 배치되어 트래픽을 실시간 감시 및 차단하는 모드.
- **API 연동(API Integration)**: 에이전트 없이 클라우드 서비스의 백엔드 API와 연동하여 정적 데이터 및 권한 설정을 모니터링하는 모드.

</details>

- **행위별 정책(Behavior-based Policy)**: 사용자, 단말, 데이터 등급, 서비스 위험도 등 Context 결합 통제.
- **프록시 연동(Proxy Integration)**: 인라인 실시간 세션 및 트래픽 유출 통제.
- **API 연동(API Integration)**: 클라우드 백엔드 **API** 기반 정적 저장 데이터 감시 및 사후 통제.

#### 한줄 요약

- 인라인 프록시의 실시간 차단 능력과 API 방식의 사후 저장 데이터 모니터링을 상호 보완 적용.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **접근 중개기(Access Broker)**: Proxy 및 API 기반으로 인바운드/아웃바운드 세션 및 저장 데이터를 수신/파싱하는 구성요소이다.
- **CASB 정책 엔진(CASB Policy Engine)**: 수집된 트래픽 및 신원/단말/데이터 위험도를 기반으로 차단/격리/허용 조치를 판단하는 엔진이다.
- **클라우드 위험 카탈로그(Cloud Risk Catalog)**: 수천 개 이상의 SaaS 서비스 보안 등급 및 위험도를 사전에 평가하여 관리하는 DB이다.
- **사용자•단말(User & Endpoint)**: 클라우드 리소스에 접근하여 데이터를 업로드/다운로드하는 사용자 및 접속 기기이다.
- **신원•자료•위험 저장소(Identity, Data & Risk Repository)**: IAM, DLP 패턴, SaaS 위험도 정책 정보가 저장된 DB이다.
- **클라우드 서비스(Cloud Service)**: CASB 통제 대상이 되는 SaaS, PaaS, IaaS 인프라 환경이다.

</details>

```text
CASB
├─ 사용자•단말
├─ 접근 중개기
├─ CASB 정책 엔진
├─ 신원•자료•위험 저장소
└─ 클라우드 서비스
```

선의 의미: 접근 중개기가 사용자•단말과 클라우드 서비스 사이에 위치하여 트래픽을 중계하고, CASB 정책 엔진이 신원/자료/위험 DB 기반으로 정책을 집행하는 구조이다.

정책 엔진은 **클라우드 위험 카탈로그**를 참조하여 미승인 SaaS 접속 여부를 자동 식별한다.

| 구성요소 | 책임 |
|:---|:---|
| 사용자/단말(User & Endpoint) | 클라우드 서비스 접속 요청 및 데이터 트래픽 생성 |
| 접근 중개기(Access Broker) | 인라인 Proxy 및 API로 트래픽/데이터 수집 및 모니터링 |
| 신원/자료/위험 저장소(Repository) | 신원 ID, DLP 규칙, SaaS 위험도 Catalog 제공 |
| CASB 정책 엔진(Policy Engine) | Context 기반 접근 허용, 차단, 암호화, 격리 결정 |
| 클라우드 서비스(Cloud Service) | 최종 사용자 요청을 전달받아 비즈니스 기능 제공 |

#### 한줄 요약

- 접근 중개기를 거친 트래픽을 정책 엔진이 Context 정보(신원, 단말, SaaS 위험도)와 비교하여 통제 조치 집행.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **격리•공유 회수(Quarantine & Share Revocation)**: 민감 데이터 유출 위험 감지 시 외부 공유 링크를 삭제하고 격리소로 이동시키는 조치이다.
- **역방향 프록시(Reverse Proxy)**: 외부 단말에서 내부/인가된 클라우드 서비스로 진입하는 인바운드 세션을 트래픽 제어하는 방식이다.
- **SaaS 사용 증거 전달(SaaS Usage Telemetry Transfer)**: 네트워크 트래픽 로그, Agent, API로부터 SaaS 접근 로그를 수집하는 단계이다.
- **서비스 위험 분류(Service Risk Classification)**: 접근 대상 SaaS의 위험 등급(Sanctioned vs Unsanctioned)을 판별하는 단계이다.
- **자료•행위 맥락 전달(Data & Behavior Context Transfer)**: 사용자 신원, 단말 보안 상태, 데이터 민감도를 정책 엔진으로 전달하는 단계이다.
- **정책 조치 결정(Policy Action Decision)**: 전달받은 Context를 바탕으로 허용, 차단, DLP 암호화, 공유 회수를 판정하는 단계이다.
- **세션•저장물 집행(Session & Storage Enforcement)**: 판정된 보안 정책을 인라인 프록시 세션 차단 또는 API 권한 삭제로 실행하는 단계이다.

</details>

```text
클라우드 접속•저장물 점검 요청
      │
      ▼
1. SaaS 사용 증거 전달
      │
      ▼
2. 서비스 위험 분류
      │
      ▼
3. 자료•행위 맥락 전달
      │
      ▼
4. 정책 조치 결정
      ├─ 허용: 제한 조건으로 접근
      ├─ 차단: 세션 거부
      └─ 위험 자료: 격리•공유 회수
                     │
                     ▼
5. 세션•저장물 집행
                     │
                     ▼
접근•조치 결과 반환
```

### 동작 원리

1. **SaaS 사용 증거 전달**: 로그•프록시•API에서 사용 증거 수집
2. **서비스 위험 분류**: 위험 카탈로그로 승인 여부 판정
3. **자료•행위 맥락 전달**: 신원•단말•민감도를 정책 엔진에 제공
4. **정책 조치 결정**: 허용•차단•격리•공유 회수 확정
5. **세션•저장물 집행**: 프록시와 API로 판정 결과 실행

#### 한줄 요약

- 로그/트래픽 수집 후 SaaS 위험도 및 데이터 민감도를 정밀 판정하여 차단, 암호화, 외부 공유 회수 집행.

## Ⅴ. 종류 및 비교

| CASB 연동 방식 | **순방향 프록시(Forward Proxy)** | **역방향 프록시(Reverse Proxy)** | **API 연동(API Integration)** |
|:---|:---|:---|:---|
| 적용 기준 | 기업 관리 단말의 SaaS 아웃바운드 통제 | 비관리/개인 단말의 인가 SaaS 접속 통제 | 사후 정적 저장 데이터 및 외부 공유 검사 |
| 핵심 특징 | 발신 세션 인라인 실시간 감시/차단 | IdP SSO 연계 인바운드 실시간 통제 | Agent 없이 클라우드 API 호출 사후 점검 |
| 한계 | 단말 Agent 설치 필요, SSL 복호화 병목 | 적용 가능 SaaS 한정, IdP 연동 필수 | API 호출 시차 존재, 실시간 세션 차단 불가 |

> 요약: 단말 관리 상태, 트래픽 방향, 실시간성 요구 수준에 맞춘 하이브리드 연동 구현.

#### 한줄 요약

- 관리 단말은 Forward Proxy, 비관리 단말 접속은 Reverse Proxy, 저장 데이터는 API 방식으로 상호 보완 적용.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **관리 단말(Managed Endpoint)**: 중앙 MDM/EDR에 의해 보안 정책 및 에이전트 통제가 적용된 기업 기기이다.
- **비관리 단말(Unmanaged Endpoint)**: 기업 보안 통제권 밖에 있는 개인 소유(BYOD) 또는 외부 기기이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| **관리 단말**의 개인 SaaS 중요 자료 업로드 | **순방향 프록시** 및 **DLP** 연동 | 아웃바운드 섀도 IT 민감 데이터 유출 차단 |
| 이미 생성된 민감 데이터의 사후 외부 노출 | **API 연동** 기반 **격리•공유 회수** | 저장 파일 주기적 스캔 및 외부 공유 링크 즉시 삭제 |
| **비관리 단말**의 기업 SaaS 접근 시 정보 유출 | **역방향 프록시(Reverse Proxy)**로 다운로드 및 캡처 제한 | BYOD 환경에서의 데이터 다운로드 차단 및 가시성 확보 |

#### 한줄 요약

- 연동 모드별 하이브리드 구성 및 DLP 연계를 통해 클라우드 환경 전반의 데이터 유출 방지.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **CASB 연동 방식 선택(CASB Integration Pattern Selection)**: 서비스 특성, 단말 통제 수준, 실시간 차단 필요성에 따라 Forward Proxy, Reverse Proxy, API 방식을 최적으로 조합하는 커스터마이징 전략이다.

</details>

- 관리 단말은 **순방향**, 비관리 단말은 **역방향**, 저장물은 **API** 선택.

#### 한줄 요약

- 섀도 IT 가시성 확보 및 하이브리드 연동(Proxy+API) 기반 클라우드 통합 데이터 보안 체계 구축.
