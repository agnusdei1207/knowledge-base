---
title: "cgroups (Control Groups)"
date: "2026-06-30"
weight: 11
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> cgroups(Control Groups)는 Linux 커널이 제공하는 자원 관리 기능으로, 프로세스 그룹 단위로 CPU·메모리·I/O 등의 자원 사용을 제한(Limit)·할당(Allocation)·계량(Accounting)·격리하는 메커니즘이다.

## Ⅱ. 구성요소 / 원리
- **계층 구조(Hierarchy)**: 트리 형태로 그룹을 구성하여 자원 정책 상속
- **서브시스템(Controller)**: cpu, memory, blkio, pids 등 자원별 제어기
- **자원 제한(Limit)**: 그룹별 상한 설정으로 자원 독점 방지
- **계량(Accounting)**: 그룹별 사용량 측정·과금 기반 제공
- **제어(Throttling/OOM)**: 한도 초과 시 스로틀링 또는 OOM(Out Of Memory) Kill

## Ⅲ. 흐름도 / 구조
```text
        cgroup root hierarchy
              │
   ┌──────────┴──────────┐
 [그룹 A]              [그룹 B]
 cpu=20%               cpu=50%
 mem=512MB             mem=2GB
 io=낮음               io=높음
   │                     │
 프로세스들            프로세스들
 (한도 내 제한·계량)  (한도 내 제한·계량)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 프로세스 그룹의 자원 사용을 제한·계량하여 공정·안정성 확보 |
| 장점 | 자원 독점·고갈 방지, QoS 보장, 사용량 모니터링·과금 |
| 한계 | 가시성 격리는 불가(네임스페이스 필요), 설정 복잡성 |

## Ⅴ. 기술사적 적용
- 네임스페이스(가시성 격리)와 결합하여 컨테이너 격리 완성
- Kubernetes의 Pod requests/limits가 cgroups로 구현되어 자원 보장
- cgroup v2로 통합 계층·일관 인터페이스 제공하여 관리 단순화
