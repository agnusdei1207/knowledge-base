---
title: "MESI/MOESI (Modified·Exclusive·Shared·Invalid / +Owned 프로토콜)"
date: "2026-06-30"
weight: 67
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 캐시 블록의 상태를 4가지(MESI: Modified·Exclusive·Shared·Invalid)로 관리하는 무효화 기반 일관성 프로토콜이며, MOESI는 Owned 상태를 추가해 더티 공유를 지원.

## Ⅱ. 구성요소 / 원리
- Modified(M): 수정됨, 유일 사본, 메모리와 불일치
- Exclusive(E): 유일 사본, 메모리와 일치(미수정)
- Shared(S): 다수 사본 공유, 메모리와 일치
- Invalid(I): 무효한 사본
- Owned(O, MOESI): 더티 사본을 공유하며 응답 책임 보유(메모리 쓰기 지연)

## Ⅲ. 흐름도 / 구조
```text
 I ──read(유일)──▶ E ──write──▶ M
 │                 │             │ (타코어 read)
 └──read(공유)──▶ S ◀───────────┘→ M은 S/O로 강등
   타코어 write → 사본 → I (무효화)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 무효화 기반으로 캐시 일관성을 상태기계로 보장 |
| 장점 | E상태로 불필요 트래픽 감소, MOESI는 더티 데이터 직접 공유 |
| 한계 | 상태 관리 복잡, 일관성 트래픽·확장성 비용 |

## Ⅴ. 기술사적 적용
- MESI → Intel x86 캐시 일관성 기본
- MOESI → AMD 프로세서, 캐시-투-캐시 전송 최적화
- MESIF(Intel, Forward 추가) 등 변형으로 확장
