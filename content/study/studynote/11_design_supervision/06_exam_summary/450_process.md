---
title: 450. 가비지 컬렉션 스톱 더 월드 메모리 튜닝 (Garbage Collection Stop-the-World Memory Tuning)
date: '2026-05-10'
tags:
- studynote-design-supervision
---

## 핵심 인사이트 (3줄 요약)
1. **본질**: 스톱 더 월드(STW, Stop-the-World)는 [[380_garbage_collection|가비지 컬렉션]] 중 애플리케이션 실행을 잠시 멈추는 현상이며, 메모리 튜닝은 이 정지 시간과 [[139_throughput|처리량]] 사이의 균형을 맞추는 작업이다.
2. **가치**: 같은 하드웨어에서도 힙 구조, 컬렉터 선택, 객체 생존 패턴 분석을 통해 [[015_지연_데이터_관점|지연]] 시간과 장애 확률을 크게 줄일 수 있다.
3. **판단 포인트**: 단순히 `Xmx`를 키우는 것이 아니라 GC [[568_logs_distributed_logging_elk_fluentd|로그]], Full GC 빈도, pause 목표, [[561_container_based_deployment|컨테이너]] 메모리 한계를 함께 보아야 제대로 된 튜닝이 된다.

---

## Ⅰ. 개요 및 필요성
대규모 [[090_service_kubernetes_network_load_balancing|서비스]]에서 [[138_response_time|응답 시간]]이 갑자기 튀는 원인을 추적하다 보면 CPU나 네트워크보다 먼저 GC pause가 문제인 경우가 많다. 애플리케이션 스레드가 잠깐이라도 모두 멈추면 거래 [[015_지연_데이터_관점|지연]], [[573_timeout_retry_backoff_strategy|타임아웃]], 재시도 폭증, 심하면 장애 전파로 이어질 수 있다. 특히 실시간 거래, [[014_api_posix|API]] 게이트웨이, 대량 배치 혼재 시스템에서는 짧은 정지 시간도 체감 품질에 큰 영향을 준다.

메모리 튜닝의 목적은 “GC를 없애는 것”이 아니라 **예측 가능한 pause와 안정적인 [[233_recovery_database_restoration_overview|회복]] 패턴을 만드는 것**이다. Young 영역이 너무 작으면 잦은 Minor GC가, Old 영역이 과도하게 차면 긴 Full GC가 생길 수 있다. 따라서 GC 종류, 객체 생존률, 힙 크기, 트래픽 패턴을 함께 봐야 한다.

```text
┌──────────────────── 요청 처리 시간 축 ────────────────────┐
│ 요청 처리 │ 요청 처리 │ STW Pause │ 요청 처리 │ 요청 처리 │
│   12ms    │   15ms    │   480ms   │   14ms    │   13ms    │
└──────────────────────────────────────────────────────────┘
                          ▲
                          └─ 사용자는 이 구간을 장애처럼 체감
```

기술사 답안에서는 STW를 단순 JVM 내부 현상이 아니라 **[[090_service_kubernetes_network_load_balancing|서비스]] 품질과 직결되는 운영 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]]**로 설명해야 설득력이 높다.
- **📢 섹션 요약 비유**: 교실 청소를 하려고 수업을 잠깐 멈추는 것은 필요하지만, 너무 자주 또는 너무 오래 멈추면 수업 자체가 흐트러지는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리
메모리 튜닝은 힙을 Young/Old 중심으로 나누어 보고, 객체가 얼마나 빨리 죽는지, 오래 살아남는지, 어느 시점에 승격되는지를 해석하는 데서 출발한다. 이후 컬렉터가 어떤 방식으로 회수하고, 어느 단계에서 STW가 길어지는지 분석해 파라미터와 컬렉터 전략을 조정한다.

```text
┌──────────────────────────── JVM Heap 관점 ────────────────────────────┐
│ Young 영역 ── Minor GC ──▶ 살아남은 객체 승격 ──▶ Old 영역            │
│    │                           │                    │                  │
│    └─ 짧지만 잦은 STW 가능     └─ 승격 과다 시      └─ Full GC 길어짐   │
│                                                 Metaspace / Native   │
└───────────────────────────────────────────────────────────────────────┘
```

