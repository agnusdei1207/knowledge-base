---
title: "Rootless 컨테이너 보안 (Rootless Container Security)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 128
---

# 📖 【암기용】 개념 완전 이해

> 목적: Rootless 컨테이너 보안을 처음 봐도 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: Rootless 컨테이너는 컨테이너 런타임과 컨테이너 프로세스를 호스트 root가 아닌 일반 사용자 권한으로 실행하는 방식이다.
- **왜 필요한가**: 일반 컨테이너의 root는 namespace 안의 root이지만 런타임·데몬 취약점이 있으면 호스트 root 권한으로 이어질 수 있다.
- **핵심 직관**: 컨테이너 안에서는 관리자로 보이게 하되, 건물 전체 열쇠가 아니라 임대 사무실 열쇠만 주는 방식임.

## 깊이 이해
- **배경·문제의식**: Docker 데몬은 전통적으로 root 권한으로 동작했다. 데몬 소켓 접근 권한을 얻으면 이미지 실행, 볼륨 마운트, 호스트 파일 접근으로 권한 상승이 가능하다.
- **작동 원리**: User namespace가 컨테이너 UID 0을 호스트의 비특권 UID 범위에 매핑한다. Rootless Docker, Podman, containerd rootless는 네트워크·스토리지·cgroup 제약을 사용자 공간 기능으로 처리한다.
- **비유**: 호텔 투숙객에게 객실 안에서는 모든 조명을 조작할 수 있게 하지만, 전기실·기계실 출입 권한은 주지 않는 구조이다.
- **구체 예시**: 컨테이너 내부 UID 0이 호스트 UID 100000~165535 범위로 매핑되면, 컨테이너 탈출 시에도 `/etc/shadow` 같은 root 소유 파일 쓰기가 차단된다.
- **흔한 오해·주의점**: Rootless는 만능 격리가 아니다. 낮은 포트 바인딩, overlayfs, cgroup delegation, host network 사용에 제약이 있고 커널 취약점 패치는 별도이다.

## 연결 개념
- User Namespace: 컨테이너 root와 호스트 UID를 분리하는 핵심 기능
- Seccomp·AppArmor·SELinux: rootless 위에 추가하는 시스템콜·MAC 통제
- 공급망 보안: rootless 빌드로 CI 빌더의 호스트 권한 상승 경로를 축소

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. rootful과 rootless 차이를 권한 상승, 운영 제약, 적용 기준으로 정리한다.
> 핵심: Rootless는 컨테이너 보안 도구가 아니라 호스트 root 권한 의존을 제거하는 실행 모델이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Rootless Container Security는 컨테이너 런타임·프로세스를 비root 사용자로 실행해 컨테이너 탈출 시 호스트 root 권한 획득 가능성을 낮추는 방식이다.
> 2. **가치**: Docker socket, privileged daemon, root-owned runtime의 권한 상승 경로를 줄이고 CI/CD 빌드 노드의 blast radius를 제한한다.
> 3. **판단 포인트**: User namespace 매핑, cgroup v2 delegation, rootless networking, storage driver 제약을 함께 평가해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 컨테이너 권한 상승 경로 이해 확인 | rootful daemon, Docker socket, UID mapping | 컨테이너 내부 root와 호스트 root를 동일시 |
| rootless 적용 한계 판단 확인 | low port, host network, overlayfs, cgroup delegation | rootless만 적용하면 모든 탈출 취약점 차단이라고 단정 |
| 실무 적용 방안 확인 | Podman, Rootless Docker, BuildKit, Kubernetes userns | 운영 제약과 예외 기준 누락 |

> 요약: 이 문제는 root 권한 제거의 의미와 rootless 전환 시 네트워크·스토리지·자원 제약을 함께 판단하는지를 본다.

---

## Ⅰ. 개요 및 필요성

Rootless는 비root 컨테이너 실행 모델이다. 컨테이너 플랫폼의 권한 상승 사고는 런타임·데몬·소켓 권한에서 시작되는 경우가 많다. Rootless는 사용자 네임스페이스로 컨테이너 root를 호스트 일반 UID에 매핑해 탈출 시 피해 범위를 제한한다.

---

## Ⅱ. 구조 및 구성요소

```text
User Login -> Rootless Runtime
  / User Namespace: UID 0 -> host subuid
  / Rootless Network: slirp4netns / pasta
  / Rootless Storage: fuse-overlayfs
Container Process -> Non-root Host UID -> Audit
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| User Namespace | 컨테이너 UID 0을 호스트 비root UID로 매핑 | `/etc/subuid`, `/etc/subgid` 범위 필요 |
| Rootless Runtime | 데몬·런타임을 사용자 권한으로 실행 | Podman, Rootless Docker, BuildKit |
| Rootless Network | 사용자 공간 네트워크 제공 | slirp4netns, pasta, 낮은 포트 바인딩 제약 |
| Rootless Storage | 비root 파일시스템 레이어 처리 | fuse-overlayfs, overlayfs 커널 지원 확인 |

> 요약: Rootless는 User namespace를 중심으로 네트워크와 스토리지를 사용자 권한에서 처리해 호스트 root 의존을 줄인다.

---

## Ⅲ. 동작원리 및 흐름도

```text
사용자 실행 -> subuid/subgid 확인 -> User namespace 생성
-> Runtime 비root 실행 -> Container UID 매핑
-> Network/Storage 사용자 공간 처리 -> 로그·정책 점검
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 사용자별 subuid·subgid 범위 할당 | `/etc/subuid` 65,536개 이상 범위 |
| 2 | rootless runtime 설치·실행 | Docker rootless, Podman rootless 상태 |
| 3 | 컨테이너 UID 0을 호스트 비root UID로 매핑 | `/proc/<pid>/uid_map` 확인 |
| 4 | 네트워크·스토리지·cgroup 제약 검증 | 포트, throughput, cgroup v2 delegation |

