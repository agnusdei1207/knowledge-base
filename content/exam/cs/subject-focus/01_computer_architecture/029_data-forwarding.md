---
title: "데이터 포워딩 (Data Forwarding / Bypassing)"
date: "2026-06-30"
weight: 29
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> RAW(Read After Write) 데이터 해저드 시 결과를 레지스터 라이트백 전에 후속 명령의 입력으로 직접 전달하여 스톨을 줄이는 기법이다.

## Ⅱ. 구성요소 / 원리
- 포워딩 경로: EX/MEM, MEM/WB 파이프라인 레지스터→ALU 입력 우회 연결
- 포워딩 유닛: 소스/목적 레지스터 번호 비교로 우회 여부 판단
- 멀티플렉서(MUX)로 ALU 입력을 레지스터 값 대신 포워딩 값으로 선택
- Load-Use 해저드는 포워딩만으로 불가 → 1사이클 스톨 병행 필요

## Ⅲ. 흐름도 / 구조
```text
I1: ADD R1,R2,R3   IF ID EX─┐MEM WB
                            │(EX/MEM 포워딩)
I2: SUB R4,R1,R5      IF ID EX
                  스톨 없이 R1 결과 즉시 사용
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | RAW 해저드의 스톨 제거로 CPI 유지 |
| 장점 | 라이트백 대기 없이 결과 즉시 활용 |
| 한계 | 추가 경로·MUX 비용, Load-Use는 스톨 불가피 |

## Ⅴ. 기술사적 적용
- 컴파일러 명령어 재배치(Load 다음 독립 명령 삽입)와 병행해 Load-Use 스톨 회피
- 토마술로의 CDB(Common Data Bus) 브로드캐스트가 포워딩의 동적 일반화 형태