| 조정 영역 | 의미 | 대표 튜닝 포인트 |
| :--- | :--- | :--- |
| 힙 크기와 세대 비율 | Young/Old 공간 배분과 승격 압력 결정 | `-Xms`, `-Xmx`, Young 비율, Survivor 조정 |
| 컬렉터 선택 | [[139_throughput|처리량]]형, 균형형, 저지연형 특성 차이 | Parallel GC, G1 GC, ZGC/Shenandoah 선택 |
| 관측과 [[395_verification_process_review|검증]] | 실제 pause·할당률·[[233_recovery_database_restoration_overview|회복]] 패턴 [[396_validation|확인]] | GC [[568_logs_distributed_logging_elk_fluentd|로그]], [[162_apm_application_performance_management|APM]], [[078_heap_datastructure|heap]] dump, [[194_container_virtualization_docker_namespace|container]] memory 같이 [[396_validation|확인]] |

STW는 GC마다 완전히 없애는 대상이 아니라 줄이거나 분산하는 대상이다. G1은 지역(Region) 기반으로 예측 가능한 pause를 노리고, ZGC·Shenandoah는 [[014_concurrency|동시성]] 처리를 늘려 긴 정지를 크게 줄인다. 대신 CPU 사용량, 튜닝 난도, [[288_version_ihl_tos_total_length|버전]] 호환성은 함께 고려해야 한다.
- **📢 섹션 요약 비유**: 창고를 정리할 때 물건을 자주 조금씩 치울지, 구역을 나눠 순서대로 치울지, 거의 문을 닫지 않고 계속 정리할지를 고르는 문제와 같다.

---

## Ⅲ. 비교 및 연결
실무에서는 “어떤 GC가 최고인가”보다 업무 성격과 [[015_지연_데이터_관점|지연]] 허용치에 맞는가가 중요하다. 같은 시스템이라도 [[228_batch_processing_hadoop_spark|배치 처리]] 중심과 실시간 [[014_api_posix|API]] 중심은 정반대 선택을 할 수 있다.

| 비교 항목 | Parallel GC | G1 GC | ZGC / Shenandoah |
| :--- | :--- | :--- | :--- |
| 지향점 | [[139_throughput|처리량]] 우선 | 균형형 | 초저지연 우선 |
| STW 특성 | 상대적으로 길 수 있음 | 예측 가능한 pause 목표 | 매우 짧은 pause 지향 |
| 운영 난도 | 비교적 단순 | 현재 가장 범용적 | JVM [[288_version_ihl_tos_total_length|버전]]·환경 이해 필요 |
| 적합 업무 | 배치, [[139_throughput|처리량]] 중심 | 일반 [[090_service_kubernetes_network_load_balancing|서비스]], 혼합 워크로드 | 대화형·실시간 [[015_지연_데이터_관점|지연]] 민감 [[090_service_kubernetes_network_load_balancing|서비스]] |

또한 이 주제는 [[612_memory_leak_detection|메모리 누수]] 진단, 힙 덤프 분석, [[561_container_based_deployment|컨테이너]] 메모리 제한, 애플리케이션 캐시 전략과 직접 연결된다. 즉 GC 튜닝만으로 해결되지 않는 경우가 많으므로 누수와 과할당을 구분하는 문장이 답안에 꼭 들어가야 한다.
- **📢 섹션 요약 비유**: 큰 청소차가 한 번에 모두 치우는 방식, 구역별로 나눠 치우는 방식, 사람들이 다니는 동안 최대한 방해 없이 치우는 방식의 차이와 비슷하다.

---

## Ⅳ. 실무 적용 및 기술사 판단
실무 튜닝은 보통 **GC [[568_logs_distributed_logging_elk_fluentd|로그]] 확보 → pause 원인 분해 → 힙/컬렉터 조정 → 부하 재검증** 순서로 진행한다. 먼저 Minor/Full GC 빈도와 pause 시간을 [[396_validation|확인]]하고, 객체 할당률과 생존률을 본 뒤, 필요하면 힙 크기, Young 비율, 컬렉터 종류를 조정한다. 이때 [[561_container_based_deployment|컨테이너]] 환경에서는 JVM 힙 밖의 native memory, [[092_thread_lwp|thread]] [[057_stack|stack]], [[176_direct_addressing|direct]] buffer도 함께 고려해야 한다.

