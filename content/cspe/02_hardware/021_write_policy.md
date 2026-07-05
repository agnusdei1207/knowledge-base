---
title: 쓰기 정책 — Write-through vs Write-back (Write Policy)
date: 2026-07-05
tags: ["cspe-hardware"]
weight: 21
---

## Ⅰ. 개요
- 정의: CPU가 캐시에 데이터를 썼을 때, 이를 주메모리에 반영하는 시점을 결정하는 정책
- 배경: 메모리 접근 지연 시간과 데이터 일관성 간의 균형을 맞추기 위한 선택
- 출제 의도: 각 정책의 성능 특성(Latency, Bandwidth) 및 일관성 유지 방법 이해

## Ⅱ. 구성요소
- ASCII 구조도
  [Write-through]                [Write-back]
  CPU -> Cache -> Memory         CPU -> Cache (Mark Dirty)
           | (Simultaneous)              | (Later when evicted)
           v                             v
        Immediate                      Deferred

- 구성요소 표
| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| Dirty Bit | 데이터 수정 여부를 표시하는 태그 비트 (WB 필수) | 수정 표시 포스트잇 |
| Write Buffer | 메모리 쓰기 성능을 보완하기 위한 임시 저장소 | 출고 대기장 |
| Eviction | 캐시 교체 시 Dirty 라인을 메모리에 기록 | 퇴거 시 정산 |
> 요약: 즉시 반영(Through)과 나중 반영(Back)의 차이임

## Ⅲ. 절차
- ASCII 흐름도 (Write-back)
  (Write Req) -> (Write to Cache) -> (Set Dirty Bit)
                                          |
  (Cache Miss) -> (Line to Evict is Dirty?) --(Yes)--> (Write to Mem)
                                |                      |
                                +----------<-----------+
                                v
                        (Fetch New Line)

- 4단계 설명
1. 쓰기 수행: CPU가 캐시 라인에 데이터 기록 및 Dirty 비트를 1로 설정
2. 지연 반영: 메모리 업데이트 없이 캐시 내에서만 여러 번 수정 가능
3. 교체 트리거: 새로운 데이터를 위해 해당 라인을 비워야 할 때 상태 확인
4. 메모리 갱신: Dirty 비트가 설정된 경우에만 주메모리에 실제 쓰기 수행
> 요약: 최대한 메모리 접근을 미루어 버스 대역폭 낭비를 방지함

## Ⅳ. 문제점
- Write-through: 매 쓰기마다 메모리 접근이 발생하여 CPU 처리 속도 저하
- Write-back: 전원 차단이나 캐시 오류 시 최신 데이터가 메모리에 없어 손실 위험

## Ⅴ. 개선방안
- (단기) Write-allocate: 쓰기 미스 시 메모리 데이터를 캐시로 읽어온 후 쓰기 수행
- (중기) No-write-allocate: 쓰기 미스 시 캐시 거치지 않고 바로 메모리에 쓰기 (WT용)
- (장기) 비휘발성 캐시 (NVRAM): WB의 데이터 손실 위험을 물리적으로 제거

## Ⅵ. 전망
- 로드맵: 성능 중심의 현대 CPU는 모든 캐시 계층에서 Write-back 방식을 선호
- CSF: 다중 프로세서 환경에서 Write-back 캐시의 일관성(MESI) 유지 오버헤드 최소화
