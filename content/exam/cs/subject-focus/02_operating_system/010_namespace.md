---
title: "네임스페이스 (Namespace)"
date: "2026-06-30"
weight: 10
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 네임스페이스(Namespace)는 Linux 커널이 제공하는 격리 기능으로, 프로세스 그룹마다 시스템 자원(PID·네트워크·파일시스템 등)에 대한 독립된 뷰(View)를 부여하여 컨테이너의 격리를 실현한다.

## Ⅱ. 구성요소 / 원리
- **PID Namespace**: 프로세스 ID 공간 격리, 컨테이너 내 PID 1부터 부여
- **NET Namespace**: 네트워크 인터페이스·IP·라우팅·포트 격리
- **MNT(Mount) Namespace**: 마운트 포인트·파일시스템 트리 격리
- **UTS Namespace**: 호스트명(Hostname)·도메인명 격리
- **IPC Namespace**: 프로세스 간 통신(공유 메모리·세마포어) 격리
- **USER Namespace**: 사용자·그룹 ID 매핑 격리(컨테이너 root↔호스트 비특권)

## Ⅲ. 흐름도 / 구조
```text
         Host Kernel (단일 커널)
 ┌──────────────┬──────────────┐
 │ Container A  │ Container B   │
 │ PID ns(1..)  │ PID ns(1..)   │
 │ NET ns(eth0) │ NET ns(eth0)  │
 │ MNT/UTS/IPC  │ MNT/UTS/IPC   │
 │ USER ns      │ USER ns       │
 └──────────────┴──────────────┘
   (각자 독립된 자원 뷰로 격리)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 커널 공유 환경에서 프로세스별 자원 뷰를 격리(가시성 분리) |
| 장점 | 경량 격리, 컨테이너 독립성 확보, 자원 충돌 방지 |
| 한계 | 가시성 격리일 뿐 커널 공유, cgroups 없이는 자원 제한 불가 |

## Ⅴ. 기술사적 적용
- cgroups(자원 제한)와 결합하여 컨테이너 격리의 양대 축 구성
- USER Namespace로 컨테이너 권한 상승 공격 표면 축소(보안 강화)
- Docker·Kubernetes Pod의 네트워크·프로세스 격리 기반 기술
