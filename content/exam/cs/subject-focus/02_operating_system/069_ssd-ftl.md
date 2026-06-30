---
title: "SSD·FTL·마모평준화 (SSD/FTL/Wear Leveling)"
date: "2026-06-30"
weight: 69
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> SSD(Solid State Drive)는 낸드 플래시(NAND Flash) 기반 저장장치이며, FTL(Flash Translation Layer)은 논리주소를 물리주소로 매핑해 플래시의 제약(덮어쓰기 불가·제한된 수명)을 은닉하는 펌웨어 계층이다.

## Ⅱ. 구성요소 / 원리
- 플래시 특성: 읽기/쓰기는 페이지(Page) 단위, 삭제(Erase)는 블록(Block) 단위, 덮어쓰기 불가
- FTL 매핑: 논리블록주소(LBA)를 물리페이지로 변환(페이지/블록/혼합 매핑)
- 가비지 컬렉션(GC, Garbage Collection): 유효 페이지 회수 후 블록 삭제로 가용공간 확보
- 웨어레벨링(Wear Leveling): 쓰기/삭제를 전 블록에 고르게 분산해 수명 균등화
- TRIM·예비영역(Over-Provisioning): 삭제 통지·여분 공간으로 GC 효율 향상

## Ⅲ. 흐름도 / 구조
```text
호스트(LBA 요청)
   ↓
[FTL: 주소매핑 테이블]──→ 물리 페이지
   ↓                         ↓
[Wear Leveling]        [GC: 유효페이지 이동 → 블록 Erase]
   └── 쓰기 분산 ──┘
NAND: Page(R/W) ⊂ Block(Erase 단위)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 플래시 제약 은닉, 수명 연장 및 일관된 블록 인터페이스 제공 |
| 장점 | 무소음·저지연·내충격, 탐색지연 없음, 병렬 I/O 고성능 |
| 한계 | 쓰기증폭(WAF), 셀 수명 제한, GC로 인한 성능 변동 |

레벨 비교

| 항목 | HDD | SSD |
|:---|:---|:---|
| 매체 | 자기 디스크 | NAND 플래시 |
| 접근지연 | 기계적(ms) | 전자적(μs) |
| 수명관리 | 불필요 | 웨어레벨링 필수 |

## Ⅴ. 기술사적 적용
- 쓰기증폭(WAF, Write Amplification Factor) 완화 위한 OP·TRIM 설계
- 로그구조 파일시스템(LFS)·COW와 플래시 특성의 친화성
- 엔터프라이즈 NVMe·QLC 환경의 내구성·성능 트레이드오프 분석
