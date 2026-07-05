---
title: 저장 프로시저 및 트리거 (Stored Procedure and Trigger)
date: 2026-07-05
tags: ["cspe-software"]
weight: 177
---

## Ⅰ. 개요
- 정의: DB 내에 미리 컴파일되어 저장된 SQL 집합(SP)과 특정 이벤트 발생 시 자동 실행되는 프로그램(Trigger)
- 배경: 네트워크 트래픽 감소, 로직 재사용성 및 업무 규칙 자동화
| 구분 | 내용 |
|------|------|
| 출제 의도 | Stored Procedure의 성능적 이점과 Trigger의 무결성 보장 역할 구분 |

## Ⅱ. 구성요소
  App --(Call)--> [ Stored Procedure ]
  Table --(Event)--> [ Trigger ]
| 구성요소 | 설명 | 비유 |
|----------|------|------|
| Stored Proc | SQL 문들을 하나의 모듈로 묶어 컴파일한 것 | 밀키트 |
| Trigger | INSERT/UPDATE/DELETE 시 자동 호출되는 코드 | 자동 알람 |
| Parameter | 호출 시 전달되는 입력/출력 값 | 재료 |
> 요약: 데이터베이스 서버 측 로직 구현을 통한 중앙 집중 관리

## Ⅲ. 절차
  Define -> Compile -> Call/Event -> Execute
1. Definition: 비즈니스 로직을 포함한 SQL/PL-SQL 작성
2. Compilation: 구문 분석 및 최적화 후 바이너리 저장
3. Triggering: 호출 명령 또는 데이터 변경 이벤트 발생
4. Execution: 서버 내 캐시된 계획을 사용하여 즉시 실행
> 요약: 사전 정의된 로직의 서버 측 실행으로 응답 속도 향상

## Ⅳ. 문제점
- 서버 CPU 부하 가중 및 애플리케이션-DB 간 로직 분산에 따른 관리 어려움
- 트리거의 연쇄 호출(Chaining) 시 예기치 못한 부작용 및 디버깅 난해

## Ⅴ. 개선방안
- 연산 중심 로직은 앱 서버로, 데이터 중심 로직만 DB 서버로 배치
- 트리거 사용을 최소화하고 명시적인 트랜잭션 로그 기반 처리

## Ⅵ. 전망
- 서버리스 환경과의 연동을 위한 클라우드 트리거 및 데이터 거버넌스 자동화 도구로의 발전
