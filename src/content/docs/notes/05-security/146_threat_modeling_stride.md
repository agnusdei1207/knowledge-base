---
sidebar:
  order: 146
  label: "146. 위협 모델링 — STRIDE•DREAD (Threat Modeling STRIDE)"
  badge:
    text: "미출 · 70%"
    variant: note
title: "소프트웨어 아키텍처 위협 식별 및 위험 평가 : 위협 모델링 (STRIDE & DREAD)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-security"
weight: 146
extra:
  question_no: "146"
  source_status: "미출"
  source_history: ""
  priority: 70
  priority_note: "설계 단계 위협 도출 핵심 방법론, 위협 모델링(Threat Modeling), 데이터 흐름도(DFD: 외부 엔티티, 프로세스, 데이터 저장소, 데이터 흐름, 신뢰 경계 Trust Boundary), STRIDE 6대 위협 분류(Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege), DREAD 위험 평가 모델(Damage, Reproducibility, Exploitability, Affected Users, Discoverability) 및 CVSS 연계"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **위협 모델링(Threat Modeling / STRIDE & DREAD / Microsoft SDL)**: 소프트웨어 개발 생명주기(SDLC)의 설계(Design) 단계에서 시스템의 아키텍처, 데이터 흐름(DFD), 신뢰 경계(Trust Boundary)를 구조적으로 분해하여 잠재적 사이버 위협을 사전에 식별하고, DREAD 위험 평가를 통해 완화(Mitigation) 통제 우선순위를 수립하는 예방적 보안 엔지니어링 프로세스.
- **설계 결함의 후행 발견에 따른 아키텍처 재작성 결함(Design Flaw vs Coding Bug Defect)**: 단순한 코딩 버그(Buffer Overflow 등)와 달리, 인증 부재나 암호화 미적용 등 아키텍처 수준의 구조적 설계 결함은 코딩 완료 후 SAST/DAST로 발견할 경우 전체 시스템 아키텍처를 뒤엎어야 하여 막대한 비용과 프로젝트 실패를 유발하는 결함.

</details>

- 정의/개념: 설계 단계부터 보안 내재화(Secure by Design)를 달성하기 위해 **DFD 시스템 분해 및 신뢰 경계 설정 $\rightarrow$ STRIDE 6대 위협 범주 식별 $\rightarrow$ DREAD/CVSS 정량적 위험 평가 $\rightarrow$ 완화 설계 패턴(Mitigation Pattern) 적용 $\rightarrow$ 보안 요구사항 추적성(Traceability) 확보** 를 집행하는 **선제적 위협 분석 프레임워크**
- 배경/필요성: 소프트웨어 보안 취약점의 50% 이상이 아키텍처 설계 결함에서 기인함에 따라, 개발 초기(Shift-Left) 단계에서 구조적 취약점을 원천 제거할 체계적 기법 필요

#### 한줄 요약
- 위협 모델링은 DFD와 STRIDE를 통해 설계 단계의 구조적 위협을 식별하고 DREAD로 위험을 평가한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **STRIDE 6대 위협 범주 및 침해되는 보안 속성**:
  - **Spoofing (신분 위장)**: 타인이나 정상 시스템으로 가장 $\longleftrightarrow$ 인증(Authentication) 침해.
  - **Tampering (데이터 변조)**: 전송 중이거나 저장된 데이터 무단 수정 $\longleftrightarrow$ 무결성(Integrity) 침해.
  - **Repudiation (행위 부인)**: 자신이 수행한 악의적 행위를 증거 없이 부인 $\longleftrightarrow$ 부인방지(Non-repudiation) 침해.
  - **Information Disclosure (정보 노출)**: 비인가 대상에게 기밀 데이터 유출 $\longleftrightarrow$ 기밀성(Confidentiality) 침해.
  - **Denial of Service (서비스 거부)**: 자원 고갈로 정상 서비스 방해 $\longleftrightarrow$ 가용성(Availability) 침해.
  - **Elevation of Privilege (권한 상승)**: 비인가 사용자가 관리자 권한 획득 $\longleftrightarrow$ 인가(Authorization) 침해.

</details>

