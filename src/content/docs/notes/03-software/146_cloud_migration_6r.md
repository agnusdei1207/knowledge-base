---
sidebar:
  order: 146
  label: "146. 클라우드 마이그레이션 6R"
  badge:
    text: "기출 · 70%"
    variant: note
title: "클라우드 마이그레이션 6R (Cloud Migration 6R)"
date: "2026-08-25T11:00:00+09:00"
tags:
  - "notes-software"
weight: 146
extra:
  question_no: "146"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "이전 방식 선택과 단계별 위험 통제가 최근 출제됨"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **클라우드 마이그레이션 6R**: 레거시 워크로드를 클라우드로 이전할 때 가치와 제약에 따라 결정하는 6대 전략(Rehost, Replatform, Refactor, Repurchase, Retain, Retire).
- **Lift-and-Shift**: 코드 수정 없이 가상머신 이미지를 클라우드로 그대로 복제 이전하는 Rehost 방식.

</details>

- 정의/개념: 온프레미스 레거시 시스템을 클라우드로 이관 시 **비즈니스 가치와 복잡도에 따라 Rehost, Replatform, Refactor, Repurchase, Retain, Retire 6가지 전략으로 분류한 의사결정 프레임워크**
- 배경/필요성: 모든 레거시 시스템을 획일적 전면 재개발(Big-Bang)로 추진 시 발생하는 **예산 초과, 프로젝트 지연 및 이관 실패로 인한 비즈니스 마비 해결 불가**

#### 한줄 요약
- 시스템의 가치와 복잡도에 따라 6가지 전략을 최적 매핑하여 안전한 클라우드 전환을 완수한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Replatform (Lift-Shift-and-Tweak)**: 코드는 유지하면서 DB만 관리형 PaaS(RDS)로 교체하여 운영 부담을 줄이는 부분 최적화.
- **Refactor (Re-architect)**: MSA 및 쿠버네티스/서버리스 기반의 클라우드 네이티브로 전면 재개발하는 전략.

</details>

- 단순 리프트앤시프트부터 전면 클라우드 네이티브까지 **단계별 이전 경로 제공**
- 상용 SaaS 전환(Repurchase), 현행 유지(Retain), 자산 폐기(Retire)를 포함한 **포괄적 자산 최적화**
- 시스템 간 상호 의존성을 분석하여 차수별로 이전하는 **Wave 기반 단계적 컷오버**

#### 한줄 요약
- 6대 이전 전략과 Wave 기반 단계적 컷오버를 통해 마이그레이션 위험을 최소화한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **6R 3대 영역 분류**: Technical Migration(기술 이전), Modernization(현대화 재설계), Business Disposition(비즈니스 정제).

</details>

```text
[클라우드 마이그레이션 6R 전략 구조]
|-- 1. Technical Migration (기술 인프라 이전)
|   |-- Rehost (Lift-and-Shift: 코드 수정 0%, EC2 VM 복제)
|   `-- Replatform (Lift-and-Tweak: 관리형 RDS/PaaS 교체)
|-- 2. Modernization (클라우드 네이티브 현대화)
|   `-- Refactor (Re-architect: MSA, K8s 컨테이너, 서버리스 전면 재개발)
`-- 3. Business Disposition (비즈니스 및 자산 정제)
    |-- Repurchase (Drop-and-Shop: 상용 SaaS 완제품 도입)
    |-- Retain (Do Nothing: 규제 및 잔존 감가상각으로 현행 유지)
    `-- Retire (Decommission: 중복 및 불필요 레거시 자산 영구 폐기)
```

선의 의미: 계층 및 전사 레거시 자산을 기술 이전, 현대화, 비즈니스 정제의 3대 영역 6가지 전략으로 분기 배치하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **Rehost (재호스팅)** | 애플리케이션 수정 없이 **가상머신(EC2)으로 그대로 이전하여 마이그레이션 속도 극대화** | Lift-and-Shift |
| **Replatform (재플랫폼)**| 코드는 유지하되 **DB를 RDS 등 클라우드 관리형 PaaS로 교체하여 운영 효율 향상** | Lift-and-Tweak |
| **Refactor (재설계)** | 핵심 비즈니스 시스템을 **MSA 및 컨테이너(K8s) 기반의 클라우드 네이티브로 전면 재개발** | Cloud-Native |
| **Repurchase (재구매)** | 레거시 커스텀 패키지를 **Salesforce, Workday 등 완성형 SaaS 솔루션으로 대체** | Drop-and-Shop |
| **Retain (유지)** | 기술적 제약이나 감가상각이 남은 시스템을 **당분간 온프레미스에 그대로 존치** | 위험 분산 |
| **Retire (폐기)** | 더 이상 비즈니스 가치가 없거나 중복된 **레거시 서버 및 소프트웨어 영구 종료** | 비용 절감 |

