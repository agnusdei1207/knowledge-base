---
sidebar:
  order: 92
  label: "092. CASB 클라우드 접근 보안 브로커"
  badge:
    text: "기출 · 70%"
    variant: note
title: "클라우드 서비스 가시성 및 데이터 보호 : CASB (Cloud Access Security Broker)"
date: "2026-08-22T08:15:00+09:00"
tags: ["notes-network"]
weight: 92
extra:
  question_no: "092"
  source_status: "기출"
  source_history: "122회, 137회"
  priority: 70
  priority_note: "Gartner 4대 핵심 축(가시성, 컴플라이언스, 데이터 보안, 위협 방어) 및 Forward/Reverse Proxy, API 연동"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **CASB(Cloud Access Security Broker)**: 온프레미스 사용자 및 엔드포인트 디바이스와 복수의 클라우드 서비스(SaaS, PaaS, IaaS) 사이에 위치하여, 기업의 보안 정책(가시성, 컴플라이언스, 데이터 보안, 위협 방어)을 일관되게 적용·집행하는 클라우드 특화 보안 게이트웨이 (Gartner 정의).
- **섀도우 IT(Shadow IT)**: 기업 IT 부서 및 보안 담당자의 승인 없이 임직원이 임의로 업무에 활용하는 비인가 SaaS/클라우드 서비스(개인 웹하드, 메신저 등)로 인해 발생하는 보안 사각지대.

</details>

- 정의/개념: 사용자-클라우드 간 트래픽을 인라인 프록시(**Forward/Reverse Proxy**) 및 **API 커넥터(API Integration)** 로 중계하여, 섀도우 IT 가시성 확보, 클라우드 DLP, 사용자 행위 분석(UEBA) 및 악성코드 유입을 차단하는 **클라우드 접근 통제 브로커**
- 배경/필요성: SaaS 도입 확산과 원격근무 증가로 인해 기존 네트워크 경계 방화벽의 가시성을 벗어난 HTTPS 암호화 클라우드 트래픽을 통한 기업 기밀 데이터 유출 및 컴플라이언스 위반을 방어할 요구

#### 한줄 요약
- 사용자와 클라우드 서비스 사이에서 섀도우 IT 가시성을 확보하고 데이터 유출 및 위협을 통제하는 클라우드 보안 브로커이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Gartner CASB 4대 핵심 기둥(4 Pillars)**:
  1. **가시성(Visibility)**: 섀도우 IT 탐지 및 클라우드 사용 현황 감사
  2. **데이터 보안(Data Security)**: 클라우드 DLP, 암호화, DRM 연동 및 접근 제어
  3. **위협 방어(Threat Protection)**: 비정상 계정 행위(UEBA) 탐지 및 클라우드 악성코드 차단
  4. **컴플라이언스(Compliance)**: GDPR, HIPAA, ISMS 등 규제 준수 모니터링
- **하이브리드 배치(Hybrid Deployment)**: 실시간 업로드 차단을 위한 인라인 프록시와 저장된 데이터의 소급 감사를 위한 비동기 API 연동의 결합 구조.

</details>

- **섀도우 IT 완벽 식별 및 위험도 평가**: 전 세계 수만 개 SaaS 애플리케이션의 보안성(인증, 암호화, 데이터 보존)을 점수화(Risk Scoring)하여 등급별 통제
- **정밀한 클라우드 DLP(Data Loss Prevention)**: 개인정보(주민번호, 카드번호), 영업기밀 정규식 및 지문(Fingerprint) 매칭 기반 업로드/다운로드 차단
- **사전 차단 및 사후 감사(API) 통합**: 실시간 프록시 통제와 더불어 클라우드 내부의 퍼블릭 링크 자동 회수 및 악성 파일 격리 동시 수행

#### 한줄 요약
- 4대 핵심 축(가시성, 컴플라이언스, DLP, 위협 방어), 섀도우 IT 위험 평가, 프록시/API 결합 통제를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **순방향 프록시(Forward Proxy)**: 관리 단말(사내 PC)에 에이전트를 설치하여 모든 아웃바운드 인터넷 트래픽을 가로채 비인가 SaaS 접속 및 파일 업로드를 차단하는 방식.
- **역방향 프록시(Reverse Proxy)**: 비관리 단말(BYOD, 개인 스마트폰)이 회사의 인가된 클라우드(IdP/SSO)에 접속할 때 게이트웨이로 트래픽을 강제 우회시켜 다운로드를 제한하는 방식.
- **API 연동(API-based Scanning)**: SaaS 서비스(M365, Google Workspace, Box)의 백엔드 API를 직접 호출하여 저장된 데이터의 권한 설정, 공유 링크(Public Link) 및 악성코드를 비동기 스캔하는 방식.

