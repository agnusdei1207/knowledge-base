---
sidebar:
  order: 87
  label: "087. 모델 DoS (Model Denial of Service)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "모델 DoS (Model Denial of Service)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-security"
weight: 87
extra:
  question_no: "087"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "138회 최신 기출이며 추론 자원 고갈 통제가 중요함"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **DoS(Denial of Service)**: 시스템 자원을 고갈시켜 인가된 사용자의 정상적인 서비스 이용을 방해하는 거부 공격이다.
- **모델 DoS(Model Denial of Service / Model DoS)**: 비대칭적 고비용 추론 요청, 100k 이상의 초장문 프롬프트, 무한 도구 호출(Tool Loop)을 의도적으로 유발하여 LLM의 연산 자원, 메모리, 클라우드 API 예산을 고갈시키는 보안 공격 기법이다.
- **GPU(Graphics Processing Unit)**: AI 모델의 트랜스포머 매트릭스 병렬 연산을 처리하는 핵심 하드웨어 가속기이다.
- **API(Application Programming Interface)**: LLM 추론 서비스를 클라이언트에게 제공하는 REST/gRPC 통신 접속점이다.
- **AI(Artificial Intelligence)**: 자연어, 이미지, 데이터를 지능적으로 추론 집행하는 소프트웨어 체계이다.
- **요청별 비용 차이(Asymmetric Resource Consumption / Cost Difference)**: 전통적 Web DoS와 달리, 단 1개의 요청일지라도 컨텍스트 토큰 크기 및 반복 Tool Call 여부에 따라 서버 자원 소모량이 1,000배 이상 급증하는 비대칭 특성이다.

</details>

- 정의/개념: 모델 DoS(Model Denial of Service)는 공격자가 100k 토큰 이상의 대용량 컨텍스트 주입, 악의적 초장문 출력 유도, 또는 에이전트 무한 도구 호출(Infinite Tool Loop)을 제출하여 AI 시스템의 **GPU** 메모리, KV 캐시, API 연산 예산을 마비시키는 서비스 거부 기술이다.
- 배경/필요성: 단순 IP 기반 요청 수(RPS) 제한만으로는 단 1건의 악의적 고비용 프롬프트 공격을 막을 수 없어, 토큰 단위의 비대칭 자원 소비를 런타임 통제하는 가버넌스가 필수이기 때문이다.

#### 한줄 요약

- 초장문 문맥 입력과 무한 도구 호출을 유도하여 GPU 연산, KV 캐시 메모리 및 클라우드 API 예산을 고갈시키는 서비스 거부 공격이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **컨텍스트 비용(Context Window Cost / Token Cost)**: 입력/출력 토큰 길이가 길어짐에 따라 트랜스포머 아키텍처의 self-attention 연산량($O(N^2)$)과 KV 캐시 메모리가 폭발적으로 늘어나는 비용 특성이다.
- **도구 순환(Infinite Tool Loop / Recursive Tool Execution)**: AI 에이전트가 완결 조건을 찾지 못해 외부 API, DB 검색, 코드 실행을 무한히 재귀 호출하여 외부 시스템 자원까지 마비시키는 현상이다.
- **테넌트 공정성(Multi-Tenant Fairness / SLA Guarantee)**: 멀티 테넌트 SaaS 환경에서 특정 1개 사용자의 고비용 DoS 요청으로 인해 다른 사용자의 추론 응답 속도가 보장되지 못하는 현상이다.

</details>

- 단 1건의 요청만으로 $O(N^2)$ 자원 점유를 유발하는 비대칭적 자원 고갈(Asymmetric Amplification) 특성을 가진다.
- 외부 API, DB 조회가 얽힌 **도구 순환**을 통해 2차 연쇄 도시(Cascading DoS) 및 클라우드 과금 폭탄(Sponge Attack)을 야기한다.
- 멀티 테넌트 SaaS 서비스의 **테넌트 공정성** 유지를 위해 토큰 가중치 쿼터 및 런타임 샌드박싱 조치를 강제한다.

#### 한줄 요약

- 토큰 연산 비대칭 자원 고갈, 연쇄적 도구 순환 과금 폭탄 및 테넌트 공정성 파괴 특성을 지닌다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **비용 추정(Cost Estimation / Token Pre-computation)**: 프롬프트 수신 즉시 입력 토큰 수, 예상 출력 길이, Tool 호출 가능성을 정밀 계산하여 자원 하중을 사전 추정하는 모듈이다.
- **입장 제어(Admission Control)**: 사전 추정된 자원 하중이 현재 GPU 용량이나 사용자의 잔여 예산을 초과 시 추론 집행을 즉시 거부하거나 큐에 수용하는 통제 관문이다.
- **쿼터(Resource Quotas / Rate Limiting)**: 사용자/테넌트별 분당 토큰(TPM), 분당 요청(RPM), 일일 최대 연산 금액을 지정하는 제한 정책이다.
- **회로 차단기(Circuit Breaker)**: 런타임 중 특정 프롬프트가 예상을 깨고 도구 호출 무한 루프나 초장문 토큰을 뿜어낼 때 즉시 연결을 강제 끊어버리는 2차 방화벽이다.

