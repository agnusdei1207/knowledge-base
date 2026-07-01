---
title: "GitOps (GitOps)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 61
---

# 📖 【암기용】 개념 완전 이해

> 목적: GitOps를 처음 보는 사람도 배포 통제 원리를 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: Git을 시스템 희망 상태의 단일 원천으로 삼는 운영 방식
- **왜 필요한가**: 수동 kubectl, 콘솔 변경, 배포 스크립트가 섞이면 실제 운영 상태와 문서가 어긋남. GitOps는 선언형 매니페스트와 자동 조정으로 이 차이를 줄임.
- **핵심 직관**: 운영자가 서버에 직접 명령하지 않고, Git에 원하는 모습을 적으면 컨트롤러가 클러스터를 그 상태로 맞춤.

## 깊이 이해
- **배경·문제의식**: CI/CD가 배포 자동화를 제공해도 운영 환경에서 긴급 변경, 권한 남용, 구성 편류가 발생함. 특히 Kubernetes는 YAML 수백 개가 연결되어 변경 이력과 승인 흐름이 없으면 장애 원인 추적 시간이 증가함.
- **작동 원리**: 애플리케이션 매니페스트, Helm chart, Kustomize overlay를 Git에 저장하고 Argo CD나 Flux가 주기적으로 실제 클러스터 상태와 비교함. 차이가 있으면 동기화하거나 경고를 발생시킴.
- **비유**: 매장 직원이 물건을 임의 배치하지 않고, 본사 진열도면을 보고 매장 상태를 계속 맞추는 방식임.
- **구체 예시**: 운영 네임스페이스의 Deployment replica를 3에서 5로 변경하려면 PR 승인 후 merge하고, Argo CD가 3분 주기로 감지해 Kubernetes API에 적용함.
- **흔한 오해·주의점**: GitOps는 CI 빌드 도구가 아님. 이미지 빌드와 테스트는 CI가 담당하고, GitOps는 배포 희망 상태와 실제 상태의 조정에 초점을 둠.

## 연결 개념
- Kubernetes Declarative API: YAML 상태를 API 서버에 적용하는 기반
- Argo CD/Flux: pull 기반 동기화와 drift detection 수행
- DevSecOps: PR 승인, RBAC, 서명 검증을 배포 통제에 결합

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: GitOps는 도구명이 아니라 Git desired state, pull-based reconciliation, audit trail을 결합한 운영 통제 모델임.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: GitOps는 Git 저장소를 애플리케이션·인프라 희망 상태의 단일 원천으로 삼고 컨트롤러가 실제 상태를 조정하는 운영 방식임.
> 2. **가치**: PR 승인, commit 이력, drift detection으로 변경 추적성을 확보하고 MTTR 30분 목표의 롤백 경로를 제공함.
> 3. **판단 포인트**: Push 배포보다 pull 기반 동기화, RBAC 분리, 서명된 매니페스트 검증 여부가 채점 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 선언형 운영 모델 이해 확인 | Git desired state, reconcile loop, drift detection | Git을 단순 소스 저장소로만 설명 |
| 배포 통제 역량 확인 | PR 승인, RBAC, 감사로그, rollback commit | CI와 CD 경계를 혼동 |
| Kubernetes 운영 판단 확인 | Argo CD/Flux, Helm/Kustomize, namespace 권한 분리 | 클러스터 직접 변경을 허용하는 답안 |

> 요약: GitOps 문제는 Git 기반 변경 승인과 pull 기반 자동 조정을 통해 운영 편류를 통제하는 능력을 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: Git 기반 운영 상태 관리
- 배경: Kubernetes와 IaC 확산으로 환경별 YAML, Secret, 정책 변경이 증가해 수동 변경 추적만으로는 운영 상태와 Git 상태의 차이를 식별하기 어렵다.
- 필요성: Argo CD·Flux 같은 조정기가 Git desired state와 클러스터 actual state를 비교해 drift 감지, PR 승인, 롤백 이력을 Git 흐름으로 통제한다.

---

## Ⅱ. 구조 및 구성요소

