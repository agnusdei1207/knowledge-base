---
title: "RAW·WAR·WAW (Read After Write / Write After Read / Write After Write)"
date: "2026-06-30"
weight: 28
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 파이프라인에서 명령어 간 레지스터/메모리 접근 순서로 발생하는 데이터 의존성 유형으로, 참(RAW)·역(WAR)·출력(WAW) 의존성으로 나뉜다.

## Ⅱ. 구성요소 / 원리
- RAW(Read After Write): 참 의존성(True), 선행 쓰기 결과를 후행이 읽음 → 본질적 의존
- WAR(Write After Read): 역 의존성(Anti), 선행 읽기 전 후행이 덮어씀
- WAW(Write After Write): 출력 의존성(Output), 두 명령이 같은 위치에 순서대로 씀
- WAR·WAW는 자원 재사용으로 생긴 가짜 의존성 → 레지스터 리네이밍으로 제거

## Ⅲ. 흐름도 / 구조
```text
RAW:  I1: R1←...      I2: ...←R1   (읽기 전 쓰기 완료 필요)
WAR:  I1: ...←R2      I2: R2←...   (I1 읽기 이후 I2 쓰기)
WAW:  I1: R3←...      I2: R3←...   (최종값=I2 보장)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 의존성 식별로 결과 정확성 보장 |
| 장점 | 분류 기반 최적 해소(포워딩/리네이밍) 설계 |
| 한계 | RAW는 제거 불가, 미해소 시 스톨 유발 |

## Ⅴ. 기술사적 적용
- RAW: 데이터 포워딩으로 지연 최소화 / WAR·WAW: 레지스터 리네이밍으로 제거
- 토마술로 알고리즘·OoO 실행에서 가짜 의존성 해소로 ILP 극대화