`Xmx`를 키우면 당장 Full GC 빈도가 줄어들 수는 있지만, 한번 발생한 pause가 더 길어질 수도 있다. 반대로 힙을 과도하게 작게 잡으면 GC가 너무 자주 돌게 된다. 따라서 [[015_지연_데이터_관점|지연]] 목표, [[139_throughput|처리량]], 인프라 여유, JDK [[288_version_ihl_tos_total_length|버전]]을 함께 보는 균형 감각이 중요하다.

### 판단 [[435_checklist_based_testing|체크리스트]]
- GC [[568_logs_distributed_logging_elk_fluentd|로그]] 기준으로 문제의 핵심이 잦은 Minor GC인지, 긴 Full GC인지 구분했는가?
- 애플리케이션 [[612_memory_leak_detection|메모리 누수]]와 정상 캐시 증가를 분리해 해석했는가?
- [[561_container_based_deployment|컨테이너]] 메모리 제한과 JVM 외 메모리 사용량까지 포함해 용량을 잡았는가?
- 파라미터 변경 후 부하 시험으로 pause 시간과 [[138_response_time|응답 시간]]을 다시 [[395_verification_process_review|검증]]했는가?

흔한 오판은 “메모리 늘리면 해결된다”와 “최신 저지연 GC로 바꾸면 끝난다”이다. 실제로는 객체 [[252_creational_patterns_overview|생성 패턴]], 캐시 [[164_policy|정책]], 코드 누수, 시스템 부하 특성이 더 큰 원인일 수 있다.
- **📢 섹션 요약 비유**: 창고가 어지럽다고 무조건 더 큰 창고를 빌리는 것이 아니라, 무엇이 쌓이고 왜 안 빠지는지 먼저 봐야 제대로 정리된다.

---

## Ⅴ. 기대효과 및 결론
GC STW 메모리 튜닝을 체계적으로 수행하면 [[138_response_time|응답 시간]] 급등을 줄이고, 장애성 재시도와 [[573_timeout_retry_backoff_strategy|타임아웃]]을 완화하며, 동일 자원에서 더 안정적인 [[090_service_kubernetes_network_load_balancing|서비스]] 품질을 얻을 수 있다. 또한 GC 문제를 코드 문제, 캐시 문제, [[612_memory_leak_detection|메모리 누수]] 문제와 구분해 대응할 수 있어 운영 의사결정도 빨라진다.

결론적으로 이 주제는 JVM 파라미터 암기가 아니라 **pause의 원인을 증거로 설명하고, 업무 특성에 맞는 메모리 전략을 고르는 능력**이다. 기술사 답안에서는 STW 의미, 세대 구조, 컬렉터 비교, [[568_logs_distributed_logging_elk_fluentd|로그]] 기반 튜닝 절차를 함께 제시하는 것이 핵심이다.
- **📢 섹션 요약 비유**: 도로 정체를 줄이려면 차를 무작정 넓은 주차장으로 보내는 것이 아니라, 어느 구간에서 막히는지 보고 신호와 차선을 조정해야 하는 것과 같다.

---

### 📌 관련 개념 맵
- **Minor GC / Full GC**: 짧지만 잦은 회수와 길지만 무거운 회수의 대표 구분
- **G1 GC**: 지역 기반 회수로 pause 목표를 조절하는 범용 컬렉터
- **ZGC / Shenandoah**: 초저지연을 위해 동시 처리 비중을 높인 저지연 컬렉터
- **GC [[119_log_analysis|로그 분석]]**: pause 시간, 회수 주기, 승격 패턴을 증거로 [[396_validation|확인]]하는 핵심 도구
- **[[612_memory_leak_detection|메모리 누수]] 진단**: 튜닝으로 가려지기 쉬운 근본 원인을 분리해 보는 활동

### 📈 관련 키워드 및 발전 흐름도
```text
기본 힙 설정 운영
        │
        ▼
GC 로그 기반 STW 원인 분석
        │
        ▼
세대 비율 · 컬렉터 · 힙 크기 조정
        │
        ▼
부하 재검증 · 저지연 GC · 컨테이너 메모리 최적화
```

### 👶 어린이를 위한 3줄 비유 설명
1. 방을 정리하려고 잠깐 놀던 걸 멈추는 시간이 바로 스톱 더 월드예요.
2. 방이 너무 작거나 정리 방법이 나쁘면 자주 오래 멈추게 돼요.
3. 그래서 방 크기와 정리 방법을 잘 고르면 덜 멈추고 더 오래 재미있게 놀 수 있어요.
