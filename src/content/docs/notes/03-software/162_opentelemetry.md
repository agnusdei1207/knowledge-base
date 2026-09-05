---
sidebar:
  order: 162
  label: "162. OpenTelemetry"
  badge:
    text: "기출 · 70%"
    variant: note
title: "OpenTelemetry (OpenTelemetry)"
date: "2026-08-31T10:48:00+09:00"
tags:
  - "notes-software"
weight: 162
extra:
  question_no: "162"
  source_status: "기출"
  source_history: "135회"
  priority: 70
  priority_note: "관측 신호 수집 표준의 구조와 적용 출제"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **OpenTelemetry(OTel)**: Metrics, Logs, Traces를 벤더 중립적으로 생성·수집·가공·전송하기 위한 CNCF 표준 오픈소스 프레임워크.
- **Auto-Instrumentation**: 소스코드 수정 없이 Java Agent 바이트코드 조작이나 eBPF를 통해 HTTP, DB 호출을 자동 계측.
- **Collector Pipeline**: 수신(Receiver) $\to$ 가공(Processor) $\to$ 전송(Exporter) 3단계로 구성된 모듈형 텔레메트리 가공 파이프라인.

</details>

- 정의/개념: 메트릭·로그·추적을 OTLP로 수집·가공·전송하는 표준 프레임워크
- 배경/필요성: 모니터링 벤더별 전용 SDK/프로토콜 사용으로 인한 극심한 벤더 종속(Lock-in), 다중 에이전트 중복에 따른 성능 저하 및 백엔드 교체 시 소스코드 전면 재작성 한계

#### 한줄 요약
- OTel 표준 SDK와 수집기로 코드 수정 없이 다중 백엔드 전송

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **OTLP (OpenTelemetry Protocol)**: 텔레메트리 데이터를 초고속으로 인코딩하여 전송하기 위한 OTel 전용 표준 프로토콜.

</details>

- 백엔드 교체 시에도 애플리케이션 코드 수정을 배제하는 완전한 벤더 중립성
- Java Agent 등을 통한 소스코드 무수정 자동 계측(Auto-Instrumentation)
- PII 마스킹, 샘플링, 다중 백엔드 전송을 전담하는 OTel Collector 파이프라인

#### 한줄 요약
- 벤더 중립성·자동 계측·수집기 파이프라인으로 표준 관측성 제공

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **OTel 3대 핵심 아키텍처**: App Instrumentation(OTel API/SDK), Collector Layer(Receiver/Processor/Exporter), Backend Storage.

</details>

```text
[OpenTelemetry 파이프라인 아키텍처 구조]
|-- OTel API
|   `-- 벤더 비종속 계측 추상화 인터페이스 제공
|-- OTel SDK
|   `-- 인메모리 버퍼링 및 OTLP 패킷 직렬화 전송
|-- OTel Collector
|   |-- Receiver (OTLP, Prometheus 등 다중 신호 수신)
|   |-- Processor (PII 토큰 마스킹 및 메모리 상한 제어)
|   `-- Exporter (Tempo, Loki 등 다중 백엔드 저장소 라우팅)
`-- OTLP 프로토콜
    `-- 메트릭, 로그, 추적 신호 초고속 압축 전송
```

| 구성요소 | 책임 | 주요 특징 |
|:---|:---|:---|
| OTel API (인터페이스) | 애플리케이션에서 메트릭·스팬 생성을 위한 추상 인터페이스 제공 | 무의존성 명세 |
| OTel SDK (구현체) | 문맥 전파·샘플링을 수행하고 OTLP 패킷으로 직렬화 전송 | 런타임 바인딩 |
| OTel Collector (수집기) | 수신·가공·전송 파이프라인으로 데이터 가공 및 라우팅 | 독립 프록시 데몬 |
| OTLP (전송 프로토콜) | Protobuf 기반 메트릭·로그·추적 신호 초고속 압축 전송 | gRPC Port 4317 |

#### 한줄 요약
- API가 계측 지점을, Collector가 전송 대상을 각각 격리해 두므로 SDK 구현이나 저장 백엔드가 바뀌어도 애플리케이션 코드는 손대지 않는다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Collector 처리 5단계**: OTLP 패킷 수신 $\to$ K8s 메타데이터 보강 $\to$ PII 마스킹 $\to$ 배치 및 메모리 제어 $\to$ 다중 백엔드 전송.

</details>

```text
애플리케이션에서 OTLP 텔레메트리 패킷 방출
        │
   1. [Receiver 수신] 포트 4317로 OTLP gRPC 패킷 접수
        │
   2. [Processor 메타 보강] 파드 이름 및 네임스페이스 라벨 주입
        │
   3. [Processor PII 마스킹] 정규식 기반 토큰 및 민감 헤더 마스킹 정제
        │
   4. [Processor 배치 제어] 메모리 리미터 기반 OOM 방지 및 배치 패킹
        │
   5. [Exporter 다중 전송] 메트릭, 트레이스, 로그를 각 저장소로 병렬 전송
