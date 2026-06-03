---
title: 86. GitOps (깃옵스) - 선언적 인프라 자동화 및 지속적 동기화
date: '2026-04-10'
tags:
- studynote-devops
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[119_gitops_single_source_of_truth|GitOps]] (Git-based Operations)는 Git을 단일 진실 공급원으로 삼아 선언형 상태를 운영하는 방식이다.
> 2. **가치**: [[062_infrastructure_as_code|Infrastructure as Code]] ([[793_iac_idempotency_template|IaC]])와 달리 실제 시스템을 Git 선언과 계속 맞춘다는 점이 핵심이다.
> 3. **판단 포인트**: 드리프트 감지, [[098_rollback_strategy_pipeline_error_threshold|롤백]], [[606_auditing_linux_auditd|감사]] 추적이 자동화되어 수동 배포보다 재현성과 통제력이 높다.

---

## Ⅰ. 개요 및 필요성
GitOps는 배포 명령이 아니라 원하는 상태 선언을 중심에 둔다. 사람이 서버에 직접 들어가 수정하는 대신, 저장소의 선언을 컨트롤러가 읽고 클러스터 상태를 맞춘다.

변경 이력, 리뷰, 승인, [[098_rollback_strategy_pipeline_error_threshold|롤백]]이 모두 Git 흐름 안에 남는 것이 가장 큰 장점이다.
- **📢 섹션 요약 비유**: 노트 한 장이 시스템의 기준이 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리
| 구성 요소 | 역할 | 포인트 |
|:---|:---|:---|
| Git 저장소 | 원하는 상태의 원본 | [[067_pull_request_pr_merge_request_code_review|PR]] 리뷰, 이력 추적 |
| 매니페스트 | 배포 선언 | 재현성 |
| 컨트롤러 | 선언과 실제를 비교 | 드리프트 감지 |
| [[205_kubernetes_container_orchestration|Kubernetes]] 클러스터 | 실제 실행 환경 | 자동 [[212_synchronization_mechanisms|동기화]] |
| [[114_argocd_gitops_cd|Argo CD]] | 대표적인 [[119_gitops_single_source_of_truth|GitOps]] 도구 | 싱크와 헬스 체크 |

┌──────────┐ commit ┌───────────────┐ sync ┌───────────────┐
│   Git    │──────▶│   [[114_argocd_gitops_cd|Argo CD]]     │─────▶│ [[205_kubernetes_container_orchestration|Kubernetes]]    │
│  repo    │       │ controller    │      │ cluster       │
└────┬─────┘       └──────┬────────┘      └──────┬────────┘
     │ drift detect          │ actual [[272_state_pattern|state]]          │
     └──────────────────────◀─┴───────────────────────┘
- **📢 섹션 요약 비유**: 기준과 실제를 계속 비교하는 로봇이 핵심이다.

---

## Ⅲ. 비교 및 연결
| 비교 항목 | [[119_gitops_single_source_of_truth|GitOps]] | 수동 [[077_kube_api_server_k8s_hub|kubectl]]/apply | 전통적 [[090_configuration_item|CI]]/CD 푸시 |
|:---|:---|:---|:---|
| 진실의 원천 | Git | 사람 기억 | [[123_pipe|파이프]]라인 결과 |
| 변경 방식 | 선언형 | 명령형 | 배포 명령 중심 |
| [[606_auditing_linux_auditd|감사]]/추적 | 매우 강함 | 약함 | 중간 |
| 드리프트 [[658_ir_recovery|복구]] | 자동 | 수동 | 부분 자동 |

GitOps는 IaC와 [[090_configuration_item|CI]]/CD를 묶되, 운영 기준을 Git에 고정한다.
- **📢 섹션 요약 비유**: 수동 배포와 달리 기록이 남는다.

---

## Ⅳ. 실무 적용 및 기술사 판단
- [ ] 모든 배포 가능한 상태를 Git 저장소에 넣는다.
- [ ] [[067_pull_request_pr_merge_request_code_review|PR]] 승인 없이는 운영 반영이 되지 않도록 한다.
- [ ] 비밀값은 별도 보안 저장소로 분리한다.
- [ ] 자동/수동 [[212_synchronization_mechanisms|동기화]] [[164_policy|정책]]과 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 기준을 정한다.

- ❌ 운영 서버에 직접 들어가서 임시 수정하는 습관
- ❌ Git과 실제 클러스터가 서로 다른 두 진실이 되는 상태
- ❌ 비밀값을 평문으로 저장하는 것
- **📢 섹션 요약 비유**: 직접 수정보다 다시 맞추는 구조가 중요하다.

---

## Ⅴ. 기대효과 및 결론
GitOps는 사람의 실수 자체를 없애기보다, 실수가 생겨도 다시 맞출 수 있게 만든다. 그래서 배포는 빠르기만 한 과정이 아니라 복원 가능한 과정이 된다.
- **📢 섹션 요약 비유**: 운영을 코드로 되돌릴 수 있어야 안전하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Git 저장소 | 원하는 상태를 보관하는 기준점이다. |
| [[114_argocd_gitops_cd|Argo CD]] | 선언과 실제를 맞추는 조정자다. |
| 드리프트 | 실제 상태와 선언의 차이다. |
| [[098_rollback_strategy_pipeline_error_threshold|롤백]] | 이전 선언으로 되돌리는 안전장치다. |
| [[793_iac_idempotency_template|IaC]] ([[062_infrastructure_as_code|Infrastructure as Code]]) | 인프라를 코드로 다루는 바탕이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
코드 커밋 → PR 리뷰 → 머지 → 동기화 → 드리프트 감지 → 실제 상태 재조정
```

### 👶 어린이를 위한 3줄 비유 설명

1. 레시피 노트를 보고 로봇이 요리하는 방식과 비슷하다.
2. 노트가 같으면 어디서 요리해도 맛을 다시 낼 수 있다.
3. 노트와 맛이 다르면, 다시 노트대로 맞추면 된다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 86 / 373

← **이전**: [[085_canary_release_progressive_delivery_weight_routing|85. 카나리 배포 (Canary Release) - 1% 트래픽 점진적 무중단 배포]]
**다음**: [[087_push_based_deployment_jenkins_ci_cd_security_risk|87. 푸시 기반(Push-based) 배포 - 기존 CI/CD 젠킨스의 보안 한계]] →

---