```text
Developer -> Git PR/Merge -> Desired State Repo
Desired State Repo -> Argo CD/Flux -> Kubernetes API -> Running Cluster
Running Cluster -> Drift Detection -> Sync/Alert -> Audit Log
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Git Repository | 매니페스트, Helm chart, Kustomize overlay 저장 | commit hash가 변경 기준점 |
| Reconciler | 실제 상태와 희망 상태 비교 | Argo CD, Flux poll/webhook |
| Cluster API | Deployment, Service, Ingress 적용 | Kubernetes RBAC로 권한 제한 |
| Audit/Policy | 승인, 서명, 로그 검증 | GPG/Sigstore, OPA Gatekeeper |

> 요약: GitOps 구조는 Git 원천, 조정 컨트롤러, Kubernetes API, 감사 정책이 연결되어 변경을 추적 가능한 단위로 만든다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요구 변경 -> Git PR -> Review/Merge -> Controller Pull
-> Desired/Live Diff -> Sync Apply -> Health Check
-> Drift Alert/Rollback
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 변경자가 YAML 또는 chart 수정 후 PR 생성 | CODEOWNERS 2인 승인 |
| 2 | CI가 kubeconform, conftest, image tag 검증 | 정책 위반 0건 |
| 3 | Argo CD/Flux가 Git commit을 pull | sync interval 1~3분 |
| 4 | live state와 desired state diff 계산 | out-of-sync 리소스 식별 |
| 5 | 적용 후 health, readiness, rollback 확인 | 배포 실패 시 이전 commit 복귀 |

> 요약: GitOps는 PR 승인 후 컨트롤러가 Git을 pull하고 diff, sync, health check 순서로 실제 상태를 맞춘다.

---

## Ⅳ. 특징

| 구분 | 기존 Push CD | GitOps | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 배포 방향 | CI 서버가 클러스터에 push | 클러스터 내부 컨트롤러가 pull | 외부 CI의 cluster-admin 권한 제거 |
| 변경 추적 | 배포 로그 중심 | commit, PR, diff 중심 | 감사 추적 단위 commit hash |
| 편류 통제 | 수동 점검 | drift detection 자동 경고 | sync 주기 1~5분 |
| 롤백 | 재배포 스크립트 실행 | 이전 commit revert | MTTR 30분 이하 목표 |

> 요약: GitOps는 배포 권한을 컨트롤러로 축소하고 Git commit을 변경·감사·롤백의 공통 기준으로 사용한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Jenkins push CD | Argo CD/Flux pull CD | 클러스터 접근권한 분리 필요 시 GitOps |
| 비용/성능 | 스크립트 유지보수 | 선언형 매니페스트 관리 | 앱 20개 이상, 환경 3개 이상일 때 효과 측정 |
| 운영/위험 | 콘솔 긴급 변경 허용 | Git 외 변경 drift 감지 | 운영 변경 승인률 95% 이상 목표 |
| 보안/감사 | 배포자 개인 권한 | 컨트롤러 service account | RBAC 최소권한, 감사로그 180일 보관 |

> 요약: GitOps는 다중 환경과 감사 요구가 있는 Kubernetes 운영에서 push CD보다 권한·추적성 통제가 명확하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 잘못된 매니페스트 반영 | PR 검증 부재 | kubeconform, conftest, OPA gate | 정책 실패 배포 0건 |
| Secret 노출 | Git 평문 저장 | SealedSecrets, External Secrets, SOPS | secret scanning 0건 |
| 무한 동기화 | admission webhook과 manifest 충돌 | ignoreDifferences, policy 예외 등록 | sync 실패 5분 이상 0건 |
| 권한 과다 | 컨트롤러 cluster-admin 사용 | namespace RBAC, project 분리 | 권한 점검 월 1회 |

> 요약: GitOps 리스크는 정책 검증, secret 분리, RBAC 최소권한으로 통제하고 sync 실패율로 운영 품질을 판단한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 동기화 품질 | sync success rate 99% 이상 | Argo CD metric, alert |
| 변경 추적 | 운영 변경 100% PR 연결 | Git audit, ticket link |
| 복구 시간 | rollback MTTR 30분 이하 | incident timeline |
| 보안 통제 | 미승인 cluster 변경 0건 | Kubernetes audit log |

> 요약: GitOps 도입 효과는 sync 성공률, PR 연결률, 롤백 시간, 미승인 변경 건수로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. Argo CD AppProject로 dev/stage/prod namespace와 repo를 분리하고 RBAC role을 읽기, sync, admin 3단계로 설정함.
2. PR 단계에 kubeconform, conftest, Trivy image scan을 넣고 정책 실패 시 merge 차단 gate를 구성함.
3. 운영 장애 시 image tag와 values commit을 이전 버전으로 revert하고 sync window를 통해 10분 내 복구 절차를 표준화함.

**결론 (2줄):**
- 기술사 판단: Kubernetes 다중 환경, 감사 요구, 배포자 권한 분리가 있으면 GitOps를 선택하고 단일 VM 배포는 기존 CD로 충분함.
- 향후 방향: GitOps는 Sigstore 서명, SBOM, OPA 정책을 결합해 배포 공급망 통제 모델로 발전함.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "GitOps를 설명하시오" | desired/live diff, reconcile loop, drift detection | Push CD와 GitOps 비교, Argo CD/Flux 적용 |
| 요구사항 명시형 | "도입 방안을 제시하시오", "운영 통제를 설계하시오" | PR gate, RBAC, rollback 흐름 | 정책검증, secret 분리, 감사로그 기준 |

> 요약: 설명형은 Git 기반 조정 원리를, 설계·방안형은 권한·정책·감사 기준을 중심으로 목차를 전환한다.
