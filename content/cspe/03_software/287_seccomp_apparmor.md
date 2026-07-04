---
title: "Seccomp·AppArmor (Seccomp AppArmor)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 287
---

# 📖 【암기용】 개념 완전 이해

> 목적: Seccomp·AppArmor를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: Seccomp와 AppArmor는 리눅스 커널이 제공하는 **강제적 접근 제어**(MAC, Mandatory Access Control) 계열의 **공격면 축소**(Attack Surface Reduction) 통제다 — 컨테이너 프로세스가 "무엇을 할 수 있는가"를 커널 차원에서 제한한다.
- **왜 필요한가**: 컨테이너는 namespace로 "보이는 범위"를, cgroup으로 "쓸 수 있는 자원량"을 제한하지만, 둘 다 호스트와 같은 커널을 그대로 공유한다는 사실은 바꾸지 못한다. 컨테이너 프로세스가 커널 취약점을 건드릴 수 있는 system call을 자유롭게 호출할 수 있다면, 격리를 뚫고 호스트로 넘어가는 "컨테이너 탈출(Container Escape)"이 가능해진다.
- **핵심 직관**: namespace·cgroup이 "어디까지 보이고 얼마나 쓸 수 있는지"를 정하는 울타리라면, Seccomp는 "작업자에게 공구 5개만 지급"(쓸 수 있는 시스템 콜 자체를 줄임)이고, AppArmor는 "출입 가능한 방과 열 수 있는 서랍을 지정"(경로 기준으로 리소스 접근을 줄임)이다. 울타리 안에서도 손에 쥔 도구와 열 수 있는 문을 한 번 더 좁히는 것이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| MAC(강제적 접근 제어) | 리소스 소유자가 아니라 시스템 정책이 접근 가능 여부를 강제로 결정하는 방식 — Seccomp·AppArmor가 속하는 상위 범주 | 회사 보안 규정(개인 재량 아님) |
| DAC(임의적 접근 제어) | 파일 소유자가 chmod로 권한을 정하는 기존 리눅스 방식 — MAC과 대비된다 | 내 방 열쇠는 내가 관리 |
| System Call(시스템 콜) | 프로세스가 커널에 파일·네트워크·프로세스 관련 작업을 요청하는 통로 | 커널에 거는 전화 |
| Seccomp(SECure COMPuting mode) | 프로세스가 호출할 수 있는 system call 목록을 화이트/블랙리스트로 제한하는 커널 기능 | 지급되는 공구 개수 제한 |
| BPF Filter | Seccomp이 "이 system call을 허용/차단할지"를 판단하는 데 쓰는 소형 필터 프로그램 형식 | 공구함 검수 체크리스트 |
| AppArmor | 파일 경로·capability·네트워크 접근을 프로파일(텍스트 규칙)로 제한하는 LSM 구현체 | 방·서랍 단위 출입증 |
| LSM(Linux Security Module) | 커널에 보안 훅을 심어 접근 제어 모듈을 꽂을 수 있게 하는 프레임워크 — AppArmor·SELinux가 이 위에서 동작하는 구현체 | 다양한 자물쇠를 꽂을 수 있는 공용 문틀 |
| Capability | root 권한을 세분화한 단위(예: 네트워크 설정 권한만 있는 `CAP_NET_ADMIN`) | 만능키를 용도별 열쇠로 쪼갠 것 |
| Enforce / Complain(Permissive) 모드 | 위반 시 실제로 차단하는 모드(enforce)와 로그만 남기고 허용하는 모드(complain) | 실전 배치 전의 리허설 |
| RuntimeDefault | 컨테이너 런타임(containerd 등)이 기본 제공하는 Seccomp 프로파일 | 기본 안전벨트 |

## 깊이 이해

### 왜 namespace·cgroup만으로는 부족한가 — 실제 컨테이너 탈출 사례
- namespace는 "이 프로세스가 볼 수 있는 프로세스 목록·파일시스템·네트워크"를 격리하고, cgroup은 "CPU·메모리를 얼마나 쓸 수 있는지"를 제한한다. 그러나 둘 다 "커널 코드 자체를 실행할 수 있는가"는 막지 않는다. 실제로 CVE-2019-5736(runc 취약점)은 컨테이너 안에서 조작한 프로세스가 호스트의 runc 바이너리를 덮어써 호스트를 장악하는 탈출을 가능하게 했다 — namespace가 완벽히 걸려 있어도 커널 레벨의 결함이나 과도한 권한이 있으면 뚫린다는 것을 보여준 사례다. Seccomp·AppArmor는 이런 탈출에 필요한 위험 system call·경로 접근 자체를 원천 차단해 공격면을 줄인다.

