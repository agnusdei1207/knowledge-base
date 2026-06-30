---
title: "인터럽트·DMA (Interrupt / Direct Memory Access)"
date: "2026-06-30"
weight: 72
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 인터럽트(Interrupt)는 입출력 완료·예외 발생 시 CPU 흐름을 비동기로 전환하는 신호이며, DMA(Direct Memory Access)는 CPU 개입 없이 주변장치와 메모리가 직접 데이터를 전송하는 기법이다.

## Ⅱ. 구성요소 / 원리
- 인터럽트: IRQ 라인, 인터럽트 컨트롤러(PIC/APIC), 인터럽트 벡터 테이블(ISR 주소), 우선순위·마스킹
- 문맥전환: 현재 PC·레지스터 저장 → ISR 수행 → 복귀(IRET)
- DMA: DMA 컨트롤러(DMAC), 시작주소·전송길이 레지스터, 버스 중재(Bus Arbitration)
- DMA 모드: Burst(연속 점유), Cycle Stealing(틈새 점유), Transparent
- DMA 완료 시 CPU에 인터럽트로 통지

## Ⅲ. 흐름도 / 구조
```text
[Device] --IRQ--> [DMAC] --bus req--> [CPU 버스양도]
   |                 |
   +-- 직접 전송 --> [Memory]  (CPU는 연산 수행)
   |                 |
   +-- 전송완료 --> Interrupt --> [CPU] ISR 처리
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | CPU 부하 경감, 대용량 I/O 효율 전송 |
| 장점 | 비동기 처리, CPU·I/O 병렬성 확보, 폴링 대비 효율 |
| 한계 | 버스 경합, 인터럽트 오버헤드·캐시 일관성 관리 필요 |

## Ⅴ. 기술사적 적용
- 폴링(Polling) 대비: 이벤트 기반으로 CPU 낭비 제거
- NVMe·고속 SSD에서 MSI-X 다중 인터럽트로 큐별 분산 처리
- 네트워크 NIC의 인터럽트 모더레이션·DMA 디스크립터 링 적용
