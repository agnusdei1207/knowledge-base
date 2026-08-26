---
sidebar:
  order: 72
  label: "072. CASB 클라우드 접근 보안 브로커 (Cloud Access Security Broker)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "SaaS 가시성 및 인라인/API 데이터 유출 방지 : CASB (Cloud Access Security Broker & Gartner 4대 기둥)"
date: "2026-08-26T14:48:22+09:00"
tags:
  - "notes-security"
weight: 72
extra:
  question_no: "072"
  source_status: "기출"
  source_history: "122회, 137회"
  priority: 70
  priority_note: "Gartner CASB 4대 핵심 기둥(가시성, 데이터 보안, 위협 방지, 컴플라이언스), 배치 모델(Forward Proxy, Reverse Proxy, Out-of-band API Connector, Log-based Discovery), 그림자 IT(Shadow IT) 및 DLP"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **CASB(Cloud Access Security Broker / Gartner 표준)**: 온프레미스 사내망 및 원격 근무자 단말과 멀티 클라우드 SaaS(Microsoft 365, Salesforce, Google Workspace 등) 애플리케이션 사이에 위치하여, 기업의 통합 보안 정책을 실시간 인라인(Inline) 및 비동기 API 기반으로 중계·집행하는 클라우드 보안 브로커 솔루션.
- **그림자 IT 및 비인가 데이터 유출(Shadow IT & Data Exfiltration Defect)**: 보안팀의 승인 없이 임직원이 임의의 퍼스널 SaaS(개인 Dropbox, Notion 등)를 업무에 활용하여 기업의 핵심 기밀과 개인정보가 외부로 무단 반출되는 가시성 및 통제 공백.

</details>

- 정의/개념: 가트너 CASB 4대 핵심 기둥인 **가시성(Visibility) $\rightarrow$ 데이터 보안(DLP/암호화) $\rightarrow$ 위협 방지(Malware/UEBA) $\rightarrow$ 컴플라이언스(Compliance)** 를 바탕으로, **Forward/Reverse Proxy 및 API Connector** 를 하이브리드로 결합하여 SaaS 데이터 생애주기를 통제하는 **엔터프라이즈 SaaS 보안 아키텍처**
- 배경/필요성: 경계 방화벽만으로는 **SaaS 내부 데이터 통제 불가**

#### 한줄 요약
- 가시성, DLP, 위협 방지, 컴플라이언스 4대 기둥과 하이브리드(Proxy+API) 배치를 통해 SaaS 데이터 유출을 완벽히 차단한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Gartner CASB 4대 핵심 기둥**:
  1. **가시성 (Visibility)**: 방화벽/SWG 로그를 분석하여 전사 Shadow IT 사용 현황 및 위험 점수(Risk Score) 가시화.
  2. **데이터 보안 (Data Security)**: 정밀 정규식/ML 기반 DLP를 통해 민감 데이터의 클라우드 업로드 차단 및 암호화.
  3. **위협 방지 (Threat Protection)**: 저장된 파일의 악성코드 스캔 및 계정 탈취(UEBA 이상 행위) 탐지.
  4. **컴플라이언스 (Compliance)**: HIPAA, GDPR, ISMS-P 등 규제 요구사항에 따른 SaaS 구성 점검.

</details>

- **하이브리드 듀얼 아키텍처 (Hybrid Deployment)**: 실시간 업로드/다운로드 차단을 위한 **인라인 프록시**와 저장 데이터 및 공유 링크 감시를 위한 **Out-of-band API 커넥터**의 결합
- **맥락 인식형 세분화 인가 (Context-Aware DLP)**: 관리 단말에서는 다운로드 허용, 비인가 개인 단말(BYOD)에서는 웹 뷰어 전용 열람 및 워터마크 강제
- **무마찰 사후 정화 (Out-of-band Remediation)**: SaaS API를 호출하여 외부에 '전체 공개'로 설정된 기밀 파일의 공유 링크를 실시간 자동 회수

#### 한줄 요약
- 4대 기둥 기반 통제, 프록시+API 하이브리드 배치, 맥락 인식 DLP, 비인가 공유 링크 자동 회수를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **CASB 4대 핵심 배치 모듈**:
  1. **Log-based Discovery**: 네트워크 로그 기반 SaaS 식별 및 위험도 측정.
  2. **Forward Proxy**: 에이전트 기반으로 모든 아웃바운드 SaaS 트래픽 인라인 검사.
  3. **Reverse Proxy**: DNS CNAME 변경을 통해 인가된 기업용 SaaS 트래픽만 중계 (BYOD 지원).
  4. **API Connector**: SaaS 공급자 REST API를 통해 저장 파일 검사 및 권한 자동 회수.

