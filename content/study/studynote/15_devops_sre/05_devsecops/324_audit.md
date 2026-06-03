+++
title = "Chaos Engineering"
date = "2026-05-09"
categories = ["studynote-devops-sre"]
+++

> **핵심 인사이트**
> - [[751_chaos_engineering|Chaos Engineering]] ([[751_chaos_engineering|카오스 엔지니어링]])은 프로덕션 시스템에 의도적 장애를 주입해 시스템의 약점을 사전에 발견하는 규율이다.
> - [[151_steady_state_hypothesis_validation|Steady State Hypothesis]] (정상 상태 가설)을 정의하고, 실험 후 시스템이 가설을 유지하는지 [[395_verification_process_review|검증]]하는 과학적 방법론이다.
> - Netflix가 2011년 Chaos Monkey를 공개하며 시작됐고, 현재 [[190_cncf_landscape_observability|CNCF]] [[031_에코_반향|에코]]시스템에서 광범위하게 적용된다.

---

## Ⅰ. [[751_chaos_engineering|Chaos Engineering]] 원칙

카오스 실험 5단계:

```
1. Steady State 정의 → SLI 기준 정상 상태 지표 선정
2. 가설 설정 → "노드 하나 장애나도 응답률 99% 유지"
3. 실험 설계 → 실패 유형 선택
4. 실험 실행 → 최소 폭발 반경으로 시작 → 점진적 확대
5. 결과 분석 → Steady State 벗어난 경우 취약점 발견
```

> 📢 **Ⅰ 섹션 요약 비유**
> [[751_chaos_engineering|카오스 엔지니어링]]은 소방 훈련 — 실제 화재 전에 연기를 피워 대피 경로와 소화 시스템을 [[395_verification_process_review|검증]]한다.

---

## Ⅱ. 주요 장애 주입 유형

| 장애 유형          | 예시                                     |
|--------------------|------------------------------------------|
| [[085_pod_kubernetes_container_unit|파드]]/[[561_container_based_deployment|컨테이너]] 종료  | 랜덤 [[085_pod_kubernetes_container_unit|파드]] 삭제                           |
| [[1002_network_delay_rtt_oneway_delay_components|네트워크 지연]]       | 특정 [[090_service_kubernetes_network_load_balancing|서비스]] 간 200ms [[141_latency|latency]] 주입        |
| 네트워크 패킷 손실  | 30% 패킷 드롭                            |
| 노드 장애           | 워커 노드 중단                           |
| CPU/메모리 포화     | 리소스 고갈 시뮬레이션                   |
| 클라우드 AZ 장애    | 전체 가용 영역 트래픽 차단               |

> 📢 **Ⅱ 섹션 요약 비유**
> 장애 주입은 예방주사 — 약한 형태의 병원균을 넣어 항체(내성)를 키운다.

---

## Ⅲ. 도구 생태계

| 도구         | 특징                                       |
|--------------|--------------------------------------------|
| [[149_chaos_monkey_chaos_mesh|Chaos Monkey]] | Netflix [[191_oss_license_compliance|오픈소스]], EC2 랜덤 종료            |
| LitmusChaos  | [[190_cncf_landscape_observability|CNCF]] 프로젝트, K8s 네이티브 카오스         |
| Chaos [[389_mesh_topology|Mesh]]   | [[190_cncf_landscape_observability|CNCF]] 인큐베이팅, 네트워크 장애 특화        |
| Gremlin      | 상용 [[309_saas|SaaS]], 엔터프라이즈 기능               |
| AWS FIS      | AWS [[670_fault_injection_chaos_testing_kernel|Fault Injection]] Simulator              |

GameDay (게임데이): 전체 팀이 참가해 대규모 장애 시나리오를 실제로 실행하는 훈련 이벤트.

> 📢 **Ⅲ 섹션 요약 비유**
> LitmusChaos는 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 환경의 소방청 — 훈련 시나리오를 체계적으로 관리하고 결과를 리포트한다.

---

## Ⅳ. 카오스 실험의 안전 원칙

1. **최소 폭발 반경**: 스테이징 → 운영 일부 → 전체 순으로 확대
2. **자동 중단 장치**: Steady [[272_state_pattern|State]] 벗어나면 실험 자동 [[098_rollback_strategy_pipeline_error_threshold|롤백]]
3. **비즈니스 영향 최소화**: 저트래픽 시간대 실행
4. **팀 공지**: 실험 전 On-[[189_subroutine_call_return|call]] 팀에 사전 통보

```
카오스 실험 안전 게이트
Staging → Canary(5%) → 25% → 50% → 100%
          자동 중단 조건 항상 활성화
```

> 📢 **Ⅳ 섹션 요약 비유**
> 카오스 실험은 다이너마이트 폭파 훈련 — 항상 안전거리를 확보하고, 비상 정지 버튼을 손에 쥔 채 [[216_progress_in_synchronization|진행]]한다.

---

## Ⅴ. 개념 맵 및 발전 흐름도

### 개념 맵

| 구성 요소              | 역할                                      |
|------------------------|-------------------------------------------|
| [[751_chaos_engineering|Chaos Engineering]]      | 의도적 장애 주입으로 내성 [[395_verification_process_review|검증]]           |
| [[151_steady_state_hypothesis_validation|Steady State Hypothesis]]| 정상 상태 기준 지표 정의                  |
| Blast [[541_radius_remote_authentication_aaa|Radius]]           | 실험으로 영향받는 범위                    |
| [[149_chaos_monkey_chaos_mesh|Chaos Monkey]]           | Netflix의 최초 카오스 도구                |
| LitmusChaos            | [[190_cncf_landscape_observability|CNCF]] K8s 네이티브 카오스 프레임워크       |
| GameDay                | 대규모 팀 장애 시나리오 훈련 이벤트      |

### 관련 키워드 및 발전 흐름도

```
Chaos Engineering
    ├── Steady State Hypothesis → 실험 기준 정의
    ├── 장애 주입 → 네트워크/파드/노드/리소스
    ├── LitmusChaos / Chaos Mesh → K8s 네이티브 도구
    ├── GameDay → 팀 규모 장애 훈련
    └── Resilience Engineering → 장애 내성 시스템 설계
```

> 🧒 **어린이 비유**
> [[751_chaos_engineering|카오스 엔지니어링]]은 레고 성이 얼마나 튼튼한지 보려고 일부러 블록 하나를 빼보는 것이에요. 그래도 성이 무너지지 않으면 합격!
