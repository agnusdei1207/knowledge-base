---
sidebar:
  order: 71
  label: "071. 클라우드 보안 공유 책임 모델 (Cloud Shared Responsibility)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "클라우드 보안 공유 책임 모델 (Cloud Shared Responsibility)"
date: "2026-08-13T20:24:00+09:00"
tags:
  - "notes-security"
weight: 71
extra:
  question_no: "071"
  source_status: "기출"
  source_history: "137회"
  priority: 70
  priority_note: "137회 기출이며 서비스모델별 책임 설계가 반복 활용됨"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **공유 책임 모델(Cloud Shared Responsibility Model)**: 클라우드 서비스 제공자(CSP)와 클라우드 이용 고객(Customer) 간에 물리적 인프라, 하이퍼바이저, OS, 데이터, 계정 통제 책임의 분담 한계를 명확히 구분한 보안 원칙이다.
- **책임 공백(Responsibility Void / Accountability Gap)**: CSP와 고객 어느 쪽도 해당 통제의 수행•관리•증명 책임을 지정하지 않아 보안 사고 위험에 노출되는 통제 누락 상태이다.

</details>

- 정의/개념: CSP와 고객 통제를 나누는 **공유 책임 모델**
- 배경/필요성: CSP 전담 오인은 **책임 공백•고객 설정 오류** 유발

#### 한줄 요약

- CSP는 인프라/플랫폼 보안을, 고객은 데이터/계정/설정 보안을 서비스 모델별로 할당하여 책임 공백을 방지하는 모델이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **통제 소유권(Control Ownership)**: 특정 보안 통제 항목에 대해 요구사항 이행, 설정 유지, 검증 책임을 갖는 주체(CSP vs Customer)를 명확히 정의하는 권한 개념이다.
- **운영 증적(Operational Audit Evidence)**: 통제 이행 여부를 입증하는 감사 로그, SOC 2/ISMS-P 인증서, WAF 설정 내역 등의 디지털 검증 증거이다.

</details>

- **통제 소유권**을 명확히 식별하여 IaaS, PaaS, SaaS 서비스 모델별로 관리 영역을 세분화한다.
- CSP 제공 상속 통제(Inherited Control)와 고객 관리 직접 통제의 범위를 RACI Matrix로 표준화한다.
- 계약, 로그, 보안 가시성 툴을 통한 **운영 증적** 수집으로 통제 이행의 법적•감사적 입증을 완성한다.

#### 한줄 요약

- 서비스 모델별 **통제 소유권•운영 증적** 명확화

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **공동 통제(Shared / Joint Control)**: 패치 관리, IAM 연동 등 CSP와 고객이 협력하여 각자 영역을 구성해야 완성되는 통제이다.
- **상속 통제(Inherited Control)**: 데이터센터 물리 보안 등 CSP의 보안 수행 결과를 고객이 자신의 보안 통제로 온전히 인정받는 항목이다.
- **서비스 수준 협약(Service Level Agreement, SLA)**: 가용성, 장애 처리, 서비스 보장 수준 및 법적 보상과 책임 범위를 명시한 계약서이다.
- **사고 인터페이스(Incident Management Interface)**: 보안 침해 발생 시 CSP와 고객 간의 상호 통보 핫라인, 침해 조사 협력 및 로그 공유 절차이다.

</details>

```text
                     [서비스·계약 경계]
                       /             \
                [제공자 통제]     [고객 통제]
                       \             /
                     [공동·상속 통제]
                              |
                    [증적·사고 인터페이스]
```

선의 의미: 서비스 계약 경계 하에 CSP 및 고객의 개별 통제, 공동/상속 통제, 증적 교환 및 침해사고 대응 인터페이스 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| 서비스·계약 경계 | 클라우드 서비스 계약서 및 **SLA** 상 책임 한계 구획 정의 |
| 제공자 통제 (CSP) | 데이터센터 물리 보안, 서버 하드웨어, 스토리지, 하이퍼바이저, 네트워크 기초 통제 |
| 고객 통제 (Customer) | 데이터 암호화, IAM 계정/권한, OS 패치(IaaS), 네트워크 방화벽 설정, 앱 코드 |
| 공동·상속 통제 | **공동 통제**(네트워크 패치, 환경 설정) 및 **상속 통제**(물리 보안 등) 분담 이행 |
| 증적·사고 인터페이스 | **사고 인터페이스** 핫라인 개설, SOC 감사 보고서 및 실시간 보안 로그 수집 교환 |

#### 한줄 요약

- CSP 인프라 보안과 고객 자산 보안 경계를 구획하고, 공동/상속 통제 정의 및 사고 인터페이스를 통해 협력 체계를 구성한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **책임 할당 행렬(Responsibility Assignment Matrix / RACI Matrix)**: 통제별 담당자(Responsible), 최종책임자(Accountable), 협의자(Consulted), 통보자(Informed)를 식별하는 매트릭스이다.
- **책임 검증 계획(Responsibility Verification Plan)**: CSP 및 고객의 보안 통제 이행 결과를 어떤 주기로 검증하고 평가할 것인지 정한 계획이다.
- **제공자 통제•증적 추출(CSP Control & Audit Evidence Extraction)**: CSP가 담당하는 인프라 통제의 감사 보고서(SOC 등)를 수집하는 단계이다.
- **고객 통제•소유자 정의(Customer Control & Owner Definition)**: 고객이 전담할 IAM, 데이터, 설정의 내부 담당자를 지정하는 단계이다.
- **서비스 계층•책임 경계 매핑(Service Layer & Responsibility Boundary Mapping)**: IaaS/PaaS/SaaS 모델에 맞게 통제 영역을 레이어별 할당하는 단계이다.
- **RACI•책임 검증 계획 수립(RACI & Responsibility Verification Plan Setup)**: 통제 항목별 RACI 행렬을 작성하고 검증 방안을 구체화하는 단계이다.
- **증적 검증•책임 공백 개선(Audit Evidence Verification & Void Remediation)**: 증적을 검증하여 식별된 책임 공백을 시정 조치하는 단계이다.

