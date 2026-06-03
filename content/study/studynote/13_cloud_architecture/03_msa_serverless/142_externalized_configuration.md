+++
weight = 142
title = "142. Externalized Configuration - 외부 설정 관리 패턴"
date = "2026-04-19"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Externalized Configuration은 **애플리케이션의 [[009_config|설정]](DB URL·API키·[[576_feature_flag_ab_testing_rollout|Feature Flag]])을 코드 외부(환경변수·[[009_config|Config]] Server·[[567_vault|Vault]])로 분리**하여, 코드 변경 없이 환경별(dev/staging/prod) [[009_config|설정]]을 관리하는 패턴이다.
> 2. **가치**: [[009_config|설정]]이 코드에 하드코딩되면 **환경별 빌드가 필요**하고 [[514_secret_management_vault_kms|시크릿]] 유출 위험이 있지만, 외부화하면 **하나의 이미지로 모든 환경**에 배포하고 런타임에 [[009_config|설정]]을 주입한다.
> 3. **판단 포인트**: [[200_12_factor_app_cloud_native_principles|12-Factor App]] 원칙의 "[[009_config|Config]]"항목이며, Spring Cloud [[009_config|Config]]·HashiCorp Consul·K8s [[102_configmap_secret_kubernetes_12_factor_app|ConfigMap]]/[[514_secret_management_vault_kms|Secret]]·Vault가 핵심 도구이다.

---

## Ⅰ. 개요 및 필요성

```text
코드에 설정 → 환경별 빌드 필요 → 위험
외부 설정:
  환경변수 (12-Factor)
  Config Server (Spring Cloud Config)
  K8s ConfigMap/Secret
  Vault (시크릿 암호화)
```

- **📢 섹션 요약 비유**: 외부 [[009_config|설정]]은 **유니폼(코드)과 이름표([[009_config|설정]])를 분리**하는 것이다. 같은 유니폼에 이름표만 바꾸면 된다.

---

## Ⅱ~Ⅴ. 결론

Externalized Configuration은 **12-Factor App의 핵심**이며, [[009_config|Config]] Server+Vault로 안전하게 관리한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **외부 [[009_config|설정]]** | 코드-[[009_config|설정]] 분리 |
| **12-Factor** | [[009_config|Config]] 원칙 |
| **[[009_config|Config]] Server** | 중앙 [[009_config|설정]] 서버 |
| **[[567_vault|Vault]]** | [[177_secrets_management_vault_kubernetes|시크릿 관리]] |
| **[[102_configmap_secret_kubernetes_12_factor_app|ConfigMap]]** | K8s [[009_config|설정]] 주입 |

### 📈 관련 키워드 및 발전 흐름도

```text
[하드코딩 (~2010)] → [환경변수 (12-Factor, 2011)]
    → [Spring Cloud Config (2015)]
    → [K8s ConfigMap/Secret (2016)]
    → [현재: Vault + Dynamic Secrets — 자동 회전]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 외부 [[009_config|설정]]은 **유니폼과 이름표를 분리**하는 거예요.
2. 같은 유니폼(코드)에 **이름표([[009_config|설정]])만 바꾸면** 다른 환경에서 사용해요.
3. 비밀번호는 **금고([[567_vault|Vault]])**에 따로 보관해서 안전해요!
