---
sidebar:
  order: 168
  label: "168. 소버린 클라우드 (Sovereign Cloud)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "소버린 클라우드 (Sovereign Cloud)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 168
extra:
  question_no: "168"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "데이터 주권과 운영 통제권 직접 출제"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Sovereign Cloud (소버린 클라우드)**: 데이터가 저장된 물리적 위치(Data Residency)뿐만 아니라, 시스템 운영 주체와 암호키 통제권까지 현지 법(Local Jurisdiction)의 지배를 받도록 설계된 최고 수준의 독립형 클라우드.
- **Data Sovereignty (데이터 주권)**: 국가나 기업이 스스로 생성한 데이터에 대해 해외 정부나 글로벌 CSP(Cloud Service Provider)의 간섭 없이 독립적인 접근/통제 권한을 행사하는 권리.
- **US CLOUD Act (클라우드 액트법)**: 미국 기업(AWS, Azure)이 해외에 저장한 데이터라도 미국 정부가 요구하면 의무적으로 제출해야 하는 법령으로, 유럽(EU) 등에서 소버린 클라우드를 도입하게 된 결정적 계기.

</details>

- 정의/개념: 외산 CSP 인프라를 사용하더라도 암호키와 운영 권한을 전적으로 자국 기업(또는 공공기관)이 통제하여 타국의 사법권 개입을 차단하는 자율적 데이터 주권 보장 아키텍처인 **Sovereign Cloud**
- 배경/필요성: EU의 GDPR 및 미국 CLOUD Act 발효로 인해, 민감한 공공/금융 데이터가 글로벌 CSP의 미국 본사로 무단 유출되거나 열람될 위험성 원천 차단 요구성

#### 한줄 요약

- 자료를 국내에 두는 것에서 끝나지 않고 누가 운영하고 누가 암호키를 승인하며 다른 환경으로 옮길 수 있는지까지 통제하는 모델이다.

## Ⅱ. 특징 (Sovereign Cloud 3대 주권 보장 요건)

<details><summary>핵심 용어</summary>

- **Operational Sovereignty (운영 주권)**: 글로벌 CSP 본사의 엔지니어가 백도어로 접속하지 못하도록 현지 국적의 직원(Local Staff)만이 서버 관리 권한을 행사하는 원칙.

</details>

- **Data Sovereignty (자국 내 데이터 저장 및 암호화 키 고객 독점 보유 통제)**
- **Operational Sovereignty (CSP 엔지니어의 무단 접근 차단 및 현지 파트너사 운영 강제)**
- **Technical Sovereignty (오픈소스 표준 기반 아키텍처로 벤더 종속 탈피 및 데이터 이동성 보장)**

#### 한줄 요약

- 데이터센터가 국내에 있어도 해외 운영자가 암호키를 통제하고 데이터를 이전할 수 있다면 주권 요구가 충족되지 않으므로 데이터 거주지와 운영 통제권을 함께 평가한다.

## Ⅲ. 구조 및 구성요소 (Sovereign Cloud 구현 4-Layer 구조)

<details><summary>핵심 용어</summary>

- **External KMS (외부 키 관리 시스템)**: CSP(AWS) 내부의 KMS를 쓰지 않고, 고객이 온프레미스 장비나 로컬 파트너의 KMS 장비에서 암호키를 생성·보유하여 CSP가 절대 데이터를 열어보지 못하게 막는 기술.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   Sovereign Cloud Control Architecture                 │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Jurisdiction (관할권) : [Local Law (GDPR) > US CLOUD Act]           │
│ 2. Operation (운영권)    : [Local Partner (KT/NAVER)] ──X── [AWS Staff]│
│ 3. Encryption (암호권)   : [Customer-Owned External KMS]               │
│ 4. Residency (저장권)    : [Data Center Local Region Only]             │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 데이터의 물리적 저장(Residency) 위에서 암호키(KMS)와 로컬 파트너의 운영(Operation)이 결합되어 최종적인 국가 사법 관할권(Jurisdiction) 방어막을 형성하는 구조.

| 핵심 계층 (Layer) | 통제 기술 및 정책 요건 | 실무 구현 솔루션 예시 |
|:---|:---|:---|
| **Data Residency**| **데이터와 백업본의 100% 자국(Local) 내 저장** | AWS Seoul Region, Azure Korea |
| **Key Sovereignty** | **CSP 접근 불가한 외부/고객 통제 KMS 암호화**| AWS XKS (External Key Store) |
| **Operational Control**| **외국인 CSP 직원의 시스템/데이터 접근 원천 차단**| Local 파트너사(MSP) 독점 운영 계약|
| **Code & Exit Strategy**| **언제든 타 클라우드로 탈출 가능한 개방형 기술** | K8s 기반 컨테이너 이식성 확보 |

#### 한줄 요약

- 주권 요구가 출입 규칙을 정하면 신원 경계와 키 경계가 사람과 데이터의 문을 지키고 감사 체계가 모든 출입과 퇴거를 증명한다.

