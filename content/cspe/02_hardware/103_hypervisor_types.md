---
title: "서버 가상화 — Type 1·Type 2 하이퍼바이저 (Hypervisor Types)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 103
---

# 서버 가상화 - Type 1·Type 2 하이퍼바이저 (Hypervisor Types)

## 미리 알고가기

- 하이퍼바이저: 물리 서버 자원을 가상머신에 분할·격리해 제공하는 계층임
- Type 1: 하드웨어 위에서 직접 동작하는 bare-metal 하이퍼바이저임
- Type 2: 호스트 운영체제 위에서 애플리케이션처럼 동작하는 hosted 하이퍼바이저임
- VM(Virtual Machine): 가상 CPU(Central Processing Unit), 메모리, 디스크, 네트워크를 가진 논리 서버 인스턴스임
- OS(Operating System): 하드웨어 자원 관리와 애플리케이션 실행 환경을 제공하는 운영체제임
- I/O(Input/Output): 스토리지·네트워크·주변장치 입출력 경로를 통칭함

## Ⅰ. 개요

- **정의/개념**: Type 1·Type 2 하이퍼바이저는 가상머신 관리 계층이 물리 하드웨어에 직접 위치하는지, 호스트 OS 위에 위치하는지를 기준으로 구분한 서버 가상화 방식임.
- **배경/필요성**: 서버 통합과 클라우드 운영은 강한 격리와 고성능이 필요하지만, 개발·교육 환경은 설치 편의와 호스트 OS 연동이 중요할 수 있음. 위치 계층을 구분하면 장애 범위와 성능 오버헤드를 명확히 판단할 수 있음.
- **비유**: Type 1은 건물 전체를 관리하는 전용 관리실이고, Type 2는 기존 사무실 안에 추가로 설치한 임시 관리 데스크와 같음.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 가상화 플랫폼 구조 선택 | bare-metal, hosted, 성능, 격리, 운영성 | 제품명 나열 중심 답안 |

> 요약: Type 1과 Type 2는 하이퍼바이저 위치 차이가 성능·격리·운영 목적 차이로 이어짐.

## Ⅱ. 특징 및 비교

| 판단 기준 | Type 1 하이퍼바이저 | Type 2 하이퍼바이저 |
|:---|:---|:---|
| 위치 | 하드웨어 위에서 직접 실행 | 호스트 OS 위에서 실행 |
| 성능·격리 | 낮은 오버헤드와 강한 격리에 유리 | 호스트 OS 경로로 오버헤드와 의존성 증가 |
| 운영 목적 | 데이터센터, 클라우드, 운영 서버 | 개발, 테스트, 교육, 개인 환경 |
| 장애 범위 | 하이퍼바이저와 관리 도메인 중심 | 호스트 OS 장애가 VM에 영향 |

> 요약: 운영 서버에는 Type 1, 편의성과 호스트 통합이 중요한 환경에는 Type 2가 적합함.

- **적용 조건**: 운영 서비스는 격리와 장애 범위, 개발 환경은 편의성과 호스트 연동을 우선함
- **선택 지표**: CPU ready, I/O latency, 관리 자동화 수준을 함께 확인해야 함

## Ⅲ. 구성요소/구조

```text
+------------------+       +------------------+
| VM / Guest OS    |       | VM / Guest OS    |
+------------------+       +------------------+
| Type 1 Hypervisor|       | Type 2 Hypervisor|
+------------------+       +------------------+
| Hardware         |       | Host OS          |
+------------------+       +------------------+
                           | Hardware         |
                           +------------------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| 가상머신 | 게스트 OS와 애플리케이션이 실행되는 논리 서버임 | 입주 사무실 |
| 하이퍼바이저 | vCPU, 메모리, I/O, 스케줄링, 격리를 담당함 | 건물 관리자 |
| 호스트 OS | Type 2에서 장치 드라이버와 파일시스템을 제공하는 기반 OS임 | 기존 사무실 인프라 |
| 물리 하드웨어 | CPU, 메모리, 스토리지, 네트워크 자원을 제공함 | 건물 설비 |

> 요약: 하이퍼바이저 구조는 VM과 물리 자원 사이에 어떤 계층이 추가되는지로 구분됨.

### 원리/흐름도

```text
+----------+      +----------+      +----------+      +----------+
| Register | ---> | Create   | ---> | Schedule | ---> | Operate  |
+----------+      +----------+      +----------+      +----------+
```

1. **자원 등록** — CPU, 메모리, 스토리지, 네트워크를 가상화 플랫폼에 등록함
2. **VM 생성** — vCPU(Virtual CPU), vRAM(Virtual RAM), 가상 디스크, 가상 NIC(Network Interface Card), 게스트 OS 이미지를 구성함
3. **자원 스케줄링** — 하이퍼바이저가 VM별 CPU 시간, 메모리, I/O 요청을 배분함
4. **운영 관리** — snapshot, migration, HA(High Availability), monitoring, patching으로 수명주기를 관리함

> 요약: 서버 가상화는 물리 자원을 등록하고 VM에 논리 자원으로 배분한 뒤 지속 운영하는 과정임.

## Ⅳ. 문제점 및 개선방안

- **P1 성능 오버헤드**: CPU ready time, I/O emulation, 메모리 ballooning이 워크로드 지연을 증가시킬 수 있음
- **P1 대응**: 적정 overcommit, paravirtual driver, NUMA(Non-Uniform Memory Access) affinity, I/O passthrough를 적용함 (확인: CPU ready and p99 latency)
- **P2 격리·보안 위험**: VM escape, side-channel, 관리 콘솔 침해가 다중 테넌트 환경에 큰 영향을 줄 수 있음
- **P2 대응**: 하이퍼바이저 패치, 관리망 분리, RBAC(Role-Based Access Control), secure boot, side-channel 완화 설정을 운영함 (확인: hardening compliance)
- **P3 운영 복잡도**: VM sprawl, snapshot 남용, 라이선스·패치 관리 누락이 비용과 위험을 증가시킴
- **P3 대응**: VM lifecycle policy, snapshot retention, template 표준화, CMDB(Configuration Management Database) 연계를 적용함 (확인: orphan VM count)

> 요약: 하이퍼바이저 운영 위험은 자원 경합, 격리, 수명주기 관리에서 발생하며 표준 운영 규율로 통제해야 함.

## Ⅴ. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| 운영 서버 통합 | Type 1 하이퍼바이저로 VM(Virtual Machine)을 집적하고 overcommit, NUMA affinity, HA(High Availability)를 표준화함 | CPU ready time, p99 latency |
| 개발·검증 환경 | Type 2 하이퍼바이저로 호스트 OS(Operating System)와 파일·네트워크를 쉽게 연동하고 데이터 등급을 제한함 | VM provision time, host impact |
| 다중 테넌트 클라우드 | 관리망 분리, RBAC, 패치 기준선, side-channel 완화를 운영 통제에 포함함 | hardening compliance, audit finding count |

> 요약: Type 선택은 용도별 격리 수준, 운영 자동화, 성능 지표가 함께 맞을 때 타당함.

## Ⅵ. 결론

- **발전 방향**: 경량 VM, confidential computing, container와 VM 통합 운영, edge virtualization이 확대됨
- **기술사적 판단**: Type 선택은 성능 요구, 보안 경계, 운영 자동화, 라이선스, 장애 대응 체계를 기준으로 해야 함
- **기술사 제언**: 운영 서버는 Type 1 기반 표준 플랫폼으로 통제하고, Type 2는 개발·검증 목적과 데이터 보호 기준을 명확히 제한해야 함
