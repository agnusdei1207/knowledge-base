---
sidebar:
  order: 77
  label: "077. 비밀 관리 - Vault•AWS Secrets (Secrets Management)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "동적 자격증명 발급 및 비밀 생애주기 관리 : Secrets Management (HashiCorp Vault & AWS Secrets Manager)"
date: "2026-08-31T10:48:00+09:00"
tags:
  - "notes-security"
weight: 77
extra:
  question_no: "077"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "NIST SP 800-57(키 관리), 하드코딩 비밀 배제, 워크로드 신원(OIDC/K8s SA), 동적 비밀(Dynamic Secrets & Lease/TTL), HashiCorp Vault vs AWS Secrets Manager, Shamir 봉인 해제(Unseal)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **비밀 관리(Secrets Management / NIST SP 800-57)**: 데이터베이스 패스워드, API 인증 키, 클라우드 IAM 자격증명, SSH 키, TLS/SSL 개인키 등 시스템 접근에 필요한 모든 디지털 기밀(Secret)에 대해 저장, 발급, 회전(Rotation), 폐기(Revocation), 감사 추적에 이르는 전체 생애주기를 암호화하여 중앙 통제하는 보안 아키텍처.
- **소스코드 하드코딩 및 장기 고정 비밀의 위험(Hardcoded & Long-lived Secrets Defect)**: 개발 편의를 위해 소스코드, Dockerfile, Git 저장소, 환경변수 파일에 고정된 마스터 DB 비밀번호를 평문 하드코딩하여, Git 저장소 유출이나 인사이동 시 침해 위험이 무기한 지속되는 구조적 취약점.

</details>

- 정의/개념: 고정된 비밀번호의 하드코딩을 원천 금지하고, **워크로드 신원(K8s SA/OIDC) 인증 $\rightarrow$ 동적 비밀(Dynamic Secrets) 온디맨드 실시간 발급 $\rightarrow$ 시한부 리스(Lease/TTL) 결속 $\rightarrow$ 자동 만료 및 침해 시 원클릭 폐기(Revocation)** 를 집행하는 **자격증명 제로 트러스트 관리 체계**
- 배경/필요성: 마이크로서비스 및 멀티 클라우드 환경에서 소스코드, Git 저장소, 환경변수(ConfigMap), CI/CD 파이프라인 전반에 DB 패스워드와 API 키가 평문 하드코딩되고 장기 고정 비밀(Long-lived Secrets)이 방치됨에 따라, 단 한 번의 자격증명 유출로도 전사 인프라가 연쇄 장악되는 치명적 보안 위협이 발생함에 따라, 워크로드 신원(K8s SA/OIDC) 기반의 무고정 자격증명(Zero Standing Privileges), 시한부 리스(Lease/TTL)가 결속된 동적 비밀(Dynamic Secrets) 온디맨드 발급 및 자동 회전을 집행하는 Secrets Management(HashiCorp Vault / AWS Secrets Manager) 아키텍처를 도입하여 **비밀 하드코딩 100% 제거, 자격증명 노출 시간 창의 극단적 단축 및 중앙 집중식 암호화 감사 추적**을 달성할 필요

#### 한줄 요약
- 코드 내 하드코딩을 배제하고, 워크로드 신원 기반의 일회성 동적 자격증명 발급과 자동 회전으로 비밀을 통제한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **동적 비밀(Dynamic Secrets)**: 워크로드가 데이터베이스 접근을 요청하는 바로 그 순간(Just-In-Time)에 타깃 DB에 일회용 임시 계정(`v-token-1234`)과 패스워드를 실시간 생성하여 발급하고, 작업 종료 또는 TTL 만료 시 DB에서 계정 자체를 자동 삭제(Drop User)하는 차세대 비밀 관리 기법.
- **리스 및 TTL(Lease & Time to Live)**: 발급된 모든 동적 비밀에 암호학적 임대 계약(Lease)과 유효시간(예: 1시간)을 부여하여, 시간 만료 시 중앙 금고가 타깃 시스템의 자격증명을 강제 폐기하는 메커니즘.

</details>

- **무고정 자격증명 (Zero Standing Secrets)**: 사전에 고정 생성된 계정을 공유하지 않고, 요청 시점에만 생성되는 시한부 일회성 계정 사용
- **워크로드 신원 기반 부트스트랩 (Identity-based Bootstrap)**: 비밀번호 대신 K8s Service Account 토큰이나 AWS IAM Role을 신원 증명으로 제출하여 금고 인증 완결
- **중앙 집중식 감사 추적 (Audit Trail)**: 어떤 마이크로서비스가 몇 시 몇 분에 어떤 DB의 비밀을 인출해 갔는지 모든 접근 이력을 암호화 로그로 실시간 보존

