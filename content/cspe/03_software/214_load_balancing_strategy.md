---
title: "로드 밸런싱 전략 (Load Balancing Strategy)"
date: "2026-07-11"
tags:
  - "cspe-software"
weight: 214
extra:
  question_no: "214"
  exam_status: "미출제"
---

## 미리 알고가기

- 로드 밸런싱은 정상 Backend 집합에서 연결·요청을 선택 정책에 따라 분배하고 장애·과부하 대상을 제외하는 기능임
- L4는 IP·Port·Connection, L7은 HTTP Host·Path·Header·Cookie·요청 상태를 기준으로 대상을 선택함
- Round Robin은 요청 비용이 비슷할 때, Least Request는 처리 시간이 다른 요청이 섞일 때 선택 근거가 생김
- Consistent Hash는 사용자·키를 같은 Backend에 연결해 Cache·Session 지역성을 유지하지만 Backend 변경 시 일부 키가 이동함
- Retry·Slow Start·Outlier Ejection을 함께 조정하지 않으면 장애 Backend의 요청이 다른 Backend에 재시도되어 부하가 증폭됨

## 작성 근거(검토용)

- 로드 밸런싱은 정상 Backend, 선택 입력, 요청 비용, 상태 추적, 지역성, 장애 제외, 연결 종료를 핵심 축으로 설명함
- 비교표는 각 알고리즘의 선택 기준·필요 상태·적합 부하·유의점을 같은 질문으로 대비함
- API와 분산 Cache는 p99 지연·최대 Backend Queue·키 이동률·Cache 적중률로 검증함

## Ⅰ. 개요

- **정의/개념**: 로드 밸런싱은 Listener가 요청 특성과 Backend 상태를 확인하고 선택 알고리즘·가중치·지역성에 따라 정상 Backend로 연결·요청을 전달하는 트래픽 분배 구조임
- **배경/필요성**: Instance별 처리 용량·요청 시간·상태 데이터가 다르고 장애·확장이 발생하므로 고정 순환이 아닌 관측 가능한 선택 기준과 제외·복귀 절차가 필요함

## Ⅱ. 특징

- Active·Passive Health Check와 Outlier Detection으로 연결 실패·오류·지연 기준을 넘은 Backend를 제외함
- Connection Pool과 HTTP/2·gRPC Multiplexing에서는 Connection 수와 실제 진행 Request 수가 다르므로 알고리즘 입력을 구분함
- Weight가 정적 용량인지 실시간 부하 보고인지 정하고 새·복구 Backend에는 Slow Start로 요청 비율을 늘림
- Zone·Region 우선순위와 Spillover 기준으로 로컬 처리와 장애 시 원격 전환 범위를 정함
- Session Affinity와 Hash Key는 상태 지역성을 제공하지만 특정 사용자·키 편중과 Scale-In 시 재배치를 유발함
- Connection Draining과 최대 요청 시간을 설정해 배포·Scale-In 중 신규 배정과 진행 요청 종료를 분리함

## Ⅲ. 종류 및 비교

| 알고리즘 | 선택 기준 | 필요한 상태 | 적합 부하 | 유의점 |
|:---|:---|:---|:---|:---|
| Round Robin | 정상 Backend 순환 순서 | Backend 목록·현재 위치 | 요청 비용과 Backend 용량이 비슷함 | 장기 요청·용량 차이를 반영하지 않음 |
| Weighted Round Robin | 정적·동적 Weight 비율 | Backend별 Weight | Instance 용량·할당량이 다름 | Weight 산정 주기와 Slow Start 필요 |
| Least Request·P2C | 후보의 진행 Request 수 | Backend별 활성 Request | 요청 처리 시간이 서로 다름 | 진행 수가 실제 CPU·Queue 비용과 다를 수 있음 |
| Least Time·EWMA | 관측 지연과 진행 Request | 최근 지연·오류 표본 | Backend 지연 편차가 지속됨 | 표본 지연·급격한 복귀에 완화 기준 필요 |
| Consistent Hash·Maglev | 사용자·Session·Data Hash | Hash Ring·Table·Backend 집합 | Cache·Session·Shard 지역성 필요 | Hot Key와 Backend 변경 시 키 이동 발생 |

> 요약: 균등 비용은 Round Robin, 진행 요청 차이는 Least Request, 지연 편차는 EWMA, 상태 지역성은 Consistent Hash로 반영함.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Listener·Protocol Parser | L4 Connection 또는 L7 요청의 분배 입력을 추출함 |
| Service Discovery·Backend Pool | 주소·Zone·Version·Weight와 정상 Backend 집합을 제공함 |
| Health·Outlier Detector | Probe·연결 실패·오류·지연으로 Backend 제외·복귀를 결정함 |
| Selection Algorithm | 순서·Weight·진행 요청·지연·Hash로 대상을 선택함 |
| Connection Pool·Queue | Backend 연결을 재사용하고 동시 요청·대기 한도를 적용함 |
| Retry·Drain·Telemetry | 재시도 예산·종료 연결과 Backend별 요청·오류·지연을 관리함 |

```text
Client -> Listener -> Healthy Backend Pool -> Selection Policy -> Backend
                         Health·Outlier          Queue·Retry·Drain
```

> 요약: Discovery·Health가 후보 집합을 만들고 선택 알고리즘이 요청 특성·부하 상태로 Backend를 정함.

## Ⅴ. 원리 및 절차 흐름도

```text
요청 수신 -> 후보 필터링 -> 정책 입력 계산 -> Backend 선택 -> 전달·관측 -> 제외·복귀
```

1. **요청 수신**: Listener가 Connection과 L7 Route·Hash Key·Session 정보를 해석함
2. **후보 필터링**: Health·Zone·Version·Circuit 상태로 선택 가능한 Backend를 구성함
3. **정책 입력 계산**: Weight·진행 Request·지연 표본·Hash 값을 알고리즘에 제공함
4. **Backend 선택**: 정책 결과에 따라 연결 Pool을 얻고 요청을 전달함
5. **관측·상태 전이**: 지연·오류·Queue를 갱신하고 Outlier 제외·Slow Start 복귀·Drain을 수행함

> 요약: 정상 후보를 먼저 정한 뒤 요청 비용·부하·지역성 입력으로 Backend를 선택하고 결과를 다음 선택에 반영함.

## Ⅵ. 실무 사례

1. API Cluster는 Least Request와 Outlier 제외를 적용하고 p99 지연·최대 Backend Queue 길이를 확인함
2. 분산 Cache는 Consistent Hash와 Virtual Node를 적용하고 Backend 변경 시 키 이동률·Cache 적중률을 확인함

## Ⅶ. 결론

- 로드 밸런싱은 요청 비용·Backend 용량·상태 지역성·Health·재시도·Drain을 측정 가능한 선택 정책으로 연결해야 함