### Seccomp가 실제로 무엇을 차단하는가 — 구체 수치
- 리눅스 커널은 300개가 넘는 system call을 제공하지만, 일반적인 애플리케이션은 그중 극히 일부만 쓴다. Docker의 기본 Seccomp 프로파일은 약 44개의 system call을 명시적으로 차단한다. 대표적으로 `unshare`(새 namespace 생성), `mount`(파일시스템 마운트), `reboot`(시스템 재부팅), `ptrace`(다른 프로세스 감시·조작), `kexec_load`(커널 교체) 등이 막힌다 — 이 목록의 공통점은 "정상적인 웹 서버·배치 작업이라면 쓸 일이 없지만, 컨테이너 탈출·권한 상승에는 핵심적으로 쓰이는 system call"이라는 점이다.
- Kubernetes pod에 `securityContext.seccompProfile.type: RuntimeDefault`를 지정하면 이 기본 차단 목록이 바로 그 파드에 적용된다. 별도 설정이 없으면(구버전 기준) Seccomp가 아예 적용되지 않아 300개 넘는 system call이 전부 열려 있는 상태로 실행될 수 있다.

### AppArmor 프로파일은 실제로 어떻게 생겼는가
```
profile docker-nginx flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>
  network inet tcp,
  deny /etc/shadow rwklx,
  deny /proc/sys/** wklx,
  /var/log/nginx/*.log w,
}
```
- 이 프로파일은 "TCP 네트워크는 허용하되, `/etc/shadow`는 읽기·쓰기·잠금·실행 전부 금지, `/proc/sys` 하위 쓰기도 금지, nginx 로그 파일에는 쓰기만 허용"을 선언한다. Seccomp가 "어떤 동작(system call)을 할 수 있는가"를 본다면, AppArmor는 "어떤 경로·자원에 접근할 수 있는가"를 경로 단위로 통제한다는 차이가 여기서 드러난다.

### enforce로 바로 넘어가면 안 되는 이유 — 운영 판단
- 새 프로파일을 처음부터 enforce(위반 시 즉시 차단) 모드로 걸면, 미처 예상 못 한 정상 동작(로그 회전 스크립트가 특정 경로에 접근하는 것 등)까지 막혀 서비스 오류가 난다. 그래서 실무에서는 먼저 complain(로그만 남기고 허용) 모드로 최소 며칠~1주 이상 운영하며 "정상적으로 어떤 접근이 발생하는가"의 audit log를 충분히 모은 뒤, 그 패턴에 맞춰 프로파일을 다듬고 나서야 enforce로 전환한다.

## 연결 개념
- Linux Capability - root 권한 세분화
- Kubernetes Pod Security Standards - 컨테이너 보안 기준
- Falco - 런타임 행위 탐지

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Seccomp와 AppArmor의 통제 대상을 구분하고, Kubernetes 보안 컨텍스트와 운영 검증 지표로 연결한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Seccomp는 system call을 제한하고 AppArmor는 파일·capability 접근을 프로파일로 제한하는 Linux 커널 보안 기능이다.
> 2. **가치**: 컨테이너가 호스트 커널을 공유하는 구조에서 권한 상승과 컨테이너 탈출 공격면을 줄인다.
> 3. **판단 포인트**: RuntimeDefault, custom profile, permissive/complain mode를 workload 특성에 맞게 선택해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Linux 컨테이너 보안 통제 이해 확인 | system call 제한과 MAC 프로파일 차이 | 둘을 동일한 접근통제라고 처리 |
| Kubernetes 적용 역량 확인 | securityContext, seccompProfile, AppArmor annotation | Pod Security와 런타임 정책 연결 누락 |
| 운영 리스크 판단 확인 | profile tuning, 차단 로그, 예외 승인 | 업무 프로세스 중단 위험 누락 |

> 요약: 이 키워드는 컨테이너 격리의 한계를 커널 통제로 보완하는 구조를 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: Seccomp·AppArmor는 커널 기반 접근 제한이다.
- 배경: 컨테이너는 호스트 커널을 공유하므로 system call과 파일 접근을 최소화해야 한다.
- 필요성: Kubernetes securityContext와 프로파일로 컨테이너 탈출 공격면을 줄여야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Container Process -> Linux Kernel -> Seccomp Filter / AppArmor Profile -> Allow/Deny -> Audit Log
                              +-> Kubernetes securityContext
                              +-> RuntimeDefault Profile
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Seccomp Profile | 허용·차단 system call 정의 | BPF filter, RuntimeDefault |
| AppArmor Profile | 파일 경로, capability, network 접근 제한 | enforce/complain mode |
| securityContext | Kubernetes pod/container 보안 설정 | seccompProfile, capabilities drop |
| Audit Log | 차단 이벤트와 프로파일 위반 기록 | dmesg, auditd, kube event |
| Runtime | 프로파일을 컨테이너 실행에 적용 | containerd, CRI-O |

