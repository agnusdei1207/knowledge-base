---
sidebar:
  order: 141
  label: "141. 클라우드 서비스 모델: IaaS•PaaS•SaaS"
  badge:
    text: "기출 · 70%"
    variant: note
title: "클라우드 서비스 모델: IaaS•PaaS•SaaS (Cloud Service Models)"
date: "2026-08-26T09:57:00+09:00"
tags:
  - "notes-software"
weight: 141
extra:
  question_no: "141"
  source_status: "기출"
  source_history: "120회, 125회, 131회, 132회"
  priority: 70
  priority_note: "서비스별 운영 책임 경계가 반복 출제됨"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **클라우드 3대 서비스 모델(NIST)**: IaaS(가상화 인프라 제공), PaaS(개발 런타임 제공), SaaS(완성형 소프트웨어 구독 제공).
- **공동 책임 모델(Shared Responsibility)**: CSP와 고객 간에 하드웨어, OS, 미들웨어, 애플리케이션, 데이터의 관리 책임을 분계하는 모델.

</details>

- 정의/개념: IT 자원의 제어 권한과 운영 책임 범위에 따라 **인프라 제공(IaaS), 플랫폼 제공(PaaS), 완성형 소프트웨어 제공(SaaS)** 으로 분류한 클라우드 아키텍처
- 배경/필요성: 온프레미스 인프라의 고비용 부담 및 클라우드 도입 시 **제어권과 운영 관리 책임 경계 불명확에 따른 보안 설정 누락 해결 불가**

#### 한줄 요약
- 제어권의 수준과 운영 효율성에 따라 IaaS, PaaS, SaaS를 선택하여 비즈니스 민첩성을 극대화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Control vs Convenience Trade-off**: IaaS는 OS 및 커널 수준의 높은 자유도를 제공하지만 운영 부담이 크고, SaaS는 관리 부담이 0이지만 커스터마이징이 제한적.
- **Pay-as-you-go**: 사용한 컴퓨팅 자원 및 구독 라이선스 수량만큼만 비용을 지불하는 종량제 모델.

</details>

- 서버 가상화, 런타임, 앱 계층별 **명확한 운영 책임 경계 분리(Separation of Concerns)**
- 인프라 구축 기간을 수개월에서 수 분으로 단축하는 **신속한 온디맨드 프로비저닝**
- 사용한 자원과 기간만큼만 지불하는 **종량제(Pay-as-you-go) 비용 최적화**

#### 한줄 요약
- 계층별 책임 분리, 신속한 프로비저닝, 종량제 비용 모델을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **IaaS / PaaS / SaaS 스택 계층**: Applications, Data, Runtime, Middleware, OS, Virtualization, Servers, Storage, Networking.

</details>

```text
[클라우드 서비스 모델별 책임 경계 구조]
|-- IaaS (Infrastructure as a Service: AWS EC2, GCP Compute Engine)
|   |-- [고객 책임] Applications, Data, Runtime, Middleware, OS 패치
|   `-- [CSP 책임] Virtualization, Servers, Storage, Networking
|-- PaaS (Platform as a Service: AWS Elastic Beanstalk, Heroku)
|   |-- [고객 책임] Applications, Data
|   `-- [CSP 책임] Runtime, Middleware, OS, Virtualization, Hardware
`-- SaaS (Software as a Service: Google Workspace, Salesforce, Microsoft 365)
    `-- [CSP 책임] 애플리케이션부터 물리 인프라까지 전 계층 관리 (고객은 계정/데이터 사용)
```

선의 의미: 계층 및 IaaS(OS 이상 고객), PaaS(앱/데이터만 고객), SaaS(완제품 CSP 관리)의 관리 책임 경계 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| IaaS (인프라형) | 물리 서버/네트워크를 가상화하여 제공하며 **고객은 OS 설치, 미들웨어 구성, 보안 패치 전담** | 높은 제어권과 이식성 |
| PaaS (플랫폼형) | OS 및 실행 런타임(Java, Python 등)을 자동 제공하며 **고객은 비즈니스 코드와 데이터 배포에 집중**| 개발 생산성 극대화 |
| SaaS (소프트웨어형) | 완성된 웹/모바일 소프트웨어를 제공하며 **고객은 계정 권한 및 데이터 입력/활용만 수행** | 제로 인프라 관리 |
| 공동 책임 모델 | CSP(클라우드 자체의 보안)와 고객(클라우드 내부의 보안)의 **보안 및 규제 준수 경계 규정** | 보안 누락 방지 |

