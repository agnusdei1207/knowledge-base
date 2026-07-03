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
- **개요**: Rootless 컨테이너는 호스트에 root 권한을 전혀 요구하지 않고 **user namespace**로 컨테이너 내부 UID 0(root)을 호스트의 일반 사용자 UID 범위에 매핑해 실행하는 방식이다.
- **왜 필요한가**: 전통적 Docker는 daemon 자체가 root로 동작해, daemon socket 탈취나 컨테이너 탈출 취약점이 곧바로 호스트 root 권한 획득으로 이어질 수 있었다 — 180(컨테이너 보안)의 여러 통제 축 중에서도 "애초에 root가 아니면 탈출해도 얻을 게 없다"는 근본적인 축이다.
- **핵심 직관**: 컨테이너 안에서는 UID 0(사장님처럼) 보이지만, 건물(호스트) 등기부등본에는 평범한 직원으로 등록된 상태다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| User Namespace | 프로세스가 보는 UID/GID와 커널이 실제로 다루는 UID/GID를 분리하는 리눅스 namespace — 이 개념의 핵심 메커니즘 | 사내 직함과 실제 등본상 신분이 다른 것 |
| UID/GID 매핑 | 컨테이너 내부 UID 0~65535를 호스트의 특정 구간(예: 100000~165535)에 1:1 대응시키는 표 | 사내 직급 - 실제 신분증 번호 대응표 |
| /etc/subuid, /etc/subgid | 사용자별로 위임받은 서브 UID/GID 범위를 정의하는 시스템 파일(보통 사용자당 65,536개) | 개인에게 배정된 가짜 사번 발급 대장 |
| RootlessKit | rootless 환경에서 user namespace·네트워크·마운트를 조율하는 도구 | 실행을 대행하는 관리업체 |
| slirp4netns | 커널 권한 없이 사용자 공간에서 네트워크 NAT를 에뮬레이션하는 도구 | 정식 통신 인프라 대신 쓰는 사설 중계기 |
| fuse-overlayfs | 커널 overlay 마운트 권한 없이 FUSE(사용자 공간 파일시스템)로 레이어를 합치는 도구 | 정식 창고 시스템 대신 쓰는 임시 조립 선반 |
| CAP_SYS_ADMIN | 마운트, namespace 조작 등 강력한 권한을 포괄하는 capability — rootless에서는 호스트 레벨로 위임되지 않음 | 마스터키 중 가장 강력한 한 개 |

## 깊이 이해

### root daemon 모델의 구조적 위험 (배경)
- 기존 Docker는 `dockerd`가 root로 상시 실행되고, `docker` CLI는 `/var/run/docker.sock`을 통해 이 daemon에 명령을 보낸다. 이 소켓에 접근할 수 있는 사용자는 사실상 host root와 동등하다 — 컨테이너에 호스트 루트 디렉터리를 마운트하고 `chroot`하면 호스트 파일시스템 전체를 조작할 수 있기 때문이다.
- 즉 "컨테이너 이미지 자체는 안전"해도, daemon socket 접근권한이나 런타임 취약점 하나가 곧장 host root로 직결되는 구조적 약점이 있었다.

### user namespace의 UID 매핑을 수치로 이해
- `/etc/subuid`에 `alice:100000:65536`이라고 적혀 있으면, 사용자 alice에게 호스트 UID 100000번부터 65,536개(100000~165535)가 위임된다.
- alice가 rootless 컨테이너를 실행하면, 컨테이너 내부에서 `id`를 쳤을 때는 `uid=0(root)`로 보이지만, 실제로 호스트 프로세스 테이블에서 `ps aux`로 보면 그 프로세스는 UID 100000으로 돌고 있다. 컨테이너 내부에서 새 파일을 만들면 소유자가 내부에서는 `root:root`, 호스트에서는 `100000:100000`으로 보인다.
- 결과: 컨테이너 안에서 "root 권한으로" 무엇을 해도, 커널이 실제로 검사하는 권한은 host UID 100000 — 즉 일반 사용자 권한이다. 컨테이너를 탈출해도 호스트에서는 평범한 비특권 프로세스일 뿐이다.

