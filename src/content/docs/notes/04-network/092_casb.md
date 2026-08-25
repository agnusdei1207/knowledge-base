---
sidebar:
  order: 92
  label: "092. CASB 클라우드 접근 보안 브로커"
  badge:
    text: "기출 · 70%"
    variant: note
title: "클라우드 가시성 및 데이터 보호 : CASB (Cloud Access Security Broker)"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 92
extra:
  question_no: "92"
  source_status: "기출"
  source_history: "122회, 137회"
  priority: 70
  priority_note: "Gartner 4대 핵심 축(가시성, 컴플라이언스, 데이터 보안, 위협 방어) 및 Forward/Reverse Proxy, API 연동"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **CASB (Cloud Access Security Broker)**: 사용자 단말과 클라우드 SaaS 사이에 위치하여 가시성, 컴플라이언스, 데이터 보안, 위협 방어를 집행하는 보안 게이트웨이.
- **Shadow IT (섀도우 IT)**: 보안 부서의 승인 없이 임직원이 임의로 업무에 사용하는 비인가 클라우드 서비스로 인한 보안 사각지대.

</details>

- 정의/개념: 사용자-클라우드 간 트래픽을 인라인 프록시 및 API 연동으로 중계하여 **가시성 확보, 클라우드 DLP, 접근 통제 및 위협 방어를 집행하는 클라우드 보안 브로커**
- 배경/필요성: 멀티 SaaS 도입 확산 및 원격근무 증가로 인한 **비인가 섀도우 IT 난립, 데이터 외부 무단 공유·유출 및 클라우드 보안 사각지대 발생**

#### 한줄 요약
- Gartner 4대 기둥과 하이브리드 배치 모델을 통해 분산된 클라우드 데이터와 섀도우 IT를 통합 통제한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Gartner 4대 기둥**: 가시성(Visibility), 컴플라이언스(Compliance), 데이터 보안(Data Security), 위협 방어(Threat Protection).
- **UEBA (User and Entity Behavior Analytics)**: 정상 사용자의 접속 시간, 위치, 다운로드 패턴을 학습하여 계정 탈취 및 내부자 유출을 감지하는 이상 행위 분석.

</details>

- **Gartner 4대 핵심 기능 완벽 충족**: 가시성 확보, 컴플라이언스 준수, **데이터 손실 방지(클라우드 DLP), 위협 방어 일괄 제공**
- **3대 하이브리드 배치 모델 지원**: 사내 관리 단말(Forward), 개인 단말(Reverse), **스토리지 백엔드(API) 전방위 수용**
- **머신러닝 기반 이상 행위 탐지(UEBA)**: 비정상적 대량 다운로드 및 지리적 동시 접속 등 **계정 도용 실시간 격리**

#### 한줄 요약
- Gartner 4대 기능, 하이브리드 프록시/API 배치, UEBA 기반 이상 행위 탐지를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Forward vs Reverse vs API**: 관리 단말 인라인 통제(Forward), BYOD 인가 앱 통제(Reverse), 클라우드 저장 데이터 사후 감사(API).

</details>

```text
[CASB 하이브리드 배치 및 제어 아키텍처]
|-- Managed Endpoints (사내 관리 PC -> Forward Proxy: 전 트래픽 가로채기 & 섀도우 IT 차단)
|-- Unmanaged BYOD (개인 모바일 -> Reverse Proxy: IdP SAML 연동 & 웹 격리 다운로드 제한)
`-- CASB Core Security Engine
|   |-- SaaS Risk Catalog DB (수만 개 SaaS 애플리케이션 위험도 점수 평가)
|   |-- Cloud DLP Engine (파일 내 민감정보 정규식 매칭, DRM 암호화)
|   `-- UEBA Engine (비정상 행위 감지 및 실시간 세션 강제 종료)
`-- Cloud SaaS Backends (M365, Google Workspace, AWS S3: API 커넥터 비동기 권한 감사)
```

선의 의미: 관리/비관리 단말 트래픽이 프록시를 거치고 저장된 데이터는 백엔드 API로 지속 검사되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **Forward Proxy** | 관리 단말의 에이전트 기반 인라인 검사, **비인가 SaaS(Shadow IT) 차단** | Inline Mode |
| **Reverse Proxy** | 비관리 단말(BYOD)의 **인가 SaaS 접속 통제, 다운로드 제한 및 마스킹** | Clientless |
| **API 커넥터** | 백엔드 SaaS 감사 API 연동, **저장 데이터 DLP 검사 및 공유 링크 회수** | Out-of-Band |
| **위험 카탈로그 DB**| 수만 개 SaaS 앱의 **인증 체계, 암호화 수준 등 위험도 점수(0~100) 제공** | Risk Scoring |
| **클라우드 DLP 엔진**| 콘텐츠 딥 스캐닝, **개인정보/소스코드 매칭, DRM 암호화 및 유출 차단**| Data Protection |

#### 한줄 요약
- Forward Proxy, Reverse Proxy, API 커넥터, 위험 카탈로그 DB, DLP 엔진이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Revoke Public Share (공유 링크 회수)**: 임직원이 대외비 문서를 '전체 공개' 링크로 잘못 설정했을 때 CASB가 API를 통해 이를 감지하고 즉각 비공개로 강제 전환하는 기능.

</details>

```text
CASB SaaS 위험 평가, 인라인 DLP 검사 및 API 공유 회수 파이프라인
        │
   1. [SaaS 업로드 시도] 사용자가 사내 단말에서 외부 SaaS로 파일 업로드 시도 시 CASB 인입
        │
   2. [SaaS 위험도 판정] 카탈로그 DB와 대조하여 인가(Sanctioned) 여부 및 위험 점수 평가
        │
   3. [클라우드 DLP 검사] 파일 페이로드를 디코딩하여 개인정보, 소스코드 패턴 정밀 스캔
        │
   ├─ [DLP 정책 위반 시] ➔ 업로드 즉각 차단, 파일 자동 DRM 암호화 및 보안팀 경보
   ▼