```

#### 한줄 요약
- 수집기가 마스킹·배치·재전송을 대신 떠맡아 애플리케이션은 백엔드 장애를 알 필요가 없어지지만, 그만큼 수집기 자체가 새로운 병목이자 메모리 상한 관리 대상이 된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Agent vs Gateway Mode**: 노드마다 데몬셋으로 띄우는 Agent 방식과 중앙 집중 클러스터로 띄우는 Gateway 방식.

</details>

| 비교 항목 | 에이전트 모드 (Agent: DaemonSet) | 게이트웨이 모드 (Gateway: Deployment) |
|:---|:---|:---|
| 배치 토폴로지 | K8s Worker Node마다 데몬셋 배포 | 중앙 K8s 클러스터에 Deployment 배포 |
| 주요 핵심 역할 | 로컬 파드 텔레메트리 초저지연 수집 | 전사 데이터 집계 및 중앙 PII 마스킹 |
| 네트워크 오버헤드 | 로컬 통신으로 오버헤드 최소화 | 중앙 수집기 트래픽 발생 |
| 실무 권장 패턴 | 노드 로컬 1차 수집 전담 | 중앙 집중 2차 가공 및 전송 전담 |

#### 한줄 요약
- 노드 수집은 Agent 모드, 중앙 가공은 Gateway 모드 적용

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Memory Limiter**: 트래픽 폭증 시 OTel Collector가 메모리 부족(OOM)으로 다운되는 것을 막기 위해 임계치 초과 시 데이터를 안전하게 드롭하는 보호 장치.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 민감정보(PII) 유출 | Collector Processor에서 토큰 정제 및 민감 헤더 삭제 | 보안 컴플라이언스 100% 준수 |
| 트래픽 폭증 시 OOM 발생 | Collector에 memory_limiter 및 batch 프로세서 적용 | 수집기 무중단 안정성 확보 |
| 자동 계측 시 CPU 저하 | 계측 스코프를 HTTP 및 DB 쿼리 메서드로 한정 | 앱 CPU 오버헤드 3% 미만 유지 |
| 단일 백엔드 장애 파급 | Exporter에 sending_queue 및 재시도 백오프 설정 | 데이터 유실 방지 및 비동기 격리 |

#### 한줄 요약
- 네 대책은 가공 책임을 수집기에 몰아준 대가로 생긴 메모리·CPU 부담을 상한과 큐로 되묶는 선택이며, 계측 범위를 좁힐수록 오버헤드는 줄고 관측 사각지대는 늘어난다.

## Ⅶ. 결론

- 클라우드 네이티브 관측성(Observability) 생태계의 가장 지배적인 글로벌 텔레메트리 사실상 표준(CNCF Graduate 프로젝트)으로 확립되었으며, 실무 구축 시에는 소스코드 무수정 Java/eBPF 자동 계측(Auto-Instrumentation), PII 민감정보 마스킹 및 OOM을 방어하는 OTel Collector `memory_limiter` 파이프라인, 노드 데몬셋(Agent)과 중앙 집계(Gateway) 2계층 토폴로지 구성, OTLP gRPC(포트 4317) 초고속 직렬화 전송을 결합하여 애플리케이션 오버헤드를 최소화하면서 완전한 데이터 이식성과 보안 거버넌스를 달성

#### 한줄 요약
- OpenTelemetry는 단일 표준 API/SDK와 3단계 Collector 파이프라인을 통해 텔레메트리를 벤더 독립적으로 수집하는 핵심 기술이다.
