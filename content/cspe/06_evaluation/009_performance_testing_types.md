---
title: "성능 테스트의 유형 (Performance Testing Types)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-evaluation"
weight: 9
---

## 📖 【암기용】 핵심 요약

*   **한눈에**: 시스템의 응답성, 처리량, 확장성 및 안정성을 확인하기 위해 **다양한 부하 시나리오(Load Profile)를 인위적으로 생성하여 시스템의 거동을 검증**하는 품질 보증 활동.
*   **깊이 이해**:
    *   **배경**: 기능이 정상 동작한다고 해서 실운영의 대규모 트래픽을 버틸 수 있는 것은 아님. 오픈 첫날 서버가 다운되는 참사(System Crash)를 막기 위해 사전에 극한의 스트레스를 가해보는 과정.
    *   **작동 원리**: 가상 사용자(Vuser)를 생성하는 부하 발생기(Load Generator)를 통해 대상 시스템에 트래픽을 주입하고, APM을 통해 내부 자원의 포화 지점(Saturation Point)과 지연 변곡점(Knee Point)을 찾음.
    *   **비유**: **신차 주행 테스트**. 
        *   **부하(Load)**: 정원 5명을 태우고 시속 100km로 잘 달리는지 테스트.
        *   **스트레스(Stress)**: 시속 200km로 밟아서 엔진이 언제 퍼지는지, 퍼진 후 다시 시동이 걸리는지 테스트.
        *   **소크(Soak)**: 72시간 동안 쉬지 않고 달려서 오일이 새거나(Leak) 타이어가 마모되는지 테스트.
        *   **스파이크(Spike)**: 급가속/급제동을 반복하며 시스템의 순간 회복력(Auto-scaling)을 테스트.
    *   **구체 예시**: 수강신청 시스템 오픈 전, 스파이크 테스트(Spike Test)를 통해 1초 만에 1만 명의 트래픽을 주입함. 이때 K8s의 HPA(Horizontal Pod Autoscaler)가 30초 내에 Pod를 정상적으로 스케일 아웃하는지 검증함.
    *   **흔한 오해/주의점**: "부하 테스트 도구(JMeter)를 돌리기만 하면 끝난다"는 착각. 도구는 트래픽을 만들 뿐, 진짜 핵심은 DB Lock, GC Pause, Thread 대기 등의 병목을 찾아내는 **분석(Analysis) 및 튜닝(Tuning)**에 있음.
*   **연결 개념**: 병목 분석(Bottleneck Analysis), TPS, APM(Application Performance Management), Auto-scaling, SLA/SLO

---

## 📝 【답안용】 서술 골격

> **💡 핵심 인사이트**
> *   **본질**: 부하 발생기(Generator)와 성능 모니터(APM)를 결합하여 시스템의 **물리적/논리적 한계치(Capacity Limit)**를 정량화하는 과정.
> *   **가치**: 단순히 SLA 만족 여부를 넘어, 장기 운영 시의 누수(Memory Leak)와 피크 시의 장애 복원력(Resilience)을 사전 확보.
> *   **판단 포인트**: 테스트 목적에 맞게 Ramp-up(부하 점진 증가) 패턴을 다르게 설계하는 시나리오 수립 능력이 핵심.

### Ⅰ. 시스템 안정성의 최종 관문, 성능 테스트 개요
*   **정의**: 시스템에 인위적인 부하(Load)를 가하여 목표한 처리량(TPS)과 응답시간(RT)을 만족하는지, 그리고 어떤 조건에서 장애가 발생하는지 측정하는 테스트 기법.
*   **목적**: 목표 성능(SLA) 충족 여부 검증, 병목(Bottleneck) 구간 식별 및 튜닝, 적정 시스템 용량(Capacity) 산정.

### Ⅱ. 성능 테스트의 4대 주요 유형 (Load Profiles)
*   **Load Test (부하 테스트)**: 
    *   목적: 예상되는 **최대 피크 부하**를 인가하여 목표 성능(SLA) 달성 여부 확인.
    *   패턴: 점진적 증가(Ramp-up) 후 일정 시간 유지.