#### 한줄 요약
- 동적 비밀 온디맨드 발급, 리스(Lease) 기반 수명 통제, 워크로드 신원 인증, 전수 감사 로깅을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **비밀 관리 플랫폼 4대 핵심 모듈 (HashiCorp Vault 기준)**:
  1. **Auth Methods (인증 메서드)**: K8s, AWS IAM, OIDC, AppRole 등을 통해 클라이언트 워크로드 신원 검증.
  2. **Policy Engine (정책 엔진)**: HCL/JSON 기반 선언적 정책을 통해 비밀 경로별 인가(Read/Write) 판정.
  3. **Secrets Engines (비밀 엔진)**: DB(MySQL/PostgreSQL), AWS, PKI 등 타깃 백엔드와 연동하여 동적 계정 생성.
  4. **Lease & Storage Core**: AES-256-GCM 스토리지 암호화 및 리스 수명주기/폐기 관리.

</details>

```text
[ 마이크로서비스 워크로드 (Kubernetes Pod) ]
                     │ (1. K8s Service Account JWT 토큰 제출)
                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 1. 중앙 비밀 관리 금고 (HashiCorp Vault / AWS Secrets Manager) ]     │
│  ├─ Auth Method: K8s API 서버와 통신하여 Pod 신원 무결성 검증          │
│  ├─ Policy Engine: 해당 Pod에 부여된 인가 룰(`path "database/creds/app"`) 대조│
│  └─ [ Secrets Engine 구동 ➔ 타깃 DB와 실시간 관리자 통신 ]              │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (2. 일회성 임시 계정 생성 명령: CREATE USER)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 2. 타깃 백엔드 데이터베이스 (Target Database: MySQL / PostgreSQL) ]   │
│  └─ [ `user_temp_9876` 계정 및 난수 패스워드 생성 완료 ]                │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (3. 1시간 유효 Lease ID + 자격증명 반환)
                                     ▼
[ 워크로드 ➔ 임시 자격증명으로 DB 작업 수행 ➔ 1시간 후 Vault가 DB에서 계정 자동 DROP ]
```

선의 의미: 워크로드가 K8s 신원으로 금고에 인증하면, 비밀 엔진이 타깃 DB에 임시 계정을 생성하여 워크로드에 리스 결속 자격증명을 반환하는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **워크로드 신원 인증기** | K8s SA, AWS IAM, OIDC 토큰을 검증하여 애플리케이션의 신원을 무결하게 식별 | Auth Method |
| **정책 엔진 (Policy Engine)**| 비밀 경로(Path) 및 수행 연산(Read/List)에 대한 최소 권한 인가 정책 판정 | Policy Core |
| **동적 비밀 엔진** | 타깃 DB, CSP, PKI와 API로 연동하여 일회용 계정 및 단기 인증서 실시간 발급 | Dynamic Engine |
| **리스 관리자 (Lease Manager)**| 발급된 자격증명의 TTL 만료 감시, 리스 갱신 및 침해 시 원클릭 긴급 폐기 집행 | Lifecycle Core |
| **암호화 스토리지 (Storage)**| 저장된 마스터 암호키 및 정적 비밀을 AES-256-GCM으로 봉인 격리 보관 | Storage Engine |

#### 한줄 요약
- 워크로드 인증기, 정책 엔진, 동적 비밀 엔진, 리스 관리자, 암호화 스토리지가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **동적 비밀 발급 및 폐기 5단계 흐름**:
  1. 워크로드가 K8s 토큰으로 금고에 로그인
  2. 금고가 정책 확인 후 타깃 DB에 일회용 임시 계정 생성
  3. 시한부 리스(Lease ID)와 함께 자격증명 발급
  4. 워크로드가 임시 계정으로 DB 쿼리 실행
  5. TTL 만료 즉시 금고가 DB에서 해당 임시 계정 자동 삭제

</details>

```text
1. [워크로드 신원 인증] K8s Pod가 기동 시 자신의 Service Account 토큰을 Vault로 전송하여 인증 요청
            │
            ▼
2. [정책 평가 및 DB 호출] Vault가 K8s API로 토큰 검증 완료 ➔ `database/creds/payment-role` 정책 확인 후 DB로 연결
            │
            ▼
3. [일회용 임시 자격 생성] Vault 비밀 엔진이 MySQL DB에 `CREATE USER 'v-token-abc'@'%' IDENTIFIED BY '난수'` 실행
            │
            ▼
4. [단기 리스 발급 및 작업]
    ├─ Vault가 워크로드에 임시 자격증명과 `Lease ID(TTL: 3600s)` 반환
    └─ 워크로드가 해당 임시 계정으로 결제 트랜잭션 DB 작업 안전 수행
            │
            ▼
5. [자동 만료 및 계정 소멸]
    ├─ 1시간 경과 후 리스 만료 (또는 침해 감지 시 긴급 Revoke API 호출)
    └─ Vault가 MySQL DB에 접속하여 `DROP USER 'v-token-abc'` 즉각 실행 (자격증명 완전 소멸)
```

**동작 원리**

1. **워크로드 신원 인증**: 서비스 계정 토큰 검증
2. **정책 평가 및 DB 호출**: 접근 권한 확인
3. **일회용 임시 자격 생성**: 백엔드 계정 생성
4. **단기 리스 발급 및 작업**: TTL 결속 자격 반환
5. **자동 만료 및 계정 소멸**: 리스 종료 시 계정 삭제

