---
title: 204. 컨테이너 보안 / Pod 시큐리티 (PSA/PSP)
date: '2026-04-21'
tags:
- studynote-cloud-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[205_kubernetes_container_orchestration|Kubernetes]] PSA([[198_pod_kubernetes_minimum_deployment_unit|Pod]] [[283_security_tactics|Security]] Admission)는 Pod를 Privileged·[[025_baseline|Baseline]]·Restricted 세 보안 프로파일로 분류하여, 루트 실행·호스트 네트워크 접근 같은 위험 구성을 클러스터 레벨에서 강제로 차단하는 입장 통제 메커니즘이다.
> 2. **가치**: [[561_container_based_deployment|컨테이너]] 탈출([[252_container_escape_vm_gvisor_kata|Container Escape]]) 공격의 핵심 전제 조건인 "루트 권한 [[561_container_based_deployment|컨테이너]] 실행"을 [[164_policy|정책]]으로 원천 차단하여, [[561_container_based_deployment|컨테이너]] 킬 체인의 진입 장벽을 높인다.
> 3. **판단 포인트**: [[205_kubernetes_container_orchestration|Kubernetes]] 1.25에서 PodSecurityPolicy([[018_psp_tsp|PSP]])가 제거되고 PSA로 완전 대체됐다. Restricted 프로파일을 기본값으로 시작하고, 예외는 명시적으로 허용하는 "[[010_least_privilege|최소 권한 원칙]]([[010_least_privilege|Least Privilege]])"이 핵심이다.

---

## Ⅰ. 개요 및 필요성

[[561_container_based_deployment|컨테이너]] 환경의 보안 위협은 전통 [[598_vm_migration_nic|VM]] 환경과 다르다. [[561_container_based_deployment|컨테이너]]는 호스트 커널을 공유하므로, 특권(Privileged) [[561_container_based_deployment|컨테이너]]가 탈출하면 전체 노드, 나아가 클러스터 전체를 장악할 수 있다. 이것이 "[[561_container_based_deployment|컨테이너]] 킬 체인([[194_container_virtualization_docker_namespace|Container]] Kill Chain)"의 핵심 시나리오다.

실제 공격 사례: 2019년 [[667_container_runtime_hw_isolation|runc]] 취약점(CVE-2019-5736)은 Privileged [[561_container_based_deployment|컨테이너]]에서 호스트 [[501_file_definition_logical_record|파일]] 시스템의 `/proc/self/exe`를 통해 호스트 [[667_container_runtime_hw_isolation|runc]] 바이너리를 덮어쓸 수 있는 취약점이었다. 루트가 아닌 [[561_container_based_deployment|컨테이너]]에서는 이 공격이 불가능했다.

Kubernetes는 이를 방어하기 위해 PodSecurityPolicy([[018_psp_tsp|PSP]])를 도입했지만, 복잡한 [[009_config|설정]]과 [[569_rbac|RBAC]] 통합 문제로 운영이 어려웠다. 1.21에서 deprecated, 1.25에서 완전 제거되고 PSA([[198_pod_kubernetes_minimum_deployment_unit|Pod]] [[283_security_tactics|Security]] Admission)로 대체됐다.

📢 **섹션 요약 비유**: PSA는 건물 출입문 보안과 같다. [[275_visitor_pattern|방문자]]([[198_pod_kubernetes_minimum_deployment_unit|Pod]])가 들어오기 전에 "이 사람이 마스터키(root)를 가졌는지", "보안 구역(host network)에 접근하려는지"를 체크하여, 위험한 사람은 애초에 입장 자체를 막는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### PSA 세 가지 보안 프로파일

| 프로파일 | 허용 수준 | 적합 상황 |
|:---|:---|:---|
| **Privileged** | 제한 없음 (모든 권한 허용) | [[037_system_daemon|시스템 데몬]], 인프라 에이전트 (최소 사용) |
| **[[025_baseline|Baseline]]** | 알려진 [[356_privilege_escalation|권한 상승]] 차단 | 일반 앱 워크로드, 최소한의 보안 |
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

### K8s PSA [[061_namespace|네임스페이스]] 레이블 [[009_config|설정]]

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

### Restricted 준수 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 예시

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

### [[018_psp_tsp|PSP]] vs PSA 비교

| 항목 | [[018_psp_tsp|PSP]] (구, 제거됨) | PSA (신, 현재) |
|:---|:---|:---|
| K8s [[288_version_ihl_tos_total_length|버전]] | ~1.24 (1.25에서 제거) | 1.22 도입, 1.25 [[169_evolutionary_algorithms|GA]] |
| [[009_config|설정]] 방식 | RBAC와 복잡한 통합 | [[061_namespace|네임스페이스]] 레이블 단순 [[009_config|설정]] |
| 유연성 | 세밀한 커스터마이징 | 3개 표준 프로파일 |
| 운영 복잡도 | 높음 | 낮음 |
| 외부 도구 | [[237_opa_open_policy_agent_gatekeeper|OPA]] Gatekeeper, Kyverno로 보완 가능 | 동일 |

### [[237_opa_open_policy_agent_gatekeeper|OPA]] Gatekeeper vs PSA