*   **Stress Test (스트레스 테스트)**:
    *   목적: 한계치 이상의 극단적 부하를 가해 **시스템 파괴점(Breaking Point)**과 장애 후의 자동 **복원력(Resilience)** 확인.
    *   패턴: 시스템이 다운될 때까지 부하를 계속 증가시킴.
*   **Soak / Endurance Test (소크/내구성 테스트)**:
    *   목적: 평균적인 부하를 **장시간(24~72시간)** 인가하여 Memory Leak, DB Connection 누수 점검.
    *   패턴: 일정한 부하를 장기간 평탄하게 유지.
*   **Spike Test (스파이크 테스트)**:
    *   목적: 이벤트, 티켓팅 등 **순간적 폭증**에 대한 시스템 거동(Auto-scaling 반응 등) 확인.
    *   패턴: 부하를 0에서 최대치로 수 초 내에 수직 상승시킴.

### Ⅲ. 성능 테스트 핵심 분석 지표 및 한계 곡선
```text
[성능 포화 곡선 (Performance Curve)]
   지표
    │                 ↗ 응답시간(RT) 폭증 (Knee Point)
    │               /
    │      ________/ 
    │     /  ───────→ TPS 한계 도달 (Saturation Point)
    │    / 
    └───┴──────────┴─────────→ 가상 사용자 수 (Vusers)
        안정 구간     포화 구간
```
*   **Knee Point**: 응답 시간이 급격히 튀기 시작하는 변곡점. 시스템 최적 처리 용량.
*   **Saturation Point**: CPU/Memory 포화로 더 이상 TPS가 늘지 않는 시스템 절대 한계점.

### Ⅳ. 성능 테스트 수행 5단계 프로세스
1.  **목표 수립**: 주요 비즈니스 트랜잭션 도출, Target TPS/RT(SLA) 설정.
2.  **환경 구축**: Production과 동일하거나 비례 축소된 환경 구성, APM(OpenTelemetry, Scouter) 세팅.
3.  **시나리오 작성**: Vuser 행위 스크립팅, Think Time 및 Pacing 설정(실제 사용자 행동 모사).
4.  **수행 및 모니터링**: Load Generator(JMeter, nGrinder, k6)를 통한 부하 인가.
5.  **결과 분석 및 튜닝**: 병목 지점(App, DB, Network) 식별 후 튜닝 및 재테스트(반복).

### Ⅴ. 성능 테스트 성공을 위한 실무적 제언
*   **테스트 격리(Isolation)**: 통제할 수 없는 외부 연동 API는 Mock Server(Stub)로 대체하여 대상 시스템의 순수 성능만 측정.
*   **테스트 데이터 초기화**: 반복적인 테스트로 인해 DB에 데이터가 누적되어 성능이 저하되는(Data Skew) 현상을 방지하기 위한 Teardown 절차 필수.

### Ⅵ. Cloud-Native 환경에서의 성능 테스트 트렌드
*   **Chaos Engineering 결합**: 단순히 트래픽만 가하는 것이 아니라, 부하 상황에서 특정 Pod를 고의로 죽여 시스템의 회복력(Self-healing)을 테스트.
*   **Shift-Left Performance Testing**: CI/CD 파이프라인에 k6 등의 코드로 된 성능 테스트(Performance as Code)를 통합하여, 개발 초기 단계부터 성능 저하(Regression)를 상시 모니터링.

---

### 🔄 문제 유형별 목차 전환 (실전 팁)
*   **"유형 및 이론"** 문제: Ⅱ·Ⅲ을 전진 배치하여 `[Ⅱ. 부하 패턴(Load Profile)에 따른 성능 테스트 4대 유형]`, `[Ⅲ. Knee Point와 Saturation Point 기반 성능 한계 곡선 분석]`으로 개념적 이해도를 증명.
*   **"테스트 실무 및 최신 동향"** 문제: Ⅳ·Ⅵ을 강조하여 `[Ⅳ. APM 연계 기반 병목 탐지 프로세스]`, `[Ⅵ. CI/CD 파이프라인 통합 및 Chaos Engineering 연계 전략]`으로 최신 실무 역량을 강력히 어필.
