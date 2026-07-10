---
title: 자바 가비지 컬렉션 GC — G1·ZGC (Java GC)
date: 2026-07-05
tags: ["cspe-software"]
weight: 161
---

## Ⅰ. 개요
- 정의: JVM 내 더 이상 사용되지 않는 객체를 식별하여 메모리를 해제하는 자동 관리 메커니즘
- 배경: 도달할 수 없는 객체 회수, allocation 지속, heap 부족 방지, pause·throughput 목표 관리 필요
| 구분 | 내용 |
|------|------|
| 출제 의도 | G1(Heap Region), ZGC(Colored Pointers) 알고리즘의 차이와 STW 최소화 원리 파악 |

## Ⅱ. 구성요소
  [ Region ] [ Region ] [ Region ]
  [  Eden  ] [ Surviv ] [  Old   ]
  -> G1: Region 분할, ZGC: 64bit colored pointer
| 구성요소 | 설명 | 비유 |
|----------|------|------|
| Region | 힙을 고정 크기 단위로 분할 관리 | 아파트 단지 |
| Colored Pointers | 객체 상태를 포인터 비트에 저장(ZGC) | 물건 꼬리표 |
| SATB | concurrent marking 시작 시점에 도달 가능했던 객체가 누락되지 않게 write barrier로 추적함 | marking 정확성 |
> 요약: GC는 root에서 도달 가능한 객체를 식별하고 collector 정책에 따라 reclaim·compact·reference update를 수행함

## Ⅲ. 절차
  Marking -> Copying -> Relocation -> Remapping
  (STW 최소화 지향)
1. Initial Mark: 루트에서 참조 객체 짧게 식별
2. Concurrent Mark: 애플리케이션 중단 없이 생존 객체 파악
3. Remark/Relocate: 마킹 완료 및 객체 재배치 수행
4. Cleanup/Remap: 빈 영역 회수 및 참조 갱신
> 요약: concurrent·parallel 단계와 stop-the-world 구간을 나눠 live object를 mark·relocate하고 pause·throughput을 측정함

## Ⅳ. 문제점
- GC 수행 중 애플리케이션이 멈추는 Stop-The-World 발생
- 대용량 힙 메모리 사용 시 스캔 성능 저하 및 CPU 부하

## Ⅴ. 개선방안
- G1 GC의 Region 기반 수집 또는 ZGC의 지연 없는 재배치 적용
- Colored Pointer 및 Load Barrier 활용으로 병렬성 극대화

## Ⅵ. 전망
- 클라우드 네이티브 환경의 마이크로서비스 확대로 지연시간 1ms 미만의 ZGC 표준화 및 하드웨어 가속 결합 전망