</details>

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 1. 엔드포인트 단말 계층 (Managed PC / Unmanaged BYOD) ]               │
│  ├─ 관리 단말: Forward Proxy Agent 설치 ➔ [ 전사 모든 SaaS 트래픽 검사 ] │
│  └─ 개인 단말(BYOD): IdP SSO 연동 ➔ Reverse Proxy로 트래픽 강제 리다이렉트│
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (실시간 인라인 트래픽)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 2. CASB 중앙 제어 엔진 (Inline Proxy & Policy Engine) ]               │
│  ├─ 실시간 SSL/TLS 복호화 및 맥락 분석 (사용자, 기기 Posture, 위치)     │
│  ├─ 인라인 DLP 엔진: 주민번호/소스코드 탐지 시 ➔ [ 파일 업로드 즉시 차단]│
│  └─ 워터마크 주입 및 DRM 암호화 자동 적용                               │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (정상 패킷 중계)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 3. 타깃 멀티 클라우드 SaaS (M365, Google Workspace, Salesforce) ]    │
│  ├─ 저장 파일 및 권한 변경 이벤트 발생                                   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (웹훅 이벤트 & 주기적 REST API 폴링)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 4. CASB API 커넥터 엔진 (Out-of-band API Connector Engine) ]          │
│  ├─ 저장 파일 멀웨어/랜섬웨어 실시간 스캔 및 격리                       │
│  └─ "전체 공개 공유 링크" 탐지 시 ➔ [ SaaS API 호출하여 공유 권한 즉각 회수]│
└─────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 인라인 프록시가 실시간 업로드/다운로드 트래픽을 가로채고, 백그라운드에서 API 커넥터가 저장된 데이터의 공유 상태를 교차 제어하는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **클라우드 디스커버리 엔진** | 방화벽/SWG 로그를 파싱하여 전사 그림자 IT 앱을 식별하고 위험 점수 산출 | Visibility |
| **중앙 정책 엔진** | 주체, 기기 무결성, 데이터 민감도를 대조하여 차단, 허용, 암호화, 워터마킹 결정 | Core Brain |
| **인라인 프록시 (Forward/Reverse)**| SSL 트래픽을 실시간 복호화하여 패킷 내 민감 데이터 업로드/다운로드 즉시 차단 | Data Plane (Inline)|
| **API 커넥터 (Out-of-band)**| SaaS 벤더 REST API를 호출하여 저장 파일 검사, 악성코드 격리, 공유 링크 자동 회수 | Data Plane (API) |
| **UEBA 행위 분석 엔진** | 평소와 다른 새벽 시간대 대용량 다운로드 등 비정상 계정 탈취 징후 탐지 | Threat Detection |

#### 한줄 요약
- 디스커버리 엔진, 중앙 정책 엔진, 인라인 프록시, API 커넥터, UEBA 분석기가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **CASB 인라인 DLP 및 API 정화 5단계 흐름**:
  1. 사용자 SaaS 접근 요청 및 맥락(신원/기기) 평가
  2. 인라인 프록시에서 실시간 트래픽 복호화 및 DLP 규칙 검사
  3. 기밀 데이터 업로드 시도 즉각 차단
  4. 백그라운드 API 커넥터가 저장 데이터 및 공유 링크 상시 감사
  5. 비인가 외부 공유 파일 탐지 시 공유 권한 즉각 박탈

</details>

```text
1. [SaaS 접속 및 맥락 분석] 사용자가 M365 접속 시도 ➔ CASB가 IdP 신원 및 단말 보안 상태(BYOD) 확인
            │
            ▼
2. [인라인 실시간 DLP 검사]
    ├─ 사용자가 고객 개인정보 1만 건이 포함된 Excel 파일 업로드 시도
    ├─ CASB 프록시가 파일 본문 검사(Deep Packet Inspection) ➔ 주민번호 정규식 탐지
    └─ [업로드 패킷 즉각 드롭(Block) & 사용자 화면에 보안 경고 팝업]
            │
            ▼
3. [정상 트래픽 안전 중계] 악성/기밀 유출 없는 정상 요청은 M365 클라우드로 트래픽 통과
            │
            ▼
4. [비동기 API 저장 데이터 감사 (Out-of-band)]
    ├─ 타 사용자가 사내 OneDrive 파일에 대해 "링크가 있는 모든 사람에게 공개" 설정 변경
    └─ M365 웹훅 이벤트를 수신한 CASB API 커넥터가 정책 위반 인지
            │
            ▼
5. [공유 링크 자동 회수] CASB가 M365 REST API를 호출하여 공개 권한을 즉시 "사내 특정 부서 한정"으로 강제 원복
```

