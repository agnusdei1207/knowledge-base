+++
weight = 54
title = "54. ConfigMap과 Secret"
date = "2026-05-01"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ConfigMap은 비민감 [[009_config|설정]]을, Secret은 민감한 [[009_config|설정]]을 분리해 관리하는 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 객체다.
> 2. **가치**: 이미지를 바꾸지 않고 환경별 [[009_config|설정]]을 주입할 수 있어 배포 유연성이 높아진다.
> 3. **판단 포인트**: Secret은 숨긴다고 끝이 아니다. 암호화, 권한, 회전, 감사가 필요하다.

---

## Ⅰ. 개요 및 필요성

애플리케이션 이미지를 환경별로 다시 빌드하면 배포가 느려진다. 그래서 [[009_config|설정]]은 외부화해야 한다. ConfigMap과 Secret이 그 역할을 한다.

[[009_config|설정]]과 비밀정보를 코드에서 분리하면 운영이 쉬워지고, 이미지 재사용성이 높아진다.

- **📢 섹션 요약 비유**: ConfigMap과 Secret은 도시락에 붙이는 메모와 금고 열쇠를 따로 보관하는 일이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

ConfigMap은 일반 [[009_config|설정]]값을 저장하고, Secret은 패스워드, 토큰, 키 같은 민감 정보를 저장한다. 둘 다 환경변수나 볼륨으로 주입할 수 있다.

```text
ConfigMap ─┐
           ├→ Pod (env / volume)
Secret   ──┘
```

| 객체 | 용도 | 주의점 |
| :--- | :--- | :--- |
| [[102_configmap_secret_kubernetes_12_factor_app|ConfigMap]] | 일반 [[009_config|설정]] | 환경 분리 |
| [[514_secret_management_vault_kms|Secret]] | 민감 정보 | 암호화/권한 |
| [[001_bigdata_3v_5v|Volume]] | [[501_file_definition_logical_record|파일]] 주입 | [[516_mount_mechanism|마운트]] 관리 |
| Env Var | 프로세스 주입 | [[568_logs_distributed_logging_elk_fluentd|로그]] 노출 주의 |

핵심은 애플리케이션이 [[009_config|설정]]값을 코드에 박아 두지 않고, 런타임에 주입받게 하는 것이다.

- **📢 섹션 요약 비유**: ConfigMap은 반찬 레시피, Secret은 금고 비밀번호다.

---

## Ⅲ. 비교 및 연결

ConfigMap과 Secret은 둘 다 구성 관리를 위해 쓰이지만, 민감도와 [[571_protection_vs_security|보호]] 수준이 다르다. Secret은 base64 인코딩만으로 [[571_protection_vs_security|보호]]되는 것이 아니다.

| 항목 | [[102_configmap_secret_kubernetes_12_factor_app|ConfigMap]] | [[514_secret_management_vault_kms|Secret]] |
| :--- | :--- | :--- |
| 민감도 | 낮음 | 높음 |
| 사용 예 | URL, [[186_character_stuffing_dle_stx_etx|flag]] | 패스워드, 토큰 |
| [[571_protection_vs_security|보호]] | 일반 권한 | 암호화/접근제어 |

외부 [[514_secret_management_vault_kms|Secret]] Manager와 연동하면 더 강한 보안과 회전 정책을 적용할 수 있다. 환경변수보다 [[501_file_definition_logical_record|파일]] [[516_mount_mechanism|마운트]]가 더 적합한 경우도 많다.

- **📢 섹션 요약 비유**: ConfigMap은 메모장, Secret은 자물쇠 달린 금고다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 환경별 [[009_config|설정]]을 분리하고, Secret은 최소 권한으로 접근해야 한다. 또한 [[568_logs_distributed_logging_elk_fluentd|로그]]나 이미지에 비밀이 남지 않도록 주의해야 한다.

### [[435_checklist_based_testing|체크리스트]]

1. 민감 정보와 일반 [[009_config|설정]]이 분리되는가?
2. Secret이 암호화 및 권한 통제를 받는가?
3. 환경별 오버라이드가 가능한가?
4. rotation과 audit가 준비되어 있는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- Secret을 ConfigMap처럼 느슨하게 다루는 경우
- 이미지를 환경마다 다시 빌드하는 경우
- 비밀번호를 [[568_logs_distributed_logging_elk_fluentd|로그]]나 코드에 남기는 경우

기술사 관점에서는 ConfigMap과 Secret이 배포 유연성과 보안을 동시에 높이는 핵심 객체라는 점을 설명해야 한다.

- **📢 섹션 요약 비유**: ConfigMap은 식단표, Secret은 냉장고 열쇠다.

---

## Ⅴ. 기대효과 및 결론

ConfigMap과 Secret을 잘 쓰면 배포가 깔끔해지고, 보안과 운영 분리가 쉬워진다. [[205_kubernetes_container_orchestration|Kubernetes]] 운영의 기본 패턴이다.

정리하면, [[009_config|설정]]은 이미지 밖으로 빼고, 비밀은 더 강하게 [[571_protection_vs_security|보호]]해야 한다.

- **📢 섹션 요약 비유**: ConfigMap은 안내문, Secret은 숨겨 둔 보물지도다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[102_configmap_secret_kubernetes_12_factor_app|ConfigMap]] | 비민감 [[009_config|설정]] |
| [[514_secret_management_vault_kms|Secret]] | 민감 정보 |
| Env Var | 주입 방식 |
| [[001_bigdata_3v_5v|Volume]] | [[501_file_definition_logical_record|파일]] 주입 |
| External [[514_secret_management_vault_kms|Secret]] | 외부 비밀관리 |

### 📈 관련 키워드 및 발전 흐름도

```text
하드코딩 설정
    │
    ▼
ConfigMap / Secret
    │
    ▼
Pod 주입
    │
    ▼
환경 분리 / 회전 / 감사
```

이 흐름은 [[009_config|설정]]과 비밀정보를 코드에서 분리해 운영하는 방법을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. ConfigMap은 메모지에 적은 일반 정보예요.
2. Secret은 남에게 보이면 안 되는 비밀번호예요.
3. 둘을 나눠 두면 정리도 쉽고 안전해요.
