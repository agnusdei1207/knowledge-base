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

- **컨테이너 보안(Container Security)**: 이미지 빌드부터 배포(Admission), 런타임까지 전 주기에서 위협을 차단하는 다층 방어 보안 체계.
- **Seccomp (Secure Computing Mode)**: 컨테이너의 불필요한 시스템 콜(System Call)을 커널 레벨에서 차단하는 보안 모듈.
- **AppArmor / SELinux**: 컨테이너의 파일 접근, 네트워크, 프로세스 실행 권한을 규제하는 강제 접근 제어(MAC) 보안 모듈.
- **OPA / Gatekeeper**: 특권(Privileged) 설정이나 태그 오용 등 위험한 파드 생성을 배포 시점에 자동 차단하는 정책 엔진.

</details>

- 정의/개념: 이미지 취약점 스캔, Admission Webhook (OPA/Gatekeeper) 차단, 런타임 커널 시스템 콜 차단(Seccomp/AppArmor)으로 컨테이너 탈출 해킹을 미연에 방지하는 **Container Security Framework**
- 배경/필요성: 컨테이너 해킹 시 호스트 OS 커널(Host Kernel) 탈출(Container Escape)을 통한 전사 클러스터 붕괴 사고 차단 필요성

#### 한줄 요약

- 이미지 반입, 배포 승인, 실행 권한, 실행 중 행동을 서로 다른 지점에서 검사해야 하나의 통제가 뚫려도 다음 통제가 피해를 막는다.

## Ⅱ. 특징 (컨테이너 4단계 다층 보안 레이어)

<details><summary>핵심 용어</summary>

- **Shift-Left Security**: 개발/빌드 단계(CI/CD)로 보안 검사를 전진 배치하여 이미지 취약점을 사전에 차단하는 보안 사상.

</details>

- **빌드 단계(Build)**: Trivy/Grype 이미지 CVE 스캔 및 서명(Cosign).
- **배포 단계(Admission)**: OPA Gatekeeper/Kyverno 정책 기반 위험 파드 차단.
- **런타임 단계(Runtime)**: Seccomp 시스템 콜 제한 및 AppArmor 프로필 적용.
- **이상 행위 감시(Monitoring)**: Falco 기반 비정상 행위(쉘 접속 등) 실시간 탐지.

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

| 보안 레이어 | 담당 도구 | 주요 기술 메커니즘 |
|:---|:---|:---|
| **Build/Image** | Trivy, Cosign | 이미지 CVE 취약점 스캔 및 서명 검증 |
| **Admission** | OPA Gatekeeper | 특권 Pod 및 루트 실행 차단 |
| **Kernel** | Seccomp, AppArmor | 불필요 시스템 콜 및 파일 접근 제한 |
| **Detection** | Falco (eBPF) | 해킹 및 쉘 접속 이상 행위 감지 |

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

- **다층 방어 보안 체계 구축 및 컨테이너 런타임 보안 강화 체계 확립**
