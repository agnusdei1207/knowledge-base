---
title: "Rootless 컨테이너 (Rootless Container)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 181
---

# 📖 【암기용】 개념 완전 이해

> 목적: Rootless 컨테이너를 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 호스트 root 권한 없이 사용자 네임스페이스로 컨테이너를 실행하는 방식
- **왜 필요한가**: 컨테이너 탈출이나 런타임 취약점이 발생해도 호스트 root 권한 획득으로 이어지는 경로를 줄인다.
- **핵심 직관**: 건물 관리자 열쇠 없이 자기 방 안에서만 도구를 쓰게 만드는 컨테이너 실행 방식이다.

## 깊이 이해
- **배경·문제의식**: 전통적 Docker daemon은 root 권한으로 동작해 daemon socket 노출, privileged 실행, 런타임 취약점이 호스트 전체 권한 문제로 확대될 수 있다.
- **작동 원리**: user namespace가 컨테이너 내부 UID 0을 호스트 일반 UID 범위에 매핑하고, RootlessKit·slirp4netns·fuse-overlayfs가 네트워크와 스토리지 제약을 보완한다.
- **비유**: 컨테이너 내부에서는 사장처럼 보이지만 건물 밖 계약서에는 일반 직원으로 등록된 상태이다.
- **구체 예시**: 개발자 노트북에서 rootless Docker를 사용하면 `/var/run/docker.sock` root 접근 없이 이미지 빌드와 Pod 실행을 수행하고, `CAP_SYS_ADMIN` 의존 작업은 차단된다.
- **흔한 오해·주의점**: rootless는 모든 권한 문제를 제거하지 않는다. hostPath, setuid binary, 커널 취약점, 네트워크 포트 1024 미만 제약을 별도로 검토해야 한다.

## 연결 개념
- User Namespace - 컨테이너 UID와 호스트 UID를 분리하는 기반
- 컨테이너 보안 - seccomp, AppArmor, capability drop과 결합
- Pod Security Standards - runAsNonRoot, restricted profile 적용 기준

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Rootless 답안은 "root 미사용" 설명에서 끝내지 않고 UID 매핑, 권한 제한, 운영 제약, 검증 지표를 연결해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Rootless Container는 호스트 root 권한 없이 user namespace로 컨테이너 내부 root를 일반 사용자 UID에 매핑하는 실행 모델임.
> 2. **가치**: daemon socket 탈취, 런타임 취약점, privileged 오남용이 호스트 root 권한 획득으로 이어지는 경로를 줄임.
> 3. **판단 포인트**: user namespace 적용률, privileged 0건, capability drop, 1024 미만 포트·overlay·CNI 제약을 함께 판단해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 컨테이너 권한 모델 이해 확인 | user namespace, UID/GID mapping, rootless runtime | "root로 실행하지 않음"만 서술 |
| 보안 통제와 한계 판단 확인 | capability, seccomp, privileged 차단, 커널 공유 | rootless를 완전 격리로 단정 |
| 운영 적용 역량 확인 | 네트워크, 스토리지, 포트, CI/CD 적용 조건 | 제약과 검증 지표 누락 |

> 요약: 이 문제는 root 권한 제거 효과와 운영 제약을 같은 답안 안에서 균형 있게 제시해야 함.

---

## Ⅰ. 개요 및 필요성

Rootless 컨테이너는 무root 실행 모델임. 기존 root daemon 방식은 socket 노출과 런타임 취약점이 호스트 권한 침해로 확대될 수 있다. user namespace 기반 실행은 컨테이너 내부 UID 0을 호스트 일반 UID로 매핑해 권한 상승 범위를 제한한다.

---

## Ⅱ. 구조 및 구성요소

```text
User Process -> Rootless Runtime -> User Namespace -> Container Process
  / Network: slirp4netns
  / Storage: fuse-overlayfs
  / Control: seccomp/capability
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| User Namespace | 내부 root와 호스트 일반 UID 매핑 | `/etc/subuid`, `/etc/subgid` 필요 |
| Rootless Runtime | root daemon 없이 containerd, Docker, Podman 실행 | systemd user service 사용 |
| slirp4netns | 사용자 공간 네트워크 제공 | 처리량과 지연 측정 필요 |
| fuse-overlayfs | root 권한 없는 overlay filesystem | 파일 I/O 기준선 비교 필요 |

> 요약: Rootless 구조는 UID 매핑을 중심으로 네트워크와 스토리지 보완 계층을 붙여 root 권한 없이 컨테이너를 실행함.

---

## Ⅲ. 동작원리 및 흐름도

```text
사용자 요청 -> UID/GID range 확인 -> user namespace 생성 -> runtime 실행 -> container process 격리 -> audit 수집
  / 권한 필요 syscall -> seccomp/capability 기준 차단
  / privileged 요구 -> 정책 거부
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | `/etc/subuid`, `/etc/subgid`로 UID 범위 확인 | 사용자당 65,536 UID range |
| 2 | user namespace 생성 후 내부 UID 0 매핑 | host UID가 일반 사용자 |
| 3 | rootless runtime이 컨테이너 실행 | root daemon socket 미사용 |
| 4 | 네트워크와 스토리지 보완 계층 연결 | slirp4netns, fuse-overlayfs |
| 5 | 로그와 정책 위반 수집 | privileged 0건, deny event 추적 |

