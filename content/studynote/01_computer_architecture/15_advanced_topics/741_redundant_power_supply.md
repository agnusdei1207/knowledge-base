+++
title = "741. 이중화 전원 공급 장치 (Redundant Power Supply)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 전원 공급 장치 (Redundant [Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) Supply)는 서버의 전력 경로를 둘 이상으로 분리해, 전원 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 하나나 상위 급전 경로 하나가 고장 나도 시스템이 계속 동작하게 만드는 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 설계다.
> 2. **가치**: PSU ([Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) Supply Unit) 장애를 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단이 아닌 "운영 중 교체 가능한 유지보수 이벤트"로 바꾸며, [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)의 무중단 운영과 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) ([Service Level Agreement](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/)) 달성에 직접 기여한다.
> 3. **판단 포인트**: 진짜 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)는 PSU를 두 개 꽂는 것만으로 끝나지 않으며, A/B 급전 분리, 단일 PSU만으로도 전체 부하를 감당하는 용량, 핫스왑 구조까지 함께 갖춰져야 의미가 있다.

---

## Ⅰ. 개요 및 필요성

[이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 전원 공급 장치는 하나의 시스템에 둘 이상의 전원 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)과 전력 경로를 두어, 전원 계통의 [단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) (Single Point of Failure, [SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/))을 제거하는 구조다. 서버, 스토리지, 네트워크 장비는 중앙처리장치 (Central Processing Unit, CPU)나 메모리가 멀쩡해도 전력이 끊기면 즉시 멈추므로, 전원부는 가장 먼저 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)해야 하는 계층이다. 실제 장애 원인은 PSU 내부 부품 고장, 전원 케이블 이탈, 차단기 트립, 랙 전원 분배 장치 ([Power Distribution Unit](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/651_server_rack_pdu/), PDU) 장애처럼 생각보다 단순한 경우가 많다.

문제는 전원 장애가 다른 하드웨어 장애보다 훨씬 파괴적이라는 점이다. 디스크 하나가 죽으면 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하나 재구성이 가능하지만, 전원 공급이 끊기면 메모리 상태가 사라지고 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 전체가 중단된다. 그래서 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)는 "부품 하나의 고장"과 "[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단"을 동일시하지 않도록, 전원을 유지보수 가능한 장애로 바꾸는 방향으로 설계한다.

즉 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 전원은 단순히 안전장치를 하나 더 넣는 개념이 아니라, <strong>전원 고장을 시스템 정지에서 운영 이벤트로 격하하는 설계 철학</strong>이다.
- **📢 섹션 요약 비유**: 가게 문을 여는 열쇠가 하나뿐이면 분실 순간 영업이 끝난다. 여분 열쇠를 다른 사람과 다른 장소에 나눠 두면, 한 개를 잃어도 가게는 계속 연다.

---

## Ⅱ. 아키텍처 및 핵심 원리

대표적인 서버 전원 구조는 1+1 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)다. 두 개의 PSU가 각각 교류 입력을 받아 직류 출력으로 변환하고, OR-ing 회로나 핫스왑 백플레인을 통해 공통 직류 버스에 연결된다. 평상시에는 두 PSU가 부하를 나눠 갖거나, 일부 설계에서는 한쪽이 더 적극적으로 담당하고 다른 쪽이 대기 상태에 가깝게 동작한다. 중요한 것은 <strong>어느 모드이든 살아남은 한 개의 PSU가 전체 시스템 부하를 단독으로 감당할 수 있어야 한다</strong>는 점이다.

또 하나의 핵심은 전력 경로 분리다. 두 PSU를 같은 멀티탭에 꽂으면 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)만 두 개인 것이지, 급전 경로는 하나다. 그래서 실무에서는 PSU A는 [UPS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/652_ups_architecture/) (Uninterruptible [Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) Supply) A와 PDU A에, PSU B는 [UPS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/652_ups_architecture/) B와 PDU B에 연결해 상위 장애 도메인까지 분리한다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| PSU [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) | 교류를 시스템용 직류로 변환 | 각 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)이 단독으로 전체 부하를 감당해야 함 |
| A/B [UPS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/652_ups_architecture/)·PDU | 상위 전력 경로 분리 | 같은 차단기·같은 PDU 공유 금지 |
| OR-ing / 핫스왑 백플레인 | 두 출력 결합, 역류 차단 | 고장 PSU가 살아있는 PSU를 끌어내리지 않아야 함 |
| 모니터링 회로 | degraded mode 감지 | 두 번째 고장 전에 경보를 올려야 함 |

