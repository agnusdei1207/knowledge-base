+++
title = "039. 피처 플래그 (Feature Flag / Feature Toggle)"
date = 2026-03-04

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

> **핵심 인사이트**
> 1. [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/)([Feature Flag](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/))는 코드 배포와 기능 활성화를 분리하는 기술로, "항상 배포 가능한 상태(Always Deployable)"를 유지하면서 특정 사용자/비율에게만 새 기능을 점진적으로 노출할 수 있는 현대 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD의 핵심 요소다.
> 2. [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/)의 유형 — 릴리즈 토글(배포 제어), 실험 토글(A/B 테스트), 운영 토글(회로 차단기), 권한 토글(사용자 세그먼트) — 각각 생명주기와 관리 방식이 다르므로 용도를 구분하여 사용해야 한다.
> 3. [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/) 부채([Flag](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) Debt)는 주요 [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) 원인 — 사용 완료된 [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)를 정리하지 않으면 코드 복잡성이 기하급수적으로 증가하므로, [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시 만료일(Expiry Date) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)이 필수 관례이다.

---

## I. [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/) 동작 원리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">코드 배포 vs 기능 활성화 분리:</div>
<div class="kb-diagram-note">기존 방식:</div>
<div class="kb-diagram-note">배포 = 기능 활성화 동시</div>
<div class="kb-diagram-tree-item" style="--depth:1">준비 안 된 기능도 배포 시 공개</div>
<div class="kb-diagram-tree-item" style="--depth:1">장기 피처 브랜치 유지 (Merge Hell)</div>
<div class="kb-diagram-note">피처 플래그 방식:</div>
<div class="kb-diagram-note">배포: 언제든 가능 (플래그 OFF 상태)</div>
<div class="kb-diagram-note">활성화: 준비 완료 시 플래그 ON</div>
<div class="kb-diagram-note">코드 예시:</div>
<div class="kb-diagram-note">if featureFlags.isEnabled("new_checkout"):</div>
<div class="kb-diagram-note">show_new_checkout_flow()</div>
<div class="kb-diagram-note">else:</div>
<div class="kb-diagram-note">show_old_checkout_flow()</div>
<div class="kb-diagram-note">점진적 롤아웃 (Percentage Rollout):</div>
<div class="kb-diagram-note">0% -&gt; 1% -&gt; 5% -&gt; 20% -&gt; 100%</div>
<div class="kb-diagram-note">각 단계에서 에러율/성능 모니터링</div>
<div class="kb-diagram-note">문제 발생 시: 즉시 0%로 롤백 (코드 롤백 없음!)</div>
<div class="kb-diagram-note">장점:</div>
<div class="kb-diagram-note">배포 위험 최소화</div>
<div class="kb-diagram-note">장기 피처 브랜치 불필요 (트렁크 기반 개발)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/)는 새 메뉴를 주방에 준비해두고 아직 메뉴판에는 없는 것 — 준비 완료되면 메뉴판에 추가([플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) ON).

---

## II. [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/) 유형



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">피처 플래그 4가지 유형 (Martin Fowler):</div>
<div class="kb-diagram-note">1. 릴리즈 토글 (Release Toggle):</div>
<div class="kb-diagram-note">목적: 미완성 기능을 안전하게 배포</div>
<div class="kb-diagram-note">수명: 단기 (며칠~몇 주)</div>
<div class="kb-diagram-tree-item" style="--depth:1">완료 시 즉시 제거</div>
<div class="kb-diagram-note">2. 실험 토글 (Experiment Toggle):</div>
<div class="kb-diagram-note">목적: A/B 테스트, 가설 검증</div>
<div class="kb-diagram-note">수명: 실험 기간 (일주일~한 달)</div>
<div class="kb-diagram-tree-item" style="--depth:1">승리 변형 결정 후 제거</div>
<div class="kb-diagram-note">3. 운영 토글 (Ops Toggle):</div>
<div class="kb-diagram-note">목적: 런타임 성능 제어, 서킷 브레이커</div>
<div class="kb-diagram-note">수명: 장기 (영구 가능)</div>
<div class="kb-diagram-note">예: "고부하 시 ML 추천 OFF, 기본 추천 ON"</div>
<div class="kb-diagram-note">4. 권한 토글 (Permission Toggle):</div>
<div class="kb-diagram-note">목적: 사용자 세그먼트별 기능 차별화</div>
<div class="kb-diagram-note">수명: 장기</div>
<div class="kb-diagram-note">예: 프리미엄 사용자에게만 새 기능 활성화</div>
<div class="kb-diagram-note">요약:</div>
<div class="kb-diagram-note">짧은 수명: 릴리즈, 실험 토글 (빨리 제거!)</div>
<div class="kb-diagram-note">긴 수명: 운영, 권한 토글 (관리 체계 필요)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 릴리즈 토글은 임시 공사 통제선 (공사 후 제거), 권한 토글은 VIP 라운지 (영구적으로 회원만 입장).

