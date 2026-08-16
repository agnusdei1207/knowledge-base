---
sidebar:
  order: 52
  label: "052. 형상 관리: Git•브랜치 전략 (Configuration Management Git)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "형상 관리: Git•브랜치 전략 (Configuration Management Git)"
date: "2026-08-13T15:32:00+09:00"
tags:
  - "notes-software"
weight: 52
extra:
  question_no: "052"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "형상•브랜치 전략은 변경 통제 기반"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Configuration Management (SCM, 소프트웨어 형상 관리)**: 소프트웨어 생명주기 동안 변경되는 소스코드, 문서, 환경 설정 등의 변경 이력을 식별, 통제, 감사하여 시스템 무결성과 버전 추적성을 보장하는 공학적 활동.
- **Git & DVCS (Distributed Version Control System)**: 중앙 서버 외에 모든 개발자가 전체 히스토리를 가진 로컬 리포지토리(Local Repository)를 분산 소유하여 병렬 브랜치 작업 및 오프라인 커밋을 지원하는 분산 형상 관리 시스템.
- **Branch Strategy (브랜치 전략)**: 다수의 개발자가 동일 코드베이스에서 병렬로 개발할 때, 충돌을 최소화하고 안정적인 배포(Mainline)를 유지하기 위해 브랜치 생성, 병합(Merge), 릴리스 흐름 규칙을 정립한 워크플로우 (GitFlow, Trunk-based).

</details>

- 정의/개념: 소프트웨어 개발 과정의 모든 산출물(코드, 문서, 설정)에 대한 버전 식별, 통제 및 추적성을 분산 저장소(Git)와 전략적 워크플로우를 통해 체계화하는 **Configuration Management & Git Branch Strategy**
- 배경/필요성: 병렬 변경의 기준선 부재는 **덮어쓰기•릴리스 재현 실패** 유발

#### 한줄 요약

- 변경을 식별•통제하고 승인 상태를 재현하는 형상 관리가 핵심이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Baseline (형상 기준선)**: 공식적으로 검토 및 승인되어 향후 변경 통제(CCB)의 기준점이 되는 소프트웨어 형상 항목(Configuration Item)의 버전 집합체.
- **DAG (Directed Acyclic Graph)**: Git이 커밋(Commit)들의 부모-자식 관계와 히스토리 병합 흐름을 관리하기 위해 내부적으로 사용하는 방향성 비순환 그래프 데이터 구조.

</details>

- 분산 버전 관리(**DVCS**) 기반의 빠른 로컬 커밋 및 브랜칭
- **DAG (Directed Acyclic Graph)** 기반의 커밋 히스토리 추적 및 무결성(SHA-1/SHA-256) 보장
- 형상 식별, 통제, 감사(Audit), 기록의 SCM 4대 기본 활동 및 **Branch Strategy** 인가

#### 한줄 요약

- 분산 버전 관리 시스템의 이력과 커밋 계보 기반 변경 통합이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **3가지 작업 영역 (Three Trees)**: Git이 파일을 관리하는 3개 구역으로 Working Directory(작업 공간), Staging Area(Index, 커밋 대기 공간), Repository(Git Directory, 영구 커밋 보관소).

</details>

```text
[작업 공간 (Working Directory)]
      | (git add)
      ▼
[Staging Area (Index)]
      | (git commit)
      ▼
[로컬 저장소 (Local Repository)]
      | (git push)
      ▼
[원격 저장소 (Remote Repository)]
```

선의 의미: 파일 변경이 `git add`로 Staging Area에 등록되고, `git commit`으로 Local Repository에 래칭된 후 `git push`로 Remote에 동기화되는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| 작업 공간 (Working Directory) | 실제 파일 수정 상태 보관 |
| Staging Area (Index) | 다음 커밋에 포함할 파일 스냅샷 선택 |
| 로컬 저장소 (Local Repository) | 커밋 객체•트리•참조와 계보 보관 |
| 원격 저장소 (Remote Repository) | 팀 간 참조 공유와 통합 기준선 제공 |

#### 한줄 요약

