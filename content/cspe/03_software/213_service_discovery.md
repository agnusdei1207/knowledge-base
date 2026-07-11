---
title: "서비스 디스커버리 (Service Discovery)"
date: "2026-07-11"
tags:
  - "cspe-software"
weight: 213
extra:
  question_no: "213"
  exam_status: "미출제"
---

## 미리 알고가기

- 서비스 디스커버리는 동적으로 생성·종료되는 Instance의 주소·Port·상태·Metadata를 이름으로 조회하는 기능임
- Service Registry는 등록 정보의 원본이며 DNS·Resolver·Client Cache는 이를 호출 경로에 맞게 배포함
- Client-Side 방식은 Client가 Registry를 조회해 Instance를 선택하고 Server-Side 방식은 Proxy·Load Balancer가 선택함
- Health Check 실패와 등록 Lease 만료 후 주소 제거가 늦으면 종료 Instance 호출이 계속됨
- Discovery는 주소 발견만 담당하므로 Retry·Circuit Breaker·Timeout·인증 정책은 호출 계층에서 별도로 설계해야 함

## 작성 근거(검토용)

- 서비스 디스커버리는 등록·상태 확인·조회·선택·Cache·제거와 주소 최신성을 핵심 축으로 설명함
- 비교표는 Client-Side와 Server-Side 방식의 조회·선택 위치·결합·갱신·장애 범위·적합 조건을 대비함
- 내부 서비스와 API Gateway는 제거 전파 시간·종료 주소 호출률·정상 Backend 비율로 검증함

## Ⅰ. 개요

- **정의/개념**: 서비스 디스커버리는 Service Instance의 동적 주소와 상태를 Registry에 등록하고 Client 또는 Proxy가 논리 이름으로 정상 Instance를 조회·선택하는 위치 투명화 구조임
- **배경/필요성**: Auto Scaling·재배포·장애 복구로 Instance 주소가 바뀌어도 호출자가 설정 파일을 다시 배포하지 않고 정상 Backend 집합을 사용할 수 있어야 함

## Ⅱ. 특징

- Instance 또는 배포 Agent가 Service Name·Address·Port·Zone·Version·Weight를 Registry에 등록함
- Heartbeat·Active Probe·Readiness 결과와 Lease 만료로 호출 가능한 Instance 집합을 갱신함
- Resolver가 Registry·DNS 응답을 TTL 동안 Cache하고 갱신 실패 시 사용할 마지막 정상 목록의 범위를 정함
- Client 또는 Proxy가 Round Robin·Least Request·Zone·Version 규칙으로 정상 Instance를 선택함
- 종료 시 사전 등록 해제·Readiness 실패·Connection Draining 순서를 적용해 진행 요청과 신규 호출을 분리함
- Registry 복제 지연·DNS TTL·Client Cache 때문에 남은 종료 주소 호출률과 등록 전파 시간을 관측함

## Ⅲ. 종류 및 비교

| 판단 기준 | Client-Side Discovery | Server-Side Discovery |
|:---|:---|:---|
| Registry 조회 | Client Library·Sidecar가 조회 | Proxy·Load Balancer가 조회 |
| Instance 선택 | Client가 Load Balancing | 중계 계층이 Backend 선택 |
| Client 결합 | Registry API·Resolver·정책 Library 포함 | 논리 Endpoint·Proxy 계약만 사용 |
| 목록 갱신 | Client별 Cache·TTL·Watch 관리 | Proxy Fleet가 Backend 목록 관리 |
| 장애 범위 | Client Library·Cache 오류가 해당 Client에 영향 | Proxy·Control Plane 오류가 다수 Client에 영향 |
| 관측 위치 | Client 호출 Metric·Trace | Proxy Access Log·Backend Metric |
| 적합 조건 | 내부 호출에서 Client별 Zone·Version 선택 필요 | 외부·다언어 Client의 Discovery 정책 통합 필요 |

> 요약: Client-Side는 호출자가 Registry 조회와 Instance 선택을 수행하고 Server-Side는 Proxy가 정상 Backend를 선택함.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Service Instance·Registrar | 주소·Port·Metadata를 등록하고 Lease를 갱신함 |
| Health Checker | Liveness·Readiness·업무 Probe로 호출 가능 상태를 판정함 |
| Service Registry | Service Name별 Instance·상태·Version과 Lease를 저장함 |
| DNS·Resolver·Watch | Registry 변경을 이름 조회·Stream 갱신·Cache로 전달함 |
| Load Balancer·Proxy | 정상 Instance 중 Zone·Weight·부하 정책으로 대상을 선택함 |
| Deregistration·Drain | 종료 Instance를 목록에서 제거하고 기존 연결을 마무리함 |

```text
Instance -> Register·Heartbeat -> Service Registry
Client -> Resolver|Proxy -> Healthy Instance List -> Selected Instance
```

> 요약: Registry가 Lease·상태가 유효한 Instance 목록을 제공하고 Resolver·Proxy가 이를 호출 대상 선택에 반영함.

## Ⅴ. 원리 및 절차 흐름도

```text
Instance 등록 -> Health·Lease 갱신 -> 이름 조회 -> Instance 선택 -> 호출 -> 등록 해제·Drain
```

1. **Instance 등록**: Registrar가 논리 Service Name과 Address·Port·Metadata를 Registry에 기록함
2. **상태 갱신**: Heartbeat와 Health Check가 Lease와 호출 가능 여부를 유지함
3. **이름 조회**: Resolver·Proxy가 Registry·DNS에서 정상 Instance 목록을 받고 TTL·Watch로 갱신함
4. **Instance 선택**: Zone·Version·Weight·부하 정책으로 Backend를 정하고 요청을 전달함
5. **종료 처리**: Readiness를 내리고 등록을 해제한 뒤 기존 연결을 Drain해 주소를 제거함

> 요약: 등록·Health·Lease가 정상 주소 집합을 만들고 조회·선택·Drain이 동적 Instance의 호출 수명주기를 완성함.

## Ⅵ. 실무 사례

1. 내부 서비스 호출은 Registry Watch와 Client-Side 부하분산을 적용하고 제거 전파 시간·종료 주소 호출률을 확인함
2. API Gateway는 Server-Side Discovery와 Health Check를 적용하고 정상 Backend 비율·장애 전환 시간을 확인함

## Ⅶ. 결론

- 서비스 디스커버리는 등록 주체·상태 기준·조회 위치·Cache TTL·종료 전파·Registry 장애 범위를 함께 설계해야 함
