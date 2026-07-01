---
title: "GitOps (GitOps)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 284
---

# 📖 【암기용】 개념 완전 이해

> 목적: GitOps를 Git 저장소를 선언형 운영 상태의 기준으로 삼고 controller가 실제 환경을 계속 맞추는 운영 방식으로 이해하게 만든다.

## 한눈에
- **개요**: Git에 선언형 원하는 상태를 저장하고 자동 reconciliation으로 실제 시스템을 동기화하는 클라우드 네이티브 운영 방식
- **왜 필요한가**: 사람이 kubectl이나 콘솔로 직접 변경하면 누가 언제 무엇을 바꿨는지 추적하기 어렵고 환경 drift가 생긴다.
- **핵심 직관**: 설계도는 Git에 두고, 현장 감독자가 실제 건물이 설계도와 달라지면 계속 맞추는 방식이다.

## 깊이 이해
- **배경·문제의식**: Kubernetes와 IaC는 선언형 상태 관리에 적합하지만, 수동 변경과 CI/CD 권한 남용이 누적되면 감사와 복구가 어려워진다.
- **작동 원리**: Git 저장소에 원하는 상태를 commit하고 GitOps controller가 cluster 실제 상태와 비교해 drift를 감지하거나 자동 동기화한다.
- **비유**: 은행 장부를 원장으로 삼고 지점 잔액이 원장과 다르면 정산 절차가 맞추는 것과 같다.
- **구체 예시**: Argo CD가 `main` branch의 Kubernetes manifest와 cluster 상태를 비교하고, image tag 변경 commit 이후 deployment를 동기화한다.
- **흔한 오해·주의점**: GitOps는 CI/CD 전체를 의미하지 않는다. CI는 artifact를 만들고 검증하며, GitOps는 선언형 운영 상태를 배포·동기화한다.

## 연결 개념
- Kubernetes — 선언형 resource와 controller model 기반
- IaC — 인프라 상태를 코드로 관리
- DevSecOps — PR review, policy as code, 감사 추적을 Git workflow에 결합

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: GitOps는 Git을 단순 형상관리 저장소가 아니라 운영 desired state의 단일 기준으로 사용하는 방식이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: GitOps는 선언형 desired state를 Git에 저장하고 controller가 실제 상태를 지속 조정하는 운영 모델임.
> 2. **가치**: 변경 이력, 승인, rollback, drift 감지를 Git workflow와 자동 reconciliation으로 처리함.
> 3. **판단 포인트**: 선언형 상태, Git 단일 기준, pull-based controller, policy 검증, secret 관리가 함께 필요함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| GitOps 원리 확인 | desired state, reconciliation, drift | Git으로 배포 script 실행으로 축소 |
| 클라우드 네이티브 운영 확인 | Kubernetes controller, Argo CD, Flux | CI/CD와 완전 동일시 |
| 보안·감사 판단 확인 | PR review, RBAC, secret, policy | cluster-admin token을 CI에 보관 |

> 요약: 이 문제는 Git 중심 변경 통제와 controller 기반 동기화 원리를 구분해 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: Git 기준 운영 동기화
- 배경: 수동 배포와 콘솔 변경은 환경 drift, 감사 누락, rollback 지연을 유발함.
- 필요성: Git commit, review, controller reconciliation으로 변경 이력과 실제 상태를 일치시켜야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Developer -> Pull Request -> Git Desired State Repository
Git Repository -> GitOps Controller -> Target Cluster
Controller -> Diff / Sync / Health Check -> Drift Alert / Rollback
Policy / Secret -> Admission / External Secret -> Runtime
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Git Repository | 원하는 운영 상태 저장 | manifest, Helm, Kustomize |
| Pull Request | 변경 검토와 승인 | audit trail |
| GitOps Controller | diff, sync, health 확인 | Argo CD, Flux |
| Policy/Secret | 보안·규정 통제 | OPA, Sealed Secrets 등 |