</details>

```text
[ 1. 사내 관리 단말 (Managed PC) ] ────▶ (Forward Proxy: 전 트래픽 가로채기) ──┐
                                                                              │
[ 2. 외부 비관리 단말 (BYOD Mobile) ] ──▶ (Reverse Proxy: IdP SAML 연동) ──────┼─▶ [ CASB 통합 보안 엔진 ]
                                                                              │    ├─ 섀도우 IT 위험도 분석
                                                                              │    ├─ 클라우드 DLP 검사
                                                                              │    └─ UEBA 이상 행위 탐지
                                                                              │               │
[ 3. 클라우드 SaaS 스토리지 ] ◀─────── (API Integration: 비동기 감사/격리) ─────┘               ▼
     (M365, AWS S3, Google Drive)                                                [ 인가된 SaaS 서비스 접근 ]
```

선의 의미: 관리/비관리 단말 트래픽이 프록시를 거치고, 저장된 데이터는 백엔드 API로 지속 검사되는 CASB 하이브리드 아키텍처

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **Forward Proxy** | 관리 단말의 에이전트 기반 인라인 검사, 비인가 SaaS(Shadow IT) 차단 | Inline Mode |
| **Reverse Proxy** | 비관리 단말(BYOD)의 인가 SaaS 접속 통제, 다운로드 제한 및 마스킹 | Clientless |
| **API 커넥터** | 백엔드 SaaS 감사 API 연동, 기존 저장 데이터 DLP 검사 및 퍼블릭 공유 링크 회수 | Out-of-Band |
| **위험 카탈로그 DB** | 수만 개 SaaS 애플리케이션의 인증 체계, 암호화 수준 등 위험도 점수 제공 | Risk Scoring |
| **클라우드 DLP 엔진** | 콘텐츠 딥 스캐닝, 키워드/정규식 매칭, DRM 암호화 및 유출 차단 | Data Protection |

#### 한줄 요약
- Forward Proxy, Reverse Proxy, API 커넥터, 위험 카탈로그 DB, DLP 엔진이 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **공유 링크 회수(Revoke Public Share)**: 사용자가 실수 또는 고의로 기밀 파일의 공유 범위를 '전체 공개(Anyone with link)'로 변경했을 때, CASB가 API를 통해 이를 감지하고 즉각 비공개로 전환하거나 관리자에게 격리 조치하는 프로세스.

</details>

```text
1. 사용자가 사내 단말에서 외부 SaaS(Google Drive)로 업무 파일 업로드 시도 ➔ CASB 인라인 프록시 인입
            │
            ▼
2. CASB가 목적지 SaaS의 신뢰도(Risk Score)를 위험 카탈로그 DB와 대조하여 인가 여부(Sanctioned) 판정
            │
            ▼
3. 파일 페이로드를 디코딩하여 클라우드 DLP 규칙(개인정보, 소스코드, 대외비 패턴) 심층 스캐닝
            │
            ├─ [DLP 위반 탐지] ➔ 업로드 즉각 차단, 파일 자동 DRM 암호화 및 보안팀 알람
            ▼
4. [정상 파일 판정] ➔ 클라우드 SaaS로 업로드 허용 ➔ 백엔드 API 연동 모니터링 등록
            │
            ▼
5. 저장 후 비인가 퍼블릭 공유 링크 생성 감지 시 API를 통해 공유 권한 즉각 강제 회수(Revoke)
```

**동작 원리**

1. **트래픽 인터셉트**: 에이전트 또는 PAC 파일 설정을 통해 사용자 웹 트래픽을 CASB로 유도
2. **SaaS 위험 평가**: 접속 대상 서비스가 사내 승인된 애플리케이션인지 평가
3. **콘텐츠 실시간 검사**: 첨부 파일 내부의 민감 데이터 패턴 검출
4. **인라인 통제 집행**: 위험 등급에 따라 파일 업로드 차단, 알림, 화면 워터마크 적용
5. **사후 비동기 거버넌스**: API 폴링 및 웹훅을 통해 공유 설정 변경을 실시간 감시하고 불법 공유 무력화

