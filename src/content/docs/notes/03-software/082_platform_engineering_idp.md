---
sidebar:
  order: 82
  label: "082. 플랫폼 엔지니어링 IDP (Platform Engineering IDP)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "플랫폼 엔지니어링 IDP (Platform Engineering IDP)"
date: "2026-08-13T18:26:00+09:00"
tags:
  - "notes-software"
weight: 82
extra:
  question_no: "082"
  source_status: "기출"
  source_history: "134회, 135회"
  priority: 70
  priority_note: "134•135회 반복, IDP•셀프서비스 설계 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Platform Engineering (플랫폼 엔지니어링)**: 소프트웨어 개발팀이 복잡한 인프라나 K8s 설정 조작 없이, 애플리케이션 개발 본연에 집중할 수 있도록 셀프서비스 방식의 개발 인프라 플랫폼(IDP)을 구축 및 제품(Product)으로 운영하는 현대적 운영 패러다임.
- **IDP (Internal Developer Platform, 내부 개발자 플랫폼)**: 플랫폼 엔지니어링 팀이 구축한 전사 단일 셀프서비스 포털로, 환경 생성, CI/CD 배포, 텔레메트리 모니터링을 클릭 몇 번이나 API로 즉각 자동 처리하는 내부 전용 인프라 플랫폼.
- **Cognitive Load (인지 부하)**: 개별 개발자가 개발 외에 K8s YAML, Terraform, IAM 보안 설정 등 지나치게 많은 인프라 기술 지식을 습득해야 할 때 발생하는 정신적 병목 부담.

</details>

- 정의/개념: DevOps의 "You Build It, You Run It" 과도한 인지 부하를 해소하고, 개발자 셀프서비스 기반의 표준 인프라 가드레일을 제공하는 플랫폼 구축 패러다임인 **Platform Engineering & IDP**
- 배경/필요성: 팀별 인프라 직접 운영은 **인지 부하•대기•구성 편차** 유발

#### 한줄 요약

- 검증된 경로를 통한 내부 개발자 플랫폼의 셀프서비스 제공이 핵심이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Self-Service Capabilities**: 개발자가 인프라팀에 티켓을 끊어 기다리지 않고, IDP 포털에서 클릭 1번으로 K8s Namespace, DB, Redis 인스턴스를 동적 자동 프로비저닝하는 기능.
- **Golden Path (황금 경로)**: 플랫폼 팀이 전사범위로 검증한 가장 안전하고 표준화된 템플릿 기반 개발-배포-운영 가이드라인 경로.

</details>

- 개발자 **Cognitive Load (인지 부하)** 감축 및 개발자 경험(DX) 극대화
- **Self-Service Capabilities (셀프서비스)** 및 **Golden Path (표준 황금 경로)** 제공
- **Thick DevOps에서 Thin DevOps로의 전환** (플랫폼팀이 인프라 복잡성 추상화 은닉)

#### 한줄 요약

- 포털 추상화, 정책 코드 가드레일, 플랫폼 제품 운영이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Backstage**: Spotify가 공개한 대표적인 CNCF 오픈소스 내부 개발자 포털(IDP) 프레임워크로, 서비스 카탈로그, 템플릿, 문서(TechDocs)를 단일 웹 UI로 통합.

</details>

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. Developer Control Plane (개발자 단일 포털: Backstage UI / CLI)       │
├─────────────────────────────────────────────────────────────────────────┤
│ 2. Integration & Orchestration Plane (IDP Core Orchestrator: Humanitec)│
├─────────────────────────────────────────────────────────────────────────┤
│ 3. Security & Policy Plane (Policy-as-Code: Open Policy Agent - OPA)    │
├─────────────────────────────────────────────────────────────────────────┤
│ 4. Resource Plane (Infra Automation: Terraform, Crossplane, Helm)       │
├─────────────────────────────────────────────────────────────────────────┤
│ 5. Infrastructure Plane (K8s, AWS, GCP, Azure, Databases)             │
└─────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 개발자가 최상단 Control Plane(Backstage)에서 셀프서비스를 요청하면, 하부 Orchestration 및 Resource Plane이 OPA 보안 검증 후 K8s/AWS 자원을 자동 프로비저닝하는 5대 레이어 구조.

| 구성요소 | 책임 |
|:---|:---|
| 개발자 포털 | 템플릿•문서•서비스 상태의 단일 진입점 제공 |
| 서비스 카탈로그 | 소유자•의존성•운영 메타데이터 관리 |
| 자동화 워크플로 | 표준 환경 생성•배포•운영 절차 실행 |
| 정책 가드레일 | 보안•비용•신뢰성 정책을 코드로 검증 |

