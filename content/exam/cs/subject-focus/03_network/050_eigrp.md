---
title: "EIGRP (Enhanced Interior Gateway Routing Protocol)"
date: "2026-06-30"
weight: 50
tags:
  - "exam-cspe-network"
---

## Ⅰ. 정의
> Cisco가 개발한 향상된 내부 게이트웨이 라우팅 프로토콜로, DUAL(Diffusing Update Algorithm) 알고리즘 기반의 거리벡터·링크상태 특성을 결합한 하이브리드 프로토콜이다.

## Ⅱ. 구성요소 / 원리
- DUAL 알고리즘: 루프 없는(loop-free) 최적경로와 백업경로를 즉시 계산
- Successor: 목적지까지의 최적 경로(최소 메트릭, 라우팅 테이블 등록)
- Feasible Successor: 무루프 조건(FC) 만족 백업 경로, 토폴로지 테이블 보관
- 복합 메트릭: 대역폭(Bandwidth)·지연(Delay) 기본, 부하·신뢰도·MTU 옵션
- Hello/Hold로 이웃 관계 유지, 변경분만 부분/증분 업데이트

## Ⅲ. 흐름도 / 구조
```text
[Neighbor Discovery: Hello] -> [Topology Table 구성]
            |
            v
  DUAL 계산 -> Successor(최적) + FS(백업)
            |
            +-- 장애 시 FS 즉시 전환(빠른 수렴)
            +-- FS 없으면 Query 확산 -> 재계산
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 대규모 내부망에서 빠른 수렴과 무루프 경로 제공 |
| 장점 | FS 백업으로 즉시 수렴, 증분 업데이트로 대역폭 절감 |
| 한계 | 과거 Cisco 독점(현재 일부 공개), 멀티벤더 호환성 제약 |

## Ⅴ. 기술사적 적용
- OSPF 대비: EIGRP는 하이브리드·고속수렴, OSPF는 표준·링크상태(SPF)
- 단일 벤더(Cisco) 중심 캠퍼스/지사 WAN의 IGP로 적용
- 복합 메트릭 튜닝으로 대역폭·지연 기반 경로 최적화 가능
