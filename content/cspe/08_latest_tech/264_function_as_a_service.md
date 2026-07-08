---
title: "Function as a Service 서비스형 함수 (Function as a Service)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 264
extra:
  question_no: "264"
  exam_status: "기출"
  exam_history: "122회, 136회"
---

## 미리 알고가기

- FaaS는 서버리스의 대표 구현 형태로 함수 단위 코드를 이벤트에 따라 실행함
- 매우 짧고 무상태인 처리에 강하며 장기 세션 서비스에는 제약이 큼
- 서버리스가 상위 개념이라면 FaaS는 그중 함수 실행 모델에 초점을 맞춘 하위 개념임

## Ⅰ. 개요

- **정의/개념**: Function as a Service는 개발자가 함수 단위 코드를 등록하면 이벤트 발생 시 플랫폼이 해당 함수를 짧게 실행하고 호출 수와 실행 시간 기준으로 과금하는 서버리스 실행 모델임
- **배경/필요성**: 세밀한 이벤트 처리와 빠른 배포와 운영 단순화를 원하는 클라우드 애플리케이션이 늘면서 함수 단위의 초경량 실행 모델이 확산됨

## Ⅱ. 특징

- 함수 단위 배포로 단순한 이벤트 처리에 적합함
- 자동 확장과 종량 과금으로 간헐적 트래픽 대응이 효율적임
- 실행 시간과 메모리와 로컬 상태 유지에 제약이 많음
- 이벤트 소스와 관리형 서비스 연계성이 높음

## Ⅲ. 종류 및 비교

| 판단 기준 | FaaS | Serverless Container | Traditional Microservice |
|:---|:---|:---|:---|
| 배포 단위 | 함수 | 컨테이너 이미지 | 장기 실행 서비스 |
| 실행 시간 | 짧음 | 중간 | 길음 |
| 상태성 | 무상태 지향 | 제한적 상태 가능 | 상태 설계 자유 |
| 적합 업무 | 이벤트 핸들러 | 경량 API | 지속 서비스 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Function Code | 이벤트를 받아 단일 책임 작업을 수행하는 배포 단위 코드임 |
| Trigger Binding | HTTP와 큐와 스토리지 이벤트를 함수와 연결해 자동 실행되도록 하는 바인딩 계층임 |
| Stateless Runtime | 함수 인스턴스를 짧게 실행하고 종료해 무상태 처리 모델을 유지하는 실행 계층임 |
| Permission Boundary | 함수가 접근할 리소스와 권한을 최소 범위로 제한하는 보안 경계임 |
| Monitoring and Retry | 호출 성공 여부와 재시도와 로그를 관리해 이벤트 처리 신뢰성을 높이는 운영 계층임 |

```text
+---------+    +---------------+    +----------------+    +--------------+
| Trigger | -> | Function Code | -> | External State | -> | Monitor/Retry|
+---------+    +---------------+    +----------------+    +--------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 이벤트 발생   | -> | 함수 기동    | -> | 비즈니스 처리 | -> | 결과 저장    | -> | 종료 및 재시도 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **이벤트 발생**: 외부 시스템이 트리거를 생성함
2. **함수 기동**: 플랫폼이 함수 실행 환경을 준비함
3. **비즈니스 처리**: 함수가 입력을 처리하고 외부 자원을 호출함
4. **결과 저장**: 상태는 DB나 큐 같은 외부 시스템에 남김
5. **종료 및 재시도**: 실행을 끝내고 실패 시 재시도 정책을 적용함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 함수가 외부 상태와 네트워크 호출에 과도하게 의존하면 짧은 실행 모델과 충돌해 실패율과 지연이 커질 수 있음
   - 해결방안: idempotent design과 async event choreography를 적용하고 retry success rate와 function timeout rate로 검증함
2. 문제: 세밀한 함수 분할이 지나치면 호출 체인이 길어져 관측성과 디버깅 복잡도가 증가할 수 있음
   - 해결방안: bounded function granularity와 trace propagation을 적용하고 end to end trace completeness와 mean time to diagnose로 검증함
3. 문제: 권한 설정이 넓으면 짧은 코드라도 침해 시 외부 자원 피해가 커질 수 있음
   - 해결방안: least privilege IAM과 secret isolation을 적용하고 privileged action count와 unauthorized access incident rate로 검증함

## Ⅶ. 적용 사례

- 이벤트 처리 파이프라인이 비동기 오케스트레이션을 적용하며 확인 지표는 retry success rate와 function timeout rate임
- 마이크로 자동화 시스템이 분산 추적을 운영하며 확인 지표는 end to end trace completeness와 mean time to diagnose임
- 클라우드 함수 플랫폼이 최소 권한 정책을 적용하며 확인 지표는 privileged action count와 unauthorized access incident rate임

## Ⅷ. 결론

FaaS는 이벤트 중심 초경량 실행에 강하지만 함수 경계와 외부 상태와 권한 모델을 정교하게 설계해야 운영 복잡도가 억제됨.
