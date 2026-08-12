---
sidebar:
  order: 146
  label: "146. 클라우드 마이그레이션 6R (Cloud Migration 6R)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "클라우드 마이그레이션 6R (Cloud Migration 6R)"
date: "2026-08-06T23:27:50+09:00"
tags: ["notes-software"]
weight: 146
extra:
  question_no: "146"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "이전 방식 선택과 단계별 위험 통제가 최근 출제됨"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Cloud Migration 6R Framework**: AWS가 정립한 기업 레거시 시스템의 클라우드 이관 및 현대화 6대 전략 (Rehost, Replatform, Refactor/Re-architect, Repurchase, Retain, Retire).
- **Rehost (Lift-and-Shift)**: 기존 레거시 앱과 OS를 코드 변경 0% 상태로 클라우드 가상머신(EC2)으로 그대로 뜬 떠옮기는 전략.
- **Replatform (Lift-Shift-and-Tweak)**: 앱 코드는 보존하되, DB나 미들웨어를 클라우드 관리형 서비스(RDS, ElastiCache)로 부분 교체하는 전략.
- **Refactor / Re-architect (Cloud-Native)**: 클라우드 네이티브 아키텍처(MSA, Serverless, Container)로 앱 코드를 전면 재개발 및 재설계하는 최고 난이도 전략.

</details>

- 정의/개념: 기업의 온프레미스 레거시 시스템을 클라우드로 이관 시 난이도, 비즈니스 가치, 비용에 따라 6가지 분기 전략으로 판정 이행하는 체계인 **Cloud Migration 6R Framework**
- 배경/필요성: 모든 레거시 시스템을 무차별 재개발(Refactor) 시 발생하는 비용 폭증 및 마이그레이션 실패 위험 차단 요구성

#### 한줄 요약

- 워크로드별 업무 가치와 기술 제약을 평가하여 재호스팅·리팩터링·재구매·유지·폐기 중 적합한 이전 전략을 선택한다.

## Ⅱ. 특징 (6R 전략의 6대 분기 매트릭스)

<details><summary>핵심 용어</summary>

- **Repurchase, Retain, Retire**: SW 완제품(SaaS) 교체(Repurchase), 당장 이관 없이 레거시 보존(Retain), 무의미 시스템 파기(Retire).

</details>

- **1. Rehost (Lift-and-Shift: 가장 빠르고 저위험, 기술 부채 잔존)**
- **2. Replatform (RDS, ElastiCache 등 관리형 PaaS 서비스 도입 튜닝)**
- **3. Refactor (Cloud-Native MSA, K8s, Serverless 전면 재설계)**
- **4. Repurchase (SaaS 교체), 5. Retain (보존), 6. Retire (폐기 파기)**

#### 한줄 요약

- 급히 비워야 할 짐은 그대로 옮기고 오래 쓸 설비는 고쳐 옮기되, 전원선으로 연결된 장비처럼 함께 움직여야 할 시스템은 같은 웨이브로 묶는다.

## Ⅲ. 구조 및 구성요소 (Cloud Migration 6R 6대 전략 매트릭스)

<details><summary>핵심 용어</summary>

- **Migration Wave**: 의존성이 얽힌 시스템들을 그룹핑(Wave 1, Wave 2)하여 순차적으로 마이그레이션을 가동하는 스케줄링 기법.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Cloud Migration 6R Framework                    │
├────────────────────────────────────────────────────────────────────────┤
│ Low Effort / Fast Speed                                High Effort / Value│
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│ │  1. Rehost   │  │2. Replatform │  │ 3. Repurchase│  │ 4. Refactor  │ │
│ │ Lift-n-Shift │  │ Lift-n-Tweak │  │ Drop to SaaS │  │ Cloud-Native │ │
│ └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘ │
├────────────────────────────────────────────────────────────────────────┤
│ Non-Migration Strategy: 5. Retain (현 상태 온프레미스 보존), 6. Retire (시스템 파기)│
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 이관 노력(Effort)과 비즈니스 가치(Value) 축에 따른 6R 마이그레이션 분류 아키텍처.

| 6R 전략 (Strategy) | 이관 메커니즘 및 주요 내용 | 대표 적용 유스케이스 |
|:---|:---|:---|
| **1. Rehost** | **기존 VM 이미지를 그대로 EC2로 수평 복제 이관** | 데이터센터 마감 기한 촉박 시 |
| **2. Replatform** | **앱 코드는 유지, DB만 AWS RDS 관리형으로 교체** | DB 패치 오버헤드 제거 |
| **3. Repurchase** | **기존 자체 구축 CRM을 Salesforce SaaS로 전면 대체**| 사내 레거시 메일 $\rightarrow$ Workspace |
| **4. Refactor** | **모놀리식을 Microservices (EKS, Lambda)로 전면 재설계**| 핵심 결제/주문 시스템 고도화 |
| **5. Retain** | **법적 규제나 노후화로 이관 불가능 시 현 상태 유지**| 메인프레임, 레거시 장비 |
| **6. Retire** | **더 이상 아무도 안 쓰는 쓰레기 서버 파기 소멸** | 90일간 트래픽 0% 더미 서버 |

#### 한줄 요약

