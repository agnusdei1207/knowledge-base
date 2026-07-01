---
title: "OpenTelemetry (OTel)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 276
---

# 📖 【암기용】 개념 완전 이해

> 목적: OpenTelemetry를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 클라우드 네이티브 소프트웨어의 관측성 데이터(로그, 메트릭, 트레이스)를 수집, 가공, 전송하기 위한 오픈소스 표준 프레임워크
- **왜 필요한가**: 예전에는 모니터링 도구(Datadog, New Relic 등)마다 수집 방식이 달라서, 도구를 바꾸려면 소스코드를 다 고쳐야 했다(Vendor Lock-in). OpenTelemetry는 "수집 방식"을 하나로 통일해서 어떤 도구든 갈아 끼울 수 있게 해준다.
- **핵심 직관**: 관측성 데이터 수집계의 "USB 표준"이다. 어떤 기기(언어/앱)든 USB 포트(OTel SDK)만 있으면 어떤 충전기(분석 도구)에도 연결할 수 있다.

## 깊이 이해
- **배경·문제의식**: OpenTracing과 OpenCensus라는 두 개의 비슷한 프로젝트가 통합되어 탄생했다. CNCF(Cloud Native Computing Foundation)에서 Kubernetes 다음으로 가장 활발하게 기여가 일어나는 프로젝트일 만큼 클라우드 시대의 필수 기술이 되었다.
- **작동 원리**: **OTLP(OpenTelemetry Protocol)**라는 표준 프로토콜을 사용한다. 앱에 심어진 **SDK**가 데이터를 뽑아내면, **Collector**가 이를 받아서 정해진 형식으로 가공한 뒤, 실제 데이터를 저장하고 보여줄 백엔드(Prometheus, Jaeger 등)로 쏘아준다.
- **비유**: 통역관과 같다. 앱들은 각자 자기 언어(Java, Go, Python 등)로 말하지만, OTel SDK라는 통역관이 이를 "국제 공용어(OTLP)"로 바꿔준다. 덕분에 듣는 사람(분석 도구)이 누구든 상관없이 대화가 통한다.
- **구체 예시**: Java Spring Boot 앱에 OTel Agent를 붙이면 코드 수정 없이도 HTTP 호출 경로(Trace), 메모리 사용량(Metric), 에러 기록(Log)이 자동으로 수집된다.
- **흔한 오해·주의점**: OpenTelemetry는 데이터를 **보여주는(Visualization) 도구가 아니다.** 데이터를 **모아서 전달하는(Collection & Export)** 표준 도구다. 보여주는 건 Grafana 같은 다른 도구의 몫이다.

## 연결 개념
- CNCF — OpenTelemetry가 소속된 오픈소스 재단
- OTLP — 관측성 데이터 전송을 위한 표준 프로토콜
- Sidecar Pattern — OTel Collector를 컨테이너 옆에 띄우는 흔한 배포 방식
- Semantic Conventions — 데이터에 붙이는 이름(태그)을 통일한 규약

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 벤더 독립성(Vendor-neutral)과 통합 수집 구조(Unified Collection)를 중심으로 기술 체계를 서술한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: OpenTelemetry는 분산 시스템의 관측성 데이터(Metrics, Logs, Traces)를 생성, 수집, 가공, 전송하기 위한 공급업체 중립적인(Vendor-neutral) 오픈소스 표준 프레임워크이다.
> 2. **가치**: 단일 표준 프로토콜(OTLP)과 API를 통해 도구 교체 시의 코드 수정 비용을 제거하고, 마이크로서비스 간의 데이터 상관관계(Correlation)를 통합 가시화한다.
> 3. **판단 포인트**: 라이브러리 기반의 SDK 방식과 인프라 기반의 Collector 방식을 조합하여 성능 오버헤드와 운영 유연성 간의 균형을 확보해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| OpenTelemetry의 탄생 배경 및 목적 확인 | 벤더 독립성, OpenTracing+OpenCensus 통합 | 특정 상용 솔루션의 기능으로 오해 |
| 주요 구성요소 및 기술 아키텍처 확인 | API, SDK, Collector, OTLP | 구성요소 간의 흐름(Flow) 누락 |
| 실무 적용 시의 이점 및 고려사항 확인 | 코드 수정 최소화(Auto-instrumentation), 샘플링 | 성능 오버헤드에 대한 언급 누락 |

