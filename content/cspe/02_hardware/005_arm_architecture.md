---
title: "ARM 프로세서 아키텍처·동작 모드 (ARM Architecture)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 5
---

## 미리 알고가기

- Cortex-A: 애플리케이션 프로세서로 Linux, Android 같은 범용 OS 실행에 적합함
- Cortex-R: 낮은 지연과 예측 가능성을 중시하는 실시간 제어용 프로세서임
- Cortex-M: 저전력 마이크로컨트롤러용 프로세서 계열임
- TrustZone: 보안 세계와 일반 세계를 하드웨어로 분리하는 ARM 보안 기능임

## Ⅰ. 개요

- **정의**: ARM 아키텍처는 RISC 기반 ISA, 권한 모드, 예외 처리, 메모리 모델, 보안 확장을 정의하고 이를 Cortex 계열과 SoC IP로 구현하는 프로세서 아키텍처임. 전력 대비 성능, IP 라이선스, 생태계 성숙도를 기준으로 모바일, 임베디드, 서버 적용을 판단함.
- **배경/필요성**: 배터리 기반 모바일과 임베디드 기기는 낮은 전력으로 충분한 성능과 주변장치 통합이 필요함. ARM은 설계 IP와 표준 인터커넥트를 제공해 제조사가 SoC 설계 기간을 단축하도록 함.
- **비유**: ARM은 엔진 설계도와 전장 배선 표준을 제공하고, 제조사가 차량 종류에 맞게 엔진을 골라 조립하는 방식임.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| ARM 계열별 적용 영역과 보안·저전력 구조 판단 | Cortex-A/R/M, 동작 모드, TrustZone, AMBA | ARM을 단순 저전력 CPU로만 설명 |

> 요약: ARM은 RISC ISA와 IP 생태계를 기반으로 목적별 프로세서와 SoC를 검증된 IP 조합으로 구성하는 구조임.

## Ⅱ. 특징/비교

| 판단 기준 | Cortex-A | Cortex-R | Cortex-M |
|:---|:---|:---|:---|
| 목표 시스템 | 스마트폰, 서버, 고성능 임베디드 | 자동차, 저장장치, 산업 제어 | MCU, IoT, 센서 노드 |
| 운영 환경 | MMU 기반 범용 OS | 예측 가능한 RTOS 또는 펌웨어 | bare-metal 또는 경량 RTOS |
| 설계 기준 | 성능, 가상화, 보안, 대용량 메모리 | 낮은 interrupt latency, lockstep | 저전력, 낮은 비용, 단순 interrupt |
| 선택 기준 | 복잡한 앱과 멀티태스킹 필요 시 | 실시간성과 신뢰성이 중요할 때 | 배터리와 원가가 중요할 때 |

> 요약: ARM은 동일 계열명이 아니라 A/R/M 프로파일별 요구사항에 맞춰 선택해야 함.

## Ⅲ. 구성요소

```text
+------------------------------------------------+
|                    ARM SoC                     |
| +-----------+  +-----------+  +--------------+ |
| | Cortex    |  | NEON/SVE  |  | TrustZone    | |
| | A/R/M     |  | SIMD      |  | Security     | |
| +-----+-----+  +-----+-----+  +------+-------+ |
|       |              |               |         |
|       +--------------+---------------+         |
|                      v                         |
|              +---------------+                 |
|              | AMBA AXI/AHB  |                 |
|              +---------------+                 |
+------------------------------------------------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Cortex 코어 | A/R/M 프로파일별 명령 실행, 예외 처리, 전력 관리를 수행함 | 엔진 |
| 동작 모드 | user, kernel, secure/non-secure 등 권한과 실행 상태를 구분함 | 출입 등급 |
| SIMD/벡터 확장 | 멀티미디어, DSP, AI 보조 연산을 병렬 처리함 | 다구간 작업대 |
| AMBA 인터커넥트 | CPU, GPU, NPU, 메모리, 주변장치를 표준 버스로 연결함 | 도시 도로망 |

> 요약: ARM 시스템은 코어, 권한 모드, 보안 확장, 표준 버스가 결합된 SoC 플랫폼임.

## Ⅳ. 절차

```text
+----------+     +----------+     +----------+     +----------+
| Profile  | --> | License  | --> | SoC      | --> | Software |
+----------+     +----------+     +----------+     +----------+
                                      |                 |
                                      v                 v
                                   AMBA/IP          BSP/OS
```

1. **프로파일 선택** - 성능, 실시간성, 저전력 요구에 따라 Cortex-A/R/M과 ISA 버전을 선택함
2. **IP 확보** - core license 또는 architecture license를 기반으로 구현 범위를 정함
3. **SoC 통합** - AMBA, cache, memory controller, GPU/NPU, 보안 IP를 연결함
4. **소프트웨어 포팅** - bootloader, firmware, OS, driver, secure monitor를 검증함

> 요약: ARM 도입은 코어 선택에서 끝나지 않고 SoC 통합과 BSP 품질까지 포함하는 절차임.

## Ⅴ. 문제점

- **P1 라이선스 종속성**: IP 사용 조건과 비용, 수출 통제, 공급자 정책 변화가 제품 전략에 영향을 줌
- **P2 SoC 통합 복잡도**: 캐시 일관성, AMBA QoS, interrupt routing, 전력 도메인 설계가 어려움
- **P3 보안 경계 오용**: TrustZone을 적용해도 secure world 코드와 key 관리가 부실하면 공격면이 남음

> 요약: ARM 리스크는 코어 자체보다 라이선스, SoC 통합, 보안 운영에서 발생함.

## Ⅵ. 개선방안

- **P1 대응**: 장기 라이선스 조건, 대체 코어 전략, RISC-V 보조 검토를 조달 계획에 포함함 (확인: BOM, 공급망 리스크)
- **P2 대응**: AMBA 검증 IP, coherency test, power intent 검증, reference design 재사용을 적용함 (확인: SoC 검증 coverage)
- **P3 대응**: secure boot, TEE 최소 권한, key ladder, secure firmware update 절차를 표준화함 (확인: penetration test, audit log)

> 요약: ARM 시스템 품질은 IP 선정 후 통합 검증과 보안 운영 절차에서 결정됨.

## Ⅶ. 전망

- **발전 방향**: ARM은 모바일 중심에서 서버, 차량 제어, 온디바이스 AI SoC로 확장되고 SVE/SME, TrustZone, Realm 기반 격리 기능과 결합됨
- **기술사적 판단**: Cortex-A/R/M 계열은 OS 요구, 실시간 지연, 전력 예산, AMBA 버스 구조, 주변 IP 재사용성 기준으로 구분해 선택해야 함; `SPEC`, CoreMark, interrupt latency, cache coherence, DVFS 전환 지연, 주변장치 DMA 경로를 목표 workload에서 측정함
- **기술사 제언**: ARM은 ISA보다 프로파일, AMBA, 보안 실행 환경, SoC 통합 조건을 묶어 요구사항 기반으로 설명하는 것이 적합함