#### 한줄 요약

- 개발자 포털, 서비스 카탈로그, 자동화 워크플로, 정책 가드레일의 연결 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Score Spec**: 개발자가 인프라 상세 지식 없이 `score.yaml` 에 필요 자원(DB, Cache)을 선언하면 IDP가 환경별(Dev/Prod)로 알맞은 Terraform/Helm 자원으로 번역해 주는 오픈 소스 표준 사양.

</details>

```text
┌──────────────────────────────┐
│ Backstage Portal 로그인      │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 검증된 경로 선택          │
│ 2. 요청값•소유자 입력        │
│ 3. 정책 가드레일 판정        │
│ 4. 자원•파이프라인 생성      │
│ 5. 사용 성과•피드백 수집     │
└──────────────┬───────────────┘
               ▼
 [Dev DB/App 1분 만에 생성 완결]
```

### 동작 원리

1. 검증된 경로 선택: 서비스 유형에 맞는 템플릿 선택.
2. 요청값•소유자 입력: 환경•자원•책임팀 정보 구체화.
3. 정책 가드레일 판정: 보안•비용•신뢰성 정책 검증.
4. 자원•파이프라인 생성: 자동화 엔진이 환경과 전달 경로 구성.
5. 사용 성과•피드백 수집: 처리 시간•실패율•우회율 측정.

#### 한줄 요약

- 템플릿•요청값 구체화부터 사용 성과•개선 피드백까지의 제품 개선 흐름이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Product Mindset**: 플랫폼 엔지니어링 팀은 플랫폼을 내부 개발자(User)에게 파는 '제품(Product)'으로 생각하여 개발자 만족도(NPS, DX)를 지속 관측 및 개선하는 사상.

</details>

| 비교 항목 | Traditional DevOps | SRE (Site Reliability Eng.) | Platform Engineering |
|:---|:---|:---|:---|
| 핵심 슬로건 | "You Build It, You Run It" | "Class SRE implements DevOps" | **"You Build It, Platform Empowers It"** |
| 주 초점 영역 | 개발과 운영의 문화적 결합 | **시스템 신뢰성, SLA/SLO, 장애 예방** | **개발자 인지 부하 감축, IDP 셀프서비스** |
| 인프라 접근 | 각 개발팀이 직접 K8s/AWS 조작 | SRE 팀이 운영 모니터링 관리 | **플랫폼팀이 복잡성을 추상화 은닉** |
| 주요 산출물 | CI/CD 스크립트 | Error Budget, SLI/SLO | **IDP (Backstage Portal), Golden Path** |

#### 한줄 요약

- 반복 표준은 내부 개발자 플랫폼, 비정형 예외는 전통적 공용 인프라팀이 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Platform As A Product**: 플랫폼 엔지니어링 추진 시 인프라를 일방적으로 강요하지 않고, 내부 스버베이 및 DX 측정을 통해 피드백 로드맵을 구축하는 운영 방식.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 기존 개발자들이 IDP 포털을 외면하고 과거 방식으로 인프라팀에 문의 | **Golden Path의 압도적 편의성 제공 & Platform As A Product 마인드 정착**| 플랫폼 채택률 극대화 |
| 지나치게 경직된 추상화로 정밀 인프라 튜닝 불가능 | **Escape Hatch (필요시 하부 인프라 직접 조작 허용) 예외 통로 마련**| 튜닝 자율성 보존 |
| IDP 구축을 위한 초기 구축 비용 및 공수 오버헤드 | **오픈소스 Backstage + Crossplane 기반 미니멀 MVP로 출발** | 초기 비용 최적화 |

> 사례: **카카오 / 쿠팡 / 토스 전사 차원의 Spotify Backstage 기반 IDP 구축**

#### 한줄 요약

- 처리 시간, 실패율, 우회율, 만족도에 기반한 플랫폼 개선이 핵심이다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **플랫폼 엔지니어링 수립 기준(Platform Engineering Standards)**: 개발 조직 인지 부하 수준, CNCF Backstage/OPA 수용성 및 DX 생산성 지표에 의거한 체계.

</details>

- 반복 수요는 **IDP 검증 경로**, 비정형 예외는 **Escape Hatch** 적용

#### 한줄 요약

- 수요 특성에 맞는 개발 환경 제공 방식 선택 기준이 핵심이다.
