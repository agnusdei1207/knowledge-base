---
sidebar:
  order: 158
  label: "158. 컨테이너 보안: Seccomp•AppArmor•OPA"
  badge:
    text: "미출 · 70%"
    variant: note
title: "컨테이너 보안: Seccomp•AppArmor•OPA (Container Security)"
date: "2026-08-31T10:48:00+09:00"
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

<details><summary>용어 설명</summary>

- **컨테이너 보안(Container Security)**: 이미지 빌드부터 배포 승인(Admission), 런타임 커널 격리까지 전 주기를 보호하는 다층 방어 보안 체계.
- **Seccomp & AppArmor & OPA**: 시스템 콜 차단(Seccomp), 강제 접근 제어(AppArmor), 배포 시점 선언적 정책 검증(OPA Gatekeeper).

</details>

- 정의/개념: 컨테이너 이미지 빌드, 배포 승인, 런타임 전 주기에 걸쳐 **Seccomp, AppArmor, OPA를 적용하여 컨테이너 탈출과 악성 행위를 차단하는 다층 방어 체계**
- 배경/필요성: 컨테이너 환경이 호스트 OS 커널을 공유하는 구조적 특성으로 인해 단일 컨테이너 침해 시 발생하는 특권 상승 및 호스트 탈출(Container Escape), 이미지 공급망 오염(Supply Chain Attack), 악성 런타임 행위(WebShell, 비인가 시스템 콜)의 클러스터 전파 위험을 원천 차단하기 위해, 이미지 빌드 검증(Trivy/Cosign), 배포 시점 선언적 정책 강제(OPA Gatekeeper/Kyverno), 런타임 커널 시스템 콜 차단(Seccomp) 및 강제 접근 제어(AppArmor)를 결합한 **시프트 레프트(Shift-Left) 기반의 심층 방어(Defense-in-Depth) 컨테이너 보안 체계를 구축**할 필요

#### 한줄 요약
- 빌드부터 런타임까지 다계층 보안 통제를 적용하여 컨테이너 탈출과 악성 행위를 원천 차단한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Shift-Left Security**: 보안 검사를 런타임 사후 대응이 아닌 CI/CD 빌드 및 PR 단계로 전진 배치하여 취약점을 조기 제거하는 원칙.
- **Falco (eBPF Threat Detection)**: eBPF를 통해 컨테이너 내부의 비인가 쉘 실행이나 민감 파일 수정을 실시간 탐지하는 런타임 보안 도구.

</details>

- 빌드 단계 취약점 스캔(Trivy)과 서명 검증(Cosign)을 통한 **공급망 보안(Supply Chain)**
- OPA Gatekeeper를 활용하여 루트 권한 파드 배포를 차단하는 **배포 통제(Admission Control)**
- Seccomp 및 AppArmor를 통한 **커널 시스템 콜 및 파일시스템 접근 최소화**

#### 한줄 요약
- 공급망 신뢰 검증, 배포 관문 차단, 런타임 커널 제약을 결합하여 완벽한 방어막을 구축한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **컨테이너 4대 보안 계층**: Build Stage(이미지 신뢰), Admission Stage(배포 정책 검증), Runtime Kernel(시스템콜/MAC 통제), Monitoring(이상 탐지).

</details>

```text
[컨테이너 보안 구성]
|-- 이미지 신뢰
|-- 정책 엔진
|-- 보안 컴퓨팅
|-- 강제 접근 제어
`-- 런타임 탐지
```

선의 의미: 계층 및 이미지 빌드부터 API 서버 배포 검증, 런타임 커널 격리, 이상 탐지로 이어지는 심층 방어 구조

| 구성요소 | 책임 | 주요 특징 |
|:---|:---|:---|
| 이미지 신뢰 (Image Trust) | 베이스 이미지 CVE 취약점을 스캔하고 **Cosign 암호화 전자서명 무결성 검증** | Trivy, Cosign |
| 정책 엔진 (OPA Gatekeeper) | K8s Admission Webhook에서 **특권(Privileged) 설정 및 Root 실행 파드 배포 차단**| Policy-as-Code |
| 보안 컴퓨팅 (Seccomp) | 컨테이너가 호출 가능한 **리눅스 시스템 콜(System Call) 화이트리스트 필터링** | `RuntimeDefault` |
| 강제 접근 제어 (AppArmor) | 컨테이너 프로세스의 **파일 읽기/쓰기, 네트워크 소켓, 실행 권한을 강제 제한**| MAC 프로필 적용 |
| 런타임 탐지 (Falco) | eBPF 커널 이벤트를 모니터링하여 **컨테이너 내부 이상 쉘 실행 실시간 감시/경보** | 실시간 위협 탐지 |

#### 한줄 요약
- 같은 탈출 시나리오를 이미지 신뢰·배포 관문·커널 제약·런타임 탐지가 서로 다른 시점에서 나눠 막으므로, 한 계층이 뚫려도 다음 계층에서 공격 비용이 다시 부과된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **컨테이너 배포 및 실행 보안 5단계**: 이미지 서명 검증 $\to$ Admission Webhook 정책 평가 $\to$ 통과 시 Seccomp/AppArmor 적용 $\to$ 프로세스 기동 $\to$ Falco 런타임 감시.

</details>

```text
개발자가 Pod 배포 YAML을 API 서버로 제출
        │
   [이미지 서명 검증] CI/CD 및 Admission 단계에서 Cosign 서명 유효성 및 CVE 스캔 확인
        │
   [Admission Webhook 평가] OPA Gatekeeper가 `runAsNonRoot: true` 및 권한 상승 금지 검사
   ┌────┴───────────────────────────┐
  예 (보안 정책 위반)               아니오 (보안 기준 충족)
   │                                 │