4. [정상 파일 업로드] 클라우드 SaaS로 업로드 허용 ➔ 백엔드 API 모니터링 큐에 등록
        │
   ▼
5. [비인가 공유 링크 회수] 저장 후 비인가 퍼블릭 공유 링크 생성 감지 시 API로 즉시 회수(Revoke)
```

#### 한줄 요약
- SaaS 인가 판정 → DLP 심층 검사 → 인라인 업로드 차단 → 백엔드 API 스캔 → 퍼블릭 링크 자동 회수 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Forward Proxy vs Reverse Proxy vs API-Based**: 3대 배치 모델별 장단점 비교.

</details>

| 비교 항목 | 순방향 프록시 (Forward Proxy) | 역방향 프록시 (Reverse Proxy) | API 연동 (API-Based) |
|:---|:---|:---|:---|
| **적용 대상 단말** | **사내 관리 단말 (에이전트 설치)** | **비관리 단말 (BYOD, 개인 단말)** | **단말 무관 (클라우드 스토리지 전수)** |
| **통제 대상 서비스**| **모든 SaaS (인가 + 비인가 섀도우 IT)**| **인가된 SaaS (Sanctioned Cloud)** | **인가된 특정 SaaS (API 지원 앱)** |
| **데이터 검사 시점**| **실시간 인라인 (업로드/다운로드)** | **실시간 인라인 (다운로드 통제)** | **비동기 사후 검사 (저장 데이터 전수)** |
| **핵심 장점** | **섀도우 IT 100% 탐지 및 사전 차단** | 에이전트 무설치(Agentless) BYOD 통제| 실시간 망 부하 제로, 과거 데이터 감사 |
| **주요 한계** | 에이전트 배포 및 유지보수 부담 | 비인가 클라우드 접근 통제 불가 | 실시간 업로드 즉시 차단 불가 (지연) |

#### 한줄 요약
- Forward는 섀도우 IT 실시간 통제, Reverse는 BYOD 인가 앱 통제, API는 저장 데이터 사후 감사에 쓰인다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Contextual Access (조건부 접근 제어)**: 접속 단말의 신뢰도(관리/비관리 기기), 네트워크 위치, 사용자 역할에 따라 SaaS 내 읽기 전용(View-Only) 강제 등 차등 권한을 부여하는 정책.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 사내 단말에서 개인 웹하드로의 기밀 도면 유출 (섀도우 IT 활성화) | **`Forward Proxy 기반 인라인 DLP 검사` 및 미인가 SaaS 차단** | 섀도우 IT 경로 완전 차단 및 기밀 데이터 실시간 유출 방어 |
| 개인 BYOD 단말을 통한 SaaS 접속 시 기밀 문서 로컬 다운로드 | **`Reverse Proxy 기반 조건부 접근(View-Only 강제)`** 적용 | 비관리 단말 내 로컬 파일 저장 원천 차단 및 가상 뷰어 열람 |
| SaaS 내 부주의로 인한 대외비 파일 '전체 공개(Public Link)' 노출 | **`API 커넥터 기반 실시간 파일 권한 스캐닝 및 자동 회수(Revoke)`** | 비인가 공유 링크 즉시 무력화 및 데이터 주권 확보 |
| 클라우드 API 호출 쿼터(Rate Limit) 초과로 인한 감사 지연 | **웹훅(Webhook) 이벤트 드리븐 방식 및 델타 증분 스캔** 적용 | API 호출량 80% 절감 및 실시간 감사 반응성 유지 |

#### 한줄 요약
- Forward 프록시로 섀도우 IT를 막고, Reverse 프록시로 BYOD를 통제하며, API 연동으로 퍼블릭 링크 노출을 방어한다.

## Ⅶ. 결론

- 멀티 SaaS 클라우드 도입에 따른 데이터 분산과 섀도우 IT 위협에 대응하기 위해 **Gartner 4대 기둥 기반의 CASB 아키텍처를 필수 구축**하되, 완벽한 보안 통제를 실현하기 위해 **Forward Proxy(관리 단말 통제), Reverse Proxy(BYOD 조건부 접근), API Integration(저장 데이터 거버넌스)**을 결합한 하이브리드 배치 모델을 적용하고, 이를 **SASE/SSE 프레임워크**로 통합하여 클라우드 중심의 일관된 데이터 보호 체계 완성

#### 한줄 요약
- CASB는 프록시와 API 연동을 통해 섀도우 IT를 가시화하고 클라우드 내 민감 데이터를 보호하는 표준 보안 게이트웨이다.