#### 한줄 요약
- 요청마다 계정을 새로 만드는 발급 비용을 감수하는 대신 침해 시 폐기 작업과 노출 기간이 TTL 하나로 끝나므로, 상시 보관 위험을 발급 시점의 연산 비용과 맞바꾼 셈이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **비밀 관리 3대 방식 비교**: 코드 하드코딩(레거시), AWS Secrets Manager(중앙 정적), HashiCorp Vault(중앙 동적)의 비교.

</details>

| 비교 항목 | 코드 내 하드코딩 (Legacy) | AWS Secrets Manager (중앙 정적) | HashiCorp Vault (중앙 동적) |
|:---|:---|:---|:---|
| **비밀 관리 형태** | 소스코드/환경변수에 평문 기재 | 중앙 암호화 저장 및 정기 자동 회전 | **요청 시점 온디맨드 실시간 동적 생성** |
| **자격증명 수명 (TTL)** | **영구적 (유출 시 무기한 악용)** | 30일 ~ 90일 (설정된 회전 주기) | **초/분/시간 단위 극단적 단기 수명** |
| **백엔드 계정 모델** | 단일 공용 계정을 전 서버가 공유 | 사전 생성된 고정 계정의 암호 변경 | **요청마다 고유 임시 계정 개별 생성/삭제**|
| **멀티 클라우드 지원** | N/A | AWS 생태계 최적화 (타 클라우드 제약)| **AWS, Azure, GCP, 온프레미스 완벽 지원**|
| **운영 복잡도** | 없음 (보안 파탄) | **낮음 (클라우드 완전 관리형 서비스)** | 보통~높음 (금고 클러스터 HA/Unseal 운영)|

#### 한줄 요약
- 하드코딩은 치명적 취약점, AWS Secrets Manager는 관리형 정적 회전, Vault는 멀티 클라우드 동적 발급 표준이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Shamir's Secret Sharing 기반 봉인 해제(Unseal)**: Vault 마스터 키를 암호학적으로 N개의 키 조각(Unseal Keys)으로 분할하여 서로 다른 보안 담당자에게 배분하고, 서버 재기동 시 최소 M개의 조각(예: 3 of 5)이 결합되어야만 금고가 열리도록 강제하는 물리적 다중 통제 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 소스코드 및 Dockerfile 내에 마스터 DB 패스워드가 하드코딩되어 **Git 저장소 유출 시 전사 인프라가 장악되는 치명적 사고** | **NIST SP 800-57** 준수, **HashiCorp Vault 동적 비밀 엔진을 도입하여 시한부(TTL 1시간) 일회용 계정 온디맨드 발급** | 장기 고정 비밀번호 100% 원천 제거 및 자격증명 유출 시 악용 가능 시간 창 최소화 |
| 중앙 Vault 금고 서버 재부팅 시 단일 관리자 부재로 인해 **금고 봉인 해제(Unseal)가 불가능하여 전사 서비스가 마비되는 단일 장애점** | **Shamir's Secret Sharing 기반 봉인 키 분할(3 of 5 M-of-N 통제) 또는 CSP KMS 연동 자동 언실(Auto-unseal) 구축** | 관리자 1인 종속성 해소 및 고가용성(HA) 기반의 99.999% 무중단 금고 가용성 확보 |
| AWS Secrets Manager 정기 패스워드 회전(Rotation) 시점에 **기존 세션이 강제 단절되어 대규모 데이터베이스 트랜잭션 에러 발생** | **신규 패스워드와 기존 패스워드를 1시간 동안 동시 유효하게 유지하는 단계적 회전(Dual-Secret Phased Rotation) 적용** | 서비스 다운타임 제로(Zero Downtime) 기반의 안전한 데이터베이스 비밀번호 자동 회전 달성 |

#### 한줄 요약
- 동적 비밀로 하드코딩을 없애고, Auto-unseal로 가용성을 지키며, Dual-Secret 회전으로 다운타임을 방지한다.

## Ⅶ. 결론

- 애플리케이션과 인프라의 모든 자격증명 생애주기를 중앙에서 암호화 통제하고 고정 비밀번호를 완전히 제거하는 **현대 클라우드 네이티브 제로 트러스트(Zero Standing Privileges) 및 DevSecOps 비밀 거버넌스의 최상위 필수 프레임워크**로 확고히 자리 잡았으며, 머신 아이덴티티(Machine Identity) 및 Workload Identity Federation과의 통합으로 진화하는 가운데, 실무 엔터프라이즈 비밀 관리 시스템 구축 시에는 **K8s Service Account 및 CSP IAM을 활용한 워크로드 신원 기반 무암호 금고 인증, 타깃 DB와 연동한 1시간 시한부 동적 비밀(Dynamic Secrets) 발급, CSP KMS 연동 Auto-unseal을 통한 99.999% 무중단 가용성 확보, 다운타임 없는 Dual-Secret 단계적 자동 회전(Rotation)**을 결합하여 완벽한 디지털 기밀 무결성을 완성

#### 한줄 요약
- 워크로드 신원 인증과 동적 비밀 발급 및 리스 기반 자동 소멸을 통해 무결점 비밀 관리를 완성한다.