[배포 즉시 거부]                  [배포 승인 및 스케줄링]
API 서버가 요청을 Reject하고      워커 노드로 Pod 스펙 전달
개발자에게 위반 사유 반환         │
        │                            ▼
        │                       [런타임 프로필 부착]
        │                          kubelet이 Seccomp 시스템콜 필터 및 AppArmor 프로필 적용
        │                            │
   └────┴────────────────────────────┤
                                     ▼
                                runc 프로세스 기동 및 Falco eBPF 실시간 이상 행위 감시
```

#### 한줄 요약
- 정책 위반은 배포 이전에 거부되어 비용이 API 요청 반려로 끝나지만, 승인 이후의 위협은 이미 기동된 프로세스를 상대해야 하므로 탐지와 격리에 드는 비용이 자릿수 단위로 커진다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **OPA vs Seccomp vs AppArmor**: 배포 시점 명세 검증(OPA), 시스템콜 제한(Seccomp), 파일/리소스 접근 통제(AppArmor).

</details>

| 비교 항목 | OPA Gatekeeper / Kyverno | Seccomp (Secure Computing) | AppArmor / SELinux |
|:---|:---|:---|:---|
| 보안 적용 시점 | **배포 시점 (Admission Controller)** | **런타임 실행 시점 (Process Execution)** | **런타임 실행 시점 (Resource Access)** |
| 핵심 통제 대상 | **K8s YAML 오브젝트 명세 (Root, Privileged)**| **리눅스 시스템 콜 (System Calls)** | **파일 경로, 네트워크, Capabilities** |
| 강제 적용 방식 | Webhook 기반 API 배포 거부/차단 | **커널 레벨 시스템 콜 즉시 Drop/Kill** | **프로필 기반 파일 접근 Permission Denied**|
| 실무 권장 설정 | Pod Security Standards (Restricted) | **`seccompProfile: RuntimeDefault`** | **`apparmor.net/profile: runtime/default`**|

#### 한줄 요약
- OPA는 배포 명세를 검증하고, Seccomp는 시스템 콜을 제한하며, AppArmor는 파일 접근을 통제한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Container Escape**: 커널 취약점(CVE-2019-5736 등)을 악용하여 컨테이너 내부에서 호스트 노드의 Root 권한을 탈취하는 보안 위협.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 특권 파드 악용으로 호스트 커널 탈출 해킹 발생 | **OPA Gatekeeper로 `privileged: true` 및 HostPath 마운트 배포 차단** | 컨테이너 탈출 경로 원천 차단 |
| 베이스 이미지의 무거운 패키지로 인한 CVE 취약점 노출 | **Distroless 또는 Chainguard 최소 패키징 이미지로 전면 교체** | 이미지 취약점 95% 이상 제거 |
| DB 비밀번호가 컨테이너 이미지 또는 환경변수에 평문 노출 | **External Secrets Operator 연동 및 AWS Secrets Manager 주입** | 민감 크리덴셜 노출 원천 방지 |
| 컨테이너 내부 침투 후 악성코드 다운로드 및 실행 | **`readOnlyRootFilesystem: true` 설정으로 불변 런타임 강제** | 악성 웹쉘/바이너리 저장 불가 |

#### 한줄 요약
- 네 대책은 컨테이너가 쓸 수 있는 권한과 공격 표면을 깎아 얻은 안전이며, 특권과 쓰기 가능 파일시스템을 포기한 만큼 운영 편의와 컨테이너 내부 디버깅 자유를 대가로 내준다.

## Ⅶ. 결론

- 엔터프라이즈 클라우드 네이티브 환경에서 컨테이너 침해 사고를 원천 방어하는 **가장 포괄적이고 실증적인 다계층(Defense-in-Depth) 보안 프레임워크**로 확립되었으며, 실무 운영 시에는 **CI/CD 파이프라인 내 무서명 이미지 배포 차단(Cosign), OPA Admission Webhook 기반 `runAsNonRoot` 및 `readOnlyRootFilesystem` 강제, K8s 기본 `seccompProfile: RuntimeDefault` 적용, eBPF 기반 Falco 런타임 비인가 쉘 실시간 탐지·차단**을 결합하여 개발 생산성을 저해하지 않으면서 제로 트러스트 컨테이너 보안을 완성

#### 한줄 요약
- 컨테이너 보안은 배포 관문 통제와 커널 수준의 최소 권한 격리 및 실시간 위협 탐지를 결합하여 침해 확산을 원천 차단하는 핵심 클라우드 보안 기술이다.
