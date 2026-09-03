---
sidebar:
  order: 52
  label: "052. 형상 관리: Git•브랜치 전략"
  badge:
    text: "미출 · 50%"
    variant: note
title: "형상 관리: Git•브랜치 전략 (Configuration Management Git)"
date: "2026-08-31T10:48:00+09:00"
tags:
  - "notes-software"
weight: 52
extra:
  question_no: "052"
  source_status: "기출"
  source_history: ""
  priority: 50
  priority_note: "분산 버전 관리 구조와 브랜치 전략 기반 변경 통제"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **형상 관리(SCM: Software Configuration Management)**: 소프트웨어 생애주기 동안 소스 코드, 문서, 빌드 설정의 변경을 식별, 통제, 감사, 기록하는 공학 체계.
- **Git & 브랜치 전략**: 방향성 비순환 그래프(DAG) 기반의 분산 버전 관리 도구와 팀 협업 및 배포 흐름을 정의한 브랜치 운영 규칙.

</details>

- 정의/개념: 소프트웨어 자산의 변경을 체계적으로 통제하고, **Git(분산 버전 관리)** 과 **브랜치 전략**으로 병렬 개발과 지속 통합을 지원하는 형상 관리 체계
- 배경/필요성: 다수 개발자의 동시 수정에 따른 **덮어쓰기 충돌, 변경 이력 유실 및 배포 형상 불일치로 인한 릴리즈 장애 한계**

#### 한줄 요약
- 소프트웨어 변경 이력을 무결하게 관리하고 브랜치 전략으로 안정적인 협업과 배포를 지원한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **DAG(Directed Acyclic Graph)**: Git 내부에서 각 커밋이 부모 커밋의 해시를 단방향 참조하여 형성하는 순환 없는 버전 그래프.
- **형상 4대 활동**: 형상 식별(CI 정의), 형상 통제(CCB 승인), 형상 감사(무결성 검증), 형상 기록(이력 추적).

</details>

- 완전한 로컬 복제본 기반의 빠른 브랜치 생성 및 오프라인 독립 작업 지원(**DVCS**)
- **DAG (Directed Acyclic Graph)** 및 SHA-1/SHA-256 암호학적 해시 기반의 이력 무결성 보증
- 형상 식별·통제·감사·기록의 **SCM 4대 활동과 CI/CD 파이프라인의 완벽한 융합**

#### 한줄 요약
- DAG 이력은 변경 추적과 병렬 작업을 가능하게 하는 대신 병합 충돌 해소라는 새 작업을 만들므로, 브랜치 전략은 그 충돌 빈도를 조절하는 손잡이가 된다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Git 3대 영역(Working Tree, Staging Area, Local Repo)**: 작업 폴더(Working Tree) $\to$ `git add`(Staging) $\to$ `git commit`(Local Repo)의 단계별 격리 구조.

</details>

```text
[Git 3단계 영역 및 원격 저장소 구조]
|-- 작업 디렉터리 (Working Directory: 실제 소스 코드 수정 공간)
|-- 스테이징 영역 (Staging Area / Index: `git add`로 선별된 스냅샷)
|-- 로컬 저장소 (Local Repository: `git commit`으로 생성된 객체 DB - Blob, Tree, Commit)
`-- 원격 저장소 (Remote Repository: GitHub/GitLab - `git push` 및 PR 코드리뷰)
```

선의 의미: 계층 및 단계별 Git 커밋 생명주기

| 구성요소 | 책임 |
|:---|:---|
| 작업 디렉터리 | 파일 시스템 상에서 실제 소스 코드를 편집하는 로컬 작업 영역 |
| 스테이징 영역 (Index) | 다음 커밋에 포함할 변경 파일 스냅샷을 **선별 등록하는 임시 버퍼** |
| 로컬 저장소 | 로컬 시스템에 완결된 커밋 객체(Commit, Tree, Blob)를 영구 기록 |
| 원격 저장소 (Remote) | 팀 협업 및 CI/CD 파이프라인 연계를 위한 **중앙 공용 Git 저장소** |

#### 한줄 요약
- 스테이징 영역이 작업 디렉터리와 저장소 사이에 끼어 커밋 단위를 사람이 고를 수 있게 하며, 원격 저장소는 이력의 공유 정본 역할만 맡는다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Pull Request(PR / MR)**: 기능 개발 브랜치를 메인라인에 병합하기 전, 동료들의 코드 리뷰와 CI 자동화 테스트 통과를 강제하는 관문.

</details>

```text
기능 브랜치 생성 및 로컬 코딩 (`feature/login`)
        │
   `git add` & `git commit` (논리적 단위로 원자적 커밋 생성)
        │
   `git push` 및 원격 저장소에 Pull Request(PR) 생성
        │
   GitHub Actions CI 자동 트리거 (단위 테스트, SonarQube 정적 분석 통과)
        │
   동료 개발자 2인 코드 리뷰 및 승인(Approve) 완료
        │
   메인라인 브랜치(`main`)로 병합(Merge) 및 자동 스테이징 배포