> 요약: 관측성 데이터의 표준화 규격인 OTLP와 이를 처리하는 구성요소들의 유기적 결합을 설명한다.

---

## Ⅰ. 개요 및 필요성

- 정의: 클라우드 네이티브 환경에서 분산된 서비스들의 관측성 데이터(Traces, Metrics, Logs)를 수집 및 전송하기 위한 CNCF 표준 기술 세트
- 배경: 모니터링 벤더별 파편화된 SDK 사용으로 인한 기술 부채(Lock-in) 증가 및 MSA 환경의 통합 가시성 확보 난항
- 필요성: 일관된 데이터 수집 규격을 통한 시스템 가시성 강화, 도구 선택의 자유도 보장, 운영 복잡성 감소

---

## Ⅱ. 구조 및 구성요소

```text
[ Application ] --(API)--> [ SDK ] --(OTLP)--> [ OTel Collector ] --(Export)--> [ Backend ]
      |                      |                       |                            |
(Instrumentation)       (Processing)            (Aggregation)               (Storage/UI)

[핵심 요소: API/SDK, OTLP, Collector, Instrumentation]
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| API & SDK | 데이터 생성 및 전송 라이브러리 | 언어별(Java, Go 등) 구현체 제공 |
| OTLP | 데이터를 주고받는 표준 프로토콜 | gRPC 및 HTTP/JSON 기반 |
| Collector | 데이터 수집, 가공, 다중 백엔드 전송 중계기 | Receiver, Processor, Exporter 구성 |
| Instrumentation | 소스 코드에 수집 코드를 삽입하는 행위 | 자동(Auto) 및 수동(Manual) 방식 |

> 요약: 애플리케이션 내의 SDK와 외부의 Collector가 표준 프로토콜(OTLP)로 연결되는 구조를 가진다.

---

## Ⅲ. 동작원리 및 흐름도

```text
[동작 흐름: 수집(Receive) -> 가공(Process) -> 전송(Export)]
Receiver (OTLP, Jaeger, Prometheus) -> Processor (Batch, Filter, Attribute)
                                             |
Exporter (Prometheus, Elastic, Datadog) <----+
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Instrumentation | 자동 에이전트 또는 SDK를 통해 요청 시작/종료 시점 데이터 캡처 |
| 2 | 수집(Receive) | Collector가 다양한 포맷의 데이터를 수집하여 내부 공용 포맷으로 변환 |
| 3 | 가공(Process) | 민감 정보 마스킹, 데이터 압축, 메타데이터(Cloud 정보 등) 태깅 |
| 4 | 전송(Export) | 가공된 데이터를 분석 도구(Prometheus, Jaeger 등)가 요구하는 포맷으로 변환 전송 |

> 요약: 다양한 입력 포맷을 표준 형식으로 정규화한 후, 다시 목적지에 맞는 포맷으로 변환하여 전달한다.

---

## Ⅳ. 특징

| 구분 | 내용 | 판단 포인트 |
|:---|:---|:---|
| 중립성 | 특정 모니터링 벤더에 종속되지 않는 독립적 표준 | Vendor Lock-in 방지 |
| 통합성 | 트레이스, 메트릭, 로그를 하나의 SDK/프로토콜로 처리 | 데이터 간 상관관계 분석 용이 |
| 유연성 | 소스 수정 없이 Java Agent 등을 통한 자동 수집 지원 | 도입 장벽 및 운영 공수 절감 |
| 확장성 | 커스텀 Processor나 Exporter를 통해 기능 확장 가능 | 복잡한 기업 환경 요구사항 대응 |