이 그림은 진짜 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)가 "PSU 2개"가 아니라 "[모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) + 급전 경로 + 결합 회로"의 조합임을 보여 준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">True redundancy requires module redundancy and path split</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Utility A -&gt; UPS A -&gt; PDU A -&gt; PSU A --\</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">+--&gt; OR-ing bus --&gt; Server load</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Utility B -&gt; UPS B -&gt; PDU B -&gt; PSU B --/</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">If PSU A or Feed A fails, PSU B must still support the full server load.</div></div>
</div>
</div>



핫스왑 (Hot-swap) 구조가 붙으면 운영 중에도 고장 난 PSU를 뽑아 새 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)로 교체할 수 있다. 이때 시스템은 꺼지지 않고, 관리자는 경고 로그를 보고 장애 부품만 바꾸면 된다. 그래서 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 전원은 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)과 정비성을 동시에 높이는 인프라가 된다.
- **📢 섹션 요약 비유**: 비행기에 엔진이 두 개 달린 이유는 둘 다 동시에 가장 세게 돌리기 위해서가 아니라, 하나가 멈춰도 남은 하나로 착륙할 수 있게 하기 위해서다.

---

## Ⅲ. 비교 및 연결

[이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 전원을 이해할 때 가장 많이 생기는 오해는 "전원 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)이 두 개면 무조건 안전하다"는 생각이다. 실제로는 어디까지 분리했는지에 따라 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 범위가 크게 달라진다. 또한 전원 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)는 시스템 전체 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)와도 다르다. PSU가 두 개여도 메인보드 고장, 소프트웨어 버그, 단일 네트워크 경로 장애는 그대로 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단을 일으킬 수 있다.

| 구조 | [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)하는 장애 | 남는 [단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) | 해석 |
| :--- | :--- | :--- | :--- |
| 단일 PSU | 없음 | PSU, 케이블, 차단기, PDU | 일반 [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)·저가 장비 수준 |
| 듀얼 PSU + 같은 PDU | PSU [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 고장 | 상위 PDU·차단기 | 반쪽짜리 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) |
| 듀얼 PSU + A/B 급전 | PSU와 상위 급전 한 경로 고장 | 메인보드·랙 전체 정전 | [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 표준 |
| N+1 / N+N 전원 셸프 | 다수 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 중 일부 고장 | 공통 백플레인·제어부 | 대형 섀시·통신 장비 |

N+1은 필요한 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 수 N개에 예비 1개를 더 두는 구조이고, N+N은 필요한 세트를 완전히 두 벌 만드는 구조다. N+N이 더 강하지만 비용과 공간, 효율 손실도 더 크다. 따라서 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 수준은 "얼마나 중요한 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)인가"와 "얼마의 비용을 감당할 수 있는가" 사이의 타협 문제다.

또한 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 전원은 [UPS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/652_ups_architecture/), 발전기, 이중 전력 인입, 클러스터링과 연결돼야 진짜 무중단 효과가 커진다. 서버 한 대에 듀얼 PSU를 달아도 랙 전체가 단일 UPS에 의존하면 상위 장애를 막지 못하기 때문이다.
- **📢 섹션 요약 비유**: 우산 두 개를 들고 있어도 둘 다 같은 가방에 넣어 두면 가방을 잃는 순간 둘 다 사라진다. 진짜 대비는 우산 개수보다 보관 위치를 나누는 데 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 가장 먼저 확인할 것은 용량 계산이다. 예를 들어 서버 최대 소비전력이 750W라면, 1+1 구조에서 각 PSU는 적어도 750W 이상을 단독으로 낼 수 있어야 한다. 500W PSU 두 개를 꽂아 1000W처럼 보이게 만들면 평상시에는 돌아가도 한 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)이 죽는 순간 나머지 하나가 버티지 못한다. 즉 <strong><a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/">이중화</a> 구성의 총합 용량이 아니라, 생존 모드의 단독 용량</strong>을 봐야 한다.

운영 측면에서는 degraded mode 감지가 중요하다. 한 개가 죽어도 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 계속되지만, 그 순간부터는 무방비 상태다. 따라서 [BMC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/710_bmc/) ([Baseboard Management Controller](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/710_bmc/))나 관리 소프트웨어가 PSU fail, input lost, fan fail 같은 이벤트를 즉시 올리고, 현장 교체 절차가 준비되어 있어야 한다.

### 적용 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 한 개 PSU만으로 최대 부하를 감당할 수 있는가?
2. 두 전원 케이블이 서로 다른 [UPS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/652_ups_architecture/)·PDU·차단기로 분리되어 있는가?
3. 핫스왑 교체와 역류 방지 회로가 설계에 포함되어 있는가?
4. 경보 체계가 있어 두 번째 고장 전에 운영자가 인지할 수 있는가?
5. 40~60% 부하 구간의 효율과 발열, 소음까지 고려했는가?

