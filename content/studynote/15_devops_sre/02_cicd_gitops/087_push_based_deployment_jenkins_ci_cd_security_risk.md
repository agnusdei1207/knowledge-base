---
title: 87. 푸시 기반(Push-based) 배포 - 기존 CI/CD 젠킨스의 보안 한계
date: '2026-04-10'
tags:
- studynote-devops
---

## 핵심 인사이트 (3줄 요약)

    > 1. **본질**: 푸시 기반 (Push-based) 배포는 [[090_configuration_item|CI]]/CD 서버가 대상 서버로 직접 배포 명령과 자산을 밀어 넣는 방식이다.
    > 2. **가치**: [[071_jenkins_ci_cd_pipeline_automation|Jenkins]] ([[019_continuous_integration|Continuous Integration]]/[[164_continuous_delivery|Continuous Delivery]] orchestrator)는 간단한 자동화에 강하지만, 대상 서버 접근 권한이 집중되어 보안 경계가 넓어진다.
    > 3. **판단 포인트**: 배포 편의성을 얻는 대신 자격 증명, 네트워크 노출, [[606_auditing_linux_auditd|감사]] 책임이 커지므로 대규모 환경에서는 pull 기반이나 GitOps가 더 안전할 수 있다.

    ---

    ## Ⅰ. 개요 및 필요성

    푸시 기반 배포는 중앙 [[090_configuration_item|CI]] 서버가 빌드 산출물을 대상 환경으로 직접 밀어 넣는 방식이다. [[071_jenkins_ci_cd_pipeline_automation|Jenkins]] 같은 오케스트레이터가 [[538_ssh_vs_telnet_secure_remote|SSH]] ([[538_ssh_vs_telnet_secure_remote|Secure Shell]]), [[014_api_posix|API]], 원격 에이전트를 사용해 배포를 수행한다.

이 방식은 구현이 쉽고 기존 [[061_on_premise_legacy_infrastructure|온프레미스]] 환경과 잘 맞지만, 배포 서버가 사실상 [[565_privileged_accounts|특권 계정]]의 관문이 된다. 따라서 배포 편의성만 보고 선택하면 보안 경계가 넓어지고, 장애가 나면 중앙 배포 엔진이 단일 실패 지점이 될 수 있다.

    - **📢 섹션 요약 비유**: 한 사람이 모든 집의 열쇠를 들고 다니는 배달 방식이라고 생각하면 된다.

    ---

    ## Ⅱ. 아키텍처 및 핵심 원리

    푸시 모델의 흐름은 개발자 변경 → 빌드 → [[071_jenkins_ci_cd_pipeline_automation|Jenkins]] → 대상 서버 순서로 [[216_progress_in_synchronization|진행]]된다. 이때 Jenkins는 [[075_artifact_management_nexus_docker_registry|아티팩트]]를 전달할 뿐 아니라 운영 명령까지 수행하므로, 네트워크와 권한이 배포 서버에 집중된다.

| 구성요소 | 역할 | 보안 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] |
| :-- | :-- | :-- |
| [[071_jenkins_ci_cd_pipeline_automation|Jenkins]] | 빌드·배포 [[073_container_orchestration_tools|오케스트레이션]] | 관리자 권한 집중 |
| [[075_artifact_management_nexus_docker_registry|Artifact]] Repo | [[395_verification_process_review|검증]]된 빌드 저장소 | 위변조 방지 필요 |
| Deploy Credential | 원격 실행 자격 | 장기 비밀키 유출 위험 |
| Target Server | 실제 [[090_service_kubernetes_network_load_balancing|서비스]] 실행 | 침해 시 수평 이동 경로 |

```text
개발자 코드 푸시
    │
    ▼
CI 빌드 / 테스트
    │
    ▼
Jenkins 배포 실행
    │  (SSH / API / Agent)
    ▼
대상 서버에 직접 반영
```

문제는 배포가 편할수록 권한이 넓어진다는 점이다. 그래서 푸시 모델은 운영 편의성보다 통제와 [[606_auditing_linux_auditd|감사]]가 더 중요한 곳에서 특히 주의가 필요하다.

    - **📢 섹션 요약 비유**: 물건은 간단히 옮길 수 있지만, 열쇠를 잃으면 모두가 곤란해진다.

    ---

    ## Ⅲ. 비교 및 연결

    푸시 기반과 pull 기반 배포는 신뢰 경계가 다르다.

