---
title: "레이트 리미팅·스로틀링 (Rate Limiting Throttling)"
date: "2026-07-11"
tags:
  - "cspe-software"
weight: 218
extra:
  question_no: "218"
  exam_status: "미출제"
---

## 미리 알고가기

- Rate Limiting은 사용자·Tenant·API별 시간당 허용량을 넘은 요청을 거부하고 Throttling은 처리 속도·동시성을 낮춰 부하를 조절함
- Token Bucket은 일정 속도로 Token을 채우고 Bucket 용량만큼 Burst를 허용함
- Leaky Bucket은 Queue에서 고정 속도로 요청을 내보내며 Queue가 차면 지연 또는 폐기함
- HTTP 할당량 초과는 429와 Retry-After로 재시도 시점을 알리고 Server 과부하는 503·Load Shedding으로 구분함
- 분산 Limiter는 같은 Key의 원자 Counter·Clock·TTL과 지역별 할당량 합산 기준을 정해야 함

## 작성 근거(검토용)

- Rate Limiting은 식별 Key, Scope, Rate·Burst·동시성, Algorithm, 분산 상태, 응답·재시도, 관측을 핵심 축으로 설명함
- 비교표는 알고리즘별 상태·허용 동작·Burst·오차·적합 조건을 같은 질문으로 대비함
- 외부 API와 내부 추론 서비스는 429 비율·Token 소진·Queue 대기·과부하 오류율로 검증함

## Ⅰ. 개요

- **정의/개념**: 레이트 리미팅·스로틀링은 요청 Identity와 자원 비용을 기준으로 시간당 허용량·Burst·동시 실행 수를 계산해 승인·지연·거부하는 Admission Control 기법임
- **배경/필요성**: 한 소비자의 Burst·재시도와 고비용 요청이 공유 Thread·Connection·DB를 점유해 다른 소비자의 SLO를 침해하지 않도록 처리 전 자원 예산을 배분해야 함

## Ⅱ. 특징

- API Key·사용자·Tenant·IP·Route·업무 비용을 조합한 Limiter Key와 전역·지역·Instance Scope를 정의함
- 요청 수뿐 아니라 Payload Byte·Query Cost·동시 실행·CPU 추정치를 Token 비용으로 반영할 수 있음
- Local Limiter는 네트워크 호출 없이 판정하고 Global Limiter는 여러 Instance의 총 할당량을 일치시킴
- 계층형 할당량은 전역 예산을 Region·Instance에 나눠 일부 상태 저장소 장애에도 제한 범위를 유지함
- 초과 요청은 429·Retry-After, Queue 지연, 우선순위 하향, 연결 폐기 중 Client 계약에 맞는 동작을 선택함
- Client의 Exponential Backoff·Jitter와 Server Retry Budget을 연결해 제한 응답이 동시 재시도로 되돌아오지 않게 함

## Ⅲ. 종류 및 비교

| 알고리즘 | 저장 상태 | 허용 판정 | Burst 특성 | 유의점 |
|:---|:---|:---|:---|:---|
| Fixed Window Counter | Key별 현재 구간 Counter | 구간 한도 전까지 승인 | 경계 양쪽에 요청 집중 가능 | Window 경계 Burst가 실제 Rate를 초과 |
| Sliding Window Log | 허용 요청 Timestamp 목록 | 현재 시점 이전 Window 항목 제거 후 계산 | Window 내 정확한 요청 수 반영 | 요청량에 따라 Timestamp 저장량 증가 |
| Sliding Window Counter | 현재·이전 구간 Counter | 경과 비율로 이전 Counter를 가중 | 경계 Burst를 근사 완화 | 가중 추정값과 실제 요청 수 차이 발생 |
| Token Bucket | Token 수·마지막 충전 시각 | 요청 비용만큼 Token이 있으면 승인 | Bucket 용량만큼 Burst 허용 | 충전 Clock·분산 원자 갱신 필요 |
| Leaky Bucket | 대기 Queue·배출 시각 | 고정 속도로 Queue에서 처리 | 출력 Rate를 평탄화 | Queue 한도 초과 시 지연·폐기 발생 |

> 요약: 고정·슬라이딩 Window는 구간 요청 수, Token Bucket은 Rate와 Burst, Leaky Bucket은 Queue 배출 속도를 통제함.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Identity·Policy | 사용자·Tenant·Route별 Rate·Burst·동시성·우선순위를 정의함 |
| Key·Cost Calculator | 요청 Identity와 Payload·Query 비용을 Limiter Key·Token 비용으로 변환함 |
| Counter·Bucket Store | Window Counter·Token·Timestamp·TTL을 원자적으로 갱신함 |
| Local·Global Coordinator | Instance 제한과 전역 할당량을 배분·동기화함 |
| Admission·Queue | 요청을 승인·지연·거부하고 동시 실행 수를 관리함 |
| Response·Telemetry | 429·Retry-After와 사용량·거부·Queue·정책별 Metric을 제공함 |

```text
Request -> Identity·Cost -> Counter|Bucket -> Admit -> Service
                                      └-> Delay|429|Drop
```

> 요약: Identity·Cost가 정책 Key와 소비량을 만들고 Counter·Bucket 상태가 요청의 승인·지연·거부를 결정함.

## Ⅴ. 원리 및 절차 흐름도

```text
정책 조회 -> Key·비용 계산 -> 상태 충전·정리 -> 원자 판정 -> 승인·지연·거부 -> 사용량 기록
```

1. **정책 조회**: Route·Tenant·Plan에 맞는 Rate·Burst·동시성 한도를 선택함
2. **Key·비용 계산**: 인증 Identity와 요청 자원 비용을 Counter·Bucket Key와 차감량으로 변환함
3. **상태 갱신**: Window 만료 항목을 정리하거나 경과 시간만큼 Token을 충전함
4. **원자 판정**: 현재 사용량과 요청 비용을 비교해 승인·Queue·거부 상태를 한 번에 기록함
5. **응답·관측**: 처리 또는 429·Retry-After를 반환하고 Key·정책별 사용량·거부·대기를 집계함

> 요약: Limiter는 정책별 Key·비용과 현재 Window·Bucket 상태를 원자 비교해 요청 처리 방식을 확정함.

## Ⅵ. 실무 사례

1. 외부 API는 Tenant별 Token Bucket을 적용하고 429 응답률·Bucket 소진 시간을 확인함
2. 내부 추론 서비스는 동시성 제한과 Queue 상한을 적용하고 p99 대기 시간·과부하 오류율을 확인함

## Ⅶ. 결론

- 레이트 리미팅·스로틀링은 Identity·자원 비용·Burst·분산 Scope·초과 응답·Client 재시도를 하나의 예산 정책으로 설계해야 함
