---
title: 59. 마이크로 세그멘테이션 (Micro-segmentation) - 동서(East-West) 트래픽 차단
date: '2026-04-07'
tags:
- studynote-cloud
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[1044_micro_segmentation_east_west_traffic_security|마이크로 세그멘테이션]]은 [[598_vm_migration_nic|VM]], [[198_pod_kubernetes_minimum_deployment_unit|Pod]], 애플리케이션 단위로 세밀한 [[690_firewall_generation_evolution|방화벽]] [[164_policy|정책]]을 적용해 내부 트래픽까지 통제하는 보안 방식이다.
> 2. **가치**: 내부로 침투한 공격자의 횡적 이동(Lateral Movement)을 막아 피해 범위(Blast [[541_radius_remote_authentication_aaa|Radius]])를 줄인다.
> 3. **판단 포인트**: IP가 아니라 레이블, 신원, [[164_policy|정책]] 기반으로 설계해야 클라우드/[[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 환경에서 유지된다.

---

## Ⅰ. 개요 및 필요성

기존 경계 보안은 외부에서 들어오는 트래픽만 막는 데 강했다. 하지만 클라우드 내부에서는 서버와 Pod가 자유롭게 오가며 통신하므로, 내부망 침투 후 이동을 막는 장치가 필요하다.

[[1044_micro_segmentation_east_west_traffic_security|마이크로 세그멘테이션]]은 이런 동서(East-West) 트래픽을 세밀하게 나눠, 각 워크로드가 허용된 대상과만 통신하도록 만든다.

- **📢 섹션 요약 비유**: 큰 호텔 정문만 지키는 것이 아니라, 각 방마다 카드키를 다는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[164_policy|정책]]은 중앙에서 정의하지만, 차단은 각 워크로드 근처에서 수행하는 것이 핵심이다. 그래서 [[164_policy|정책]] 컨트롤러와 [[136_variance|분산]] [[690_firewall_generation_evolution|방화벽]]이 함께 필요하다.

```text
정책 컨트롤러
   ↓
레이블 기반 규칙
   ↓
분산 방화벽 / Enforcer
   ↓
Web → DB 허용, Web → HR 차단
```

| 구성 요소 | 역할 |
| :-- | :-- |
| [[164_policy|Policy]] Controller | [[007_security_policy|보안 정책]] 중앙 관리 |
| Distributed [[690_firewall_generation_evolution|Firewall]] | 워크로드 근처에서 패킷 필터링 |
| Label / Tag | IP 대신 워크로드 신원 [[655_ir_detection_analysis|식별]] |
| Network [[164_policy|Policy]] | [[205_kubernetes_container_orchestration|Kubernetes]] 수준의 통신 허용 규칙 |

[[164_policy|정책]]은 "누가 누구와 왜 통신할 수 있는가"를 중심으로 정의한다. 따라서 IP가 바뀌어도 [[164_policy|정책]]은 유지되고, [[598_vm_migration_nic|VM]] 이동이나 오토스케일링에도 흔들리지 않는다.

- **📢 섹션 요약 비유**: 방 번호가 아니라 학생증으로 출입을 제어하는 학교 복도 같다.

---

## Ⅲ. 비교 및 연결

[[1044_micro_segmentation_east_west_traffic_security|마이크로 세그멘테이션]]은 경계 [[690_firewall_generation_evolution|방화벽]]과 다르게 내부 통신 자체를 제어한다.

| 구분 | 경계 [[690_firewall_generation_evolution|방화벽]] | [[1044_micro_segmentation_east_west_traffic_security|마이크로 세그멘테이션]] |
| :-- | :-- | :-- |
| 주 대상 | North-South 트래픽 | East-West 트래픽 |
| [[289_identification_flags_fragmentation_offset|식별자]] | IP/[[446_port_and_bus|포트]] | Label/Identity |
| 강점 | 외부 차단 | 내부 확산 차단 |
| 한계 | 내부 침투 후 약함 | [[459_quic_fec_forward_error_correction|초기]] 설계와 운영 복잡도 |

또한 [[205_kubernetes_container_orchestration|Kubernetes]] NetworkPolicy, [[822_cni_container_network_interface_kubernetes|CNI]], [[090_service_kubernetes_network_load_balancing|서비스]] 메시의 mTLS와 결합하면 L7 수준까지 통제가 가능하다. 즉, 네트워크 보안이 애플리케이션 신원 보안과 연결된다.

- **📢 섹션 요약 비유**: 성문만 닫는 것과 방마다 자물쇠를 다는 것은 완전히 다른 수준의 보안이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

처음부터 완전 차단을 걸기보다, 통신 가시성을 확보한 뒤 점진적으로 제한하는 것이 안전하다.

### [[435_checklist_based_testing|체크리스트]]

1. 워크로드 간 실제 통신 지도가 있는가?
2. Default Deny [[164_policy|정책]]을 점진적으로 적용할 수 있는가?
3. 레이블/태그 기반으로 [[164_policy|정책]]을 작성하는가?
4. [[090_service_kubernetes_network_load_balancing|서비스]] 메시와 함께 L7 통제까지 고려하는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- IP 대역 중심 [[164_policy|정책]]만 고집하는 설계
- [[459_quic_fec_forward_error_correction|초기]]부터 전면 차단해 운영을 마비시키는 설계
- [[164_policy|정책]]을 수동으로만 관리해 변경 추적이 안 되는 설계

- **📢 섹션 요약 비유**: 처음부터 모든 문을 잠그기보다, 누가 오가는지 먼저 보고 필요한 문만 잠그는 것이다.

---

## Ⅴ. 기대효과 및 결론

[[1044_micro_segmentation_east_west_traffic_security|마이크로 세그멘테이션]]은 내부망을 믿지 않는 [[585_zero_skipping|Zero]] Trust의 실천 방법이다. 침해 사고가 나도 피해를 한 구역에 가두는 데 큰 효과가 있다.

운영 복잡도는 늘지만, 클라우드처럼 동적이고 [[136_variance|분산]]된 환경에서는 그 복잡도를 감수할 가치가 있다.

- **📢 섹션 요약 비유**: 배의 격실을 나눠 물이 퍼지지 않게 막는 생존 설계다.

---

## 관련 개념 맵

```text
Zero Trust
   ↓
마이크로 세그멘테이션
   ↓
Network Policy / Distributed Firewall
   ↓
횡적 이동 차단
```

---

## 관련 키워드 및 발전 흐름도

```text
경계 방화벽
   ↓
SDN 기반 분산 방화벽
   ↓
Kubernetes NetworkPolicy
   ↓
서비스 메시 + mTLS
```

---

## 어린이를 위한 3줄 비유 설명

[[1044_micro_segmentation_east_west_traffic_security|마이크로 세그멘테이션]]은 큰 집 안에도 작은 자물쇠를 다는 거예요.  
그래서 나쁜 사람이 한 방에 들어와도 다른 방으로 못 가요.  
결국 피해를 아주 작게 막을 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 58 / 371

← **이전**: [[058_hpa_vpa|58. HPA / VPA - 쿠버네티스 자동 확장 전략]]
**다음**: [[060_hypervisor_escape_vm_security_threat|60. 하이퍼바이저 우회/탈출 (Hypervisor Escape) 보안 위협]] →

---
