---
title: "Seccomp·AppArmor·SELinux (Seccomp AppArmor SELinux)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 126
---

# 📖 【암기용】 개념 완전 이해

> 목적: 리눅스 컨테이너 보안 격리를 처음 봐도 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: Seccomp, AppArmor, SELinux는 컨테이너가 커널과 파일·프로세스 자원을 남용하지 못하게 제한하는 리눅스 보안 통제이다.
- **왜 필요한가**: 컨테이너는 호스트 커널을 공유하므로 컨테이너 탈출이 발생하면 같은 노드의 다른 워크로드까지 영향을 받는다.
- **핵심 직관**: Seccomp는 시스템콜 문지기, AppArmor는 프로그램별 행동 규칙, SELinux는 라벨 기반 출입 통제임.

## 깊이 이해
- **배경·문제의식**: 컨테이너는 VM처럼 커널을 분리하지 않는다. `CAP_SYS_ADMIN`, `mount`, `ptrace` 같은 기능이 열려 있으면 취약점 1개가 호스트 권한 확대로 이어질 수 있다.
- **작동 원리**: Seccomp는 허용 시스템콜 목록으로 커널 진입을 제한한다. AppArmor는 프로파일로 파일·네트워크·capability 사용을 제한한다. SELinux는 주체·객체 라벨과 정책으로 접근을 판정한다.
- **비유**: 건물 보안으로 보면 Seccomp는 사용 가능한 문 종류 제한, AppArmor는 사원별 동선표, SELinux는 사원증 색상과 구역 등급을 대조하는 방식이다.
- **구체 예시**: Docker 기본 seccomp 프로파일은 `keyctl`, `perf_event_open`, `bpf` 등 위험 시스템콜을 차단하고, Kubernetes는 `RuntimeDefault`로 런타임 기본 프로파일을 적용할 수 있다.
- **흔한 오해·주의점**: 세 기술은 백신이 아니다. 취약 프로세스를 탐지하는 도구가 아니라, 이미 실행된 프로세스의 커널·파일 접근면을 줄이는 강제 통제이다.

## 연결 개념
- 네임스페이스·cgroup 격리: 자원 가시성과 사용량을 나누는 기반 기술
- Rootless 컨테이너: UID 매핑으로 호스트 root 권한 획득 가능성을 낮추는 실행 방식
- 최소 권한 원칙: capability drop, read-only rootfs, seccomp profile의 공통 목표

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 시스템콜·MAC·프로파일을 구분해 컨테이너 탈출 통제 관점으로 작성한다.
> 핵심: 도구명 나열이 아니라 공격면, 적용 위치, 검증 지표를 연결해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Seccomp·AppArmor·SELinux는 컨테이너 프로세스의 커널 호출, 파일 접근, 권한 행위를 제한하는 리눅스 강제 접근 통제 조합이다.
> 2. **가치**: 컨테이너 탈출 경로를 시스템콜 300개 이상 전체 허용에서 업무 필요 호출 중심으로 축소하고, capability·파일 접근을 정책으로 통제한다.
> 3. **판단 포인트**: Seccomp는 커널 진입, AppArmor는 경로 기반 프로파일, SELinux는 라벨 기반 MAC으로 적용 위치가 다름.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 컨테이너 보안 격리의 계층 이해 확인 | 시스템콜, capability, MAC, profile, label | 세 기술을 방화벽·취약점 스캐너로 설명 |
| 리눅스 커널 통제와 Kubernetes 설정 연결 확인 | `RuntimeDefault`, `allowPrivilegeEscalation:false`, `capabilities.drop` | seccomp만 적용하면 컨테이너 탈출이 0건이라고 단정 |
| 운영 검증 역량 확인 | audit log, denied syscall, policy violation, privileged pod 비율 | 정책 적용 후 오탐·예외 승인 절차 누락 |

> 요약: 이 문제는 컨테이너가 공유 커널을 사용한다는 전제를 두고, 시스템콜·MAC·권한 축소를 함께 설계하는 역량을 확인한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 컨테이너 커널 접근 통제
- 배경: 컨테이너는 호스트 커널을 공유하므로 프로세스 권한·시스템콜·파일 접근 허용 범위가 노드 침해 범위를 결정함.
- 필요성: Seccomp·AppArmor·SELinux 정책을 OCI Runtime과 Kubernetes SecurityContext에 적용해 허용 syscall과 파일 접근을 감사해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Container Process -> Linux Kernel
  / Seccomp: syscall allowlist
  / AppArmor: path based profile
  / SELinux: label based MAC
Runtime Policy -> Audit Log -> Exception Review
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Seccomp | `clone`, `mount`, `bpf` 등 시스템콜 허용·차단 | BPF 필터 기반, Docker·CRI 런타임 기본 프로파일 적용 |
| AppArmor | 프로세스별 파일·네트워크·capability 사용 제한 | 경로 기반 프로파일, Ubuntu 계열에서 사용 빈도 높음 |
| SELinux | 주체·객체 라벨과 타입 정책으로 접근 판정 | 라벨 기반 MAC, RHEL·OpenShift에서 기본 축 |
| Capability Drop | root 권한을 세분화해 불필요 기능 제거 | `NET_ADMIN`, `SYS_ADMIN` 제거가 기본 기준 |