- **데이터 흐름도(DFD) 기반의 직관적 시각화**: 프로세스, 데이터 저장소, 데이터 흐름, 외부 엔티티와 이들 간의 신뢰 경계(Trust Boundary)를 명확히 정의
- **구조화된 컴포넌트별 위협 매핑 (STRIDE-per-Element)**: DFD 각 구성요소 유형별로 발생 가능한 STRIDE 위협을 매트릭스로 기계적 도출하여 누락 원천 방지
- **위협에서 완화 대책까지의 양방향 추적성(Traceability)**: 도출된 위협 $\rightarrow$ 보안 요구사항 $\rightarrow$ 코드 구현 $\rightarrow$ 침투 테스트 케이스로 1:1 대응 관리

#### 한줄 요약
- DFD 신뢰 경계 시각화, STRIDE 6대 위협 매핑, DREAD 정량 평가, 양방향 추적성을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **위협 모델링 3대 핵심 분석 아티팩트**:
  1. **Data Flow Diagram (DFD 4대 요소 + 신뢰 경계)**: 시스템 추상화 도면.
  2. **STRIDE Threat Matrix**: 컴포넌트별 6대 위협 매핑 및 완화 패턴.
  3. **DREAD Risk Scoring (5대 평가 축)**: Damage, Reproducibility, Exploitability, Affected Users, Discoverability.

</details>

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 1. DFD 시스템 분해 및 신뢰 경계 (Data Flow Diagram & Trust Boundary) ] │
│  ├─ [ 외부 엔티티 (User) ] ➔ (요청 전송) ➔ [ 신뢰 경계 1: 인터넷/DMZ ]   │
│  ├─ [ 웹/API 프로세스 ] ➔ (데이터 흐름) ➔ [ 신뢰 경계 2: DMZ/내부망 ]    │
│  └─ [ 비즈니스 로직 프로세스 ] ➔ (쿼리 전송) ➔ [ 데이터 저장소 (DB) ]   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (STRIDE-per-Element 위협 식별)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 2. STRIDE 위협 식별 및 완화 패턴 매핑 (Threat Identification) ]        │
├───────────────────────────────────┬─────────────────────────────────────┤
│ [ STRIDE 위협 도출 ]              │ [ 대응 완화 패턴 (Mitigation) ]      │
│ ├─ S: 가짜 사용자 로그인 위장    │ ➔ mTLS, FIDO2, OAuth 2.0 / OIDC 인증│
│ ├─ T: 전송 패킷 및 DB 데이터 변조│ ➔ HMAC 서명, 디지털 서명, DB 암호화 │
│ ├─ R: 결제 후 주문 사실 부인     │ ➔ 감사 로그 WORM 저장, 타임스탬프   │
│ ├─ I: 메모리/통신 상 개인정보 유출│ ➔ TLS 1.3 암호화, AES-256 저장 암호화│
│ ├─ D: API 요청 폭주로 서버 마비  │ ➔ Token Bucket Rate Limiting, WAF   │
│ └─ E: 일반 유저가 관리자 권한 탈취│ ➔ RBAC/ABAC 최소 권한 원칙(PoLP) 강제│
└───────────────────────────────────┴─────────────────────────────────────┘
                                     │ (위험 우선순위 정량화)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 3. DREAD / CVSS 위험 평가 및 백로그 등록 (Risk Prioritization) ]       │