## Ⅳ. 흐름도 (External KMS 기반 데이터 접근 차단 흐름)

<details><summary>핵심 용어</summary>

- **Digital Sovereignty (디지털 주권)**: 데이터 주권, 소프트웨어(기술) 주권, 하드웨어 공급망 주권을 모두 포괄하는 국가 차원의 최상위 독립 통제권.

</details>

```text
[US Government Demand] ──► [Global CSP (AWS/Azure)] ──► [Attempt to Read Customer Data]
                                                                     │
                                                                     ▼ (Blocked!)
[Customer Controlled External KMS] ◄──(Require Decryption Key)── [Encrypted Storage]
           │
           ▼
[Customer Rejects Key Access] ──► [Data Remains Unreadable (Sovereignty Kept!)]
```

### 동작 원리

1. **Foreign Demand**: 미국 정부가 자국 법을 근거로 CSP 본사에 특정 한국 기업의 데이터 열람 요구.
2. **Key Request**: CSP가 저장된 암호화 데이터를 풀기 위해 한국 기업이 소유한 External KMS에 복호화 키 요청.
3. **Sovereign Block**: 한국 기업이 키 접근을 거부함에 따라 CSP는 쓰레기(암호화된 텍스트) 데이터만 쥐게 되어 **소버린 주권 방어 완결**.

#### 한줄 요약

- 관할 운영자가 요청해도 고객 키 정책이 거부하면 복호화할 수 없고 허용된 작업만 국내 워크로드에서 실행되어 감사 기록으로 남는다.

## Ⅴ. 종류 및 비교 (Data Residency 대 Sovereign Cloud 1:1 비교)

<details><summary>핵심 용어</summary>

- **Data Residency (데이터 레지던시)**: "물리적 서버 위치만 국내에 둘 뿐", 운영권과 암호키 통제권은 여전히 글로벌 CSP가 쥐고 있는 기초 단계 클라우드 요건.

</details>

| 비교 항목 | Data Residency (데이터 거주) | Sovereign Cloud (소버린 클라우드) |
|:---|:---|:---|
| **물리적 저장 위치** | 자국 내 리전 (Local Region) 보장 | **자국 내 리전 (Local Region) 보장** |
| **운영 인력 국적** | 글로벌 CSP 직원 원격 접근 가능 | **자국 내 지정 인력만 접근 권한 승인** |
| **암호화 키 (KMS)**| CSP가 관리하는 클라우드 내부 키 | **고객이 독점 통제하는 외부 독립 키 (XKS)**|
| **해외 정부 강제력** | US CLOUD Act에 의해 열람당할 위험 | **암호키 및 운영권 방어로 열람 100% 차단** |

#### 한줄 요약

- 데이터 레지던시는 자료의 주소를 고정하고 소버린 클라우드는 주소뿐 아니라 관리자, 열쇠, 이동 수단의 결정 권한까지 제한한다.

## Ⅵ. 실무 고려사항 및 대책 (소버린 클라우드 3대 실무 과제)

<details><summary>핵심 용어</summary>

- **Exit Strategy (탈출 전략/출구 전략)**: 특정 CSP가 파산하거나 적대적 인수합병이 발생했을 때, 즉각 데이터와 시스템을 다른 플랫폼으로 옮길 수 있는 포터빌리티(Portability) 설계.

</details>

| 3대 소버린 도입 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. 암호키 CSP 종속** | AWS KMS 기본 기능 사용 시 백도어 우려| **AWS XKS 또는 온프레미스 HSM 장비 연동** |
| **2. 기술 벤더 락인** | CSP의 독점 PaaS (DynamoDB 등) 사용 | **K8s, PostgreSQL 등 오픈소스 기반 아키텍처 수립**|
| **3. 막대한 운영 비용** | 로컬 파트너 전담 및 외부 솔루션 라이선스| **국가 안보/금융 등 1급 민감 데이터에만 선별 적용**|

> 사례: **독일 T-Systems와 Google Cloud의 파트너십(T-Systems가 암호키/운영 전담) Sovereign Cloud 적용**

#### 한줄 요약

- 본 데이터만 국내에 두지 말고 지원 로그와 백업의 처리 위치까지 추적하고 정기적으로 다른 환경에 복원해 출구 계획의 실행 가능성을 확인해야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **소버린 클라우드 수립 기준**: Data Residency 기본 충족, External KMS 암호권 보장, 로컬 파트너 운영권 및 Exit Strategy(컨테이너화)에 의거한 체계.

</details>

- **소버린 클라우드 수립 기준**에 따라 공공/금융/국방 클라우드 도입 시 **External KMS & Operational Sovereignty** 필수 적용

#### 한줄 요약

- 민감도가 높을수록 지역 제한에서 관할 인력, 외부 키 승인, 이전·폐기 검증까지 통제 단계를 높이고 이를 증적으로 확인해야 한다.
