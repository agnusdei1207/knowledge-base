---
title: "VRRP·HSRP (Virtual Router Redundancy Protocol/Hot Standby Router Protocol)"
date: "2026-06-30"
weight: 58
tags:
  - "exam-cspe-network"
---

## Ⅰ. 정의
> 다수의 물리 라우터를 하나의 가상 게이트웨이로 묶어, 액티브 장비 장애 시 백업이 즉시 대체함으로써 기본 게이트웨이의 단일장애점(SPOF)을 제거하는 이중화 프로토콜이다.

## Ⅱ. 구성요소 / 원리
- 가상 IP/MAC: 호스트는 가상 IP를 게이트웨이로 사용, 물리장비 변경 무관
- Master(VRRP)/Active(HSRP): 실제 패킷 전달을 담당하는 대표 라우터
- Backup/Standby: 대표 장애 시 승계 대기 라우터
- 우선순위(Priority): 값이 높은 장비가 대표 선출
- 프리엠션(Preemption): 우선순위 높은 장비 복구 시 대표 탈환
- Hello/Advertisement 주기로 생존 감시, 미수신 시 절체

## Ⅲ. 흐름도 / 구조
```text
[Host] -> 가상IP(GW)
   |        ^
   v        |
[R1 Master/Active]==Hello==[R2 Backup/Standby]
   장애 발생 -> Hello 끊김 -> R2가 가상IP/MAC 승계
   -> 트래픽 무중단 전환(프리엠션 시 복구 후 복귀)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 기본 게이트웨이 이중화로 무중단 L3 가용성 확보 |
| 장점 | 호스트 설정 변경 불필요, 빠른 절체, 표준(VRRP) |
| 한계 | 동일 서브넷 내 한정, 대역폭 분산 미흡(추가 설계 필요) |

## Ⅴ. 기술사적 적용
- VRRP(표준 RFC) vs HSRP(Cisco 독점) vs GLBP(부하분산) 비교 선택
- 가상IP 단위 그룹 분리로 액티브-액티브 부하분산 설계
- 코어/분배 계층 이중화·스택·MLAG와 결합해 종단 가용성 강화
