---
title: 스마트 NIC 및 DPU (SmartNIC and DPU)
date: 2026-07-05
tags: [cspe-hardware]
weight: 68
---

## Ⅰ. 개요
- 정의: 네트워킹, 스토리지, 보안 연산을 CPU로부터 오프로드하여 처리하는 전용 프로세서
- 배경: 가상화 및 보안 처리에 따른 호스트 CPU의 부하(Tax) 급증 해결 필요
- 출제 의도: 데이터 중심 컴퓨팅(Data-centric)으로의 패러다임 변화 이해도 측정

## Ⅱ. 구성요소
- ASCII 구조도
  [ Host CPU ] <---- PCIe ----> [ DPU (Data Processing Unit) ]
                                |  - ARM/MIPS Core (Control) |
                                |  - Hardware Accel (Crypto) |
                                |  - Network Engine (OVS)    |
                                +----------------------------+

- 구성요소 표
| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| Accelerator | 암호화, 압축 등 특정 연산을 전담하는 하드웨어 | 조리 전문 기구 |
| Embedded Core | 가상 스위칭 및 제어 로직을 수행하는 프로세서 | 주방 보조원 |
| High Speed I/O | 100G 이상의 고대역폭 네트워크 인터페이스 | 대용량 통로 |

- > 요약: CPU는 애플리리케이션에 집중하고, 인프라 처리는 DPU가 전담

## Ⅲ. 절차
- ASCII 흐름도
  (Packet) -> [DPU 수신] -> [보안/캡슐화 해제] -> [메모리 DMA] -> (App)

1. 패킷 수신: 고속 네트워크 인터페이스를 통한 데이터 인입
2. Offload 처리: CPU 개입 없이 DPU 내 가속기에서 패킷 분석 및 변환
3. 데이터 전달: PCIe 인터페이스를 통해 호스트 메모리로 직접 전달
4. 정책 갱신: 호스트의 제어부로부터 네트워킹/보안 정책 동기화

- > 요약: 데이터 경로(Data Path)를 CPU 외부에서 완결하여 지연시간 단축

## Ⅳ. 문제점
- 개발 난이도: DPU 전용 SDK(P4, DPDK 등) 활용을 위한 높은 기술 장벽
- 벤더 종속성: 제조사별 아키텍처 상이로 인한 상호운용성 부족

## Ⅴ. 개선방안
- 표준화: SONiC 등 오픈 소스 기반의 네트워크 운영체제 도입 확대
- 추상화 레이어: 상위 애플리케이션과 하드웨어 간 공통 API(DOCA 등) 활용

## Ⅵ. 전망
- 로드맵: IPU(Infrastructure PU)로 진화하여 데이터센터 전체 자원 가상화 주도
- CSF: 전력 효율(Performance per Watt) 최적화 및 프로그래밍 가능성 확보