- 자산 목록과 연결 지도를 평가표에 겹쳐 본 뒤, 각 시스템의 처리 방법과 함께 움직일 웨이브를 정하고 실패하면 돌아올 조건까지 붙인다.

## Ⅳ. 흐름도 (6R 마이그레이션 의사결정 나무 흐름)

<details><summary>핵심 용어</summary>

- **Migration Assessment Tree**: 시스템 가치, 기술 노후도, 데이터 주권을 측정하여 6R 중 최적 경로로 분류하는 의사결정 로직.

</details>

```text
[System Assessment]
  ├── 더 이상 쓰지 않는 시스템인가? ───────────────► [6. Retire (파기)]
  ├── 온프레미스 규제/특수장비 필수인가? ──────────► [5. Retain (유지)]
  ├── SaaS 솔루션으로 대체 가능한가? ────────────► [3. Repurchase (SaaS)]
  ├── IDC 마감 기한이 당장 3개월 이내인가? ────────► [1. Rehost (Lift-n-Shift)]
  ├── DB 오버헤드만 줄이고 싶은가? ──────────────► [2. Replatform (RDS)]
  └── 장기적 Cloud-Native MSA 재설계인가? ────────► [4. Refactor (MSA)]
```

### 동작 원리

1. **Discovery & Assessment**: AWS Application Discovery Service로 전사 500대 서버 트래픽 스캔.
2. **Classification**: 의사결정 나무에 의거 300대 Rehost, 100대 Replatform, 50대 Refactor, 50대 Retire 분류.
3. **Execution**: Wave 1부터 순차적으로 마이그레이션 실행 (**6R Migration 완결**).

#### 한줄 요약

- 연결된 장비를 한 차량에 묶고 도착지에서 작동과 자료를 확인한 뒤, 검사표를 통과하면 사용처를 바꾸고 실패하면 원래 장소로 돌린다.

## Ⅴ. 종류 및 비교 (Rehost vs Replatform vs Refactor 3대 핵심 이관 비교)

<details><summary>핵심 용어</summary>

- **Modernization Level**: Rehost (0% 현대화) $\rightarrow$ Replatform (30% 현대화) $\rightarrow$ Refactor (100% Cloud-Native 현대화).

</details>

| 비교 항목 | Rehost (Lift-and-Shift) | Replatform (Lift-and-Tweak) | Refactor (Cloud-Native) |
|:---|:---|:---|:---|
| **이관 속도** | **최상 (수일~수주일 내 완료)** | 중간 (수개월 소요) | **느림 (6개월~1년 이상 소요)** |
| **코드 변경 범위**| **0% (전혀 코드 안 건드림)** | 미세 수정 (DB 커넥션 튜닝) | **100% (MSA, Container 전면 재개발)** |
| **Cloud-Native 혜택**| 최하 (Cloud 이점 활용 불가) | 중간 (DB 자동 백업/패치 활용) | **최상 (오토스케일링, 고가용성 100%)** |
| **초기 이관 비용**| **최저 (저비용)** | 중간 | **최고 (개발 인력 투입 비용 과다)** |

#### 한줄 요약

- 이사 기한이 급하면 그대로 옮기고 장기 가치가 크면 고쳐 옮기며, 규제 때문에 못 옮기면 남기고 쓰지 않는 시스템은 연결 관계를 확인한 뒤 종료한다.

## Ⅵ. 실무 고려사항 및 대책 (6R 마이그레이션 3대 실무 지침)

<details><summary>핵심 용어</summary>

- **Cutover Strategy (전환 전략)**: 레거시에서 클라우드로 최종 스위칭 시 빅뱅(Big Bang) 전환과 단계적(Phased Rollout) 전환 선택.

</details>

| 3대 마이그레이션 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. All-Refactor Fallacy** | 모든 서비스를 다 MSA 재개발하려다 예산 오버 | **Rehost로 일단 빠르게 옮긴 후 차근차근 Refactor**|
| **2. Unknown Dependency** | 알려지지 않은 서버 간 조용한 의존성으로 다운 | **AWS Application Discovery Service로 의존성 시각화** |
| **3. Data Migration Sync** | 이관 도중 발생한 DB 델타 데이터 유실 | **AWS DMS (Data Migration Service) CDC 실시간 동기화**|

> 사례: **삼성전자 / KB국민은행 AWS 마이그레이션 6R 프레임워크 적용 사례**

#### 한줄 요약

- 자산 인벤토리와 의존성 맵을 함께 확인하고 연관 워크로드를 같은 웨이브로 묶은 뒤, 성공 기준을 통과한 시스템만 원 환경에서 해제한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **6R Framework 수립 기준(6R Migration Standards)**: Business Value, Effort, Rehost/Replatform/Refactor 분류 및 Wave 스케줄링에 의거한 체계.

</details>

- **6R Framework 수립 기준**에 따라 전사 클라우드 마이그레이션 수립 시 **Cloud Migration 6R Framework & AWS DMS** 필수 적용

#### 한줄 요약

- 이사 기한과 장기 사용 가치를 함께 보고 짐마다 옮길 방법을 고른 뒤, 서로 연결된 장비는 같은 웨이브로 묶는다.