#### 한줄 요약
- SaaS 인가 판정, DLP 심층 검사, 인라인 업로드 차단, 백엔드 API 스캔, 퍼블릭 링크 자동 회수 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Forward Proxy vs Reverse Proxy vs API 모드**: CASB의 3대 배치 모델별 기술적 특성과 적용 범위 비교.

</details>

| 비교 항목 | 순방향 프록시 (Forward Proxy) | 역방향 프록시 (Reverse Proxy) | API 연동 (API-Based) |
|:---|:---|:---|:---|
| **적용 대상 단말** | **사내 관리 단말 (에이전트 설치)** | **비관리 단말 (BYOD, 개인 단말)** | **단말 무관 (클라우드 스토리지 전수)** |
| **통제 대상 서비스** | **모든 SaaS (인가 + 비인가 섀도우 IT)**| **인가된 SaaS (Sanctioned Cloud)** | **인가된 특정 SaaS (API 지원 앱)** |
| **데이터 검사 시점** | **실시간 인라인 (업로드/다운로드)** | **실시간 인라인 (다운로드 통제)** | **비동기 사후 검사 (저장 데이터 전수)** |
| **주요 장점** | 섀도우 IT 100% 탐지 및 사전 차단 | 에이전트 무설치(Agentless) BYOD 통제 | 실시간 망 부하 제로, 과거 데이터 감사 |
| **주요 한계** | 에이전트 배포 및 유지보수 부담 | 비인가 클라우드 접근 통제 불가 | 실시간 업로드 즉시 차단 불가 (지연) |

#### 한줄 요약
- Forward는 섀도우 IT 실시간 통제, Reverse는 BYOD 인가 앱 통제, API는 저장 데이터 사후 감사에 쓰인다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **BYOD 데이터 잔존(BYOD Residual Risk)**: 직원이 개인 스마트폰으로 회사 M365나 이메일에 접속하여 문서를 열람/다운로드한 후, 해당 기기가 분실되거나 퇴사 시 기밀 데이터가 기기에 영구 잔존하는 보안 위험.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 사내 관리 단말에서 개인 웹하드로의 기밀 설계도면 유출 (섀도우 IT 활성화) | **Forward Proxy 기반 인라인 DLP 검사** 및 미인가 SaaS 업로드 차단 | 섀도우 IT 경로 완전 차단 및 기밀 데이터 실시간 유출 100% 방어 |
| 개인 BYOD 단말을 통한 인가 SaaS 접속 시 기밀 문서 로컬 다운로드 및 유출 | **Reverse Proxy 기반 조건부 접근 제어(Contextual Access)** 적용 (View-Only 강제) | 비관리 단말 내 로컬 파일 저장 원천 방지 및 클라우드 가상 뷰어 열람 |
| SaaS 내 임직원의 부주의로 인한 대외비 파일 '전체 공개(Public Link)' 노출 | **API 커넥터 기반 실시간 파일 권한 스캐닝 및 자동 공유 회수(Revoke)** 구성 | 외부에 노출된 비인가 공유 링크 즉시 무력화 및 데이터 주권 확보 |

#### 한줄 요약
- Forward 프록시로 섀도우 IT를 막고, Reverse 프록시로 BYOD를 통제하며, API 연동으로 퍼블릭 링크 노출을 방어한다.

## Ⅶ. 결론

- 멀티 SaaS 클라우드 도입에 따른 데이터 분산과 섀도우 IT 위협에 대응하기 위해 **Gartner 4대 기둥 기반의 CASB 아키텍처**를 필수 구축하되, 완벽한 보안 통제를 실현하기 위해 **Forward Proxy(관리 단말 통제)**, **Reverse Proxy(BYOD 조건부 접근)**, **API Integration(저장 데이터 거버넌스)** 을 결합한 하이브리드 배치 모델을 적용하고, 이를 **SASE/SSE 프레임워크**로 통합하여 클라우드 중심의 일관된 데이터 보호 체계를 완성

#### 한줄 요약
- Forward, Reverse 프록시와 API 연동을 결합한 CASB를 통해 섀도우 IT 가시성과 클라우드 데이터 보안을 실현한다.