---

## III. [카나리 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/) vs 블루-그린 vs [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">배포 전략 비교:</div>
<div class="kb-diagram-note">블루-그린 배포:</div>
<div class="kb-diagram-note">Blue: 현재 프로덕션</div>
<div class="kb-diagram-note">Green: 새 버전 준비</div>
<div class="kb-diagram-tree-item" style="--depth:1">트래픽을 Blue에서 Green으로 전환</div>
<div class="kb-diagram-tree-item" style="--depth:1">롤백: 트래픽 다시 Blue로</div>
<div class="kb-diagram-note">단점: 두 배의 인프라 비용</div>
<div class="kb-diagram-note">카나리 배포:</div>
<div class="kb-diagram-note">새 버전을 일부 트래픽(5%)에 먼저 노출</div>
<div class="kb-diagram-tree-item" style="--depth:1">문제 없으면 점진적 확대</div>
<div class="kb-diagram-tree-item" style="--depth:1">인프라 효율적</div>
<div class="kb-diagram-note">피처 플래그:</div>
<div class="kb-diagram-note">코드는 하나 (단일 서버)</div>
<div class="kb-diagram-note">플래그 설정으로 사용자별 다른 경험</div>
<div class="kb-diagram-tree-item" style="--depth:1">인프라 비용 없음, 즉시 롤백</div>
<div class="kb-diagram-tree-item" style="--depth:1">카나리보다 더 세밀한 제어 가능</div>
<div class="kb-diagram-note">혼용:</div>
<div class="kb-diagram-note">카나리 배포 + 피처 플래그 조합</div>
<div class="kb-diagram-note">인프라 수준: 카나리 (5% 서버)</div>
<div class="kb-diagram-note">기능 수준: 피처 플래그 (특정 사용자)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)는 새 메뉴를 일부 테이블에만 제공, [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/)는 같은 주방에서 VIP 고객에게만 특별 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) — 비용과 제어 수준 차이.

---

## [IV](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/). [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/) 부채 관리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">피처 플래그 부채 (Flag Debt):</div>
<div class="kb-diagram-note">증상:</div>
<div class="kb-diagram-note">if flag_A and not flag_B or (flag_C and flag_D)</div>
<div class="kb-diagram-tree-item" style="--depth:1">조건 복잡도 폭발</div>
<div class="kb-diagram-tree-item" style="--depth:1">테스트 케이스 기하급수적 증가</div>
<div class="kb-diagram-tree-item" style="--depth:1">더 이상 어떤 플래그가 무엇인지 모름</div>
<div class="kb-diagram-note">예방 원칙:</div>
<div class="kb-diagram-note">1. 만료일 설정:</div>
<div class="kb-diagram-note">{</div>
<div class="kb-diagram-note">"name": "new_checkout",</div>
<div class="kb-diagram-note">"expiry": "2025-04-15",</div>
<div class="kb-diagram-note">"owner": "checkout-team"</div>
<div class="kb-diagram-note">}</div>
<div class="kb-diagram-note">2. 플래그 레지스트리:</div>
<div class="kb-diagram-note">모든 플래그를 중앙 문서화</div>
<div class="kb-diagram-note">소유팀, 목적, 만료일 필수</div>
<div class="kb-diagram-note">3. 정기 정리 (Flag Cleanup):</div>
<div class="kb-diagram-note">스프린트마다 만료된 플래그 코드 제거</div>
<div class="kb-diagram-note">4. 최대 활성 플래그 수 제한:</div>
<div class="kb-diagram-note">팀당 동시 최대 10개 등 정책 수립</div>
<div class="kb-diagram-note">SaaS 도구:</div>
<div class="kb-diagram-note">LaunchDarkly, Flagsmith, Unleash, Optimizely</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) 부채는 방 청소 미루기 — 당장은 편하지만 쌓이면 방 전체를 청소해야 하는 상황이 됨.