> 요약: Rootless는 UID 매핑 후 일반 사용자 권한으로 runtime을 실행하고, 필요한 권한은 정책과 커널 격리로 제한함.

---

## Ⅳ. 특징

| 구분 | Rootful 컨테이너 | Rootless 컨테이너 | 수치/판단 포인트 |
|:---|:---|:---|:---|
| 권한 | daemon root 실행 | 사용자 권한 실행 | root daemon socket 0개 |
| 격리 | namespace + capability | user namespace 추가 | host UID 일반 사용자 |
| 네트워크 | CNI, host port 자유 | slirp4netns 제약 | 1024 미만 포트 별도 처리 |
| 스토리지 | overlayfs 직접 사용 | fuse-overlayfs 사용 | I/O 지연 벤치마크 |

> 요약: Rootless는 권한 경계를 줄이는 대신 네트워크, 스토리지, 포트 사용 제약을 설계 조건에 포함해야 함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | root daemon | rootless runtime | 개발자 워크스테이션, 다중 사용자 서버 |
| 비용/처리 | CNI 직접 경로 | 사용자 공간 네트워크 | p95 지연 기준선 대비 20% 이내 |
| 운영/위험 | socket 탈취 시 root 권한 | host UID 일반 사용자 | Docker socket 노출 환경 |

> 요약: Rootless는 개발·CI·다중 사용자 환경에 우선 적용하고, 고처리 네트워크 워크로드는 기준선 측정 후 선택함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 권한 부족 실패 | privileged, CAP_SYS_ADMIN 의존 | workload 권한 목록화, capability drop | 실행 실패율, deny event |
| 네트워크 지연 | 사용자 공간 패킷 처리 | p95 지연 벤치마크, CNI 대안 검토 | p95 latency, throughput |
| 정책 우회 | rootful fallback 허용 | admission 정책, CI 검사 | rootful Pod 0건 |

> 요약: 운영 리스크는 권한 요구, 네트워크 경로, rootful 예외를 지표로 추적해야 함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 권한 | privileged 0건, root daemon socket 0건 | kube audit, host scan |
| 격리 | user namespace 적용률 100% | runtime inspect |
| 처리 | 기준선 대비 p95 지연 20% 이내 | k6, iperf3, fio |

> 요약: 도입 후 권한 제거와 처리 지연을 동시에 측정해야 운영 판단이 가능함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 개발·CI 환경부터 rootless Docker 또는 Podman 적용, `/etc/subuid`와 `/etc/subgid`에 사용자당 65,536 범위 할당
2. Kubernetes는 `runAsNonRoot: true`, `allowPrivilegeEscalation: false`, `capabilities.drop: ALL`을 admission 정책으로 강제
3. p95 지연, 파일 I/O, 포트 사용을 rootful 기준선과 비교하고 예외 workload는 만료일 있는 승인 절차 적용

**결론 (2줄):**
- 기술사 판단: 다중 사용자·개발·CI 환경은 Rootless를 기본값으로 두고, 커널 기능 의존 workload는 rootful 예외를 제한적으로 허용함
- 향후 방향: Rootless runtime, user namespace, eBPF runtime detection이 컨테이너 권한 최소화 기준으로 결합됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Rootless 컨테이너를 설명하시오", "기술하시오" | user namespace와 runtime 실행 흐름 | rootful 대비 권한·네트워크·스토리지 차이 |
| 요구사항 명시형 | "보안 방안을 제시하시오", "비교하시오", "설계하시오" | UID 매핑, capability, admission 통제 | 적용 조건, 예외 기준, 검증 지표 |

> 요약: 설명형은 권한 모델, 보안형은 root 권한 제거와 운영 제약의 균형 판단으로 전환함.