</details>

```text
[서비스·계약 경계]
          |
          +-- [클라우드 제공자]
          |          |
          |          v
          |   1. 제공자 통제·증적 추출 --+
          |                               |
          `-- [클라우드 고객]             |
                     |                    |
                     v                    |
              2. 고객 통제·소유자 정의 --+
                                          |
                                          v
                                [통제 거버넌스]
                                          |
                                          v
                         3. 서비스 계층·책임 경계 매핑
                                          |
                                          v
                         4. RACI·책임 검증 계획 수립
                                          |
                                          v
                                 [감사·사고 대응]
                                          |
                                          v
                         5. 증적 검증·책임 공백 개선
                                          |
                                          `-- 공백·사고 개선 결과
```

### 동작 원리

1. **제공자 통제•증적 추출**: CSP 통제•감사 보고서 확인
2. **고객 통제•소유자 정의**: 데이터•IAM•OS 책임자 지정
3. **서비스 계층•책임 경계 매핑**: CSP•고객•공동 영역 구획
4. **RACI•책임 검증 계획 수립**: 역할•증적 검증 기준 정의
5. **증적 검증•책임 공백 개선**: 누락 통제 식별•보완

#### 한줄 요약

- 통제 소유자 정의, 레이어별 책임 매핑, RACI 매트릭스 수립 및 주기적 증적 검증으로 책임 공백을 해소한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **서비스형 인프라(Infrastructure as a Service, IaaS)**: 컴퓨팅 자원(VM, Storage, Network)을 제공받고 OS부터 응용까지 고객이 직접 통제하는 모델이다.
- **서비스형 플랫폼(Platform as a Service, PaaS)**: 개발 런타임, DB를 CSP가 관리하고, 고객은 애플리케이션 및 데이터 보안만 전담하는 모델이다.
- **서비스형 소프트웨어(Software as a Service, SaaS)**: 완제품 소프트웨어를 제공받아 고객은 사용자 계정 access 및 데이터 보안만 관리하는 모델이다.
- **운영체제(Operating System, OS)**: 하드웨어와 앱을 연결하는 시스템으로 IaaS 환경의 핵심 고객 관리 대상이다.

</details>

| 클라우드 서비스 모델 | IaaS (예: AWS EC2) | PaaS (예: AWS RDS, App Runner) | SaaS (예: M365, Salesforce) |
|:---|:---|:---|:---|
| 적용 기준 | 인프라 제어 최상, 커스텀 필요 환경 | 애플리케이션 개발 생산성 중심 환경 | 즉시 사용 가능한 표준 비즈니스 앱 |
| CSP 책임 영역 | 물리 데이터센터, 하드웨어, 하이퍼바이저 | 인프라 + OS + 미들웨어 + DB 런타임 보안 | 인프라 + OS + 런타임 + 앱 소프트웨어 전반 |
| 고객 책임 영역 | **OS** 패치, 네트워크 방화벽, 데이터, IAM | 애플리케이션 코드 보안, DB 데이터, IAM | 데이터 분류, 사용자 계정/권한 통제(IAM) |
| 빈번 사고 원인 | OS 미패치, S3 Public 공개 설정 오류 | 미들웨어 취약점, 비인가 DB 접근 | 계정 도용, 비인가 외부 파일 공유 설정 |

#### 한줄 요약

- IaaS는 OS 패치부터 고객 책임이며, PaaS와 SaaS로 갈수록 CSP 책임 범위가 확장되나 데이터/계정 관리는 항상 고객 책임이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **NIST SP 800-145**: 클라우드 컴퓨팅의 5대 필수 특징, 3대 서비스 모델, 4대 배치 모델의 정의 표준이다.
- **ISO/IEC 27017:2015**: 클라우드 서비스 제공자와 고객의 개별 정보보호 통제 및 가이드라인을 제시하는 국제 클라우드 보안 표준이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 책임 한계 오인 및 서비스 모델별 분류 미비 | **NIST SP 800-145** 규격 적용 | IaaS/PaaS/SaaS 서비스 계층별 통제 한계 수립 |
| 클라우드 보안 통제 표준 가이드 부재 | **ISO/IEC 27017:2015** 준용 | CSP-Customer 간 37개 클라우드 전용 보안 통제 항목 정렬 |
| 스토리지 퍼블릭 노출 등 설정 오류 | CSPM(Cloud Security Posture Management) 연동 | 자동화된 오설정 탐지 및 실시간 책임 공백 차단 |

#### 한줄 요약

- NIST SP 800-145 및 ISO 27017 표준을 준용하여 통제 경계를 정립하고, CSPM 툴로 고객 책임 영역의 오설정을 탐지한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **통제별 책임 완결성(Control Responsibility Completeness)**: 전체 클라우드 기술 스택에 단 하나의 미지정 영역도 존재하지 않도록 책임 및 검증을 명확화한 상태이다.

</details>

- **통제별 책임 완결성**을 확보하고 **IaaS**, **PaaS**, **SaaS**의 서비스 모델에 입각한 고객 전담 보안 통제를 철저히 집행한다.

#### 한줄 요약

- **IaaS•PaaS•SaaS 책임 경계**별 고객 통제 집행