### 네트워크·스토리지 보완 계층이 필요한 이유 (구체 예시)
- 일반 컨테이너는 root 권한으로 커널의 네트워크 네임스페이스에 직접 veth를 만들고 브리지에 연결한다(CNI). rootless는 이 커널 조작 권한이 없으므로, slirp4netns가 사용자 공간 TCP/IP 스택으로 NAT를 흉내낸다 — 대가로 처리량이 커널 네이티브 경로보다 떨어질 수 있어, 고성능 네트워크 워크로드는 기준선 대비 처리량·p95 지연을 벤치마크(iperf3 등)로 확인해야 한다.
- 마찬가지로 overlayfs 커널 마운트도 root 권한이 필요해, rootless는 FUSE 기반 fuse-overlayfs로 대체한다. 파일 I/O가 잦은 워크로드는 기준선 대비 지연을 fio 등으로 측정해봐야 한다.
- 1024 미만의 특권 포트(예: 80, 443)도 커널이 root에게만 bind를 허용하므로, rootless 컨테이너는 기본적으로 1024 이상 포트만 열 수 있다 — 앞단에 리버스 프록시를 두거나 `net.ipv4.ip_unprivileged_port_start` 커널 파라미터를 조정해 우회한다.

### rootless가 막는 것과 막지 못하는 것 (판별 원리)
- **막는 것**: daemon socket 탈취가 host root로 직행하는 경로, `--privileged` 류의 명령이 호스트 커널 자원을 직접 건드리는 경로.
- **막지 못하는 것**: 컨테이너 내부 애플리케이션 취약점 자체(컨테이너 안에서는 여전히 UID 0이므로 컨테이너 내부 파일은 자유롭게 건드림), user namespace 관련 커널 자체의 취약점, hostPath로 민감 디렉터리를 마운트하면 매핑된 UID 권한 내에서 여전히 접근 가능.
- **판별 원리**: "이 워크로드가 host 커널 자원(네트워크 device, 커널 모듈, host 포트 등)을 직접 다뤄야 하는가"를 먼저 묻는다. 그렇다면 rootless 예외(제한적 rootful) 대상, 아니면 rootless 기본값.

### 비유와 흔한 오해
- **비유**: 계약직 사원이 사내에서는 "팀장" 직함으로 불려도, 회사 밖 등기부등본이나 은행 거래에서는 원래 신분(평사원)으로만 인정되는 것과 같다 — 사내 호칭(컨테이너 내부 root)이 외부 실권(호스트 권한)을 만들어주지 않는다.
- **오해 1**: "rootless면 완전히 안전하다" — 틀렸다. 180에서 다룬 seccomp, AppArmor, capability drop, admission 통제와 별개 축이며 이들을 대체하지 않는다. rootless는 "권한 상승의 최종 도착지"를 없애는 것이지, 컨테이너 내부 취약점 자체를 막지 않는다.
- **오해 2**: "rootless는 성능이 항상 동일하다" — 네트워크(slirp4netns)와 스토리지(fuse-overlayfs)는 사용자 공간 에뮬레이션이라 커널 네이티브 대비 오버헤드가 있을 수 있어, 고처리량 워크로드는 반드시 벤치마크로 검증해야 한다.

## 연결 개념
- 컨테이너 보안 (180) - seccomp·AppArmor·capability drop 등 다른 통제 축과 결합해 다층 방어를 구성
- User Namespace - 리눅스 namespace 중 rootless의 핵심 메커니즘
- Pod Security Standards - `runAsNonRoot: true` 등 restricted 등급이 요구하는 권한 최소화 기준

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

- 개요: root 권한 없는 컨테이너 실행 모델
- 배경: 기존 root daemon 방식은 socket 노출과 런타임 취약점이 호스트 권한 침해로 확대될 수 있다.
- 필요성: user namespace로 컨테이너 내부 UID 0을 호스트 일반 UID에 매핑해 권한 상승 범위를 제한한다.

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
