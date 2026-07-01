---
title: "네임스페이스·cgroup 격리 (Namespace Cgroup Isolation)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 127
---

# 📖 【암기용】 개념 완전 이해

> 목적: 네임스페이스와 cgroup 격리를 처음 봐도 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 네임스페이스는 보이는 세계를 나누고, cgroup은 쓸 수 있는 자원량을 제한하는 리눅스 커널 격리 기능이다.
- **왜 필요한가**: 컨테이너는 프로세스를 빠르게 실행하지만 서로의 PID, 네트워크, 파일시스템, CPU, 메모리를 침범하면 서비스 장애와 권한 상승이 발생한다.
- **핵심 직관**: 네임스페이스는 방 배정표, cgroup은 전기·수도 사용량 계량기임.

## 깊이 이해
- **배경·문제의식**: 컨테이너는 하나의 커널 위에서 여러 애플리케이션을 실행한다. 커널 객체를 그대로 공유하면 한 프로세스가 다른 프로세스를 보거나 자원을 고갈시킬 수 있다.
- **작동 원리**: PID, Mount, Network, IPC, UTS, User, Cgroup namespace가 가시성을 나누고, cgroup v2가 CPU, memory, io, pids 사용량을 계층적으로 제한한다.
- **비유**: 같은 건물에 입주한 회사들이 사무실·전화망·출입명부를 따로 쓰고, 전력 계약 용량을 따로 두는 것과 같다.
- **구체 예시**: Kubernetes Pod는 동일 Pod 내 컨테이너가 Network namespace를 공유해 `localhost` 통신을 사용하고, 컨테이너별 memory limit 초과 시 OOMKill이 발생한다.
- **흔한 오해·주의점**: 네임스페이스와 cgroup만으로 보안이 끝나지 않는다. capability, seccomp, AppArmor/SELinux, 이미지 서명까지 함께 적용해야 한다.

## 연결 개념
- Seccomp·AppArmor·SELinux: namespace·cgroup 위에서 커널 접근과 객체 접근을 추가 통제
- Rootless 컨테이너: User namespace를 활용해 컨테이너 root를 호스트 비root UID에 매핑
- Kubernetes ResourceQuota·LimitRange: cgroup 제한을 네임스페이스 단위 정책으로 관리

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 가시성 격리와 자원 격리를 분리해 컨테이너 보안·운영 답안으로 구성한다.
> 핵심: 네임스페이스는 "무엇을 볼 수 있는가", cgroup은 "얼마나 쓸 수 있는가"를 통제한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Namespace·cgroup 격리는 리눅스 커널 객체의 가시성과 CPU·메모리·I/O 사용량을 분리하는 컨테이너 실행 기반이다.
> 2. **가치**: PID·Network·Mount 격리와 memory·cpu·pids 제한으로 프로세스 침범, 포트 충돌, 자원 고갈을 제어한다.
> 3. **판단 포인트**: 보안 격리는 namespace, 자원 품질은 cgroup, 권한 통제는 capability·LSM으로 나누어 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 컨테이너 커널 격리 원리 확인 | PID, Mount, Network, User namespace와 cgroup v2 | Docker 명령어 사용법만 설명 |
| 보안과 자원 통제 구분 확인 | 가시성 격리 vs 사용량 제한 | namespace를 CPU 제한 기술로 오기 |
| Kubernetes 운영 적용 판단 확인 | request, limit, ResourceQuota, OOMKill | limit 미설정으로 노드 자원 고갈 위험 누락 |

> 요약: 이 문제는 컨테이너 격리를 VM과 비교하기보다 커널 가시성 분리와 자원 제한의 역할 차이를 묻는다.

---

## Ⅰ. 개요 및 필요성

컨테이너 커널 격리의 기본 단위이다. 네임스페이스는 프로세스가 보는 PID·네트워크·마운트 공간을 나누고, cgroup은 CPU·메모리·I/O 사용량을 제한한다. 멀티테넌트 클러스터에서는 격리 누락이 정보 노출, 서비스 중단, 노드 자원 고갈로 이어진다.

---

## Ⅱ. 구조 및 구성요소

