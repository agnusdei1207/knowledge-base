---
title: 26. VCS (Version Control System) — 형상 이력 관리 시스템
date: '2026-04-29'
tags:
- studynote-software-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: VCS (Version Control System, [[288_version_ihl_tos_total_length|버전]] 관리 시스템)는 소프트웨어의 소스 코드·문서·[[009_config|설정]] 파일의 변경 이력을 추적하고, 이전 [[288_version_ihl_tos_total_length|버전]]으로 되돌리거나 여러 사람의 변경을 병합하는 협업 도구로, [[167_scm_software_configuration_management|SCM]] ([[020_software_configuration_management|Software Configuration Management]])의 핵심 구현체다.
> 2. **가치**: Git이 지배적인 현대 DVCS (Distributed VCS) 시대에서 브랜치 [[268_strategy_pattern|전략]]([[053_gitflow|GitFlow]], [[040_trunk_based_development|Trunk-Based Development]])은 [[090_configuration_item|CI]]/CD 파이프라인과 팀 협업 방식을 결정하는 핵심 아키텍처 결정이다. 단순한 코드 저장소를 넘어 "변경 제안→리뷰→병합→배포"의 전체 소프트웨어 개발 워크플로우를 조직한다.
> 3. **판단 포인트**: CVCS (Centralized VCS, 중앙집중형)와 DVCS (Distributed VCS, [[136_variance|분산]]형)의 가장 큰 차이는 "오프라인 작업 가능성"과 "[[454_spof|단일 장애점]]([[454_spof|SPOF]]) 여부"다. Git의 로컬 전체 이력 [[016_replication_factor|복제]]는 서버 장애 시에도 개발을 계속하고 빠른 [[658_ir_recovery|복구]]를 가능하게 한다.

---

## Ⅰ. 개요 및 필요성

```text
┌────────────────────────────────────────────────────────────┐
│           VCS 유형 진화                                      │
├──────────────────────────────────────────────────────────┤
│ 1세대 LVCS  │ 로컬 버전 관리 (RCS, SCCS)                    │
│ (Local)     │ 단일 파일 이력, 협업 불가                      │
│─────────────┼──────────────────────────────────────────── │
│ 2세대 CVCS  │ 중앙 서버 (SVN, CVS, Perforce)                │
│ (Central)   │ 단일 서버, 오프라인 작업 불가, SPOF           │
│─────────────┼──────────────────────────────────────────── │
│ 3세대 DVCS  │ 분산 (Git, Mercurial)                         │
│ (Distrib.)  │ 전체 이력 로컬 복제, 오프라인 작업, 빠른 분기  │
└──────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: VCS의 진화는 은행 시스템의 진화다. 개인 장부(LVCS) → 은행 중앙 서버(CVCS) → 각자 완전한 사본을 가진 [[136_variance|분산]] 원장(DVCS/[[004_blockchain|블록체인]] 유사). [[136_variance|분산]] 원장은 서버가 죽어도 거래가 계속된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Git 기본 아키텍처 (3 트리)

```text
[작업 디렉토리]  git add  [스테이징 영역]  git commit  [로컬 저장소]
  수정된 파일  ─────────>  변경 준비 파일  ──────────>  커밋 이력
                                                           │
                                               git push    ▼
                                             [원격 저장소 (GitHub)]
```

### 브랜치 [[268_strategy_pattern|전략]] 비교

```text
GitFlow:
main ──────────────────────────────────── v1.0
  │                                        │
  └─ develop ──── feature/A ─── merge ────┘
                └─ feature/B ─── merge

Trunk-Based:
main ─── commit ─── commit ─── commit ─── (Feature Flag)
  (매일 main에 직접 커밋, CI/CD 즉시)
```

- **📢 섹션 요약 비유**: GitFlow는 장기 프로젝트의 단계별 관리(건축의 설계→시공→준공 단계), Trunk-Based는 지속적 현장 개선(매일 소량씩 개선하는 린 생산 방식)이다.

---

## Ⅲ. 비교 및 연결

| 항목 | SVN (CVCS) | Git (DVCS) |
|:---|:---|:---|
| **저장소** | 중앙 서버 단일 | 각 로컬에 전체 [[016_replication_factor|복제]] |
| **오프라인** | 불가 | 가능 (commit, branch, log) |
| **브랜치 비용** | 비쌈 (디렉토리 복사) | 매우 저렴 (포인터 이동) |
| **[[454_spof|SPOF]]** | 있음 | 없음 ([[136_variance|분산]]) |

- **📢 섹션 요약 비유**: SVN은 중앙 도서관(서버)에 원본만 있는 대출 시스템이고, Git은 모든 회원이 전체 도서 목록 사본을 가진 [[136_variance|분산]] 도서관이다. 중앙이 불이 나도 회원들의 사본으로 [[658_ir_recovery|복구]] 가능하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### Git 핵심 [[158_instruction|명령어]] 워크플로우

```bash
# 기능 개발 브랜치 생성
git checkout -b feature/user-auth