> 요약: '표준화'를 통해 관측성 데이터의 수집 효율성과 활용 자유도를 극대화하는 특징을 가진다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 수동 Instrumentation | 자동 Instrumentation | 선택 기준 |
|:---|:---|:---|:---|
| 구현 방식 | 개발자가 직접 코드에 API 호출 삽입 | Java Agent 등을 사용하여 런타임 주입 | 개발 리소스 가용성 |
| 정밀도 | 매우 높음 (특정 비즈니스 데이터 포함) | 높음 (표준 라이브러리 호출 위주) | 분석 요구사항 상세 수준 |
| 유지보수 | 라이브러리 업데이트 시 코드 수정 필요 | 소스 수정 불필요 | 장기적 운영 비용 |

> 요약: 표준 지표 수집은 자동 방식을 기본으로 하고, 핵심 비즈니스 로직에만 수동 방식을 가미하는 전략이 주효하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 자원 오버헤드 | Collector의 과도한 CPU/메모리 사용 | 샘플링 및 리소스 제한(Limit) 설정 | Collector 노드의 자원 사용률 |
| 네트워크 부하 | 방대한 관측 데이터 전송으로 인한 대역폭 점유 | 데이터 압축 및 로컬 수집(Sidecar) 활용 | 애플리케이션 대비 관측 데이터 트래픽 비중 |
| 버전 호환성 | API/SDK와 Collector 간의 버전 불일치 | Semantic Conventions 준수 및 버전 동기화 | 데이터 전송 실패 및 드랍(Drop) 횟수 |

> 요약: 성능 영향을 최소화하기 위한 샘플링과 배포 모델(Sidecar vs Gateway) 선정이 실무의 핵심이다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 데이터 유실률 | 전체 생성 데이터 대비 수집 성공률 99% 이상 | Collector In/Out 메트릭 비교 |
| 전송 지연 | 수집 후 백엔드 도달까지 5초 이내 | End-to-End 지연 시간 측정 |
| SDK 오버헤드 | 앱 성능 저하(지연 시간 증가) 3% 이내 | 수집 활성화 전후 부하 테스트 비교 |

> 요약: 데이터의 완결성과 함께 애플리케이션 성능에 미치는 영향을 주기적으로 점검해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 다중 클라우드 모니터링 통합: AWS, Azure 등 이기종 환경의 지표를 OTel로 단일화하여 통합 대시보드 구축
2. 분산 서비스 추적: MSA 환경에서 서비스 간 호출 경로를 Trace ID로 엮어 장애 지점을 수초 내에 특정
3. 벤더 전환 전략: 상용 솔루션 비용 최적화를 위해 OTel Collector의 Exporter 설정만 변경하여 다른 솔루션으로 즉시 전환

**결론 (2줄):**
- 기술사 판단: OpenTelemetry는 관측성 데이터 수집의 사실상 표준(De-facto Standard)으로 자리 잡았으며, 이제는 선택이 아닌 필수 인프라 요소이다.
- 향후 방향: 로그(Logs) 지원이 안정화됨에 따라 3대 기둥의 완벽한 통합이 이루어지고, AI 기반 분석 도구들과의 연동이 가속화될 것이다.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "OpenTelemetry에 대해 설명하시오" | API, SDK, Collector 아키텍처 및 OTLP | 벤더 독립성 및 데이터 통합 이점 |
| 요구사항 명시형 | "벤더 종속성 없는 관측성 체계 구축 방안" | Collector의 Receiver/Exporter 구성 전략 | 도구 전환(Migration) 용이성 및 고려사항 |
| 기술 심화형 | "분산 시스템 가시성 확보 기술" | Trace Context Propagation(문맥 전파) 원리 | 자동 수집(Auto-instrumentation) 메커니즘 |
