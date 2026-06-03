---
title: 445. 성능 테스트 (Performance Test) 4가지 유형
date: '2026-05-08'
tags:
- studynote-software-engineering
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[282_performance_tactics|성능]] 테스트 ([[282_performance_tactics|Performance]] Test) 4가지 유형은(는) [[001_software_engineering_definition|소프트웨어 공학]]의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[[346_maintainability_portability|유지보수성]]·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

[[282_performance_tactics|성능]] 테스트는 사용자가 몰렸을 때 시스템이 얼마나 잘 버티는지를 본다. 기능이 맞아도 느리면 서비스는 실패한다.

대표 유형은 부하, 스트레스, [[129_spike_agile_technical_investigation|스파이크]], [[449_endurance_soak_test|내구성 테스트]]다. 각각 목표가 다르므로 섞지 않는 것이 중요하다.

- **📢 섹션 요약 비유**: 자동차는 시동만 걸리는 게 아니라, 언덕과 고속도로도 달려 봐야 한다.

---

다음은 [[282_performance_tactics|성능]] 테스트 ([[282_performance_tactics|Performance]] 의 핵심 구조와 흐름을 보여주는 다이어그램이다.

```text
┌─────────────────────────────────────────────────────────────┐
│                  성능 테스트 (Performance                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [입력/요구사항] ──▶ [핵심 처리 과정] ──▶ [출력/결과물]  │
│       │                    │                    │          │
│       ▼                    ▼                    ▼          │
│   요구 분석           설계·적용           품질 검증        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

이 다이어그램은 [[282_performance_tactics|성능]] 테스트 ([[282_performance_tactics|Performance]] 가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 [[395_verification_process_review|검증]]된 결과물을 산출하는 흐름을 보여준다.

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

[[282_performance_tactics|성능]] 테스트는 부하를 점진적으로 높이거나, 급격히 올리거나, 오래 유지하면서 시스템 반응을 본다.

| 유형 | 핵심 질문 |
|:---|:---|
| [[446_load_test|부하 테스트]] | 목표 부하까지 버티는가 |
| [[447_stress_test|스트레스 테스트]] | 한계를 넘으면 어떻게 깨지는가 |
| [[448_spike_test|스파이크 테스트]] | 급증 상황에 즉시 반응하는가 |
| [[449_endurance_soak_test|내구성 테스트]] | 오래 버티며 누수가 없는가 |

```text
부하 증가 -> 반응 확인 -> 병목 확인 -> 한계/복구 확인
```

이 네 가지는 [[282_performance_tactics|성능]]의 서로 다른 면을 보여 준다.

- **📢 섹션 요약 비유**: 사람의 체력도 달리기, 계단, 급출발, 장거리 걷기를 따로 봐야 한다.

---

---

---

---

## Ⅲ. 비교 및 연결

[[282_performance_tactics|성능]] 테스트는 단순 속도 측정이 아니다. 안정성, [[658_ir_recovery|복구]]력, 장시간 운영 능력까지 포함한다.

| 구분 | 보는 것 | 대표 목적 |
|:---|:---|:---|
| 부하 | 목표 [[139_throughput|처리량]] | 정상 한계 [[396_validation|확인]] |
| 스트레스 | 붕괴와 [[658_ir_recovery|복구]] | 한계 반응 [[396_validation|확인]] |
| [[129_spike_agile_technical_investigation|스파이크]] | 순간 급증 | 급격한 변화 대응 |
| 내구성 | 장기 유지 | 누수와 피로 [[396_validation|확인]] |

이 네 유형을 나누면 [[282_performance_tactics|성능]] 문제의 원인을 더 정확히 찾을 수 있다.

- **📢 섹션 요약 비유**: 자동차를 볼 때 최고 속도, 급브레이크, 급가속, 장거리 주행을 따로 본다.

---

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 배포 전 [[395_verification_process_review|검증]], 이벤트 대응, 용량 계획, 인프라 증설 판단에 쓴다. 목표 수치와 측정 지표를 먼저 정해야 한다.

체크 포인트는 다음과 같다.
1. 응답시간, [[139_throughput|처리량]], 오류율을 함께 본다.
2. 임계값과 합격 기준을 명시한다.
3. 실제 사용자 패턴과 비슷하게 만든다.

- **📢 섹션 요약 비유**: 운동선수의 기록은 달리기 속도 하나만으로 결정되지 않는다.

---

---

---

---

## Ⅴ. 기대효과 및 결론

[[282_performance_tactics|성능]] 테스트는 병목과 한계를 미리 보여 준다. 그래서 장애를 예방하고 용량 계획을 세우는 데 유용하다.

결론적으로 이 개념은 "[[282_performance_tactics|성능]] [[395_verification_process_review|검증]]의 큰 우산"이다. 아래의 세부 테스트를 묶어 이해하면 된다.

- **📢 섹션 요약 비유**: 체력 테스트라는 큰 이름 아래 여러 종목이 있는 것과 같다.

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[001_software_engineering_definition|소프트웨어 공학]] ([[001_software_engineering_definition|Software Engineering]]) | [[282_performance_tactics|성능]] 테스트 ([[282_performance_tactics|Performance]] Test) 4가지 유형의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [[003_sdlc|소프트웨어 생명주기]] ([[131_sdlc_system_development_life_cycle_waterfall_agile|SDLC]], Software Development Life Cycle) | [[282_performance_tactics|성능]] 테스트 ([[282_performance_tactics|Performance]] Test) 4가지 유형은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | [[282_performance_tactics|성능]] 테스트 ([[282_performance_tactics|Performance]] Test) 4가지 유형 적용 결과는 QA 활동을 통해 [[395_verification_process_review|검증]]되고 측정된다 |
| [[020_software_configuration_management|형상 관리]] ([[167_scm_software_configuration_management|SCM]], [[020_software_configuration_management|Software Configuration Management]]) | [[282_performance_tactics|성능]] 테스트 ([[282_performance_tactics|Performance]] Test) 4가지 유형에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    │
    ▼
성능 테스트 (Performance Test) 4가지 유형 개념 정립
    │
    ▼
표준화 및 방법론 체계화 (ISO, CMMI, Agile)
    │
    ▼
클라우드 네이티브·AI 기반 확장 적용
    │
    ▼
지속적 개선 및 DevOps·MLOps 통합
```

이 흐름은 [[002_software_crisis|소프트웨어 위기]] 인식 → 체계적 방법론 개발 → 표준화 → 현대적 플랫폼 적용으로 이어지는 발전 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[282_performance_tactics|성능]] 테스트 ([[282_performance_tactics|Performance]] Test) 4가지 유형은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [[001_software_engineering_definition|소프트웨어 공학]]은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.