```

#### 한줄 요약
- CI 검증과 사람 리뷰는 잡아내는 결함의 종류가 다르므로, 자동 검증만으로 병합하면 설계 수준의 문제가 그대로 메인라인에 들어간다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **GitFlow vs GitHub Flow vs Trunk-based**: 5단계 정형 브랜치 GitFlow, PR 기반 단순 GitHub Flow, 단기 브랜치 매일 병합 Trunk-based.

</details>

| 브랜치 전략 | GitFlow (정형적 다중 브랜치) | GitHub Flow (경량 브랜치) | Trunk-based Development (지속 통합형) |
|:---|:---|:---|:---|
| 브랜치 구조 | **main, develop, feature, release, hotfix** | main + 단기 feature 브랜치 | **단일 Trunk(main) + 1일 미만 단기 브랜치** |
| 배포 주기 | 정기 릴리즈 (수 주~수 개월 주기) | PR 머지 즉시 수시 배포 | **하루 수십 회 지속적 배포 (CI/CD)** |
| 병합 충돌 위험 | 장기 브랜치로 **Merge Hell 위험 높음** | 기능 단위 격리로 중간 수준 | **잦은 병합으로 충돌 위험 극소화** |
| 주 적용 분야 | 금융 계정계, 임베디드, 패키지 SW | 웹 서비스, SaaS, 스타트업 | **빅테크(구글, 넷플릭스), 고도화된 DevOps** |

#### 한줄 요약
- 엄격한 정기 릴리즈는 GitFlow, 웹 서비스는 GitHub Flow, 초고속 지속 배포는 Trunk-based를 채택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Protected Branch(보호 브랜치)**: `main` 브랜치에 직접 Push를 금지하고, 오직 CI 통과와 승인된 PR을 통해서만 병합을 허용하는 보안 정책.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 미검증 코드의 메인 브랜치 직접 푸시로 장애 발생 | **보호 브랜치(Protected Branch) 및 PR 2인 승인 강제** | 메인라인 안정성 보장 및 비인가 배포 차단 |
| API Key, 패스워드 등 민감 정보의 Git 노출 | **Pre-commit Hook(Gitleaks) 및 GitGuardian 연동** | 커밋/푸시 시점에 기밀 유출 100% 원천 차단 |
| 장기 생존 브랜치로 인한 대규모 병합 충돌(**Merge Hell**) | **트렁크 기반 개발(Trunk-based) 및 기능 플래그(Feature Flag)** | 브랜치 수명 1일 이내 단축 및 충돌 최소화 |
| 잘못된 Rebase로 인한 원격 커밋 히스토리 파괴 | **공유 브랜치 Force Push(`-f`) 절대 금지 룰 설정** | 커밋 그래프 무결성 및 협업 안정성 유지 |

#### 한줄 요약
- 브랜치 전략은 병렬 작업 자유도와 통합 비용을 맞바꾸는 선택이므로, 통합 지연이 더 비싼 조직은 트렁크 기반으로 옮기고 이력 무결성은 보호 브랜치와 Force Push 금지로 지킨다.

## Ⅶ. 결론

- 현대 데브옵스(DevOps) 파이프라인 및 소프트웨어 공학의 **가장 근본적인 형상 관리 및 협업 인프라 표준**으로 확립되었으며, 실무 프로젝트에서는 **배포 주기와 조직 역량에 맞춰 브랜치 전략(초고속 배포를 위한 Trunk-based + Feature Flag)을 선택하고, 메인라인 안정성을 위한 보호 브랜치(Protected Branch)와 PR 2인 승인 강제, 시크릿 유출 방지를 위한 Pre-commit 훅(Gitleaks)**을 결합하여 형상 무결성을 보장

#### 한줄 요약
- 형상 관리는 소프트웨어의 모든 변경을 투명하게 추적하고 브랜치 전략을 통해 팀 협업의 충돌을 방지하는 엔지니어링의 기본 인프라다.