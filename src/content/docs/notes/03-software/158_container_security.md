---
sidebar:
  order: 158
  label: "158. 컨테이너 보안: Seccomp•AppArmor•OPA (Container Security)"
  badge:
    text: "미출 • 70%"
    variant: note
title: "컨테이너 보안: Seccomp•AppArmor•OPA (Container Security)"
date: "2026-08-10T10:00:00+09:00"
tags:
  - "notes-software"
weight: 158
extra:
  question_no: "158"
  source_status: "미출"
  source_history: ""
  priority: 70
  priority_note: "배포 정책과 커널 통제를 잇는 보안 설계가 중요함"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Container Security**: 컨테이너 이미지 빌드(Dev), 레지스트리 저장, K8s 배포(Admission), 런타임(Runtime Execution) 4단계 전 라이프사이클에 걸쳐 보안 위협을 차단하는 다층 방어(Defense-in-Depth) 보안 체계.
- **Seccomp (Secure Computing Mode)**: 컨테이너 프로세스가 리눅스 커널로 요청하는 300여 개의 시스템 콜(System Call: `ptrace`, `reboot` 등) 중 불필요한 시스템 콜을 억제 차단하는 리눅스 커널 보안 모듈.
- **AppArmor / SELinux**: 컨테이너의 파일 시스템 접근 경로, 네트워크 포트, 프로세스 실행 자격을 규제하는 리눅스 MAC(Mandatory Access Control) 보안 모듈.
- **OPA / Gatekeeper (Open Policy Agent)**: K8s Admission Webhook 단계에서 `privileged: true` 설정이나 `latest` 태그 이미지를 가진 위험한 Pod의 생성을 사전에 자동 차단하는 선언적 정책 엔진.

</details>

- 정의/개념: 이미지 취약점 스캔, Admission Webhook (OPA/Gatekeeper) 차단, 런타임 커널 시스템 콜 차단(Seccomp/AppArmor)으로 컨테이너 탈출 해킹을 미연에 방지하는 **Container Security Framework**
- 배경/필요성: 컨테이너 해킹 시 호스트 OS 커널(Host Kernel) 탈출(Container Escape)을 통한 전사 클러스터 붕괴 사고 차단 필요성

#### 한줄 요약

- 이미지 반입, 배포 승인, 실행 권한, 실행 중 행동을 서로 다른 지점에서 검사해야 하나의 통제가 뚫려도 다음 통제가 피해를 막는다.

## Ⅱ. 특징 (컨테이너 4단계 다층 보안 레이어)

<details><summary>핵심 용어</summary>

- **Shift-Left Security**: 개발/빌드 단계(CI/CD)로 보안 검사를 전진 배치하여 이미지 취약점을 사전에 차단하는 보안 사상.

</details>

- **1. Build Phase (Trivy / Grype 이미지 CVE 취약점 스캔 & Cosign 서명)**
- **2. Admission Phase (OPA Gatekeeper / Kyverno 선언적 정책 차단)**
- **3. Runtime Phase (Seccomp System Call 제한 & AppArmor Profile 적용)**
- **4. Behavioral Monitoring (Falco 기반 런타임 쉘 접속 및 이상 행위 실시간 감시)**

#### 한줄 요약

- 게이트키퍼가 특권 설정을 입구에서 거부하고 보안 컴퓨팅 모드와 앱아머가 승인된 컨테이너의 시스템 호출과 파일 접근을 실행 중에 제한한다.

## Ⅲ. 구조 및 구성요소 (4대 런타임/배포 보안 툴 아키텍처)

<details><summary>핵심 용어</summary>

- **Falco (Runtime Threat Detection)**: eBPF를 활용해 컨테이너 내부에서 `/etc/shadow` 읽기, `bash` 쉘 획득 등 비정상 악성 행위를 실시간 감지해 Slack 알림을 쏘는 CNCF 오픈소스.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   Container Security Defense-in-Depth                  │
├────────────────────────────────────────────────────────────────────────┤
│ [1. Build: Trivy CVE Scan] ──► [2. Admission: OPA Gatekeeper Check]   │
│                                           │ (Check Passed)             │
│                                           ▼                            │
│ [3. Runtime: Seccomp / AppArmor Profile] ──► [4. Detection: Falco eBPF] │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 빌드 단계부터 런타임 감시까지 4단계로 철통 보안을 거치는 파이프라인.

| 보안 레이어 | 담당 도구 (Tool) | 주요 역할 및 실무 기술 메커니즘 |
|:---|:---|:---|
| **Build & Image** | **Trivy, Cosign** | **이미지 CVE 취약점 스캔 및 디지털 서명 검증** |
| **Admission Control**| **OPA Gatekeeper, Kyverno**| **`privileged: true` 및 `root` 실행 Pod 생성 차단**|
| **Kernel Hardening** | **Seccomp, AppArmor** | **불필요한 Linux System Call 및 파일 경로 차단** |
| **Runtime Detection**| **Falco (eBPF)** | **컨테이너 해킹/쉘 접속 이상 행위 실시간 감지** |