</details>

```text
모델 DoS 방어 구조
├─ 요청 경계
│  ├─ 인증 게이트웨이
│  └─ 비용 추정기
├─ 자원 배분 경계
│  ├─ 입장 제어기
│  └─ 공정 스케줄러
└─ 실행 경계
   └─ 예산·회로 차단기
```

선의 의미: 인증/비용 추정기 요청 경계, 입장 제어/스케줄러 자원 배분 경계 및 예산/회로 차단기 실행 경계를 정합 연계한 방어 구조이다.

| 방어 도메인 계층 | 핵심 구성 요소 | 주요 기능 및 책임 |
|:---|:---|:---|
| 요청 경계 | 인증 게이트웨이, **비용 추정**기 | 프롬프트 토큰화 사전 카운트 및 예상 API 연산 비용 정량 추정 |
| 자원 배분 경계 | **입장 제어**기, 공정 스케줄러 | 사용자별 **쿼터**(TPM/RPM) 대조, GPU 무부하 슬롯을 고려한 입장 허용/거부 |
| 실행 경계 | **회로 차단기** (Circuit Breaker) | 런타임 중 Max Tokens 초과 또는 **도구 순환** 무한 루프 감지 시 프로세스 강제 종료 |

#### 한줄 요약

- 비용 추정기 요청 심사, 입장 제어기의 TPM/RPM 쿼터 집행 및 런타임 회로 차단기(Circuit Breaker) 조치로 방어 라인을 구축한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **가중 쿼터(Weighted Quotas / Token-bucket Rate Limiter)**: 요청 단순 건수(RPS)가 아니라 입력/출력 토큰 수와 사용된 모델 체급(7B vs 70B)을 종합 계산하여 쿼터를 차감하는 방식이다.
- **축소 응답(Degraded Response / Graceful Degradation)**: 자원 고갈 및 과부하 시 시스템 전체 다운 대신 하위 체급 모델(예: GPT-4o $\rightarrow$ GPT-4o-mini)로 자동 스위칭해 서비스를 계속 제공하는 품질 완화 기법이다.
- **입력 토큰•문맥 확장(Input Token & Context Window Amplification)**: 100k 토큰 이상의 무의미한 장문 입력을 프롬프트에 주입하는 공격 단계이다.
- **병렬 작업•대기열 누적(Parallel Job & Queue Bottleneck)**: 동일 IP/계정에서 고비용 프롬프트를 다량 분산 제출하여 큐를 꽉 채우는 단계이다.
- **반복 추론•도구 자원 소비(Recursive Inference & Tool Resource Exhaustion)**: LLM이 반복 토큰 생성 및 외부 API 재귀 호출을 집행하는 자원 고갈 단계이다.
- **메모리•연산 슬롯 고갈(Memory & Compute Slot Exhaustion)**: GPU KV 캐시 메모리가 방전되고 정상 인스턴스가 멈추는 단계이다.
- **지연•오류•서비스 거부 전파(Latency & Cascading Denial-of-Service Propagation)**: 정상 멀티 테넌트 사용자의 추론 요청이 타임아웃 504 오류를 뿜으며 마비되는 타격 단계이다.

</details>

```text
대형 문맥·병렬 추론 요청
              |
              v
1. 입력 토큰·문맥 확장
              |
              v
2. 병렬 작업·대기열 누적
              |
              v
3. 반복 추론·도구 자원 소비
              |
              v
4. 메모리·연산 슬롯 고갈
              |
        정상 추론 요청
              |
              v
5. 지연·오류·서비스 거부 전파
              |
              v
         지연·실패 결과
```

### 동작 원리

1. **입력 토큰•문맥 확장**: 공격자가 100k 토큰 이상의 비신뢰 고비용 텍스트를 주입한다.
2. **병렬 작업•대기열 누적**: 병렬 멀티 세션을 열어 GPU 추론 대기열 큐를 점유한다.
3. **반복 추론•도구 자원 소비**: 반복적인 긴 토큰 생성 및 외부 API 재귀 호출을 유도한다.
4. **메모리•연산 슬롯 고갈**: vLLM/TGI 엔진의 KV 캐시 메모리가 폭발하며 컴퓨팅 가속기 가용성이 고갈된다.
5. **지연•오류•서비스 거부 전파**: 정상 사용자의 추론 요청이 무한 대기하며 504 타임아웃 장애로 확산된다.