| 항목 | PSA | [[237_opa_open_policy_agent_gatekeeper|OPA]] Gatekeeper |
|:---|:---|:---|
| 목적 | [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 보안 프로파일 적용 | 커스텀 [[164_policy|정책]] 강제 |
| [[164_policy|정책]] 언어 | 내장 프로파일 | Rego 언어 |
| 적용 범위 | [[198_pod_kubernetes_minimum_deployment_unit|Pod]]/[[513_container_security|컨테이너 보안]] | 모든 K8s 리소스 |
| 복잡도 | 낮음 | 높음 (강력함) |
| 권장 사용 | 기본 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 보안 | 조직 커스텀 [[164_policy|정책]] |

📢 **섹션 요약 비유**: PSA는 건물 표준 보안 규정(3가지 등급)이고, [[237_opa_open_policy_agent_gatekeeper|OPA]] Gatekeeper는 회사만의 특별 보안 규정을 추가로 만드는 도구다. 표준 규정으로 시작하고, 필요한 커스텀 규정은 Gatekeeper로 추가한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**PSA 마이그레이션 [[268_strategy_pattern|전략]] ([[018_psp_tsp|PSP]] → PSA)**:
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

**[[561_container_based_deployment|컨테이너]] 킬 체인 방어 레이어**:
```
공격 단계              방어 수단
─────────────────────────────────────────
1. 취약점 코드 실행  → SAST/DAST, 이미지 스캔
2. 컨테이너 내부 탐색 → Read-only FS, capabilities 제거
3. 권한 상승 시도    → allowPrivilegeEscalation: false
4. 호스트 접근 시도  → hostNetwork/PID 금지, seccomp
5. 클러스터 이동     → NetworkPolicy, RBAC 최소 권한
```

**기술사 판단 포인트**:
- PSA는 [[061_namespace|네임스페이스]] 레벨 적용이므로, 시스템 [[603_component_independent_deployment_unit|컴포넌트]](kube-system)와 일반 워크로드를 별도 [[061_namespace|네임스페이스]]에 분리해야 한다.
- Restricted 프로파일 적용 시 기존 [[207_helm_kubernetes_package_manager_chart|Helm]] 차트나 [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]]([[302_service_mesh_istio|Istio]] 등)가 위반할 수 있으므로 사전 [[606_auditing_linux_auditd|감사]]가 필수다.
- [[237_opa_open_policy_agent_gatekeeper|OPA]] Gatekeeper나 Kyverno를 함께 사용하면 이미지 태그 latest 금지, 리소스 제한 강제 등 PSA 이상의 [[164_policy|정책]]을 적용 가능하다.

📢 **섹션 요약 비유**: PSA를 enforce 모드로 바로 적용하면 기존 서비스가 갑자기 배포 불가 상태가 될 수 있다. [[606_auditing_linux_auditd|감사]] 모드로 시작해서 위반 목록을 만들고 하나씩 고치는 것이 현명한 접근이다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 설명 |
|:---|:---|
| [[561_container_based_deployment|컨테이너]] 탈출 방어 | Privileged [[561_container_based_deployment|컨테이너]] 실행 원천 차단 |
| 규정 준수 자동화 | 보안 [[164_policy|정책]]이 인프라에 내재화됨 |
| 공격 표면 축소 | 불필요한 Linux 캐퍼빌리티 제거 |
| [[606_auditing_linux_auditd|감사]] 용이성 | [[061_namespace|네임스페이스]] 레이블로 [[164_policy|정책]] 상태 즉시 [[396_validation|확인]] |

PSA는 K8s 보안의 첫 번째 방어선이다. Restricted 프로파일을 기본값으로 시작하고, 예외는 명시적으로 허용하는 "기본 거부(Default Deny)" 원칙이 [[738_zero_trust_architecture_least_privilege|제로 트러스트 보안]] 모델의 [[561_container_based_deployment|컨테이너]] 구현이다.

📢 **섹션 요약 비유**: PSA의 Restricted 프로파일은 공항 보안 검색대와 같다. 모든 사람([[198_pod_kubernetes_minimum_deployment_unit|Pod]])이 기본적으로 검사를 받고, 특별한 사유가 있는 사람(시스템 [[603_component_independent_deployment_unit|컴포넌트]])만 우선 통로를 사용할 수 있다. 기본이 "검사"이고 예외가 "면제"다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[237_opa_open_policy_agent_gatekeeper|OPA]] Gatekeeper | PSA 이상의 커스텀 K8s [[164_policy|정책]] 강제 도구 |
| [[561_container_based_deployment|컨테이너]] 이미지 스캔 | PSA와 함께 [[561_container_based_deployment|컨테이너]] 킬 체인의 앞단 방어 |
| [[569_rbac|RBAC]] ([[569_rbac|Role-Based Access Control]]) | PSA와 함께 K8s [[010_least_privilege|최소 권한 원칙]] 구현 |
| NetworkPolicy | [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 간 통신을 제어하는 PSA 보완 [[164_policy|정책]] |
| [[080_seccomp|seccomp]] / [[584_apparmor|AppArmor]] | 시스템 콜 수준의 [[561_container_based_deployment|컨테이너]] 격리 강화 |
| Kyverno | Rego 없이 YAML로 K8s [[164_policy|정책]]을 정의하는 대안 |

### 👶 어린이를 위한 3줄 비유 설명

1. PSA는 놀이터 입장 규칙과 같아. "관리자(root)처럼 행동하거나 담장(host network) 너머를 넘보는 사람은 입장 불가!"

### 📈 관련 키워드 및 발전 흐름도

```text
PodSecurityPolicy (PSP, 폐지됨)
    │
    ▼
Pod Security Admission (PSA): 네임스페이스 레벨 보안
    ├─► Privileged: 제한 없음
    ├─► Baseline: 위험 설정 차단
    └─► Restricted: 최소 권한 강제
    │
    ▼
OPA Gatekeeper · Kyverno → 세밀한 정책 관리
```
2. Restricted 프로파일은 가장 엄격한 규칙이야. 꼭 필요한 장난감(캐퍼빌리티)만 가져올 수 있어.
3. 특별히 필요한 경우(시스템 [[603_component_independent_deployment_unit|컴포넌트]])만 예외로 허용하고, 기본값은 항상 "최소 권한"이야.