#### 한줄 요약

- 서명된 이미지가 입장권이라면 Admission은 복장 검사, SecurityContext는 지급 권한, Linux 커널은 실제 행동을 막는 잠금장치다.

## Ⅳ. 흐름도 (OPA Gatekeeper & Seccomp 런타임 검증 흐름)

<details><summary>핵심 용어</summary>

- **Admission Webhook**: K8s API 서버가 Resource를 etcd에 기재하기 직전, OPA/Kyverno 로 검증 요청을 보내 통과(Allow) 여부를 묻는 훅.

</details>

```text
[kubectl apply pod.yaml] ──► [kube-apiserver Admission Webhook]
                                            │
                                            ▼ (Check OPA Policy)
 [Pod Run on Node with Seccomp] ◄── [Allow] ┴ ── [Deny: Privileged Root Pod Blocked]
```

### 동작 원리

1. **Admission Webhook**: 개발자가 `privileged: true` (Root 권한) Pod 배포 시도.
2. **OPA Policy Check**: Gatekeeper가 Rego 정책 위반을 감지하여 API 서버에서 `Deny` 차단.
3. **Seccomp Enforcement**: 정상 통과된 Pod만 Node 상에서 `Seccomp default profile` 적용 구동 (**Container Security 완결**).

#### 한줄 요약

- 배포 전에 특권과 이미지 출처를 검사하고 실행 시에는 런타임이 전달한 프로필을 커널이 매 호출과 접근마다 강제한다.

## Ⅴ. 종류 및 비교 (SecurityContext 3대 핵심 옵션 1:1 비교)

<details><summary>핵심 용어</summary>

- **securityContext Attributes**: `readOnlyRootFilesystem: true`, `runAsNonRoot: true`, `allowPrivilegeEscalation: false`.

</details>

| securityContext 설정 옵션 | 보안 위험 예방 효과 | 실무 필수 적용 기준 |
|:---|:---|:---|
| **`runAsNonRoot: true`** | **Container가 Root 계정으로 구동되어 호스트 점령 예방**| 필수 적용 |
| **`allowPrivilegeEscalation: false`** | SUID 바이너리로 권한 상승 해킹 시도 차단 | 필수 적용 |
| **`readOnlyRootFilesystem: true`**| 악성코드나 웹쉘 파일 다운로드 자체를 차단 | **필수 적용 (불변 런타임)**|

#### 한줄 요약

- OPA는 위험한 배포 명세를 막고 보안 컴퓨팅 모드는 호출 종류를, 앱아머와 보안 강화 리눅스는 파일·장치 접근 범위를 줄인다.

## Ⅵ. 실무 고려사항 및 대책 (컨테이너 보안 3대 난제 대책)

<details><summary>핵심 용어</summary>

- **Container Escape Vulnerability**: `runC` 및 리눅스 커널 취약점(CVE-2019-5736)으로 컨테이너 내부에서 호스트 노드 Root 권한을 탈취하는 대형 사고.

</details>

| 3대 컨테이너 보안 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Container Escape** | `privileged: true` 부여로 커널 탈취 | **OPA Gatekeeper로 Privileged Pod 생성 100% 금지**|
| **2. Vulnerable Base Image**| Ubuntu/Debian 베이스 이미지 CVE 속출 | **Chainguard / Distroless 최소 베이스 이미지 전환**|
| **3. Secret File Leaks** | DB 비번을 이미지 내부나 환경변수로 박음 | **HashiCorp Vault / External Secrets Operator 연동** |

> 사례: **토스 / 당근마켓 / 쿠팡 OPA Gatekeeper & Falco & Trivy 통합 데브섹옵스(DevSecOps) 적용 사례**

#### 한줄 요약

- 새 프로필은 관찰 모드에서 정상 호출을 수집한 뒤 단계 배포하고 예외에는 소유자와 만료일을 붙여 통제 공백을 제한해야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Container Security 수립 기준(Security Standards)**: Trivy CI/CD Scan, OPA Gatekeeper Admission, Seccomp/AppArmor Profile 및 Falco eBPF Detection에 의거한 체계.

</details>

- **Container Security 수립 기준**에 따라 차세대 DevSecOps 구축 시 **Trivy & OPA Gatekeeper & Seccomp & Falco** 필수 적용

#### 한줄 요약

- 신뢰 이미지만 승인하고 비Root를 기본값으로 삼되 실제 업무 호출을 시험한 커널 프로필과 감사 사건을 함께 운영해야 한다.