│  ├─ [ DREAD 점수 산출 ] ➔ $Score = \frac{D + R + E + A + D}{5}$ (1~10점)│
│  └─ [ Jira 백로그 자동 등록 ➔ 개발 스프린트 보안 요구사항 강제 반영 ]   │
└─────────────────────────────────────────────────────────────────────────┘
```

선의 의미: DFD 도면에서 신뢰 경계를 식별하고 STRIDE 위협을 매핑하여 DREAD로 우선순위를 평가한 후 개발 백로그로 등록하는 구조

| DFD 구성요소 | 기호 및 의미 | 적용 가능한 STRIDE 위협 | 핵심 완화 대책 (Mitigation) |
|:---|:---|:---|:---|
| **External Entity (외부 엔티티)** | 사각형 (사용자, 외부 서드파티 API) | **S**poofing, **R**epudiation | 강력한 MFA 인증, 전자서명 |
| **Process (프로세스)** | 원형/둥근 사각형 (웹서버, 마이크로서비스)| **S, T, R, I, D, E** (전체 6종) | 입력값 검증, 메모리 격리, 최소 권한 |
| **Data Flow (데이터 흐름)** | 화살표 (REST API 통신, gRPC, 메시지 큐) | **T**ampering, **I**nfo Disclosure, **D**oS | TLS 1.3 암호화, HMAC 무결성 검증 |
| **Data Store (데이터 저장소)** | 평행선 (RDBMS, NoSQL, 파일 시스템) | **T**ampering, **I**nfo Disclosure, **D**oS | AES-256 컬럼 암호화, DB 접근 제어 |
| **Trust Boundary (신뢰 경계)** | 점선 (서로 다른 권한 도메인 간의 경계선)| **분석의 최우선 기준점** | API 게이트웨이, 상호 인증(mTLS) |

#### 한줄 요약
- DFD 4대 요소, 신뢰 경계, STRIDE 6대 위협 매트릭스, DREAD 5대 평가 축으로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **위협 모델링 5단계 엔지니어링 프로세스**:
  1. 모델링 대상 애플리케이션의 범위 및 보안 목표 정의
  2. 아키텍처 DFD 다이어그램 작성 및 신뢰 경계(Trust Boundary) 설정
  3. DFD 컴포넌트별 STRIDE 위협 시나리오 전수 도출
  4. DREAD 정량 평가를 통한 고위험 위협 우선순위 산정
  5. 완화 대책(Mitigation) 수립 및 개발 백로그(Jira) 등록

</details>

```text
1. [범위 및 목표 정의]
    ├─ 대상: 클라우드 금융 결제 마이크로서비스 아키텍처
    └─ [핵심 보호 자산: 결제 승인 토큰 및 고객 계좌 원장]
            │
            ▼
2. [DFD 도출 및 신뢰 경계 설정]
    ├─ 사용자 브라우저 ➔ [신뢰 경계 1] ➔ API Gateway ➔ [신뢰 경계 2] ➔ 결제 Pod ➔ 결제 DB
    └─ [신뢰 경계를 교차하는 모든 인바운드/아웃바운드 데이터 흐름 식별]
            │
            ▼
3. [STRIDE 위협 도출 (예시)]
    ├─ [T 위협] API Gateway와 결제 Pod 간 전송 중 결제 금액 변조 가능성 식별
    └─ [E 위협] 결제 Pod 내 JWT 토큰 파싱 결함으로 일반 사용자의 관리자 권한 상승 식별
            │
            ▼
4. [DREAD 위험 평가 및 점수 산정]
    ├─ 금액 변조 위협 평가: Damage(10) + Repro(8) + Exploit(7) + Affected(9) + Disc(8) = 평균 8.4점 (Critical)
    └─ [High/Critical 등급 항목을 스프린트 최우선 조치 과제로 확정]
            │
            ▼
5. [완화 대책 설계 및 백로그 추적]
    ├─ [완화 설계] Pod 간 mTLS 1.3 강제 및 JWT 서명 RS256 비대칭키 검증 추가
    └─ [Jira 티켓 발행 ➔ SAST/DAST 테스트 케이스와 1:1 매핑 후 개발 반영]