| 항목 | Push-based | [[088_pull_based_deployment_gitops_argocd_security_auto_healing|Pull-based]] / [[119_gitops_single_source_of_truth|GitOps]] |
| :-- | :-- | :-- |
| 누가 시작하는가 | 중앙 서버가 대상에 밀어 넣음 | 대상이 저장소에서 당겨옴 |
| 네트워크 노출 | 대상 서버 inbound가 늘어남 | 대상 서버 outbound 중심 |
| 자격 증명 | 중앙 배포 서버에 집중 | 짧은 수명의 토큰으로 [[136_variance|분산]] |
| [[606_auditing_linux_auditd|감사]] 추적 | 중앙 [[568_logs_distributed_logging_elk_fluentd|로그]]에 의존 | 선언형 상태와 기록이 남음 |

GitOps는 선언된 상태를 기준으로 클러스터가 스스로 맞추게 하므로, 사람이 직접 서버에 접속하는 면적을 줄인다. 따라서 푸시 모델은 소규모 폐쇄망에서 유효할 수 있지만, 보안과 재현성이 중요해질수록 pull 기반이 더 낫다.

    - **📢 섹션 요약 비유**: 각 집이 스스로 배달표를 [[396_validation|확인]]하는 방식이 더 조심스럽고 안전하다.

    ---

    ## Ⅳ. 실무 적용 및 기술사 판단

    실무에서는 배포 서버를 특권 시스템으로 다루어야 한다. 계정은 최소 권한으로 분리하고, 비밀 정보는 짧게 살며, 배포 명령은 [[075_artifact_management_nexus_docker_registry|아티팩트]] 서명과 승인 절차를 거쳐야 한다.

### [[435_checklist_based_testing|체크리스트]]
1. 배포용 계정이 운영 전 권한까지 갖고 있지 않은가?
2. 자격 증명이 장기 [[538_ssh_vs_telnet_secure_remote|SSH]] 키에 고정되어 있지 않은가?
3. [[075_artifact_management_nexus_docker_registry|아티팩트]]가 서명되거나 해시 [[395_verification_process_review|검증]]되는가?
4. 배포 실패 시 자동 [[098_rollback_strategy_pipeline_error_threshold|롤백]]이나 정지 [[164_policy|정책]]이 있는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- [[071_jenkins_ci_cd_pipeline_automation|Jenkins]] 한 대가 모든 서버의 root 비밀번호를 아는 구조
- 개발과 운영 환경이 같은 비밀 키를 공유하는 구조
- 배포 이력과 실제 서버 상태가 따로 노는 구조

    - **📢 섹션 요약 비유**: 편하다고 문을 다 열어 두면, 누가 들어왔는지 기록하기 어렵다.

    ---

    ## Ⅴ. 기대효과 및 결론

    푸시 기반 배포는 시작하기 쉽지만, 커질수록 권한 집중 문제를 드러낸다. 운영 편의와 보안 통제는 같이 봐야 하며, 규모가 커질수록 선언형 pull 모델이 더 매력적이 된다.

따라서 이 방식은 "빠른 자동화"의 출발점으로는 좋지만, 최종 목적지는 아니다. 배포 서버가 곧 신뢰 경계라는 사실을 기억하면 위험을 훨씬 정확하게 다룰 수 있다.

    - **📢 섹션 요약 비유**: 서랍 하나에 열쇠를 다 넣기보다, 필요한 집만 그때그때 여는 방식이 낫다.

    ---

    ### 📌 관련 개념 맵

    | 개념 | 연결 포인트 |
| :-- | :-- |
| [[071_jenkins_ci_cd_pipeline_automation|Jenkins]] | 배포 [[073_container_orchestration_tools|오케스트레이션]] |
| [[090_configuration_item|CI]]/CD ([[019_continuous_integration|Continuous Integration]]/[[164_continuous_delivery|Continuous Delivery]]) | 자동 빌드·배포 [[123_pipe|파이프]]라인 |
| [[538_ssh_vs_telnet_secure_remote|SSH]] ([[538_ssh_vs_telnet_secure_remote|Secure Shell]]) | 원격 실행 자격 수단 |
| [[075_artifact_management_nexus_docker_registry|Artifact]] | 배포 대상 산출물 |
| [[119_gitops_single_source_of_truth|GitOps]] | pull 기반 선언형 배포 모델 |

    ### 📈 관련 키워드 및 발전 흐름도

    코드 커밋
    │
    ▼
[[071_jenkins_ci_cd_pipeline_automation|Jenkins]] 빌드 / 테스트
    │
    ▼
대상 서버로 push 배포
    │
    ▼
권한 집중 / [[606_auditing_linux_auditd|감사]] / [[098_rollback_strategy_pipeline_error_threshold|롤백]] 관리

    ### 👶 어린이를 위한 3줄 비유 설명

    1. 한 사람이 모든 도시의 문을 직접 열어 주는 것과 비슷해요.
    2. 빠르긴 하지만, 열쇠를 잘못 쓰면 위험이 커져요.
    3. 그래서 가끔은 도시가 스스로 배달 목록을 [[396_validation|확인]]하는 편이 더 안전해요.
