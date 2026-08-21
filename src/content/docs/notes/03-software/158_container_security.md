---
sidebar:
  order: 158
  label: "158. 컨테이너 보안: Seccomp•AppArmor•OPA (Container Security)"
  badge:
    text: "미출 · 70%"
    variant: note
title: "컨테이너 보안: Seccomp•AppArmor•OPA (Container Security)"
date: "2026-08-14T02:24:00+09:00"
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

- **컨테이너 보안(Container Security)**: 이미지 빌드부터 배포(Admission), 런타임까지 전 주기에서 위협을 차단하는 다층 방어 보안 체계.
- **Seccomp(Secure Computing Mode)**: 컨테이너의 불필요한 시스템 콜(System Call)을 커널 레벨에서 차단하는 보안 모듈.
- **AppArmor / SELinux**: 컨테이너의 파일 접근, 네트워크, 프로세스 실행 권한을 규제하는 강제 접근 제어(MAC, Mandatory Access Control) 보안 모듈.
- **OPA / Gatekeeper**: 특권(Privileged) 설정이나 태그 오용 등 위험한 파드 생성을 배포 시점에 자동 차단하는 정책 엔진(Policy Engine).

</details>

- 정의/개념: Image부터 Runtime까지 통제하는 **Container Security**
- 배경/필요성: Host Kernel 공유로 침해 시 **Container Escape** 위험 확산

#### 한줄 요약

- 이미지 반입, 배포 승인, 실행 권한, 실행 중 행동을 서로 다른 지점에서 검사해야 하나의 통제가 뚫려도 다음 통제가 피해를 막는다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Shift-Left Security**: 개발/빌드 단계(CI/CD)로 보안 검사를 전진 배치하여 이미지 취약점을 사전에 차단하는 보안 사상.

</details>

- **빌드 단계**: Trivy/Grype 이미지 CVE 스캔 및 서명(Cosign).
- **배포 단계**: OPA Gatekeeper/Kyverno 정책 기반 위험 파드 차단.
- **런타임 단계**: Seccomp 시스템 콜 제한 및 AppArmor 프로필 적용.
- **이상 행위 감시**: Falco 기반 비정상 행위(쉘 접속 등) 실시간 탐지.

#### 한줄 요약

- 게이트키퍼가 특권 설정을 입구에서 거부하고 보안 컴퓨팅 모드와 앱아머가 승인된 컨테이너의 시스템 호출과 파일 접근을 실행 중에 제한한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Falco (Runtime Threat Detection)**: eBPF를 활용해 컨테이너 내부에서 `/etc/shadow` 읽기, `bash` 쉘 획득 등 비정상 악성 행위를 실시간 감지해 Slack 알림을 쏘는 CNCF 오픈소스.

</details>

```text
[Container Security]
 ├── [Image Trust]
 ├── [Admission Policy]
 ├── [Kernel Restriction]
 └── [Runtime Detection]
```

| 구성요소 | 책임 |
|---|---|
| Image Trust | **취약점**•**서명** 및 공급망 출처 검증 |
| Admission Policy | 위험한 **Pod 명세** 저장•배포 거부 |
| Kernel Restriction | **System Call•파일 접근** 최소 권한 강제 |
| Runtime Detection | 실행 중 **이상 행위** 탐지•대응 |

#### 한줄 요약

- 서명된 이미지가 입장권이라면 Admission은 복장 검사, SecurityContext는 지급 권한, Linux 커널은 실제 행동을 막는 잠금장치다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Admission Webhook**: K8s API 서버가 Resource를 etcd에 기재하기 직전, OPA/Kyverno 로 검증 요청을 보내 통과(Allow) 여부를 묻는 훅.

</details>

```text
[Pod 배포 요청]
      │
      ▼
1. Image 신뢰 검증
      │
      ▼
2. Admission Policy 평가
 ┌────┴────┐
 │ 위반    │ 허용
3. Policy 결과 처리
  │ 거부       │ 허용
[요청 거부]    ▼
        4. Runtime Profile 적용
               │
               ▼
        5. 실행•이상 행위 감시
               │
               ▼
          [실행 상태 반환]
```

### 동작 원리

1. Image 신뢰 검증: Digest•서명•취약점 기준 확인
2. Admission Policy 평가: 특권•Root•Host 접근 검사
3. Policy 결과 처리: 위반 요청 거부 또는 실행 승인
4. Runtime Profile 적용: Seccomp•MAC 통제 부착
5. 실행•이상 행위 감시: Kernel 강제와 Event 대응

#### 한줄 요약

- 배포 전에 특권과 이미지 출처를 검사하고 실행 시에는 런타임이 전달한 프로필을 커널이 매 호출과 접근마다 강제한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **securityContext Attributes**: `readOnlyRootFilesystem: true`, `runAsNonRoot: true`, `allowPrivilegeEscalation: false`.

</details>

| securityContext 설정 옵션 | 보안 위험 예방 효과 | 실무 필수 적용 기준 |
|:---|:---|:---|
| `runAsNonRoot: true` | **Container가 Root 계정으로 구동되어 호스트 점령 예방**| 필수 적용 |
| `allowPrivilegeEscalation: false` | SUID 바이너리로 권한 상승 해킹 시도 차단 | 필수 적용 |
| `readOnlyRootFilesystem: true` | 악성코드나 웹쉘 파일 다운로드 자체를 차단 | **필수 적용 (불변 런타임)**|

#### 한줄 요약

- OPA는 위험한 배포 명세를 막고 보안 컴퓨팅 모드는 호출 종류를, 앱아머와 보안 강화 리눅스는 파일·장치 접근 범위를 줄인다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Container Escape Vulnerability**: `runC` 및 리눅스 커널 취약점(CVE-2019-5736)으로 컨테이너 내부에서 호스트 노드 Root 권한을 탈취하는 대형 사고.

</details>

| 3대 컨테이너 보안 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| 1. Container Escape | 과도한 특권과 Kernel 취약점 | **Admission 차단과 Runtime 최신화**|
| 2. Vulnerable Base Image | Ubuntu/Debian 베이스 이미지 CVE 속출 | **Chainguard / Distroless 최소 베이스 이미지 전환**|
| 3. Secret File Leaks | DB 비번을 이미지 내부나 환경변수로 박음 | **HashiCorp Vault / External Secrets Operator 연동** |

> 사례: **토스 / 당근마켓 / 쿠팡 OPA Gatekeeper & Falco & Trivy 통합 데브섹옵스(DevSecOps) 적용 사례**

#### 한줄 요약

- 새 프로필은 관찰 모드에서 정상 호출을 수집한 뒤 단계 배포하고 예외에는 소유자와 만료일을 붙여 통제 공백을 제한해야 한다.

## Ⅶ. 결론

- 배포 전 **Admission**, 실행 중 Seccomp•MAC•탐지 계층 적용

#### 한줄 요약

- 이미지 신뢰를 확인하고 위험 명세를 막은 뒤 Kernel 최소 권한과 실행 탐지를 겹친다.