```

**동작 원리**

1. **체계적 완전성(Completeness)**: 직관이나 경험에 의존하지 않고 STRIDE 매트릭스를 통해 아키텍처 전 구간의 위협을 전수 조사
2. **신뢰 경계 중심 분석**: 데이터가 비신뢰 영역에서 신뢰 영역으로 넘어가는 지점에 보안 통제(인증/인가/검증) 집중 배치
3. **투자 대비 효과 극대화**: DREAD 점수화를 통해 한정된 보안 예산과 개발 인력을 가장 위험한 치명적 위협에 집중 투입
4. **보안 요구사항의 명세화**: "보안을 강화하라"는 추상적 요구 대신 "mTLS 도입으로 Tampering 방어"와 같은 구체적 기술 사양 도출
5. **지속적 모델 갱신 (TMaC)**: 신규 API 추가나 인프라 변경 시 위협 모델을 코드로 관리(Threat Modeling-as-Code)하여 지속 동기화

#### 한줄 요약
- 범위 정의, DFD/신뢰 경계 설정, STRIDE 위협 도출, DREAD 위험 평가, 완화 대책 백로그 등록 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **주요 위협 모델링 방법론 비교**:
  - STRIDE: 개발자/아키텍트 중심의 소프트웨어 아키텍처 결함 식별 (기술 중심).
  - PASTA (Process for Attack Simulation & Threat Analysis): 공격자 관점의 7단계 비즈니스 위험 시뮬레이션 (비즈니스 중심).
  - Attack Trees (공격 트리): 공격 목표를 루트 노드로 하는 트리 구조 조건 분해 (시나리오 중심).

</details>

| 비교 항목 | STRIDE 방법론 | PASTA 프레임워크 | 공격 트리 (Attack Trees) |
|:---|:---|:---|:---|
| **주요 관점** | **소프트웨어 개발자, 아키텍트 (시스템 중심)**| **공격자, 비즈니스 리스크 관리자 (위험 중심)**| **보안 분석가, 모의해커 (공격 경로 중심)**|
| **핵심 기법** | **DFD 분해 ➔ 6대 위협 범주 매트릭스 매핑**| **7단계 비즈니스 영향 분석 및 모의 침투** | **최상위 목표 달성을 위한 AND/OR 조건 분해**|
| **수행 시점** | **소프트웨어 설계(Design) 초기 단계** | 엔터프라이즈 기획 및 비즈니스 위험 분석 | 특정 침해 시나리오 상세 분석 단계 |
| **주요 장점** | **누락 없는 기술적 보안 요구사항 도출 용이**| **비즈니스 자산 가치와 보안 투자의 ROI 정렬**| 침해 경로와 사전 조건의 직관적 시각화 |
| **단점/한계점** | 비즈니스 영향도 미반영, DFD 작성 오버헤드 | 절차가 방대하여 빠른 애자일 스프린트에 부담| 시스템 전반의 포괄적 보안 대책 도출 한계 |

#### 한줄 요약
- STRIDE는 기술적 아키텍처 위협, PASTA는 비즈니스 위험 시뮬레이션, 공격 트리는 공격 경로 분석에 특화된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Microsoft SDL 및 OWASP Threat Dragon**: 소프트웨어 개발 생명주기 내 위협 모델링 자동화 도구 및 표준.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 마이크로서비스(MSA) 환경에서 내부망 통신을 안전지대로 맹신하여 **서비스 간(Service-to-Service) 신뢰 경계를 설정하지 않아 내부 침해 시 전 서비스 장악** | **제로 트러스트 원칙 준수, 모든 내부 마이크로서비스 통신 구간에 신뢰 경계를 설정하고 서비스 메시(Istio) 기반 mTLS 및 RBAC 강제** | 내부 네트워크 측면 이동 및 권한 상승 100% 원천 차단 |
| DREAD 평가 시 평가자마다 주관적 기준 편차가 발생하여 **치명적인 위협의 우선순위가 낮게 책정되어 보안 패치에서 누락되는 결함 발생** | **조직 맞춤형 객관적 평가 루브릭(Rubric)을 제정하고, 국제 표준 CVSS 3.1/4.0 기본 점수(Base Score) 산출 공식과 연계** | 위협 우선순위 산정의 객관성 및 신뢰성 100% 확보 |
| 잦은 배포가 일어나는 애자일 환경에서 수작업 위협 모델링 문서 작성이 **개발 일정 병목을 유발하여 위협 모델링이 사장되는 문제 발생** | **TMaC(Threat Modeling as Code) 도구를 도입하여 아키텍처 변경(Git PR) 시 CI/CD 파이프라인에서 위협 모델 자동 갱신** | 위협 모델링 오버헤드 70% 절감 및 최신성 유지 |

#### 한줄 요약
- 제로 트러스트 신뢰 경계로 내부 침해를 막고, CVSS 연계로 객관성을 확보하며, TMaC로 애자일 자동화를 달성한다.

## Ⅶ. 결론

- 소프트웨어의 보안 품질을 사후 패치가 아닌 설계 단계의 본원적 구조로 완성하는 최상위 엔지니어링 프레임워크인 **위협 모델링 아키텍처**는 안전한 소프트웨어 개발 생명주기(Secure SDLC)의 핵심 나침반이며, 실무 구현 시 **DFD 기반의 명확한 신뢰 경계(Trust Boundary) 설정**, **STRIDE 6대 위협 범주 전수 매핑**, **DREAD 및 CVSS 기반의 정량적 위험 우선순위화**, **코드형 위협 모델링(TMaC)을 통한 DevSecOps 파이프라인 지속 통합**을 완성하여 최고 수준의 아키텍처 복원력과 선제적 방어 체계를 완성

#### 한줄 요약
- DFD 신뢰 경계와 STRIDE/DREAD 분석을 통해 설계 단계부터 무결점 위협 모델링을 완성한다.
