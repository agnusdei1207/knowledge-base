---
title: "ECC메모리 (Error Correcting Code Memory)"
date: "2026-06-30"
weight: 85
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> ECC메모리(Error Correcting Code Memory)는 오류정정코드를 이용해 메모리 비트 오류를 자동 탐지·정정하여 데이터 무결성을 보장하는 메모리이다.

## Ⅱ. 구성요소 / 원리
- 해밍코드(Hamming Code) 기반 패리티 비트 추가
- SEC-DED(Single Error Correction, Double Error Detection): 1비트 정정·2비트 검출
- 추가 칩으로 검사비트 저장(예: 64비트당 8비트)
- Soft Error(우주선·전기적 노이즈) 대응

## Ⅲ. 흐름도 / 구조
```text
[Write] data → ECC 생성 → 저장(data+check)
[Read]  data+check → 신드롬 계산
   ├ 1bit 오류 → 자동 정정
   └ 2bit 오류 → 검출·통지(uncorrectable)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 메모리 오류로 인한 데이터 손상·다운 방지 |
| 장점 | 무결성·신뢰성↑, 무중단 운영 |
| 한계 | 추가 비용·용량, 약간의 성능 오버헤드 |

## Ⅴ. 기술사적 적용
- 서버·데이터센터·금융 등 신뢰성 필수 환경 표준
- HBM의 On-die ECC, DDR5 내장 ECC로 미세공정 오류 대응
- Chipkill·Memory Mirroring 등 고급 RAS 기능과 연계