- 작업 트리, 인덱스, 객체 데이터베이스, 참조의 연결 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Merge vs Rebase**: Merge는 두 브랜치 줄기를 합쳐 새로운 커밋(Merge Commit)을 남기는 방식, Rebase는 브랜치의 베이스 커밋을 재조정하여 깔끔한 단일 일자형 히스토리를 유지하는 방식.

</details>

```text
┌──────────────────────────────┐
│ 작업 공간 파일 수정          │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. Staging 이송             │
│ 2. 로컬 커밋                │
│ 3. Push•PR                  │
│ 4. CI 검증•Code Review      │
│ 5. Mainline 병합            │
└──────────────┬───────────────┘
               ▼
   [신규 Baseline 형성 완료]
```

### 동작 원리

1. **Staging 이송**: `git add`로 선택 파일의 Index 스냅샷 갱신
2. **로컬 커밋**: 트리와 부모 참조를 가진 커밋 객체 생성
3. **Push**•**PR**: 원격 브랜치를 공유하고 변경 검토 요청 생성
4. **CI 검증·Code Review**: 자동 검사와 동료 검토로 병합 조건 판정
5. **Mainline 병합**: 보호된 기준 브랜치에 승인 변경 통합

#### 한줄 요약

- 선택 변경 스냅샷부터 기준선 병합까지의 검증 흐름이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **GitFlow**: master, develop, feature, release, hotfix 5개 브랜치를 활용하여 정기적 대규모 릴리스를 지원하는 전통적 브랜치 전략.
- **Trunk-based Development**: 모든 개발자가 단일 main(Trunk) 브랜치에 매일 수차례 짧은 수명의 Feature 브랜치를 지속 통합(CI)하는 현대적 애자일/DevOps 브랜치 전략.

</details>

| 비교 항목 | GitFlow (전통적 확장형) | Trunk-based Development (현대 애자일형) |
|:---|:---|:---|
| 브랜치 구조 | develop•feature•release•hotfix 역할 분리 | main 중심의 짧은 feature 브랜치 |
| 브랜치 수명 | 릴리스 병행을 위한 장기 브랜치 가능 | 통합 지연을 줄이는 짧은 브랜치 |
| 통합/배포 주기 | 정기적 릴리스 주기 (배치 통합) | **지속적 통합 및 배포 (CI/CD 상시 지속 배포)** |
| 충돌 위험 | 장기 분기 시 병합 충돌 증가 | 작은 단위의 잦은 병합으로 충돌 범위 축소 |
| 필수 전제조건 | 정적 배포 절차, 수동 테스트 환경 | **고도로 자동화된 CI/CD 및 자동 테스트 파이프라인** |

#### 한줄 요약

- 잦은 배포에는 트렁크 기반 개발, 병행 버전에는 깃플로가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Protected Branch**: main/master 브랜치에 직접적인 `git push`를 금지하고, 반드시 PR 통과 및 CI 성공 시에만 병합을 허용하는 보안 통제 설정.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| main 브랜치에 무단 직투입(Direct Push)하여 코드 파괴 | **Protected Branch** 설정 및 필수 PR 승인자(Min 1~2명) 인가 | 메인라인 안정성 보장 |
| API Key / DB 비밀번호가 Git 커밋 히스토리에 유출 | **git-secrets, Gitleaks** 등 Pre-commit Hook 연동 | 보안 사고 조기 차단 |
| 장기 Feature 브랜치로 인한 최악의 Merge Hell 발생 | **Trunk-based 전환** 및 1일 1회 이상 메인라인 Rebase/Merge | 병합 충돌 최소화 |

> 사례: GitHub Enterprise + **Trunk-based Development + Protected Branch Rule** 적용

#### 한줄 요약

- 보호 브랜치, 필수 CI, 검토 승인에 기반한 기준선 보호가 핵심이다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **형상 통제 수립 기준(Configuration Management Standards)**: 배포 빈도, 조직 팀 규모, 테스트 자동화 수준에 기반한 브랜치 전략 선정 체계.

</details>

- **형상 통제 수립 기준**에 따라 continuous delivery 지향 시 **Trunk-based Development + Protected Main Branch** 채택

#### 한줄 요약

- 배포 주기와 지원 방식에 맞는 브랜치 전략으로 변경 추적성을 확보하는 것이 핵심이다.
