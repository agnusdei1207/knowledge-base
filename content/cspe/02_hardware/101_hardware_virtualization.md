---
title: "하드웨어 가상화 — VT-x·AMD-V (Hardware Virtualization)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 101
extra:
  question_no: "101"
  exam_status: "기출"
  exam_history: "137회"
---

## 미리 알고가기

- VT-x와 AMD-V는 x86 CPU가 가상머신 실행을 직접 지원하는 확장임
- VM exit은 게스트 실행 중 하이퍼바이저 개입이 필요한 사건임
- EPT와 NPT는 게스트 주소를 실제 물리 주소로 변환하는 2단계 변환 구조임

## Ⅰ. 개요

- **정의/개념**: 하드웨어 가상화는 CPU가 가상머신 실행 모드와 특권 명령 제어와 2단계 메모리 주소 변환을 직접 제공해 하이퍼바이저가 게스트 OS를 높은 호환성과 격리 수준으로 실행하게 하는 기술임
- **배경/필요성**: 순수 소프트웨어 가상화는 특권 명령 변환과 메모리 매핑 비용이 커 성능과 호환성 한계가 있었으므로, 서버 통합과 클라우드 운영을 위해 CPU 수준 지원이 필요해졌음

## Ⅱ. 특징

- 게스트 OS를 수정하지 않고도 높은 호환성으로 실행할 수 있음
- 특권 명령과 인터럽트와 I/O 접근을 CPU가 trap과 exit로 통제함
- EPT와 NPT가 shadow page table 부담을 줄여 메모리 가상화 효율을 높임
- 실제 병목은 직접 실행보다 VM exit 빈도와 I/O 가상화 경로에서 자주 발생함

## Ⅲ. 종류 및 비교

| 판단 기준 | 소프트웨어 가상화 | 하드웨어 가상화 |
|:---|:---|:---|
| 특권 명령 처리 | binary translation이나 수정 필요 | CPU trap과 VM exit로 처리 |
| 게스트 호환성 | 제약이 상대적으로 큼 | 일반 OS를 그대로 실행 가능 |
| 메모리 가상화 | shadow page table 부담 큼 | EPT와 NPT로 효율 개선 |
| 주요 병목 | 변환 오버헤드 | VM exit와 I/O 경로 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| VM Execution Mode | 게스트와 하이퍼바이저 실행 권한을 분리해 직접 실행과 안전한 제어를 동시에 가능하게 함 |
| VMCS or VMCB | 게스트 상태와 exit 조건과 제어 비트를 저장해 전환 비용과 정책의 기준이 됨 |
| EPT or NPT | 게스트 물리 주소를 호스트 물리 주소로 변환해 메모리 격리와 성능을 함께 좌우함 |
| Interrupt and I/O Virtualization | 장치 접근과 인터럽트 전달을 가상화해 실제 운영 성능과 격리 수준을 결정함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| VM 설정        | --> | 게스트 직접 실행 | --> | VM exit 처리   | --> | 재진입 실행    |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **VM 설정**: 하이퍼바이저가 vCPU 상태와 메모리 매핑과 제어 구조를 초기화함
2. **게스트 직접 실행**: CPU가 non-root 모드에서 게스트 명령을 직접 실행함
3. **VM exit 처리**: 특권 명령과 I/O와 인터럽트 발생 시 하이퍼바이저로 전환함
4. **재진입 실행**: 이벤트 처리 후 게스트 상태를 갱신하고 다시 실행함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 특권 명령과 타이머와 I/O 이벤트가 많으면 VM exit가 빈번해져 가상화 오버헤드가 급증할 수 있음
   - 해결방안: paravirtual driver와 interrupt coalescing을 적용하고 VM exit rate와 CPU ready time으로 검증함
2. 문제: 2단계 주소 변환과 TLB miss가 누적되면 메모리 집약 워크로드의 지연이 커질 수 있음
   - 해결방안: huge page와 NUMA 배치를 최적화하고 EPT miss rate와 p99 memory latency로 검증함
3. 문제: 공유 캐시와 speculative execution 특성 때문에 VM 간 정보 노출 위험이 남을 수 있음
   - 해결방안: microcode 업데이트와 side-channel mitigation을 운영하고 isolation test pass rate와 mitigation compliance로 검증함

## Ⅶ. 적용 사례

- 클라우드 VM 호스트에서는 VT-x와 EPT를 기본 활성화하고 확인 지표는 VM exit rate와 CPU ready time임
- 데이터베이스 가상화 환경에서는 huge page와 NUMA affinity를 함께 적용하고 확인 지표는 EPT miss rate와 p99 latency임
- 다중 테넌트 보안 기준선에서는 speculative execution 완화 설정을 포함하고 확인 지표는 mitigation compliance와 isolation test pass rate임

## Ⅷ. 결론

하드웨어 가상화의 가치는 가상머신을 직접 실행하는 데 있으므로, 플랫폼 평가는 코어 수보다 exit 비용과 메모리 변환 효율과 격리 수준을 함께 봐야 함.