**동작 원리**

1. **SaaS 접속 및 맥락 분석**: 신원과 단말 상태 평가
2. **인라인 실시간 DLP 검사**: 민감 데이터 업로드 차단
3. **정상 트래픽 안전 중계**: 허용 요청을 SaaS로 전달
4. **비동기 API 저장 데이터 감사**: 파일·공유 상태 점검
5. **공유 링크 자동 회수**: 정책 위반 권한 원복

#### 한줄 요약
- 접속 맥락 분석, 인라인 DLP 검사, 트래픽 중계, API 비동기 감사, 공유 링크 자동 회수 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **CASB 4대 구현 방식 비교**: 로그 분석(Discovery), Forward Proxy, Reverse Proxy, Out-of-band API Connector의 비교.

</details>

| 비교 항목 | 로그 기반 발견 (Discovery) | Forward Proxy | Reverse Proxy | API 커넥터 (Out-of-band) |
|:---|:---|:---|:---|:---|
| **배치 방식** | **방화벽/SWG 로그 수동/자동 수집** | **사용자 단말 전용 에이전트/PAC** | **IdP SSO 연동 및 DNS CNAME 변경**| **SaaS 벤더 REST API 연동** |
| **실시간 차단 가능 여부**| **불가 (사후 가시성 전용)** | **완벽 가능 (모든 SaaS 업로드 차단)**| **가능 (인가된 특정 SaaS 한정)** | 불가 (사후 격리 및 권한 회수) |
| **단말 제약 (BYOD)** | 제약 없음 | 에이전트 설치 필수 (BYOD 불가) | **에이전트 미설치 단말(BYOD) 지원** | **단말 무관 (SaaS 백엔드 통제)**|
| **네트워크 성능 지연**| **전혀 없음 (0ms)** | SSL 복호화로 인한 레이턴시 발생 | 프록시 중계 지연 발생 | **전혀 없음 (Out-of-band)** |
| **저장 데이터 감사** | 불가 | 불가 | 불가 | **완벽 지원 (멀웨어/공유 링크)** |

#### 한줄 요약
- Forward Proxy는 전사 차단, Reverse Proxy는 BYOD 차단, API는 저장 데이터 감사, Log Discovery는 가시성을 제공한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Hybrid CASB Architecture**: 인라인 프록시의 실시간 제어 능력과 API 커넥터의 사후 정화 능력을 결합하여, 성능 저하 없이 SaaS 보안 사각지대를 완전히 제거하는 엔터프라이즈 최적 구현 아키텍처.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 단일 프록시 배치 시 대용량 SSL 복호화로 인한 **네트워크 병목 발생 및 미인가 BYOD 단말 통제 불가 사각지대** | **인가 SaaS는 Reverse Proxy/API로, 비인가 SaaS는 Forward Proxy로 제어하는 Hybrid CASB 구축** | 네트워크 지연(Latency) 80% 감축 및 BYOD 포함 전사 SaaS 가시성 100% 확보 |
| 과도하게 엄격한 정규식 DLP 정책으로 인해 **정상적인 비즈니스 업무 파일 업로드가 오차단(False Positive)되는 장애** | **머신러닝 기반 문서 지문(Document Fingerprinting) 인식 도입 및 초기 모니터링 후 단계적 차단 전환** | DLP 오탐률 0.1% 이하 최소화 및 비즈니스 연속성 100% 보장 |
| 사용자가 사내 SaaS 파일에 대해 비인가 외부 공유 링크를 생성하여 **회사 기밀 데이터가 인터넷에 영구 노출되는 사고** | **SaaS 웹훅 이벤트 연동 기반 CASB API 커넥터의 실시간 비인가 공유 링크 탐지 및 즉각적 자동 회수** | 외부 노출 위험 노출 시간 1분 이내 단축 및 사후 데이터 거버넌스 완결 |

#### 한줄 요약
- 하이브리드 CASB로 성능과 사각지대를 잡고, 문서 지문으로 오탐을 줄이며, API로 비인가 공유 링크를 즉시 회수한다.

## Ⅶ. 결론

- 실시간 유출은 **인라인 프록시**, 저장 데이터는 **API 커넥터** 선택

#### 한줄 요약
- 4대 기둥과 하이브리드(Proxy+API) 배치를 결합하여 SaaS 데이터 유출 및 그림자 IT를 완벽히 통제한다.
