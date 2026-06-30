---
title: "단편화·MTU·PMTU (Fragmentation/MTU/Path MTU)"
date: "2026-06-30"
weight: 32
tags:
  - "exam-cspe-network"
---

## Ⅰ. 정의
> 링크의 최대 전송 단위(MTU)를 초과하는 패킷을 여러 조각으로 나누는 단편화와, 경로 전체의 최소 MTU를 탐색하는 PMTU Discovery 기법.

## Ⅱ. 구성요소 / 원리
- MTU(Maximum Transmission Unit): 링크가 전송 가능한 최대 페이로드(이더넷 1500B)
- Identification: 동일 원본 패킷의 조각 식별자
- Flags(DF/MF): DF=단편화 금지, MF=뒤에 조각 더 있음
- Fragment Offset: 원본 내 조각 위치(8바이트 단위)
- 재조립은 최종 수신지에서 Identification·Offset 기준 수행

## Ⅲ. 흐름도 / 구조
```text
원본 4000B → MTU 1500 경로 통과
 [Frag1 off=0  MF=1][Frag2 off=185 MF=1][Frag3 off=370 MF=0]
 DF=1 인데 초과? → 라우터가 ICMP "Too Big" 반환
 PMTU Discovery: DF=1 송신 → ICMP로 최소 MTU 학습 → 크기 조정
 수신지에서 ID+Offset로 재조립
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 이기종 링크 MTU 차이를 흡수해 패킷 전달 보장 |
| 장점 | MTU 상이 망 간 호환, PMTU로 불필요 단편화 회피 |
| 한계 | 단편화 시 처리 부하·재조립 지연, 한 조각 손실 시 전체 폐기 |

## Ⅴ. 기술사적 적용
- PMTU Discovery(DF 비트+ICMP)로 종단 간 최적 MTU 결정
- ICMP 차단(블랙홀) 시 PMTU 실패 → MSS Clamping으로 보완
- IPv6는 라우터 단편화 금지, 송신측 PMTUD 의무화