#### 한줄 요약

- 문맥 확장, 병렬 큐 점유, 반복 추론 및 외부 도구 소비, GPU 메모리 고갈, 서비스 거부 장애 확산으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **대량 호출형(Volumetric Request Flood)**: 전통적 DoS처럼 미세 프롬프트 API 호출을 무차별 봇넷으로 수만 건 쏘아 입구를 마비시키는 공격이다.
- **고비용 문맥형(Heavy Context Window Exploitation)**: 적은 단 한 번의 호출에 극대의 토큰(Context)을 채워 넣어서 GPU Self-attention 연산량을 붕괴시키는 공격이다.
- **에이전트 순환형(Recursive Agent Loop)**: LLM 에이전트의 오판을 유도하여 외부 DB/API를 종료 조건 없이 무한 루프 호출하게 만드는 Sponge 공격이다.

</details>

| 모델 DoS 공격 유형 | 대량 호출형 (Volumetric Flood) | 고비용 문맥형 (Heavy Context) | 에이전트 순환형 (Recursive Loop) |
|:---|:---|:---|:---|
| 공격 핵심 수단 | 봇넷을 이용한 무차별 API RPS 주입 | 100k 이상의 단일 초장문 프롬프트 제출 | 무한 루프 유도 프롬프트 주입 (Tool Call) |
| 타격 대상 자원 | API Gateway, Nginx web server | GPU KV 캐시, Self-Attention 연산 | 외부 API 과금 예산, 백엔드 RDBMS |
| 탐지 난이도 | 용이 (RPS 및 IP 주소 이상치 탐지) | 보통 (토큰 카운터로 사전 검출 가능) | 최고 (정상 툴 실행과 루프 탐지 간 경계 애매) |
| 대표 대응 기술 | 전통적 **DDoS** 방화벽, RPS Limit | **비용 추정**, **가중 쿼터** (TPM Limit) | Max Iteration 제한, **회로 차단기** |

#### 한줄 요약

- 대량 호출형(RPS 폭주), 고비용 문맥형(초장문 프롬프트), 에이전트 순환형(무한 툴 루프)으로 세분화된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **OWASP(Open Worldwide Application Security Project)**: 글로벌 애플리케이션 보안 가이드라인 연구 기관이다.
- **LLM10:2025 (OWASP Top 10 for LLM Applications 2025 - LLM10 Model Denial of Service)**: OWASP 2025 위험 10위에 지정된 모델 DoS 방어 규격이다.
- **DDoS(Distributed Denial of Service)**: 분산 봇넷 환경에서 발동하는 대규모 서비스 거부 공격이다.
- **행위 상관분석(Behavioral Correlation Analytics)**: 동일 사용자가 여럿 계정으로 나뉘어 쏘는 고비용 프롬프트의 상관관계를 탐지하는 분석 기술이다.
- **NIST(National Institute of Standards and Technology)**: 미국 국립표준기술연구소이다.
- **NIST 공격 분류(NIST AI Threat Classification)**: AI 시스템의 DoS 자원 고갈 경로를 체계화한 NIST 보안 규격이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| AI 모델 서비스 거부 방어 표준 미비 | **OWASP LLM10:2025** 및 **NIST 공격 분류** 기준 적용 | 전사 LLM 인프라의 토큰/연산 서비스 거부 위험 대응 |
| 1건의 고비용 프롬프트에 의한 GPU 마비 | **가중 쿼터** (TPM), Max Token 제한 및 **비용 추정** | 비대칭 고비용 입력의 GPU 진입 사전 원천 차단 |
| 에이전트 툴 연동 시 무한 루프 과금 폭탄 | Max Iteration 설정, **회로 차단기**, **축소 응답** | 런타임 과금 이상 폭주 차단 및 장애 시 서비스 유지 |

#### 한줄 요약

- OWASP LLM10:2025 및 NIST 지침 준수, TPM 가중 쿼터, Max Token 제한 및 런타임 Circuit Breaker를 적용한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **비용 기반 가용성 통제(Cost-aware Availability Governance)**: 단순 RPS 건수가 아닌 런타임 토큰 수, GPU 연산 시간, 외부 API 과금액을 실시간 측정 종합하여 서비스 가용성을 사수하는 원칙이다.

</details>

- **비용 기반 가용성 통제**에 기반하여 TPM/RPM **가중 쿼터** 설정, **회로 차단기** 및 **축소 응답** 시스템을 체계 구축한다.

#### 한줄 요약

- OWASP LLM10 준수, TPM 가중 쿼터, Max Token/Iteration 제한, Circuit Breaker 및 비용 기반 가용성 통제 체계 구축 필수.