#### 한줄 요약
- IaaS(인프라 임대), PaaS(개발 런타임 제공), SaaS(완제품 서비스)로 역할을 체계화한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **서비스 모델 선정 5단계**: 제어 수준 식별 $\to$ 운영 역량 평가 $\to$ 데이터 규제 검토 $\to$ 모델 선정 $\to$ 책임 매트릭스 확정.

</details>

```text
기업의 신규 비즈니스 시스템 클라우드 구축 요청
        │
   [제어 수준 식별] 커널 튜닝, 특수 네트워크 프로토콜 등 OS 이하 제어 필수 여부 확인
        │
   [운영 역량 평가] 사내 엔지니어링 팀이 OS 보안 패치 및 미들웨어 장애를 감당 가능한지 평가
        │
   [규제 검토] 금융/공공 규제로 데이터 저장 위치와 암호화 키를 직접 통제해야 하는지 검토
        │
   [모델 선정] 고자유도는 IaaS, 빠른 개발은 PaaS, 범용 비즈니스 솔루션은 SaaS 선정
        │
   [책임 확정] 백업, DR, 계정 보안, 패치 등 영역별 고객-CSP 간 RACI 매트릭스 공식화
```

#### 한줄 요약
- 제어 식별 → 역량 평가 → 규제 검토 → 모델 선정 → 책임 확정 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **IaaS vs PaaS vs SaaS**: 제어권(IaaS), 개발 민첩성(PaaS), 즉시 사용성(SaaS).

</details>

| 비교 항목 | IaaS (인프라형) | PaaS (플랫폼형) | SaaS (소프트웨어형) |
|:---|:---|:---|:---|
| 고객 관리 범위 | **Applications, Data, Runtime, OS** | **Applications, Data** | **계정 설정 및 데이터 활용** |
| 벤더 종속성(Lock-in)| **매우 낮음 (타 CSP로 쉬운 이식)** | 중간 (CSP 전용 런타임 종속 가능) | 높음 (데이터 추출 및 이전 복잡) |
| 개발 및 출시 속도 | 인프라 설정 필요로 상대적 지연 | **코드 작성 즉시 배포로 매우 빠름** | **도입 즉시 사용 가능 (Zero Lead-time)**|
| 최적 적용 사례 | **레거시 C/S 이전, 커스텀 HPC 연산**| **웹/모바일 백엔드, MSA API 개발** | **전사 메일, CRM, ERP, 협업 도구** |

#### 한줄 요약
- 제어권과 이식성은 IaaS, 개발 생산성은 PaaS, 즉시 도입 편의성은 SaaS를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Misconfiguration**: IaaS의 Security Group 포트 전체 개방이나 S3 버킷 Public 오픈 등 고객 설정 오류로 인한 데이터 유출 사고.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| IaaS OS 보안 패치 누락으로 인한 랜섬웨어 감염 | **AWS Systems Manager(SSM) / Ansible 기반 자동 패치 파이프라인 구축** | 정기 보안 패치 100% 자동화 |
| PaaS 전용 프레임워크 사용에 따른 벤더 락인 | **Docker 컨테이너 및 Kubernetes(CaaS) 표준 런타임 기반 패키징** | 멀티 클라우드 자유로운 이식성 확보 |
| SaaS 도입 시 외부 서비스로의 기업 기밀 데이터 유출 | **CASB(Cloud Access Security Broker) 도입 및 DLP 정책 강제** | 비인가 데이터 반출 원천 차단 |
| 공동 책임 모델 오인으로 인한 백업 누락 | **서비스 모델별 책임 매트릭스(RACI) 수립 및 고객 주도 백업 자동화** | 장애 시 데이터 무손실 복구 |

#### 한줄 요약
- 자동 패치, 컨테이너 표준화, CASB 보안, 책임 매트릭스 정립으로 서비스 모델의 위험을 방어한다.

## Ⅶ. 결론

- 제어권 확보는 **IaaS**, 개발 생산성은 **PaaS** 선택

#### 한줄 요약
- 클라우드 서비스 모델은 제어권과 운영 효율성의 균형에 따라 IaaS, PaaS, SaaS를 최적으로 배치하는 엔터프라이즈 클라우드 아키텍처의 기본 분류 체계다.