```text
Container Runtime -> Namespace Set
  / PID / Mount / Network / IPC / UTS / User
Container Runtime -> cgroup v2
  / cpu / memory / io / pids
Policy -> Metrics -> Quota Review
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| PID Namespace | 컨테이너 내부 프로세스 번호 공간 분리 | hostPID 사용 시 호스트 프로세스 노출 |
| Network Namespace | 인터페이스, 라우팅, 포트 공간 분리 | Pod 단위 공유, CNI와 연동 |
| Mount Namespace | 파일시스템 마운트 뷰 분리 | hostPath 허용 시 노드 파일 접근 위험 |
| cgroup v2 | CPU·memory·io·pids 제한 | 계층형 자원 통제, OOMKill 기준 제공 |

> 요약: 네임스페이스는 커널 객체의 보이는 범위를 나누고, cgroup은 컨테이너별 자원 사용량을 수치로 제한한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
컨테이너 생성 요청 -> Runtime clone/unshare 호출
-> Namespace 생성·조인 -> cgroup 계층 배치
-> 프로세스 실행 -> 자원 사용 측정
-> limit 초과 시 throttle 또는 OOMKill
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 런타임이 OCI spec의 namespace·resource 설정 읽기 | `config.json`, PodSpec securityContext |
| 2 | `clone`, `unshare`, `setns`로 namespace 구성 | `/proc/<pid>/ns/*` 링크 확인 |
| 3 | 프로세스를 cgroup 계층에 배치 | `/sys/fs/cgroup` cpu.max, memory.max |
| 4 | CPU throttle, memory OOM, pids 제한 적용 | throttling ratio, OOMKill count |

> 요약: 런타임은 프로세스를 별도 namespace와 cgroup 계층에 넣고, 커널은 실행 중 가시성과 자원 사용량을 계속 판정한다.

---

## Ⅳ. 특징

| 구분 | 기존/미적용 | 본 기술 적용 | 수치·기준 |
|:---|:---|:---|:---|
| 프로세스 가시성 | 호스트 PID 전체 노출 | PID namespace로 내부 PID 1부터 표시 | hostPID 허용 0건 |
| 네트워크 | 포트·라우팅 충돌 | Network namespace와 CNI로 분리 | Pod CIDR, NetworkPolicy 적용률 95% |
| 자원 사용 | 무제한 CPU·메모리 점유 | cgroup limit·request 적용 | memory limit 100%, CPU throttling 10% 이하 |
| 한계 | 설정 단순 | 커널 공유 취약점은 잔존 | 커널 CVE 패치 SLA 7일 |

> 요약: namespace·cgroup은 컨테이너 실행의 기본 격리이지만, 권한 축소와 커널 패치 없이는 탈출 위험을 제거할 수 없다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | VM 하이퍼바이저 격리 | 커널 namespace·cgroup 격리 | 경량 배포와 초 단위 시작이 필요할 때 |
| 비용/성능 | 게스트 OS별 메모리 점유 | 커널 공유, 프로세스 단위 실행 | 노드 집적도와 보안 요구를 함께 판단 |
| 운영/위험 | VM 단위 자원 예약 | request·limit·quota 정책 | 멀티테넌트는 quota와 제한 기본값 필요 |

> 요약: 컨테이너 격리는 VM보다 가볍지만 커널 공유 전제를 가지므로 자원 제한과 보안 정책을 별도 설계해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 자원 고갈 | limit 미설정, memory leak | LimitRange, ResourceQuota, VPA 권고 | limit 미설정 Pod 0건, OOMKill 월 추세 |
| 호스트 노출 | hostPID, hostNetwork, hostPath 허용 | Admission 정책, 예외 승인 30일 | host namespace 사용 승인 건수 |
| 권한 상승 | User namespace 미사용, capability 과다 | rootless, capability drop, seccomp | `SYS_ADMIN` 보유 컨테이너 0건 |

> 요약: 운영 리스크는 제한 미설정과 호스트 namespace 사용에서 발생하므로 Admission과 quota를 기본 통제로 둔다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 자원 정책 | request·limit 설정률 100% | kube-state-metrics, Policy report |
| 격리 설정 | hostPID·hostNetwork·hostPath 0건 | Kubernetes audit, OPA Gatekeeper |
| 운영 품질 | OOMKill 반복 Pod 0건, CPU throttling 10% 이하 | Prometheus, cAdvisor |

> 요약: 적용 효과는 설정률이 아니라 OOMKill, throttling, host namespace 예외 건수로 검증해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 모든 namespace에 LimitRange와 ResourceQuota를 배치해 CPU·memory request/limit 누락 Pod를 배포 전 차단함
2. Pod Security Standards restricted와 OPA Gatekeeper로 hostPID, hostNetwork, privileged, hostPath 예외를 승인제 30일 만료로 관리함
3. Prometheus·cAdvisor로 OOMKill, CPU throttling, pids usage를 수집하고 반복 OOM Pod는 배포 롤백 또는 memory limit 재산정함

**결론 (2줄):**
- 기술사 판단: 단일 업무 컨테이너는 기본 namespace·cgroup으로 충분하나, 공용 클러스터는 quota·Admission·LSM을 함께 적용해야 함
- 향후 방향: cgroup v2 통합 계층과 eBPF 관측을 결합해 자원 제한, 보안 이벤트, 비용 태깅을 동일 지표 체계로 관리해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "컨테이너 격리를 설명하시오" | namespace 생성과 cgroup 제한 흐름 | VM 격리와 컨테이너 격리 차이 |
| 요구사항 명시형 | "멀티테넌트 격리 방안을 제시하시오" | ResourceQuota·Admission 적용 절차 | host namespace 차단, limit 설정, 운영 지표 |

> 요약: 설명형은 커널 원리, 방안형은 Kubernetes 정책과 자원 지표를 중심으로 답안을 재구성한다.