> 요약: Seccomp는 커널 호출, AppArmor는 프로파일, SELinux는 라벨 정책으로 서로 다른 계층의 컨테이너 행위를 제한한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Pod Spec 작성 -> SecurityContext 지정 -> Runtime 정책 로드
-> Process 실행 -> Syscall/File/Capability 요청
-> Seccomp/AppArmor/SELinux 판정 -> 허용 또는 차단 로그
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Pod·컨테이너 보안 설정 정의 | `seccompProfile: RuntimeDefault`, privileged 0건 |
| 2 | 컨테이너 런타임이 프로파일 로드 | containerd·CRI-O 정책 로드 로그 |
| 3 | 프로세스 요청을 커널 보안 모듈이 판정 | denied syscall, AVC deny 로그 수집 |
| 4 | 예외 요청을 승인·정책 반영 | 예외 티켓, 만료일, 재검토 주기 30일 |

> 요약: 정책은 배포 시점에 주입되고 실행 시점에 커널이 판정하며, 차단 로그를 통해 예외와 오탐을 관리한다.

---

## Ⅳ. 특징

| 구분 | 기존/미적용 | 본 기술 적용 | 수치·기준 |
|:---|:---|:---|:---|
| 공격면 | 전체 시스템콜·capability 노출 | 업무 필요 시스템콜·capability만 허용 | privileged pod 0건, `SYS_ADMIN` 0건 |
| 통제 방식 | 애플리케이션 신뢰 전제 | 커널 LSM·seccomp로 강제 판정 | auditd, AVC, Kubernetes audit |
| 운영 부담 | 초기 설정 단순 | 프로파일 예외 관리 필요 | deny 로그 일 1회 검토, 예외 만료 30일 |
| 한계 | 탈출 취약점 영향 큼 | 커널 취약점 자체 패치는 별도 필요 | CVE 패치 SLA 7일 이내 |

> 요약: 본 기술은 실행 후 탐지가 아니라 커널 진입과 객체 접근을 사전에 제한하되, 예외 관리와 커널 패치를 병행해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | VM 격리 | 컨테이너 커널 공유 + LSM 정책 | 경량 배포 필요, 커널 공유 위험 수용 시 |
| 비용/성능 | 전체 VM 이미지 | 프로파일·라벨 정책 적용 | 시작 시간 초 단위 유지, 정책 운영 인력 확보 |
| 운영/위험 | 런타임 기본값 의존 | Namespace + cgroup + Seccomp/MAC 조합 | 멀티테넌트 노드는 3계층 통제 필수 |

> 요약: 컨테이너 환경은 VM 격리보다 커널 공유 위험이 크므로 런타임 기본값보다 명시 정책 적용 여부가 선택 기준이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 업무 중단 | 필요한 시스템콜 차단 | observe 모드, canary 5%, deny 로그 분석 | 차단 이벤트 1,000 request당 1건 이하 |
| 정책 우회 | privileged·hostPID·hostPath 허용 | Admission Controller, Pod Security Standards restricted | privileged pod 0건, hostPath 승인 건수 |
| 커널 취약점 | 공유 커널 CVE 미패치 | 노드 이미지 교체, live patch, 취약 노드 cordon | critical CVE 패치 7일 SLA |

> 요약: 주요 리스크는 오탐과 우회 설정이며, 배포 전 관찰 모드와 Admission 정책으로 통제해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 정책 적용률 | 운영 Pod 95% 이상 `RuntimeDefault` | Kubernetes audit, OPA Gatekeeper |
| 권한 축소 | `allowPrivilegeEscalation:false`, `capabilities.drop:ALL` | kube-bench, Kyverno report |
| 탐지·감사 | denied syscall·AVC 로그 중앙 수집 | auditd, Falco, SIEM 연계 |

> 요약: 성공 여부는 프로파일 적용률, 권한 축소 설정, 차단 로그 수집률로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. Kubernetes `securityContext`에 `seccompProfile: RuntimeDefault`, `allowPrivilegeEscalation:false`, `readOnlyRootFilesystem:true`를 기본값으로 설정함
2. OPA Gatekeeper·Kyverno로 privileged, hostPID, hostNetwork, hostPath 사용을 배포 전 차단하고 예외 승인 만료일을 30일로 제한함
3. Falco·auditd·SELinux AVC 로그를 SIEM에 연계해 denied syscall, capability 요청, 라벨 위반을 5분 이내 탐지함

**결론 (2줄):**
- 기술사 판단: 단일 테넌트 개발 클러스터는 `RuntimeDefault`부터 적용하고, 공용 운영 노드는 Seccomp+MAC+Admission 3계층을 적용해야 함
- 향후 방향: eBPF 런타임 탐지와 정책형 Admission을 결합해 배포 전 차단과 실행 중 감사 로그를 동일 통제 체계로 묶어야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "컨테이너 보안 통제를 설명하시오" | Seccomp·AppArmor·SELinux 판정 흐름 | 각 기술의 적용 위치와 한계 |
| 요구사항 명시형 | "컨테이너 탈출 방안을 제시하시오", "설계하시오" | Pod SecurityContext·Admission 적용 절차 | privileged 차단, capability drop, 감사 지표 |

> 요약: 설명형은 기술별 통제 위치를 넓게 쓰고, 방안형은 배포 전 차단과 실행 중 감사 지표를 중심으로 목차를 전환한다.
