---
title: "eBPF 확장 BPF (Extended Berkeley Packet Filter)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 268
extra:
  question_no: "268"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- eBPF는 커널을 재컴파일하지 않고도 커널 내부 특정 지점에 안전하게 프로그램을 붙여 실행하는 기술임
- 네트워킹과 보안과 관측성 분야에서 특히 강한 확장성을 제공함
- 커널 모듈보다 안전성과 민첩성이 높지만 검증 가능한 프로그램 제약을 따른다는 점이 특징임

## Ⅰ. 개요

- **정의/개념**: eBPF는 검증된 바이트코드 프로그램을 리눅스 커널 내 후크 지점에 로드해 패킷 처리와 시스템 관측과 보안 정책을 동적으로 수행하게 하는 커널 확장 기술임
- **배경/필요성**: 전통적 커널 모듈 방식은 위험성과 배포 부담이 커서 네트워크와 보안 기능을 더 안전하고 유연하게 확장할 수 있는 메커니즘이 필요해짐

## Ⅱ. 특징

- 커널 재빌드 없이 동적 로딩과 업데이트가 가능함
- JIT 기반 실행으로 높은 성능과 낮은 오버헤드를 기대할 수 있음
- 검증기와 타입 제약으로 안전성을 확보함
- 네트워킹과 보안과 observability를 하나의 플랫폼에서 확장할 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | eBPF | Kernel Module | iptables rule chain |
|:---|:---|:---|:---|
| 배포 민첩성 | 높음 | 낮음 | 중간 |
| 안전성 | 검증기 기반 높음 | 낮음 | 중간 |
| 확장성 | 매우 높음 | 높음 | 제한적 |
| 대표 영역 | observability, networking, security | 깊은 커널 기능 | 패킷 필터링 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| eBPF Program | 커널 후크 지점에서 실행되는 바이트코드 로직으로 패킷 처리나 추적이나 정책 판단을 수행함 |
| Verifier | 프로그램이 안전하게 종료되고 메모리 접근이 유효한지 검사해 커널 안정성을 보호하는 검증 엔진임 |
| Maps | 커널과 사용자 공간이 상태와 통계를 공유하는 자료 구조로 정책과 메트릭을 교환하게 함 |
| Hook Points | XDP와 TC와 kprobe 같은 다양한 후크 지점이 프로그램 실행 위치를 제공함 |
| User Space Controller | 프로그램 로딩과 맵 갱신과 결과 수집을 담당하는 사용자 공간 제어 계층임 |

```text
+------------------+    +------------------+    +------------------+
| User Controller  | -> | Verifier / Loader| -> | eBPF Hook Point  |
+------------------+    +------------------+    +------------------+
                                   |
                                   v
                              +-----------+
                              | eBPF Maps |
                              +-----------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 프로그램 작성 | -> | 검증 및 로드  | -> | 후크 실행    | -> | 맵 업데이트  | -> | 사용자 수집  |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **프로그램 작성**: 네트워크나 관측 로직을 eBPF 코드로 작성함
2. **검증 및 로드**: verifier가 안전성을 확인한 뒤 커널에 로드함
3. **후크 실행**: 지정된 커널 이벤트에서 프로그램이 동작함
4. **맵 업데이트**: 상태와 통계를 맵에 기록함
5. **사용자 수집**: 사용자 공간이 데이터를 읽고 정책을 조정함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 후크 지점과 프로그램 복잡도가 커질수록 검증 통과와 디버깅 난도가 급격히 높아질 수 있음
   - 해결방안: incremental program design과 hook specific test suite를 적용하고 verifier rejection rate와 debug turnaround time으로 검증함
2. 문제: 커널 버전 차이와 기능 지원 편차가 크면 이식성과 운영 일관성이 떨어질 수 있음
   - 해결방안: kernel capability matrix와 compatibility CI를 적용하고 cross kernel portability score와 deployment failure rate로 검증함
3. 문제: 과도한 eBPF 프로그램 삽입은 관측 오버헤드와 정책 충돌을 유발할 수 있음
   - 해결방안: program governance와 performance budget policy를 적용하고 probe overhead ratio와 conflicting policy incident count로 검증함

## Ⅶ. 적용 사례

- 클라우드 네트워킹 팀이 후크별 테스트 스위트를 운영하며 확인 지표는 verifier rejection rate와 debug turnaround time임
- 멀티커널 환경이 호환성 CI를 적용하며 확인 지표는 cross kernel portability score와 deployment failure rate임
- 보안 관측 플랫폼이 eBPF 예산 정책을 적용하며 확인 지표는 probe overhead ratio와 conflicting policy incident count임

## Ⅷ. 결론

eBPF는 커널 확장을 안전하고 민첩하게 바꾼 핵심 기술이지만 검증 난도와 커널 호환성과 운영 거버넌스를 함께 관리해야 함.
