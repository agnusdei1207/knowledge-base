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
- **개요**: Linux 컨테이너의 시스템 콜과 파일 접근을 제한하는 커널 보안 통제
- **왜 필요한가**: 컨테이너는 호스트 커널을 공유한다. 컨테이너 내부 프로세스가 과도한 system call이나 파일 접근 권한을 가지면 권한 상승과 호스트 침해로 이어질 수 있다.
- **핵심 직관**: Seccomp는 사용할 수 있는 도구 목록을 줄이고, AppArmor는 접근할 수 있는 방과 서랍을 제한한다.

## 깊이 이해
- **배경·문제의식**: 컨테이너 격리는 namespace와 cgroup만으로 충분하지 않다. 커널 취약점이나 잘못된 권한 설정이 있으면 컨테이너 탈출 위험이 생긴다.
- **작동 원리**: Seccomp는 BPF 필터로 허용 또는 차단할 system call을 정의한다. AppArmor는 프로파일로 파일 경로, capability, 네트워크 접근을 제한한다.
- **비유**: 작업자에게 필요한 공구 5개만 지급하는 것이 Seccomp이고, 작업 구역 출입증을 제한하는 것이 AppArmor다.
- **구체 예시**: Kubernetes pod에 `seccompProfile: RuntimeDefault`를 적용하고 AppArmor profile로 `/proc`, `/sys`, `/etc/shadow` 접근을 제한해 컨테이너 탈출 공격면을 줄인다.
- **흔한 오해·주의점**: Seccomp와 AppArmor는 취약점을 패치하지 않는다. 공격면을 줄이는 hardening 통제이며 이미지 스캔, RBAC, 네트워크 정책과 함께 적용해야 한다.

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

Seccomp·AppArmor는 커널 기반 접근 제한이다. 컨테이너는 호스트 커널을 공유하므로 system call과 파일 접근을 최소화해야 한다. 두 기능은 Kubernetes securityContext와 프로파일을 통해 컨테이너 탈출 공격면을 줄인다.

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

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
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