---

## V. 실무 시나리오 — 대형 이커머스 A/B 테스트



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">목표: 새 결제 플로우가 전환율 향상 가설 검증</div>
<div class="kb-diagram-note">피처 플래그 설정:</div>
<div class="kb-diagram-note">name: "new_checkout_v2"</div>
<div class="kb-diagram-note">type: experiment</div>
<div class="kb-diagram-note">rollout: 50% (무작위 A/B)</div>
<div class="kb-diagram-note">측정 지표:</div>
<div class="kb-diagram-note">주요 지표: 결제 완료율</div>
<div class="kb-diagram-note">보조 지표: 결제 포기율, 평균 결제 시간</div>
<div class="kb-diagram-note">실험 진행 (1주):</div>
<div class="kb-diagram-note">A (기존): 전환율 3.2%</div>
<div class="kb-diagram-note">B (신규): 전환율 3.8% (+18.75%!)</div>
<div class="kb-diagram-note">p-value &lt; 0.05 (통계적 유의)</div>
<div class="kb-diagram-note">결정:</div>
<div class="kb-diagram-note">신규 플로우 100% 활성화</div>
<div class="kb-diagram-note">플래그 제거 (코드 정리)</div>
<div class="kb-diagram-note">긴급 롤백 시나리오:</div>
<div class="kb-diagram-note">신규 버전에서 결제 오류 0.5% 발생</div>
<div class="kb-diagram-tree-item" style="--depth:1">LaunchDarkly 대시보드에서 플래그 OFF</div>
<div class="kb-diagram-tree-item" style="--depth:1">1초 내 전체 사용자 기존 플로우로 복귀</div>
<div class="kb-diagram-tree-item" style="--depth:1">코드 롤백 필요 없음!</div>
</div>
</div>



> 📢 **섹션 요약 비유**: A/B 테스트는 두 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 동시 운영으로 더 좋은 것 선택 — [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/)가 서버 재배포 없이 버튼 하나로 전환.

---

## 📌 관련 개념 맵

```
피처 플래그 (Feature Flag)
+-- 유형
|   +-- 릴리즈 토글 (단기)
|   +-- 실험 토글 (A/B 테스트)
|   +-- 운영 토글 (서킷 브레이커)
|   +-- 권한 토글 (사용자 세그먼트)
+-- 배포 전략과 비교
|   +-- 블루-그린, 카나리 배포
+-- 부채 관리
|   +-- 만료일, 플래그 레지스트리
+-- 도구
    +-- LaunchDarkly, Unleash, Flagsmith
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[장기 피처 브랜치 문제 (2000s)]
Merge Hell, 통합 지연
      |
      v
[트렁크 기반 개발 (Trunk-Based Development)]
단기 브랜치 + 피처 플래그
      |
      v
[피처 플래그 SaaS 등장 (LaunchDarkly, 2014)]
관리형 피처 플래그 플랫폼
      |
      v
[DORA 메트릭 연계 (2016~)]
피처 플래그 -> 배포 빈도 향상 핵심 수단
      |
      v
[현재: Progressive Delivery]
OpenFeature 표준 (CNCF)
피처 플래그 + 카나리 + 관찰 가능성 통합
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/)는 새 놀이기구를 놀이공원에 설치해두고 아직 문을 닫아두는 것처럼, 코드는 배포하되 기능은 준비될 때 열 수 있어요.
2. 새 기능을 전체 사용자의 1%에게만 먼저 보여주고 문제가 없으면 점점 늘려가는 점진적 롤아웃으로 배포 위험을 최소화해요.
3. [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/)를 많이 만들고 정리하지 않으면 "if A and not B or (C and D)" 같은 복잡한 조건이 쌓여 코드가 엉망이 되므로 만료일 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)이 필수예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 39 / 373

← **이전**: [038. 워터스크럼폴 (WaterScrumFall) — 애자일 실패 패턴](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/038_water_scrum_fall/)
**다음**: [040. 트렁크 기반 개발 (Trunk-Based Development)](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/040_trunk_based_development/) →

---