### 피해야 할 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 듀얼 PSU를 같은 멀티탭이나 같은 PDU에 꽂고 "[이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 완료"라고 판단하는 것
- 총합 용량만 보고, 단독 생존 모드 용량을 계산하지 않는 것
- 고장 경보를 무시해 한 개 죽은 상태로 장기간 운영하는 것

비용이 민감한 일반 데스크톱이나 실험용 장비라면 단일 PSU가 합리적일 수 있다. 반대로 금융, 의료, 제조 제어, [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 서버처럼 중단 비용이 큰 환경이라면 전원 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)는 사치가 아니라 기본 요구사항이다.
- **📢 섹션 요약 비유**: 소방차는 예비 연료통이 있다고 끝이 아니다. 연료통 하나가 막혀도 다른 연료 라인으로 바로 달릴 수 있어야 진짜 긴급차량이다.

---

## Ⅴ. 기대효과 및 결론

[이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 전원의 가장 큰 효과는 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 향상이다. PSU 고장, 케이블 이탈, 급전 경로 하나의 상실이 즉시 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 정지로 이어지지 않으므로, 계획되지 않은 다운타임과 긴급 야간 작업이 줄어든다. 또한 핫스왑 교체가 가능해 유지보수 시간과 운영 리스크도 낮아진다.

다만 비용, 공간, 발열, 경보 체계, 효율 저하 같은 대가가 따른다. 저부하에서 PSU 두 개를 모두 살려 두면 효율 곡선이 불리할 수 있고, 상위 전력 인프라가 단일 경로면 하부 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 효과도 제한된다. 즉 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 전원은 만능 방패가 아니라, <strong>전력 경로라는 한 축의 위험을 줄이는 매우 강력한 수단</strong>이다.

앞으로는 고효율 Titanium 급 PSU, 48V 배전, PMBus ([Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/) [Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)) 텔레메트리, 예지 정비 기반 장애 예측이 더 중요해질 것이다. 결론적으로 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 전원은 "PSU를 하나 더 다는 장치"가 아니라, <strong>전원 장애를 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 중단에서 유지보수 이벤트로 전환하는 <a href="/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/">데이터센터</a>식 사고방식</strong>으로 기억하면 된다.
- **📢 섹션 요약 비유**: 좋은 다리는 튼튼한 기둥 하나만 세우지 않는다. 한 기둥에 문제가 생겨도 다른 기둥이 무게를 받아 다리가 끊기지 않게 만든다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| PSU ([Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) Supply Unit) | 교류 전원을 시스템용 직류로 변환하는 기본 전원 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)이다. |
| [UPS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/652_ups_architecture/) (Uninterruptible [Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) Supply) | 순간 정전과 [전압](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/) 이상을 흡수해 PSU 상위 계층의 안정성을 높인다. |
| PDU ([Power Distribution Unit](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/651_server_rack_pdu/)) | 랙 단위에서 전원을 분배하며, A/B 분리가 진짜 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)의 핵심 조건이 된다. |
| Hot-swap | 시스템을 끄지 않고 고장 PSU를 교체하게 해 정비성과 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 함께 높인다. |
| [SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) (Single Point of Failure) | [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 전원이 제거하려는 대표적인 위험 개념이다. |
| 고가용성 (High [Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)) | 전원 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)는 고가용성 설계를 구성하는 하드웨어 기본 축이다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">단일 PSU 기반 서버</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">1+1 이중화 PSU</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">A/B UPS · A/B PDU 분리 급전</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Hot-swap · PMBus 텔레메트리 기반 운영</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">N+1 / N+N 전원 셸프와 랙 단위 전력 복원력</div>
</div>
</div>



이 흐름은 전원 설계가 단순 부품 추가에서 출발해, 이제는 상위 급전 경로와 운영 텔레메트리까지 포함하는 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 아키텍처로 확장되고 있음을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터가 전기를 먹는 빨대가 하나뿐이면, 그 빨대가 빠지는 순간 바로 멈춰요.
2. 빨대를 두 개로 나누고 서로 다른 전기 통에 꽂아 두면, 하나가 망가져도 다른 하나로 계속 마실 수 있어요.
3. 그래서 중요한 서버는 전기 빨대를 여분으로 준비해 두는 거예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 742 / 803

← **이전**: [740. 서버 섀시 팬 핫스왑](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/740_fan_hot_swap/)
**다음**: [742. 전압 조정기 모듈 (VRM)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/742_vrm/) →

---