> 요약: Seccomp는 system call, AppArmor는 리소스 접근을 제한하고 Kubernetes securityContext가 이를 pod 실행에 연결한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Pod 생성 -> securityContext 확인 -> 프로파일 로드 -> system call/파일 접근 평가 -> 허용/차단/로그
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | workload에 적용할 프로파일 선택 | RuntimeDefault 적용률 100% |
| 2 | 컨테이너 런타임이 프로파일 로드 | load failure 0건 |
| 3 | system call 또는 파일 접근 발생 | syscall allowlist와 경로 규칙 평가 |
| 4 | 위반 행위 차단 또는 기록 | deny log 수집률 100% |
| 5 | 업무 영향 분석 후 profile 조정 | 정상 요청 오류율 1% 이하 |

> 요약: 커널은 컨테이너 실행 중 발생하는 system call과 리소스 접근을 프로파일 기준으로 평가한다.

---

## Ⅳ. 특징

| 구분 | Seccomp | AppArmor | 수치·기술 포인트 |
|:---|:---|:---|:---|
| 통제 대상 | system call | 파일, capability, network | Linux LSM |
| 정책 형식 | JSON profile, BPF filter | text profile | RuntimeDefault |
| 적용 방식 | Kubernetes seccompProfile | annotation 또는 runtime profile | enforce/complain |
| 한계 | 업무 syscall 차단 위험 | 경로 기반 정책 관리 부담 | audit 기반 tuning 필요 |

> 요약: Seccomp는 커널 호출면, AppArmor는 리소스 접근면을 줄이며 둘을 함께 써야 컨테이너 hardening 효과가 커진다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | privileged container | RuntimeDefault와 custom profile | 민감 업무 pod |
| 비용/성능 | 제한 없음 | profile 적용과 audit tuning | 정상 요청 오류율 1% 이하 |
| 운영/위험 | 공격면 과다 | 최소 syscall과 파일 접근 | 규제·멀티테넌트 cluster |

> 요약: 민감 업무와 멀티테넌트 클러스터는 RuntimeDefault를 기본값으로 두고 예외 workload만 custom profile을 적용한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 업무 중단 | 필요한 syscall 차단 | complain mode 검증 후 enforce | 정상 트랜잭션 오류율 1% 이하 |
| 정책 미적용 | pod securityContext 누락 | admission policy로 기본값 강제 | 미적용 pod 0개 |
| 과도한 권한 | privileged, CAP_SYS_ADMIN 허용 | capabilities drop ALL, 예외 승인 | privileged pod 0개 |

> 요약: 운영 리스크는 사전 검증, admission 기본값, capability 최소화로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 적용률 | RuntimeDefault 적용 pod 100% | Kubernetes audit, policy report |
| 권한 최소화 | privileged pod 0개, CAP_SYS_ADMIN 0건 | admission log |
| 차단 품질 | 업무 오류율 1% 이하 | APM, audit deny log |

> 요약: Seccomp·AppArmor 적용은 적용률, 권한 최소화, 업무 영향 지표를 함께 봐야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. Kubernetes namespace 기본 정책으로 `seccompProfile: RuntimeDefault`와 `allowPrivilegeEscalation: false`를 적용함
2. 민감 workload는 complain mode에서 7일 이상 audit log를 수집한 뒤 custom AppArmor profile을 enforce mode로 전환함
3. OPA Gatekeeper 또는 Kyverno로 privileged container, hostPID, CAP_SYS_ADMIN, seccomp 미설정을 admission 단계에서 차단함

**결론 (2줄):**
- 기술사 판단: 일반 workload는 RuntimeDefault, 고위험 workload는 custom Seccomp·AppArmor profile과 admission policy를 적용함
- 향후 방향: 컨테이너 hardening은 Pod Security Standards, eBPF 탐지, Policy as Code와 결합한 기본 보안선으로 정착함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Seccomp와 AppArmor를 설명하시오" | 프로파일 적용과 커널 평가 흐름 | system call 제한과 MAC 차이 |
| 요구사항 명시형 | "컨테이너 보안 강화 방안을 제시하시오" | securityContext, admission, audit 흐름 | RuntimeDefault, privilege 차단, 업무 영향 기준 |

> 요약: 설명형은 기능 차이, 보안형은 Kubernetes 적용과 운영 검증 지표 중심으로 전개한다.