# 변경 사항 커밋
git add src/auth.py
git commit -m "feat: JWT 인증 모듈 추가"

# 원격에 푸시 → PR 생성 → 코드 리뷰 → 병합
git push origin feature/user-auth

# 병합 후 로컬 정리
git checkout main && git pull
git branch -d feature/user-auth
```

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- main 브랜치에 직접 커밋하는 [[128_water_scrum_fall_anti_pattern|안티패턴]]("직접 커밋"). 기능 브랜치 없이 main에 직접 커밋하면 [[330_code_review|코드 리뷰]]·[[090_configuration_item|CI]] 검사 없이 프로덕션 코드에 버그가 들어간다. Branch [[571_protection_vs_security|Protection]] Rules로 직접 커밋을 차단해야 한다.

- **📢 섹션 요약 비유**: main 직접 커밋은 도로 공사를 신호등 없이 막는 것이다. 교통 통제(브랜치·[[067_pull_request_pr_merge_request_code_review|PR]]) 없이 직접 공사하면 교통 혼란(버그)이 생긴다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **이력 추적** | 모든 변경의 책임자·시간·이유 기록 |
| **협업** | 동시 [[430_index_fast_full_scan|병렬]] 개발 + 충돌 병합 관리 |
| **[[098_rollback_strategy_pipeline_error_threshold|롤백]]** | 버그 발생 시 이전 [[288_version_ihl_tos_total_length|버전]]으로 즉시 [[658_ir_recovery|복구]] |

GitOps는 VCS(Git)를 인프라 선언적 [[009_config|설정]]의 단일 진실 원천(Single Source of Truth)으로 활용하여, Git 커밋만으로 클라우드 인프라 배포까지 자동화하는 현대 DevOps의 핵심 패턴이다.

- **📢 섹션 요약 비유**: GitOps는 Git이 모든 것의 설계도 보관소가 된 것이다. 설계도(코드+[[009_config|설정]])를 변경하면 자동으로 집(인프라)이 그에 맞게 바뀐다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[167_scm_software_configuration_management|SCM]]** | VCS는 SCM의 핵심 구현 도구 |
| **[[090_configuration_item|CI]]/CD** | VCS 커밋이 자동 빌드·배포 [[507_acid_properties|트리거]] |
| **[[053_gitflow|GitFlow]]** | VCS 브랜치 [[268_strategy_pattern|전략]]의 대표 패턴 |
| **[[119_gitops_single_source_of_truth|GitOps]]** | VCS를 인프라 관리의 SSOT로 활용 |
| **[[330_code_review|코드 리뷰]] ([[067_pull_request_pr_merge_request_code_review|PR]])** | VCS 플랫폼에서 제공하는 협업 워크플로우 |

### 📈 관련 키워드 및 발전 흐름도

```text
[LVCS — 로컬 파일 이력 관리]
    │
    ▼
[CVCS (SVN) — 중앙 서버 기반 협업]
    │
    ▼
[DVCS (Git) — 분산 전체 이력, 경량 브랜치]
    │
    ▼
[GitHub/GitLab — PR, CI/CD 통합 플랫폼]
    │
    ▼
[GitOps — Git = 인프라 SSOT, 자동 배포]
```

### 👶 어린이를 위한 3줄 비유 설명

1. VCS는 글 [[289_cqrs_db|쓰기]] 앱의 "실행 취소" 버튼 무제한 [[288_version_ihl_tos_total_length|버전]]이에요! 언제든지 이전 [[288_version_ihl_tos_total_length|버전]]으로 돌아갈 수 있어요.
2. Git은 모든 팀원이 전체 이력 사본을 가져서, 서버가 없어도 오프라인으로 작업하고 나중에 합칠 수 있어요.
3. 요즘은 Git 커밋 하나로 코드 테스트부터 서버 배포까지 자동으로 되는 [[119_gitops_single_source_of_truth|GitOps]] 세상이 됐답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 26 / 973

← **이전**: [[025_baseline|25. 기준선 (Baseline) — 형상 관리의 공식 참조점]]
**다음**: [[027_change_management|27. 변경 관리 (Change Management) — 소프트웨어 변경의 체계적 통제]] →

---
