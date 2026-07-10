---
title: 클라우드 운영체제 및 하이퍼바이저 (Cloud OS)
date: 2026-07-05
tags: [cspe-software]
weight: 142
---

## Ⅰ. 개요
| 구분 | 내용 |
|---|---|
| 정의 | 대규모 데이터 센터의 자원을 가상화하여 통합 관리하는 소프트웨어 계층 |
| 필요성 | compute·storage·network 자원 pool의 API 기반 할당·회수·격리·확장 관리 |
| 출제 의도 | 가상화 기술(Type 1/2), 하이퍼바이저 vs 컨테이너 차이 이해 |

## Ⅱ. 구성요소
```text
[ VM1 ] [ VM2 ]        [ Container1 ] [ Container2 ]
+-------------+        +---------------------------+
| Guest OS    |        |       Application         |
+-------------+        +---------------------------+
| Hypervisor  |        |      Container Engine     |
+-------------+        +---------------------------+
|   Hardware  |        |      Host OS / Kernel     |
+-------------+        +---------------------------+
```
| 구성요소 | 설명 | 비유 |
|---|---|---|
| 하이퍼바이저 | 물리 장치 위에 여러 가상 머신(VM)을 생성/실행 | 건물 관리자 |
| 클라우드 오케스트레이터 | 분산된 서버 자원을 API로 통합 제어 (OpenStack) | 지휘자 |
| 가상 스토리지/NW | 물리적 경계 없는 가상화된 저장소 및 네트워크 연결 | 가상 영토 |
> 요약: 하이퍼바이저는 하드웨어를, 컨테이너는 OS 커널을 공유하며 가상화함.

## Ⅲ. 절차
```text
User Request -> Cloud Controller -> Compute Node Selection -> VM Provision
      ^                                                         |
      +----- Resource Monitor <----- Workload Run <-------------+
```
1. 서비스 요청: 사용자가 포털이나 API를 통해 특정 사양의 인프라 요청.
2. 노드 선택: 스케줄러가 요청 자원, affinity, 장애 domain, 현재 사용량을 기준으로 host를 선택함.
3. VM 생성: 가상 이미지(VHD)를 로드하고 가상 CPU/Memory 할당 및 부팅.
4. 오토 스케일링: 부하에 따라 VM을 복제(Scale-out)하거나 사양 변경(Scale-up).
> 요약: 제어 계층은 요청 사양과 배치 정책에 따라 자원을 선택·할당하고 lifecycle과 scale 정책을 실행함.

## Ⅳ. 문제점
- VM 간 자원 경합 및 I/O 간섭(Noisy Neighbor)으로 인한 성능 불균형.
- 하이퍼바이저 취약점 발생 시 해당 호스트 내 모든 VM이 위태로운 전파 공격.

## Ⅴ. 개선방안
- QoS 제어 기법을 도입하여 인스턴스별 최소 성능(SLO) 보장 및 자원 격리.
- 마이크로 VM(Firecracker 등) 적용으로 보안 성능과 경량화 동시 달성.

## Ⅵ. 전망
- Serverless Hybrid: VM 기반과 이벤트 기반(FaaS) 아키텍처의 긴밀한 통합.
- Edge Cloud OS: 지연 시간을 줄이기 위해 에지 장치에 최적화된 분산 클라우드 제어.