> 요약: Rootless는 실행 전 UID 매핑을 준비하고, 실행 중 컨테이너 root 권한을 호스트 비root 권한으로 제한한다.

---

## Ⅳ. 특징

| 구분 | Rootful 컨테이너 | Rootless 컨테이너 | 수치·기준 |
|:---|:---|:---|:---|
| 권한 모델 | 데몬·프로세스가 호스트 root 의존 | 일반 사용자 권한으로 런타임 실행 | root-owned daemon 0건 |
| 탈출 영향 | 런타임 취약점이 root 권한으로 확산 가능 | host subuid 범위로 피해 제한 | UID mapping 확인 100% |
| 운영 제약 | host network·privileged 사용 용이 | low port, cgroup, storage 제약 | 예외 승인 건수 월 0~3건 |
| 적용 대상 | 특권 워크로드 | 개발·CI 빌드·일반 서비스 | 빌더 rootless 비율 95% |

> 요약: Rootless는 권한 상승 경로를 줄이는 대신 네트워크·스토리지·cgroup 제약을 운영 기준으로 관리해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | rootful Docker daemon | rootless Podman·Docker·BuildKit | 개발자 PC, CI 빌더, SaaS 일반 워크로드 |
| 비용/성능 | 커널 네트워크·overlayfs 직접 사용 | 사용자 공간 네트워크·fuse 계층 | 네트워크 처리량 요구와 보안 요구 비교 |
| 운영/위험 | Docker socket 접근 시 root 상당 권한 | socket 영향 범위 사용자 계정으로 제한 | 공유 빌드 노드는 rootless 우선 |

> 요약: Rootless는 특권 기능이 필요 없는 빌드·일반 서비스에서 우선 적용하고, 고성능 네트워크 워크로드는 예외 기준을 둔다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 기능 미지원 | low port, host network, cgroup 제약 | reverse proxy, cgroup v2, 예외 승인 | rootless 실패 배포 건수 |
| 운영 혼선 | rootful·rootless 이미지 경로 차이 | 표준 베이스 이미지, CI 템플릿 분리 | 표준 파이프라인 적용률 95% |
| 권한 우회 | Docker socket 마운트, privileged 허용 | Admission 차단, socket mount 금지 | `/var/run/docker.sock` 마운트 0건 |

> 요약: Rootless 전환 실패는 기능 제약과 소켓 마운트 예외에서 발생하므로 표준 파이프라인과 배포 전 정책 차단이 필요하다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 권한 상태 | rootless runtime 적용률 90% 이상 | runtime inventory, `docker info` |
| UID 매핑 | 모든 rootless 컨테이너 uid_map 확인 | `/proc/*/uid_map`, audit script |
| 예외 관리 | rootful 예외 30일 만료 | CMDB, 승인 티켓, Kubernetes audit |

> 요약: 적용 효과는 rootless 실행 비율, UID 매핑 검증, rootful 예외 만료율로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. CI 빌더를 Rootless BuildKit 또는 Podman으로 전환하고 `/var/run/docker.sock` 마운트를 0건으로 통제함
2. `/etc/subuid`, `/etc/subgid`에 사용자별 65,536개 이상 범위를 배정하고 uid_map 검증을 배포 파이프라인에 추가함
3. Kubernetes는 rootless runtime class 또는 user namespace 지원 노드풀을 분리하고, 특권 워크로드는 별도 taint·label로 격리함

**결론 (2줄):**
- 기술사 판단: CI·개발·일반 서비스는 rootless를 기본값으로 두고, host network·커널 장치 접근 워크로드만 rootful 예외로 분리해야 함
- 향후 방향: User namespace, cgroup v2, eBPF 감사 로그를 결합해 rootless 전환률과 예외 권한을 정책 코드로 관리해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Rootless 컨테이너를 설명하시오" | UID 매핑과 runtime 실행 흐름 | rootful과 rootless 차이 |
| 요구사항 명시형 | "CI 컨테이너 보안 방안을 제시하시오" | BuildKit·Podman 전환 절차 | Docker socket 차단, 예외 승인, 검증 지표 |

> 요약: 설명형은 User namespace 원리, 방안형은 빌드 노드 권한 상승 차단과 운영 예외 관리에 초점을 둔다.
