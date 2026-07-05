---
title: "SSD FTL 플래시 변환 계층 (Flash Translation Layer)"
date: "2026-07-05"
tags:
  - "cspe-hardware"
weight: 38
---

## Ⅰ. 개요
- **정의**: OS의 논리 주소(LBA)를 NAND 물리 주소(PBA)로 변환하고 GC·Wear Leveling을 수행하는 SSD 펌웨어
- **배경/필요성**: NAND 플래시는 덮어쓰기가 불가하고 블록 단위 삭제만 가능하며 셀 수명(P/E Cycle)이 제한적이므로, OS와 플래시 사이에서 이 차이를 은닉할 중간 계층이 필수임
- **비유**: 연필로 수정 가능한 HDD와 달리, 볼펜 노트(NAND)에 글을 쓰려면 빈 페이지에 새로 쓰고 목차(매핑 테이블)만 바꿔주는 비서

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| SSD 내부 동작 원리 이해 | Out-of-Place Write, 페이지/블록 매핑 차이, WAF | GC를 단순 삭제로 설명하면 감점(유효 데이터 이동 포함) |

> 요약: NAND의 덮어쓰기 불가·수명 제한을 주소 매핑과 내부 관리 알고리즘으로 은닉하는 펌웨어임

## Ⅱ. 구성요소
```text
[OS / File System]
    | LBA (논리 주소)
    v
[FTL -- SSD Controller 내부]
    |-- Address Mapping (LBA -> PBA 변환)
    |-- Garbage Collection (빈 블록 확보)
    |-- Wear Leveling (마모 평준화)
    |-- Bad Block Management (불량 블록 격리)
    v
[NAND Flash (Page/Block)]
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| 매핑 테이블 | LBA와 PBA의 대응 관계를 DRAM에 유지하는 자료구조 | 도서관 색인 카드 |
| GC (Garbage Collection) | 유효 데이터를 새 블록에 복사 후 무효 블록을 Erase하여 빈 공간 확보 | 사무실 정리: 쓸 것만 옮기고 서랍 비움 |
| Wear Leveling | 기록 위치를 순환시켜 모든 블록의 P/E Cycle을 균등하게 소모 | 타이어 위치 교환으로 균등 마모 |
| Over-Provisioning (OP) | 사용자에게 노출하지 않는 예비 블록(전체의 7~28%)으로 GC·WL 여유 공간 확보 | 비상용 여분 좌석 |

> 요약: 매핑 테이블·GC·Wear Leveling·OP가 NAND의 물리 한계를 보상하는 4대 구성요소임

## Ⅲ. 절차
```text
쓰기 요청 -> Out-of-Place Write -> 무효 페이지 누적 -> GC 수행
```
- 1단계: OS가 LBA `x`에 쓰기를 요청하면 FTL이 빈 물리 페이지 `y`에 데이터를 기록(Out-of-Place Write)
- 2단계: 매핑 테이블에서 LBA `x`의 PBA를 `y`로 갱신하고 이전 PBA를 무효(Invalid) 표시
- 3단계: 무효 페이지가 누적되어 빈 블록이 부족해지면 GC가 유효 페이지만 새 블록에 복사 후 원본 블록을 Erase
- 4단계: Wear Leveling이 Cold Data(갱신 빈도 낮은 데이터)를 마모 적은 블록에서 마모 많은 블록으로 이동하여 P/E Cycle 균등화

> 요약: 빈 공간에 새로 쓰고 매핑만 갱신하되, 공간 부족 시 GC가 정리하고 WL이 수명을 균등화함

## Ⅳ. 문제점
- 쓰기 증폭(WAF): GC 시 유효 데이터 복사로 인해 호스트 쓰기량 대비 NAND 실제 쓰기량이 2~5배 증가하여 수명을 소모함
- 매핑 테이블 DRAM 비용: 페이지 단위 매핑 시 1TB SSD 기준 약 1GB DRAM이 필요하여 원가 상승 요인임
- GC 지연(Tail Latency): 빈 블록 고갈 시 GC가 포그라운드로 전환되어 I/O 응답 지연이 수십 ms까지 급증함

> 요약: WAF에 의한 수명 감소, 매핑 DRAM 비용, GC 시점의 지연 급증이 FTL의 3대 과제임

## Ⅴ. 개선방안
1. 단기: OP 비율을 10~28%로 확대하여 GC 빈도를 낮추고 WAF를 1.0에 근접시킴
2. 중기: DRAM-less FTL(HMB 방식)을 적용하여 호스트 메모리를 매핑 테이블 캐시로 활용, 원가 절감
3. 장기: ZNS(Zoned Namespace)로 FTL의 GC 기능을 호스트 OS로 이관하여 WAF와 Tail Latency를 원천 차단

> 요약: OP 확대→DRAM-less 전환→ZNS 이관 순서로 FTL의 구조적 한계를 해소함

## Ⅵ. 전망
- 발전 방향: 오픈 채널 SSD·ZNS를 통해 FTL 기능의 호스트 이관이 진행되며, NAND 적층 고도화(039 참조)에 따라 블록 크기 증가로 GC 알고리즘 고도화가 요구됨
- 기술사적 판단: FTL 알고리즘의 최적화 수준이 동일 NAND 칩에서도 SSD 성능·수명 격차를 결정하는 핵심 차별화 요소임
- 기술사 제언: 엔터프라이즈 SSD 도입 시 WAF 측정값과 OP 비율을 RFP에 명시하고, DWPD(Drive Writes Per Day) 보증 기준을 확인할 필요
