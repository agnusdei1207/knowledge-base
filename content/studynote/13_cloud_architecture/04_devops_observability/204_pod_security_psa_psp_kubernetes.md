---
title: "PSA/PSP"
date: "2026-04-21"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) PSA([Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Admission)는 Pod를 Privileged·[Baseline](/studynote/04_software_engineering/01_overview_principles/025_baseline/)·Restricted 세 보안 프로파일로 분류하여, 루트 실행·호스트 네트워크 접근 같은 위험 구성을 클러스터 레벨에서 강제로 차단하는 입장 통제 메커니즘이다.
> 2. **가치**: [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 탈출([Container Escape](/studynote/15_devops_sre/05_devsecops/252_container_escape_vm_gvisor_kata/)) 공격의 핵심 전제 조건인 "루트 권한 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 실행"을 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 원천 차단하여, [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 킬 체인의 진입 장벽을 높인다.
> 3. **판단 포인트**: [Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) 1.25에서 PodSecurityPolicy([PSP](/studynote/04_software_engineering/01_overview_principles/018_psp_tsp/))가 제거되고 PSA로 완전 대체됐다. Restricted 프로파일을 기본값으로 시작하고, 예외는 명시적으로 허용하는 "[최소 권한 원칙](/studynote/09_security/01_intro_principles/010_least_privilege/)([Least Privilege](/studynote/09_security/01_intro_principles/010_least_privilege/))"이 핵심이다.

---

## Ⅰ. 개요 및 필요성

[컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 환경의 보안 위협은 전통 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 환경과 다르다. [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)는 호스트 커널을 공유하므로, 특권(Privileged) [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)가 탈출하면 전체 노드, 나아가 클러스터 전체를 장악할 수 있다. 이것이 "[컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 킬 체인([Container](/studynote/06_ict_convergence/03_cloud_infrastructure/194_container_virtualization_docker_namespace/) Kill Chain)"의 핵심 시나리오다.

실제 공격 사례: 2019년 [runc](/studynote/01_computer_architecture/15_advanced_topics/667_container_runtime_hw_isolation/) 취약점(CVE-2019-5736)은 Privileged [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)에서 호스트 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템의 `/proc/self/exe`를 통해 호스트 [runc](/studynote/01_computer_architecture/15_advanced_topics/667_container_runtime_hw_isolation/) 바이너리를 덮어쓸 수 있는 취약점이었다. 루트가 아닌 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)에서는 이 공격이 불가능했다.

Kubernetes는 이를 방어하기 위해 PodSecurityPolicy([PSP](/studynote/04_software_engineering/01_overview_principles/018_psp_tsp/))를 도입했지만, 복잡한 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)과 [RBAC](/studynote/09_security/11_iam_access_control/569_rbac/) 통합 문제로 운영이 어려웠다. 1.21에서 deprecated, 1.25에서 완전 제거되고 PSA([Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Admission)로 대체됐다.

📢 **섹션 요약 비유**: PSA는 건물 출입문 보안과 같다. [방문자](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/)([Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/))가 들어오기 전에 "이 사람이 마스터키(root)를 가졌는지", "보안 구역(host network)에 접근하려는지"를 체크하여, 위험한 사람은 애초에 입장 자체를 막는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### PSA 세 가지 보안 프로파일

| 프로파일 | 허용 수준 | 적합 상황 |
|:---|:---|:---|
| **Privileged** | 제한 없음 (모든 권한 허용) | [시스템 데몬](/studynote/02_operating_system/01_overview_architecture/037_system_daemon/), 인프라 에이전트 (최소 사용) |
| <strong><a href="/studynote/04_software_engineering/01_overview_principles/025_baseline/">Baseline</a></strong> | 알려진 [권한 상승](/studynote/09_security/04_endpoint_security/356_privilege_escalation/) 차단 | 일반 앱 워크로드, 최소한의 보안 |
| **Restricted** | 최소 권한 강제 | 보안 중요 워크로드, 권장 기본값 |

### Restricted 프로파일 주요 규칙

```
Restricted 프로파일이 금지하는 것:
  ❌ runAsRoot (UID=0으로 실행)
  ❌ allowPrivilegeEscalation: true
  ❌ hostNetwork: true
  ❌ hostPID: true / hostIPC: true
  ❌ privileged: true
  ❌ securityContext.capabilities 추가
  ✅ runAsNonRoot: true (필수)
  ✅ seccompProfile: RuntimeDefault (필수)
  ✅ readOnlyRootFilesystem: true (권장)
```

### K8s PSA [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/) 레이블 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)

```yaml
# 네임스페이스에 PSA 프로파일 적용
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    # enforce: 정책 위반 시 Pod 생성 거부
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: v1.28
    # audit: 위반 로그만 기록 (생성은 허용)
    pod-security.kubernetes.io/audit: restricted
    # warn: 위반 경고 메시지 (생성은 허용)
    pod-security.kubernetes.io/warn: restricted
```

### Restricted 준수 [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 예시

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
spec:
  securityContext:
    runAsNonRoot: true           # 루트 실행 금지
    runAsUser: 1000              # 일반 사용자로 실행
    runAsGroup: 3000
    fsGroup: 2000
    seccompProfile:
      type: RuntimeDefault       # 기본 seccomp 프로파일 적용
  containers:
  - name: app
    image: myapp:v1
    securityContext:
      allowPrivilegeEscalation: false   # 권한 상승 금지
      readOnlyRootFilesystem: true      # 루트 파일시스템 읽기 전용
      capabilities:
        drop:
        - ALL                           # 모든 Linux 캐퍼빌리티 제거
```

📢 **섹션 요약 비유**: Restricted 프로파일은 마치 신입 직원에게 업무에 필요한 최소한의 출입 권한만 주는 것과 같다. 마스터키(root)도 없고, 서버실(host network)도 못 들어가고, 필요한 방만 들어갈 수 있다.

---

## Ⅲ. 비교 및 연결

### [PSP](/studynote/04_software_engineering/01_overview_principles/018_psp_tsp/) vs PSA 비교

| 항목 | [PSP](/studynote/04_software_engineering/01_overview_principles/018_psp_tsp/) (구, 제거됨) | PSA (신, 현재) |
|:---|:---|:---|
| K8s [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) | ~1.24 (1.25에서 제거) | 1.22 도입, 1.25 [GA](/studynote/08_algorithm_stats/10_linear_algebra/169_evolutionary_algorithms/) |
| [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 방식 | RBAC와 복잡한 통합 | [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/) 레이블 단순 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) |
| 유연성 | 세밀한 커스터마이징 | 3개 표준 프로파일 |
| 운영 복잡도 | 높음 | 낮음 |
| 외부 도구 | [OPA](/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/) Gatekeeper, Kyverno로 보완 가능 | 동일 |

### [OPA](/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/) Gatekeeper vs PSA

| 항목 | PSA | [OPA](/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/) Gatekeeper |
|:---|:---|:---|
| 목적 | [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 보안 프로파일 적용 | 커스텀 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 강제 |
| [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 언어 | 내장 프로파일 | Rego 언어 |
| 적용 범위 | [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/)/[컨테이너 보안](/studynote/04_software_engineering/11_testing_validation/905_container_security/) | 모든 K8s 리소스 |
| 복잡도 | 낮음 | 높음 (강력함) |
| 권장 사용 | 기본 [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 보안 | 조직 커스텀 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) |

📢 **섹션 요약 비유**: PSA는 건물 표준 보안 규정(3가지 등급)이고, [OPA](/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/) Gatekeeper는 회사만의 특별 보안 규정을 추가로 만드는 도구다. 표준 규정으로 시작하고, 필요한 커스텀 규정은 Gatekeeper로 추가한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong>PSA 마이그레이션 <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a> (<a href="/studynote/04_software_engineering/01_overview_principles/018_psp_tsp/">PSP</a> -> PSA)</strong>:
```
1단계: 감사 모드 활성화 (warn + audit)
   - 기존 워크로드가 위반하는 내용을 로그로 수집
   - 제거 없이 현황 파악

2단계: 애플리케이션 수정
   - 로그 기반으로 각 워크로드의 securityContext 수정
   - runAsNonRoot, readOnlyRootFilesystem 추가

3단계: enforce 모드 전환
   - 네임스페이스별로 단계적으로 enforce 적용
   - 예외 처리가 필요한 시스템 컴포넌트 격리

4단계: 모니터링 강화
   - 정책 위반 시도 알림 설정
```

<strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/">컨테이너</a> 킬 체인 방어 레이어</strong>:
```
공격 단계              방어 수단
-----------------------------------------
1. 취약점 코드 실행  -> SAST/DAST, 이미지 스캔
2. 컨테이너 내부 탐색 -> Read-only FS, capabilities 제거
3. 권한 상승 시도    -> allowPrivilegeEscalation: false
4. 호스트 접근 시도  -> hostNetwork/PID 금지, seccomp
5. 클러스터 이동     -> NetworkPolicy, RBAC 최소 권한
```

**기술사 판단 포인트**:
- PSA는 [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/) 레벨 적용이므로, 시스템 [컴포넌트](/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)(kube-system)와 일반 워크로드를 별도 [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/)에 분리해야 한다.
- Restricted 프로파일 적용 시 기존 [Helm](/studynote/06_ict_convergence/03_cloud_infrastructure/207_helm_kubernetes_package_manager_chart/) 차트나 [사이드카](/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)([Istio](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/) 등)가 위반할 수 있으므로 사전 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)가 필수다.
- [OPA](/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/) Gatekeeper나 Kyverno를 함께 사용하면 이미지 태그 latest 금지, 리소스 제한 강제 등 PSA 이상의 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 적용 가능하다.

📢 **섹션 요약 비유**: PSA를 enforce 모드로 바로 적용하면 기존 서비스가 갑자기 배포 불가 상태가 될 수 있다. [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 모드로 시작해서 위반 목록을 만들고 하나씩 고치는 것이 현명한 접근이다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 설명 |
|:---|:---|
| [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 탈출 방어 | Privileged [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 실행 원천 차단 |
| 규정 준수 자동화 | 보안 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 인프라에 내재화됨 |
| 공격 표면 축소 | 불필요한 Linux 캐퍼빌리티 제거 |
| [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 용이성 | [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/) 레이블로 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 상태 즉시 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |

PSA는 K8s 보안의 첫 번째 방어선이다. Restricted 프로파일을 기본값으로 시작하고, 예외는 명시적으로 허용하는 "기본 거부(Default Deny)" 원칙이 [제로 트러스트 보안](/studynote/03_network/14_network_security_threats/738_zero_trust_architecture_least_privilege/) 모델의 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 구현이다.

📢 **섹션 요약 비유**: PSA의 Restricted 프로파일은 공항 보안 검색대와 같다. 모든 사람([Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/))이 기본적으로 검사를 받고, 특별한 사유가 있는 사람(시스템 [컴포넌트](/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/))만 우선 통로를 사용할 수 있다. 기본이 "검사"이고 예외가 "면제"다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [OPA](/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/) Gatekeeper | PSA 이상의 커스텀 K8s [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 강제 도구 |
| [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지 스캔 | PSA와 함께 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 킬 체인의 앞단 방어 |
| [RBAC](/studynote/09_security/11_iam_access_control/569_rbac/) ([Role-Based Access Control](/studynote/09_security/11_iam_access_control/569_rbac/)) | PSA와 함께 K8s [최소 권한 원칙](/studynote/09_security/01_intro_principles/010_least_privilege/) 구현 |
| NetworkPolicy | [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 간 통신을 제어하는 PSA 보완 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) |
| [seccomp](/studynote/02_operating_system/01_overview_architecture/080_seccomp/) / [AppArmor](/studynote/02_operating_system/10_security/584_apparmor/) | 시스템 콜 수준의 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 격리 강화 |
| Kyverno | Rego 없이 YAML로 K8s [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 정의하는 대안 |

### 👶 어린이를 위한 3줄 비유 설명

1. PSA는 놀이터 입장 규칙과 같아. "관리자(root)처럼 행동하거나 담장(host network) 너머를 넘보는 사람은 입장 불가!"

### 📈 관련 키워드 및 발전 흐름도

```text
PodSecurityPolicy (PSP, 폐지됨)
    |
    v
Pod Security Admission (PSA): 네임스페이스 레벨 보안
    +-► Privileged: 제한 없음
    +-► Baseline: 위험 설정 차단
    +-► Restricted: 최소 권한 강제
    |
    v
OPA Gatekeeper · Kyverno -> 세밀한 정책 관리
```
2. Restricted 프로파일은 가장 엄격한 규칙이야. 꼭 필요한 장난감(캐퍼빌리티)만 가져올 수 있어.
3. 특별히 필요한 경우(시스템 [컴포넌트](/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/))만 예외로 허용하고, 기본값은 항상 "최소 권한"이야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 203 / 371

<- **이전**: [203. 클라우드 비용 최적화 / FinOps](/studynote/13_cloud_architecture/04_devops_observability/203_finops_cloud_cost_optimization/)
**다음**: [205. Policy as Code / OPA Gatekeeper (쿠버네티스 정책 자동 검증)](/studynote/13_cloud_architecture/04_devops_observability/205_kustomize_helm_opa_gatekeeper_security/) ->

---
