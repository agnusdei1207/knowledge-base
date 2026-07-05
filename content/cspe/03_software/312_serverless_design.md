---
title: 서버리스 아키텍처 설계 (Serverless Design)
date: 2026-07-05
tags: [cspe-software]
weight: 312
---

## Ⅰ. 개요
- 정의: 서버의 관리/운영을 클라우드 업체에 맡기고 개발자는 코드 구현에만 집중함
- 배경: 인프라 관리 부담 해소 및 사용한 만큼 지불(Pay-as-you-go)하는 비용 효율성 지향
- 출제 의도: FaaS(Function as a Service) 및 BaaS 기반의 이벤트 기반 설계 이해도 확인

## Ⅱ. 구성요소
- ASCII 구조도
  [Event Trigger] -> [FaaS (Logic)] -> [BaaS (Storage)]
  (S3, API, DB)     (AWS Lambda)       (DynamoDB)
- 구성요소 표
| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| FaaS | 이벤트에 의해 실행되는 코드 조각(함수) | 자판기 작동 |
| BaaS | 직접 구현하지 않고 빌려 쓰는 백엔드 서비스 | 외주 배달 |
| 트리거 | 함수를 깨우는 외부 자극(HTTP 요청, 파일 업로드) | 센서 벨 |
> 요약: 인프라를 추상화하고 이벤트 트리거-비즈니스 로직-관리형 서비스로 구성함

## Ⅲ. 절차
- ASCII 흐름도
  Event Analysis -> Function Design -> State Mgmt -> Optimization
- 4단계 설명
1. Event Analysis: 함수 실행을 유발하는 트리거와 데이터 흐름 분석함
2. Function Design: 단일 책임 원칙에 따라 짧고 간결한 함수로 구현함
3. State Mgmt: 함수 간 상태 공유를 위해 외부 저장소(Redis 등) 연동 설계함
4. Optimization: 콜드 스타트(Cold Start) 지연 최소화 및 실행 메모리 설정함
> 요약: 이벤트를 식별하여 무상태 함수를 설계하고 성능을 최적화함

## Ⅳ. 문제점
- 원인이 명시된 문제/한계: 초기 호출 시 발생하는 지연(Cold Start) 및 디버깅의 어려움 존재함

## Ⅴ. 개선방안
- Ⅳ의 문제에 대응하는 방안: 웜업(Warm-up) 기법 적용 및 분산 추적(Distributed Tracing) 활용함

## Ⅵ. 전망
- 발전 방향: 엣지(Edge) 기반 서버리스 컴퓨팅 확대로 사용자 인접 초저지연 서비스 실현
- CSF: 긴 실행 시간(Timeout) 제약 고려와 함수 간 연쇄 호출(Chaining) 최적화가 관건임