#### 한줄 요약
- Rehost, Replatform, Refactor, Repurchase, Retain, Retire가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **6R 마이그레이션 5단계**: 자산 실사 $\to$ 가치/복잡도 평가 $\to$ 6R 전략 매핑 $\to$ Wave 그룹핑 $\to$ CDC 동기화 및 컷오버.

</details>

```text
기업 전사 온프레미스 IT 자산의 클라우드 마이그레이션 추진
        │
   1. [자산 실사] Discovery Service를 통해 서버 인벤토리, OS 버전, 네트워크 의존성 맵 수집
        │
   2. [가치 평가] 워크로드의 비즈니스 중요도, 변경 빈도, 유지보수 비용, 라이선스 만료일 평가
        │
   3. [전략 매핑] 미사용 자산은 Retire, 핵심 차별화 앱은 Refactor, 단순 이전은 Rehost 확정
        │
   4. [Wave 수립] 데이터베이스와 강결합된 서버들을 동일한 Wave(이관 차수)로 그룹핑
        │
   5. AWS DMS CDC로 데이터를 실시간 동기화한 후 야간 DNS 스위칭으로 무중단 컷오버 완료
```

#### 한줄 요약
- 자산 실사 → 가치 평가 → 전략 매핑 → Wave 수립 → CDC 컷오버 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **3대 기술 이전 전략 비교**: Rehost(신속 이전), Replatform(부분 개선), Refactor(전면 현대화).

</details>

| 비교 항목 | Rehost (Lift-and-Shift) | Replatform (Lift-and-Tweak) | Refactor (Cloud-Native) |
|:---|:---|:---|:---|
| 코드 수정 범위 | **수정 0% (완전 무수정)** | **부분 수정 (DB/연동 설정)** | **전면 재설계 (MSA/컨테이너)** |
| 이관 소요 기간 | **수일 ~ 수주 (가장 빠름)** | 수주 ~ 수개월 (중간) | 수개월 ~ 수년 (장기화) |
| 클라우드 이점 활용| 최소 (IaaS 비용 절감 위주)| 중간 (관리형 PaaS 운영 절감) | **최대 (오토스케일링/탄력성 극대화)**|
| 최적 적용 대상 | **데이터센터 임대 만료 긴급 이전**| **DB 운영 부담 해소가 필요한 앱** | **핵심 고객 서비스, 트래픽 폭증 앱**|

#### 한줄 요약
- 신속성은 Rehost, 운영 효율은 Replatform, 궁극의 확장성은 Refactor를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **AWS DMS CDC**: 온프레미스 DB의 트랜잭션 변경 로그를 클라우드 DB로 실시간 복제하여 컷오버 시 다운타임을 수 분 이내로 단축하는 도구.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 모든 시스템을 무리하게 MSA로 전면 재개발하려다 예산 초과 | **Rehost로 일단 신속 이관 후 2단계로 Refactor 분할 추진** | 프로젝트 성공률 극대화 및 리스크 분산 |
| 파악되지 않은 레거시 통신 의존성 누락으로 이관 후 장애 | **Discovery Service 기반 정밀 네트워크 의존성 맵 사전 분석** | 숨은 의존성 결함 사전 차단 |
| 대용량 데이터베이스 이관 시 장시간 서비스 다운타임 발생 | **AWS DMS(Database Migration Service) CDC 실시간 동기화 적용** | 컷오버 다운타임 수 분 이내 단축 |
| 이관 후 예상치 못한 클라우드 인프라 비용 폭증 | **사전 TCO 및 Right-Sizing 분석을 통한 인스턴스 최적화** | 클라우드 운영 비용 30% 절감 |

#### 한줄 요약
- 2단계 접근법, 의존성 맵 분석, DMS CDC 실시간 동기화, Right-Sizing으로 성공을 보장한다.

## Ⅶ. 결론

- 성공적인 엔터프라이즈 클라우드 전환을 위해 **자산 실사와 가치 평가를 거쳐 시스템별 6R 전략을 최적 매핑하고, DMS CDC 기반 무중단 컷오버와 2단계 점진적 현대화(Rehost $\rightarrow$ Refactor) 전략**을 결합하여 무결점 클라우드 마이그레이션 완성

#### 한줄 요약
- 클라우드 마이그레이션 6R은 시스템의 비즈니스 가치와 기술 부채를 종합 평가하여 최적의 이전 방식을 결정짓는 실증적 마이그레이션 의사결정 프레임워크다.