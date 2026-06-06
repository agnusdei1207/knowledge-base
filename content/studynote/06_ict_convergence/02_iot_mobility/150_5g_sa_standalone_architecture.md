---
title: "150. 5G Sa Standalone Architecture"
date: "2026-05-03"
tags:
  - "studynote-ict-convergence"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [SA](/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/)(Standalone, 단독 모드) 아키텍처는 과거 LTE망에 빌붙어 셋방살이하던 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [NSA](/studynote/03_network/15_nextgen_communication_architecture/766_nsa_non_standalone_5g_lte_core/)(Non-Standalone) 구조를 완전히 버리고, <strong>스마트폰 -> 기지국(RAN) -> 코어망(Core)에 이르는 전 구간을 100% <a href="/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/">5G</a> 전용 클라우드 소프트웨어(<a href="/studynote/03_network/15_nextgen_communication_architecture/768_5gc_5g_core_network_evolution/">5GC</a>)로 독립 구축한 진정한 <a href="/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/">5G</a> 생태계</strong>다.
> 2. **가치**: [NSA](/studynote/03_network/15_nextgen_communication_architecture/766_nsa_non_standalone_5g_lte_core/) 시절엔 전화가 올 때마다 폰이 5G와 [LTE](/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 사이를 휙휙 널뛰기(Flapping) 하느라 폰 배터리가 타 죽고 핑이 끊겼다. [SA](/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/) 망으로 넘어오는 순간 낡은 [LTE](/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 족쇄가 완벽히 끊어지며 단말 배터리 소모 20% 감소, 그리고 <strong>B2B 돈줄인 1ms 초저지연(<a href="/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/">uRLLC</a>) 자율주행 방벽이 물리적으로 해금(Unlock)</strong>된다.
> 3. **판단 포인트**: SA의 진정한 핵폭탄은 [안테나](/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/) 속도가 아니라 백엔드 <strong><a href="/studynote/06_ict_convergence/02_iot_mobility/151_sba_service_based_architecture_5g/">SBA</a>(<a href="/studynote/06_ict_convergence/02_iot_mobility/151_sba_service_based_architecture_5g/">Service Based Architecture</a>)</strong>에 있다. 옛날 쇳덩이 라우터([EPC](/studynote/03_network/15_nextgen_communication_architecture/753_epc_evolved_packet_core_sgw_pgw/))를 다 버리고, 코어 기능을 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)(K8s) [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 앱으로 100% [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 찢어버림으로써, 공장 전용 5G망(슬라이싱 Slicing)을 1초 만에 무한 복제해 팔아먹는 진정한 NaaS 제국이 완성되었다.

---

## Ⅰ. 개요 및 필요성

[5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 망 구축 표준은 [NSA](/studynote/03_network/15_nextgen_communication_architecture/766_nsa_non_standalone_5g_lte_core/)(Non-Standalone 비단독모드)와 [SA](/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/)(Standalone 단독모드) 두 단계의 진화 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인을 거친다. <strong><a href="/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/">SA</a>(Standalone)</strong>는 말 그대로 [LTE](/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/)(4G) 망의 도움(제어 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 짬처리)을 1%도 받지 않고, 오직 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 기지국(gNB)과 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 전용 코어([5GC](/studynote/03_network/15_nextgen_communication_architecture/768_5gc_5g_core_network_evolution/)) 뇌만으로 트래픽의 모든 길(제어/[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 자급자족 컨트롤하는 순도 100%의 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 아키텍처다.

[초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 런칭 때 사람들은 분노했다. "[5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 빵빵 터진다며! 왜 카톡 보낼 때 자꾸 폰 상단 아이콘이 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) -> [LTE](/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) -> [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 미친 듯이 춤을 추냐 폰 배터리 불타서 녹아 죽네!"
이유는 간단했다. 통신사들이 투자비를 아끼려고 <strong><a href="/studynote/03_network/15_nextgen_communication_architecture/766_nsa_non_standalone_5g_lte_core/">NSA</a>(짝퉁 과도기 망)</strong>로 깔았기 때문이다. 겉껍데기([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 다운로드)는 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [안테나](/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/)로 뚫어줬는데, 뒤에서 전화를 걸고 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)받는 메인 제어 뇌(Control Plane)는 옛날 낡은 [LTE](/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 쇳덩이([EPC](/studynote/03_network/15_nextgen_communication_architecture/753_epc_evolved_packet_core_sgw_pgw/)) 서버를 그대로 짬뽕해서 썼다. 폰 1대가 양다리 걸치고 통신 2개를 다 유지하느라 뻗은 것이다.
이를 해결하기 위한 아키텍트의 결단이 바로 [SA](/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/) 도입이다. 낡은 [LTE](/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 코어망을 영구 폐기하고, 밑바닥 서버실부터 [안테나](/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/) 끝단까지 100% [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 전용 클라우드 뇌([5GC](/studynote/03_network/15_nextgen_communication_architecture/768_5gc_5g_core_network_evolution/))로 통일 구축하여 진정한 1ms 자율주행과 배터리 광탈 방어를 실현했다.

- **📢 섹션 요약 비유**: <strong><a href="/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/">5G</a> <a href="/studynote/03_network/15_nextgen_communication_architecture/766_nsa_non_standalone_5g_lte_core/">NSA</a>(<a href="/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/">초기</a> 짝퉁 망)</strong>는 KTX 고속열차([5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [안테나](/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/) 속도)를 샀는데, 막상 기차가 달리는 <strong>'선로와 기관실(코어망 뇌)'은 옛날 덜컹거리는 무궁화호 낡은 쇳덩이 철로를 그대로 짬뽕해서 쓰는 짓</strong>입니다. 속도 내면 탈선해서 죽으니까 폰이 눈치 보며 기어갑니다(핑 튐 배터리 폭사). <strong><a href="/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/">5G</a> <a href="/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/">SA</a>(단독 모드 진화)</strong>는 옛날 철로를 폭파해 찢어버리고, 아예 처음부터 끝까지 새로 깐 <strong>'100% 최신 자석 부상 KTX 전용 선로와 최신 클라우드 기관실(<a href="/studynote/03_network/15_nextgen_communication_architecture/768_5gc_5g_core_network_evolution/">5GC</a> 뇌)'</strong>로 싹 다 갈아엎어 버린 완전체입니다!

---

## Ⅱ. 아키텍처 및 핵심 원리

[SA](/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/) 아키텍처가 세상을 뒤집은 이유는 껍데기 [안테나](/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/)가 아니라 심장(Core 뇌) 수술의 기적이다.

```text
  +-------------------------------------------------------------+
  |         5G 생태계의 파멸(NSA) -> 구원(SA) 아키텍처 진화 폭발 도면 |
  +-------------------------------------------------------------+
  |                                                             |
  | 💀 [ 1단계 과도기 (NSA: Non-Standalone 비단독 양다리 짬뽕 지옥 💥) ] |
  |                                                             |
  |  📱 내 폰 -> (제어 신호 여보세요 콜! 📞) -> 📡 4G LTE 안테나 -> 🧠 4G LTE 코어 뇌 (낡음)|
  |     |       (폰이 존나 바쁘게 두 탕 뜀 💦)                              |
  |     +---- -> (유튜브 동영상 데이터 쓩 🎥) -> 📡 5G 쌘 안테나 -> 🧠 4G LTE 코어 뇌 (병목!)|
  |                                                             |
  |  -> 파국: 폰 1대가 4G, 5G 안테나 2개에 다 무전 때리느라 배터리 타임아웃 불타 죽음 💀. |
  |          뒤쪽 뇌(Core)는 낡은 4G LTE 1개라서 데이터 쏠리면 병목 정체 폭사.      |
  |                                                             |
  |        ======= [ 🛡️ 아키텍트의 메스: 도끼로 낡은 4G 뇌 영구 절단 🔪 ] ========|
  |                                                             |
  | 🚀 [ 2단계 완전체 (SA: Standalone 100% 순혈 5G 제국 통일 ✨) ]       |
  |                                                             |
  |  📱 내 폰 -> (전화 걸기 📞 + 동영상 데이터 🎥 몽땅 한 방에!!)              |
  |             -> 📡 5G 쌘 안테나 (gNB)                                 |
  |             -> 🧠 5G 전용 클라우드 네이티브 스마트 뇌 (5GC 코어 폭발 🚀)     |
  |                                                             |
  | 🌟 아키텍트 극딜: 이것이 진정한 이혼(Decoupling)과 독립(Standalone)의 쾌속이다!  |
  |   LTE 망이랑 영원히 손절 쳤다. 폰은 5G 안테나 딱 1개랑만 통신하니 핑퐁(Flapping) |
  |   딜레이 0초 컷 + 배터리 20% 절약 꿀 빰! 그리고 뒷단 뇌가 5G 전용 슈퍼컴(5GC)이라  |
  |   드디어 네트워크 슬라이싱(가상망 무한 쪼개 팔기) 흑마법 록온(Lock-on) 봉인이 해제됐다!|
+-------------------------------------------------------------+
```

<strong><a href="/studynote/03_network/15_nextgen_communication_architecture/768_5gc_5g_core_network_evolution/">🌟 모던 [5GC</a> 뇌 (<a href="/studynote/06_ict_convergence/02_iot_mobility/151_sba_service_based_architecture_5g/">SBA</a> <a href="/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/">클라우드 네이티브</a> 융합술 ✨) 🌟]</strong>
과거 [LTE](/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 서버실은 시스코, 노키아에서 수십억 주고 사 온 무식한 쇳덩이(라우터)들이었다. [SA](/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/) 코어([SBA](/studynote/06_ict_convergence/02_iot_mobility/151_sba_service_based_architecture_5g/))는 쇳덩이를 다 버리고 일반 AWS 서버 같은 x86 깡통 위에 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)(K8s) [Docker](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 앱으로 통신망을 다 찢어발겼다. 기능들을 `[인증 API]`, `[세션 연결 API]`, `[데이터 펌프 API]` 같이 잘게 썰어서 100% 마이크로서비스로 띄웠다. 트래픽 100만 배 터지면 K8s가 0.1초 만에 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 펌프(UPF) [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 100개로 무한 오토 스케일 증식 복사시켜 셧다운 폭파를 100% 무혈 방어해 낸다.

- **📢 섹션 요약 비유**: [NSA](/studynote/03_network/15_nextgen_communication_architecture/766_nsa_non_standalone_5g_lte_core/)(짝퉁 양다리 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/))는 <strong>'최새로운 유형의 에어컨 샀는데 실외기는 10년 된 구형 돌리는 꼴'</strong>과 같습니다. 방 안의 에어컨([5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [안테나](/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/))은 최신 빵빵한데, 밖에 베란다 실외기(4G 낡은 코어 뇌)가 구형 갤갤거리는 거라 전기세 존나 퍼먹고 금방 뻗습니다. [SA](/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/)(진짜 단독 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/))는 <strong>'안에 에어컨 껍데기부터 실외기 모터 심장까지 100% 최새로운 유형의 인버터 <a href="/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/">5G</a> 모델로 싹 다 세트로 교체 쾅!!'</strong> 해버린 겁니다! 양쪽 궁합이 100% 완벽히 맞으니 전기세(배터리) 아끼고 냉기가 0.1초 컷으로 방안을 얼려버립니다.

---

## Ⅲ. 비교 및 연결

[LTE](/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 시절 뇌 정지의 1순위 주범이었던 쇳덩이 강결합을 칼로 찢어발기는 잔인한 수술이다.

| 잣대 | [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [NSA](/studynote/03_network/15_nextgen_communication_architecture/766_nsa_non_standalone_5g_lte_core/) (과도기 양다리 짬뽕 🤡) | [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [SA](/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/) (100% 단독 완전체 🚀) |
|:---|:---|:---|
| **제어 뇌(Core)** | 옛날 4G [LTE](/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 장비([EPC](/studynote/03_network/15_nextgen_communication_architecture/753_epc_evolved_packet_core_sgw_pgw/)) 재활용. 투자비 절감 꼼수. | 구형 버리고 <strong>100% 순수 <a href="/studynote/03_network/15_nextgen_communication_architecture/768_5gc_5g_core_network_evolution/">5GC</a> <a href="/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/">클라우드 네이티브</a> 뇌</strong>로 통째 교체. |
| **단말기 배터리**| 폰이 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 전봇대랑 [LTE](/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 전봇대 두 탕 뛰며 널뛰느라 불타 죽음 💀. | 폰이 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 전봇대 1개만 바라보고 직진 (양다리 0%). **배터리 수명 20% 이득 ✨.** |
| **B2B 슬라이싱** | **[절.대. 불.가.능. 파국 💥]** 낡은 4G 뇌는 클라우드 가상망 쪼개기(Slicing) 로직을 처리할 능력이 없음. | **[무한 쪼개기 해금 발동 ✨]** [5GC](/studynote/03_network/15_nextgen_communication_architecture/768_5gc_5g_core_network_evolution/) 클라우드 뇌가 1개의 물리망을 자율주행용, 공장용 100개 VPN으로 찢어 팔아먹기 쌉가능! |
| **CUPS 적용** | 불완전. 뇌(Control)와 근육(User)이 강결합 떡칠. | **완벽한 분할(Decoupling)**. 뇌([CP](/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/))는 중앙에, 근육 펌프(UP)는 유저 코앞 엣지([MEC](/studynote/03_network/12_iot_wpan_edge/627_mec_multi_access_edge_computing_5g/))로 유배시켜 1ms 광속 핑 달성! |

특히 **CUPS (Control and User Plane Separation)** 수술이 결정적이다. 4G 장비는 요금제 검사하는 똑똑한 대가리 뇌([CP](/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/))와 실제 유튜브 영상을 나르는 멍청한 근육 펌프(UP)를 기계 1대에 같이 박아놔서 병목이 났다. [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) SA는 이 둘을 도끼로 완전 갈라 찢어 뇌는 중앙 클라우드에, 근육 펌프(UPF)는 강남역 전봇대 기지국 지하실([MEC](/studynote/03_network/12_iot_wpan_edge/627_mec_multi_access_edge_computing_5g/))로 전진 배치시켰다. 덕분에 유튜브 패킷이 서울 본사까지 안 가고 0.1초 만에 강남역에서 로컬 다이렉트 반사(Local Breakout)를 치는 초저지연 기적이 터졌다.

- **📢 섹션 요약 비유**: CUPS 수술은 택배 회사 <strong>'사장님(뇌)과 오토바이 알바생(근육)의 업무 분리'</strong>와 똑같습니다. 옛날([LTE](/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/))엔 사장님 1명이 전화도 받고 배달도 다 뛰다 쓰러졌습니다(병목 💥). [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) SA는 사장님(제어 뇌)은 에어컨 빵빵한 본사에 앉아 전화([세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 허가)만 0.1초 컷으로 계속 쳐받고!! 전국 100개 동네마다 짱박아둔 무식한 배달 알바생(UPF 엣지 펌프) 100명한테 "야 니 앞마당 니가 배달해!" 카톡 명령만 쏘는 겁니다! 뇌와 손발이 철저히 찢어져 무한 쾌속 배달이 폭발하는 기적입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

무늬만 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [안테나](/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/) 교체쇼([NSA](/studynote/03_network/15_nextgen_communication_architecture/766_nsa_non_standalone_5g_lte_core/))에 속아 생명을 맡기는 짓은 인프라 의존성을 전혀 모르는 다이빙이다.

### 실무 판단 시나리오
1. <strong><a href="/studynote/06_ict_convergence/02_iot_mobility/145_uam_urban_air_mobility_evtol/">UAM</a> 에어택시 / 로봇 수술 (<a href="/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/">uRLLC</a> 초저지연 생존망)의 <a href="/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/">SA</a>(단독모드) 강제 록온(<a href="/studynote/05_database/04_transactions_concurrency/510_lock/">Lock</a>-on)</strong>:
   서울 하늘을 나는 [UAM](/studynote/06_ict_convergence/02_iot_mobility/145_uam_urban_air_mobility_evtol/) 기체. 통신사 주니어가 멍청하게 "사장님 싼 [NSA](/studynote/03_network/15_nextgen_communication_architecture/766_nsa_non_standalone_5g_lte_core/)([LTE](/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 짬뽕망)로 쏴도 속도 빵빵하니까 안 떨어짐 데헷 ㅋ"
   **파국 발동 💥**: [UAM](/studynote/06_ict_convergence/02_iot_mobility/145_uam_urban_air_mobility_evtol/) 기체가 앞 비행기랑 부딪히기 직전 0.1초 찰나에 "빨리 브레이크 명령 좀 쏴줘 💀!!" 패킷을 쐈다.
   근데 그 생명줄 제어 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 패킷이 뒷단 <strong>낡은 <a href="/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/">LTE</a> 코어망(<a href="/studynote/03_network/15_nextgen_communication_architecture/766_nsa_non_standalone_5g_lte_core/">NSA</a> 병목 쇳덩이 라우터)</strong>을 타는 그 순간!! 유튜브 4K 다운받는 1만 명 트래픽 쓰나미와 섞여 비벼지면서(병목 랙), 제어 응답이 50ms 랙(0.05초) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)에 빠져 [UAM](/studynote/06_ict_convergence/02_iot_mobility/145_uam_urban_air_mobility_evtol/) 기체가 공중 폭파 사망 멸망 참사가 터졌다.
   - <strong>판단 (<a href="/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/">SA</a> Standalone 강제 통치 🛡️)</strong>: "야 이 살인마야!! 사람 목숨 오가는 통제 핏줄에 어떻게 쓰레기 [LTE](/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 짬뽕을 비벼 돌았냐!! <strong>하늘이 두 쪽 나도 자율주행(B2B) 관제망은 <a href="/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/">100% 순혈 [5G</a> <a href="/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/">SA</a> 단독 코어망] + URLLC 전용 1ms <a href="/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/">슬라이스</a> 격리 파이프] 2단 십자 록온(<a href="/studynote/05_database/04_transactions_concurrency/510_lock/">Lock</a>)이 아니면 단 1대의 로봇도 허가 불가 컷 쾅!!!</strong>" [지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)([Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)) 1ms 통제는 [안테나](/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/) 스피드 따위로 되는 게 아니다. 뒷단 뇌 코어망 전체를 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 쇳덩이([SA](/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/))로 완전히 엎어치기 이식해야만 쟁취할 수 있는 극한의 인프라 공학이다.

2. <strong>음성 통신망 (VoNR - Voice over <a href="/studynote/03_network/15_nextgen_communication_architecture/763_5g_nr_new_radio_scalable_numerology/">New Radio</a> 대통일 융합 📞)</strong>:
   "야 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) SA로 다 갈아엎었는데 폰 전화 걸면 왜 아직도 [LTE](/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/)([VoLTE](/studynote/03_network/15_nextgen_communication_architecture/758_volte_voice_over_lte_sip_qos/))로 바뀌어 핑 튀어 빡치네?"
   **판단**: 과도기의 EPS [Fallback](/studynote/13_cloud_architecture/03_msa_serverless/129_fallback/) 꼼수다. 인터넷 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 [SA](/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/)([5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 직통)로 쌩쌩 쏘는데, 막상 제일 예민한 실시간 '음성 통화' 패킷을 날릴 때 아직 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 망이 못 미더워서 전화 오는 그 찰나에 폰 멱살을 잡고 "야 전화는 낡은 [LTE](/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 망으로 스위칭 꺾어 우회해 들어가!" 강제 기어를 튕긴 거다.
   통신사는 **VoNR (보엔알 융합 수술 ✨)** 칼을 빼든다! "이제 목소리 패킷도 무.조.건. 100% [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 전용망([SA](/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/)) 핏줄 위로만 다이렉트 얹어서 쏴버려 쾅!!" 전화를 거는 순간 [LTE](/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 널뛰기 스위칭 랙 2초가 0.1초 컷 증발 광속 다이얼이 걸리며, 진정한 올-아이피(All-IP) [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 천하 대통일의 최종 피날레가 달성된다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **공용 뇌(Shared NF) 쉐어링으로 인한 수평 연쇄 폭파 💥**: 아키텍트가 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 100개 가상 [슬라이스](/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/) 망을 띄웠다. 근데 메모리 아끼겠다고, 100개 [슬라이스](/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/)가 싹 다 1개의 공용 통합 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 봇(Shared [AMF](/studynote/03_network/15_nextgen_communication_architecture/770_amf_access_mobility_management_function/) 뇌)을 같이 찌르며 돌려쓰게 만들었다.
  가장 허접한 [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 깡통 [슬라이스](/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/)망이 해커한테 뚫려 좀비 군단이 되어 공용 [AMF](/studynote/03_network/15_nextgen_communication_architecture/770_amf_access_mobility_management_function/) 뇌에 디도스를 박아 터트려 죽였다! -> [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 뇌가 죽자 자율주행망, 수술 로봇망의 신규 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)이 모조리 올스탑 되며 전사 100개 가상망이 단 1초 만에 연쇄 타살 블랙아웃 파국이 터졌다.
  "하늘이 무너져도 1번 생명줄 [uRLLC](/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/) 자율주행망을 찢을 땐, 서버비 100억 더 들더라도 무조건 100% 완전 독립 복사(Fully Dedicated) [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 뇌를 따로 싹 다 생성해 격리 방폭문 쳐라 쾅!!"

- **📢 섹션 요약 비유**: 이 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)은, 100개의 멋진 고급 오피스텔 방을 잘 지어놓고 **'전기 두꺼비집'은 공용 복도에 달랑 1개** 놔둔 것과 같습니다. 쓰레기장 방([IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 해킹망)에서 누전 터져 두꺼비집 내려가면, 수억 원짜리 펜트하우스 방(자율주행망)도 같이 100% 정전 타죽는 바보 구조입니다. 돈이 들어도 펜트하우스는 자기 방 안에 단독 전용 두꺼비집(Dedicated NF)을 무조건 설치해야 합니다.

---

## Ⅴ. 기대효과 및 결론

[5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [SA](/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/)(Standalone) 아키텍처는 껍데기([안테나](/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/) 속도)의 쾌락에 취해 낡은 심장([LTE](/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 코어 뇌)을 방치했던 거대한 양다리 사기극([NSA](/studynote/03_network/15_nextgen_communication_architecture/766_nsa_non_standalone_5g_lte_core/))의 사슬을 영원히 끊어낸 진정한 통신망 융합 제국의 마스터피스다.

[SA](/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/) 망의 완성으로 단말기는 LTE의 눈치를 보며 널뛰던 더러운 이중 연결(Flapping)의 오버헤드를 증발 시켜 스마트폰 배터리 효율 20% 무적 방어 쉴드를 얻었다.
더 위대한 파괴력은 통신사 원가(OPEX) 인건비 수천억을 자동화로 소각 압살시켜 버린 <strong><a href="/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/">클라우드 네이티브</a>(<a href="/studynote/06_ict_convergence/02_iot_mobility/151_sba_service_based_architecture_5g/">SBA</a>)</strong> 심장 이식에 있다. 비싼 쇳덩이 장비 종속([Vendor Lock-in](/studynote/06_ict_convergence/03_cloud_infrastructure/254_cloud_vendor_lock_in_avoidance_portability_multi_cloud/))의 목을 다 잘라버리고 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 덩어리로 통신망을 다 찢어 발겨 허공에 띄움으로써, 마우스 클릭 1방으로 삼성 공장 전용 1ms 격리 핏줄([Network Slicing](/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/) 가상망)을 0.1초 컷으로 복사 증식해 월세 임대 팔아먹는 통신사 플랫폼 자본 펌핑의 특이점이 도래한 것이다.

비록 수십 조의 통짜 쇳덩이 인프라 폐기 교체 비용(CAPEX 피폭풍)을 감당할지언정, 1밀리초의 찰나에 목숨이 오가는 B2B 생존 전장 앞에서 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [SA](/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/) 단독 통치 제국만이 보여주는 완전 무결점 [스케일 아웃](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)([Scale-out](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/))과 오토 스티어링(Auto Steering) 방어 쉴드는, 다가올 [6G](/studynote/07_enterprise_systems/09_digital_transformation/419_6g_ntn_thz_ris_next_gen/) 인공위성 3D 하이브리드 대통합망의 든든한 강철 척추 DNA로 영원히 우주 끝까지 뻗어나갈 것이다.

- **📢 섹션 요약 비유**: [NSA](/studynote/03_network/15_nextgen_communication_architecture/766_nsa_non_standalone_5g_lte_core/)(짝퉁) 망에서 1ms 쾌속을 외치는 짓은, <strong>'고물 똥차 티코(<a href="/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/">LTE</a> 낡은 뇌)'</strong> 겉껍데기에 <strong>'페라리 타이어(<a href="/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/">5G</a> 최신 <a href="/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/">안테나</a>)'</strong>만 덜렁 갈아 끼워놓고 아우토반 시속 300km 로켓 밟고 달린다고 우기는 헛소리입니다. 엔진이 부들대며 터지기(병목 랙 50ms) 때문에 절대 속도를 낼 수가 없습니다 💀. 1ms 광속 핑을 완성하려면 타이어뿐만 아니라 엔진 심장 쇳덩이 전체를 모.조.리. 최신예 페라리 클라우드 엔진([5GC](/studynote/03_network/15_nextgen_communication_architecture/768_5gc_5g_core_network_evolution/) [SA](/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/) 진성 코어망)으로 싹 다 도려내 갈아엎어야만 하는 뼈저린 물리 법칙 팩트입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| <strong><a href="/studynote/03_network/15_nextgen_communication_architecture/766_nsa_non_standalone_5g_lte_core/">NSA</a> (Non-Standalone 짝퉁 과도기 망)</strong> | [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 껍데기 [안테나](/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/)(속도)만 세우고, 뒷단 통제 뇌(Core)는 구형 [LTE](/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 장비([EPC](/studynote/03_network/15_nextgen_communication_architecture/753_epc_evolved_packet_core_sgw_pgw/))에 빌붙어 쓰는 타협 망. 폰 배터리 타죽고 자율주행 1ms([uRLLC](/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/)) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 보장 절대 불가능한 사기극 파국. |
| <strong><a href="/studynote/06_ict_convergence/02_iot_mobility/151_sba_service_based_architecture_5g/">SBA</a> (<a href="/studynote/06_ict_convergence/02_iot_mobility/151_sba_service_based_architecture_5g/">Service Based Architecture</a>)</strong> | [5GC](/studynote/03_network/15_nextgen_communication_architecture/768_5gc_5g_core_network_evolution/) 코어 뇌를 구성하는 통신망 IT 융합의 끝판왕 사상. 무거운 통신 전용 장비 버리고 걍 웹 개발자 쓰는 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) [REST API](/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/) 핑퐁 치며 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)끼리 쪼개 띄우는 클라우드 대통일 헌법. |
| <strong><a href="/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/">Network Slicing</a> (<a href="/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/">네트워크 슬라이싱</a>)</strong> | [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [SA](/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/) 뇌가 완성되어야만 켤 수 있는 치트키 융합. 1개 물리 망을 도끼로 찢어(Slicing), 테슬라 전용 1ms 망, 유튜브 전용 20Gbps 망으로 100개 가상 독립 쉴드로 쪼개 팔아먹는 통신사 돈줄. |
| **CUPS (제어/사용자 평면 강제 이혼 찢기)** | 4G 시절 1기계 안에서 뇌(제어 [CP](/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/))랑 근육([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 펌프 UP) 같이 비비다 타죽던 강결합 지옥을 부순 메스. 뇌는 중앙에, 근육 펌프는 유저 코앞 전봇대([MEC](/studynote/03_network/12_iot_wpan_edge/627_mec_multi_access_edge_computing_5g/))로 유배 보내 0.1초 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 압살 치는 분리 튜닝. |
| <strong>VoNR (Voice over <a href="/studynote/03_network/15_nextgen_communication_architecture/763_5g_nr_new_radio_scalable_numerology/">New Radio</a>)</strong> | [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 폰 전화 올 때 [LTE](/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 망으로 기어 우회([Fallback](/studynote/13_cloud_architecture/03_msa_serverless/129_fallback/))해서 핑 튀는 파국을 척살하고, 음성 패킷까지 100% 순혈 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [SA](/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/) 핏줄 위로만 다이렉트 얹어서 쏴버려 광속 다이얼 치는 대통일 피날레. |

### 📈 관련 키워드 및 발전 흐름도

```text
4G (LTE) / 스마트폰 중심 넷플릭스 덤프트럭 쾌속 다운로드 혁명 달성. (하지만 B2B 기업 제어망으론 성능 부족 💥)
    |
    v
5G NSA 과도기 / 통신사 돈 아끼려고 앞단 안테나만 5G로 깔고 뇌는 LTE(EPC) 재활용 양다리 기만 -> 폰 배터리 타 죽음 💀
    |
    v
5G SA 단독모드 (SBA) / 낡은 LTE 쇳덩이 뇌 폐기 소각! 100% 5G 전용 클라우드 K8s 컨테이너 뇌(5GC) 록온 완료 ✨
    |
    v
네트워크 슬라이싱 (Slicing) 무한 창조 / 자율주행 1ms(uRLLC) 망, 유튜브망 완벽 방폭문 찢기 가상 임대 판매 🚀
    |
    v
6G 코어 NWDAF (AI 자율 뇌) 융합 / 코어망 심장에 AI 딥러닝 봇 박혀서 24시간 지 맘대로 트래픽 밸런싱 스케일 아웃 오토 스티어링 튜닝
```

### 👶 어린이를 위한 3줄 비유 설명

1. 처음에 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 스마트폰이 나왔을 때는 속도(입구 문)만 엄청 넓은 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 문을 달고, 막상 식당 안쪽 주방장(코어 뇌)은 손이 엄청 느린 옛날 <strong>4G 할아버지 요리사(<a href="/studynote/03_network/15_nextgen_communication_architecture/766_nsa_non_standalone_5g_lte_core/">NSA</a> 짝퉁 망)</strong>를 그대로 써서, 손님이 몰리면 요리가 막혀서 폰 배터리가 엄청 빨리 달았어요!
2. 그래서 대장님(아키텍트)이 낡은 할아버지 요리사를 내보내고, 입구 속도랑 완벽하게 똑같이 손이 미친 듯이 빠른 <strong>초천재 <a href="/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/">5G</a> 전용 로봇 요리사(<a href="/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/">SA</a> 단독모드 코어)</strong>로 100% 주방을 싹 다 통째로 갈아 끼웠답니다!
3. 이제 입구([안테나](/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/))부터 주방(코어 뇌)까지 100% 진짜 **Standalone** [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 완벽 통일 로봇들로 꽉 차서!! 자동차가 스스로 달리는 자율주행도 단 0.1초의 버벅거림 멈춤 없이 완벽하게 생명을 지켜주는 진짜 미래 마법 인터넷이 완성된 거예요 🚀!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 150 / 552

<- **이전**: [149. 네트워크 슬라이싱 (Network Slicing) - 5G 융합 가상 격리 전용망](/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/)
**다음**: [151. SBA (Service Based Architecture) - 5G 코어망 클라우드 네이티브 대통합 뼈대](/studynote/06_ict_convergence/02_iot_mobility/151_sba_service_based_architecture_5g/) ->

---