> 요약: GitOps는 Git 저장소, PR 승인, controller 동기화, 정책·secret 통제가 결합된 운영 구조다.

---

## Ⅲ. 동작원리 및 흐름도

```text
코드 변경 -> CI build / test -> image publish
-> manifest 변경 PR -> review / merge
-> controller diff 감지 -> sync 실행
-> health check -> drift 감시 / rollback
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | CI가 artifact 생성과 보안 검증 수행 | build, scan result |
| 2 | desired state 변경을 PR로 제출 | approval record |
| 3 | controller가 Git과 cluster 상태 차이 비교 | sync status |
| 4 | 적용 후 health와 drift를 감시 | drift count, rollback time |

> 요약: GitOps는 CI 결과를 운영 상태 변경 PR로 연결하고 controller가 실제 환경을 Git 상태에 맞춘다.

---

## Ⅳ. 특징

| 구분 | Push CD | GitOps | 판단 기준 |
|:---|:---|:---|:---|
| 배포 권한 | CI가 cluster에 push | controller가 cluster 내부에서 pull | credential 노출 위험 |
| 기준 상태 | pipeline 실행 결과 | Git desired state | 감사·rollback |
| drift 대응 | 수동 비교 | 자동 diff와 sync | 운영 환경 수 |
| 한계 | 설정 단순 | 선언형 대상에 적합 | stateful 예외 처리 |

> 요약: GitOps는 운영 권한을 controller에 두고 Git 변경 이력으로 배포와 감사 기준을 통일한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 전통 CI/CD | GitOps | 선택 기준 |
|:---|:---|:---|:---|
| 변경 승인 | pipeline 변수·수동 승인 | PR review | 감사 요구 |
| 복구 | 이전 pipeline 재실행 | Git revert | rollback 추적 |
| 환경 관리 | 환경별 script | branch, directory, overlay | multi-cluster |

> 요약: 다중 환경과 감사 요구가 강한 Kubernetes 운영에서는 GitOps가 상태 관리와 변경 추적에 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Secret 노출 | Git에 평문 저장 | external secret, sealed secret | secret scan result |
| Drift 반복 | 수동 hotfix | break-glass 절차와 backport | drift recurrence |
| 동기화 오류 | manifest 품질 미흡 | policy as code, dry-run | sync failure rate |

> 요약: GitOps 리스크는 secret, hotfix, manifest 검증에서 발생하므로 정책 검증과 예외 절차가 필요하다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 변경 추적 | 배포 변경 100% PR 기록 | Git audit |
| 동기화 | sync failure 목표 이내 | controller metric |
| 복구 | rollback lead time 단축 | incident record |

> 요약: GitOps 성과는 변경 추적률, 동기화 오류, rollback 시간으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. CI는 build, test, image scan, SBOM 생성까지 수행하고 운영 manifest 변경은 별도 GitOps repo PR로 관리함.
2. Argo CD 또는 Flux controller를 cluster에 배치하고 namespace별 RBAC와 project 권한을 분리함.
3. secret은 Git 평문 저장을 금지하고 External Secrets, Sealed Secrets, Vault 연계를 적용함.

**결론 (2줄):**
- 기술사 판단: Kubernetes 다중 환경에서는 GitOps로 desired state, 감사, drift 대응을 표준화하되 secret과 예외 변경 절차를 먼저 설계해야 함.
- 향후 방향: GitOps는 platform engineering, policy as code, progressive delivery와 결합되어 배포 승인과 rollback 자동화 기준이 됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "GitOps를 설명하시오" | PR, desired state, reconciliation 흐름 | Push CD 대비 차이 |
| 요구사항 명시형 | "Kubernetes 배포 통제 방안을 제시하시오" | controller sync와 policy 검증 절차 | secret, drift, rollback 리스크 |

> 요약: 설명형은 원리, 방안형은 보안·감사·drift 통제를 중심으로 작성한다.
