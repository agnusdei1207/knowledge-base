---
title: "package.json, pom.xml"
date: "2026-04-05"
tags:
  - "devops_sre"
---

# 종속성 격리

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 종속성 격리(Dependency [Isolation](/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/)) 원칙은 모든 외부 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)나 패키지를 명시적으로 선언하며, 해당 선언을 통해 명시된 종속성이 시스템의 다른 부분과 격리되어インストールされ, アプリケーション적동작에 영향을 주지 않아야 한다는 12팩터 앱의 제2원칙이다.
> 2. **가치**: "여기서는 되는데 저기서는 안 된다"는 종속성 불일치 문제를 원천 차단하고, 빌드Reproducibility를 보장하여 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인의 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)을 높인다.
> 3. **융합**: 패키지 관리자(package.[json](/studynote/11_design_supervision/06_exam_summary/343_json/), Gemfile, pom.xml 등)를 통해 구현되며, [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지 레이어 구조와 결합하여 완벽한 격리가 가능하다.

---

### Ⅰ. 개요 및 필요성 ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

소프트웨어 애플리케이션은고립적으로동작하는こ와/과는희에서あり, 대량의외부ライブラリやフレームワーク에의뢰하고 있는. 이러한 외부 의존성을 어떻게 관리하느냐가 애플리케이션의 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/),Reproducibility, 보안에 큰 영향을 미친다.

전통적인 종속성 관리의 문제점은 두 가지로 나뉜다. 첫째는"암시적 종속성"으로, 개발자 A가ローカルPC에 특정 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)의 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)를インストール하고 개발을 [진행](/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)했지만, 그 사실을 다른 개발자나 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/) 환경에 공유하지 않으면"여기서는 되는데 저기서는 안 된다"는 문제가 발생한다. 둘째는"전역 종속성 오염"으로, 시스템 전역에ライブラリ을/를インストール하면 다른 애플리케이션과의 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 충돌이 발생할 수 있다.

예를 들어, Python Flask 기반 앱을 개발할 때 `pip install flask`라고만 하면 시스템에 설치된 최신 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 설치된다. 개발자 A의 PC에는 Flask 2.0이, 개발자 B의 PC에는 Flask 1.0이 설치될 수 있다. 이렇게 되면 같은 [코드베이스](/studynote/15_devops_sre/01_culture_methodology/007_codebase/)에서 만든 앱이 서로 다른 동작을 보일 수 있다. 또한 개발 PC에는 Flask외에も다수의ライブラリ이/가インストール되어 있어, 본번 환경과 종속성 구성이 완전히 달라질 수 있다.

아래 다이어그램은 전통적인 암시적 종속성 관리와 명시적 종속성 격리의 차이를 보여준다.

```text
[전통적 암시적 종속성 vs 명시적 종속성 격리]

❌ 전형적 암시적 종속성 문제
+---------------------------------------------+
|  Developer A PC              |  CI Server   |
|  +---------------------+   |   +---------------+
|  | Python              |   |   |  Python       |
|  |  +- Flask (2.0)     |   |   |   +- Flask (1.0) |
|  |  +- Requests (2.28)  |   |   |   +- Requests   |
|  |  +- Pandas (1.5.0)  |   |   |   |    (2.25)   |
|  |  +- [기타 수십 개]   |   |   |   +- [다름]      |
|  | (전역 설치, 불명확)   |   |   | (전역 설치, 불일치)|
|  +---------------------+   |   +---------------+
+---------------------------------------------+
  문제: 환경 불일치 -> 배포 시 예상 못한 에러 발생

✓ 명시적 종속성 격리 (12팩터 원칙)
+-----------------------------------------------------+
|  선언적 종속성 파일 (requirements.txt, package.json)|
|  +---------------------------------------------+  |
|  | {                                          |  |
|  |   "dependencies": {                        |  |
|  |     "flask": "~2.0.0",                    |  |
|  |     "requests": "^2.28.0",                |  |
|  |     "pandas": "~1.5.0"                    |  |
|  |   }                                        |  |
|  | }                                          |  |
|  +---------------------------------------------+  |
+-----------------------------------------------------+
          |                              |
          v                              v
+---------------------+      +---------------------+
| Developer A PC      |      |  CI Server          |
| (가상환경/컨테이너)  |      |  (가상환경/컨테이너) |
| +-----------------+ |      | +-----------------+ |
| | my_app          | |      | | my_app          | |
| | +- venv/        | |      | | +- venv/        | |
| | |   +- Flask 2.0| |<------>| | |   +- Flask 2.0| |
| | |   +- Request | |동일   | | |   +- Request | |
| | |   |   2.28   | |      | | |   |   2.28   | |
| | |   +- Pandas  | |      | | |   +- Pandas  | |
| | |       1.5.0  | |      | | |       1.5.0  | |
| | +---------------+ |      | | +---------------+ |
| +---------------------+      +---------------------+
```

이 그림의 핵심은 종속성이 명시적으로 선언되면, 모든 환경(개발자 [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/), [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/) 서버, 프로덕션)에서 동일한판본적 종속성이 설치된다는 점이다. 이를 통해"동일한 [코드베이스](/studynote/15_devops_sre/01_culture_methodology/007_codebase/) + 동일한 종속성 선언 = 동일한 동작"이라는 공식이 성립한다. 가상 환경(Virtual [Environment](/studynote/15_devops_sre/02_cicd_gitops/066_gitlab_flow_environment_branch_strategy/))이나 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 사용하면 종속성이 시스템 전역이 아닌 애플리케이션 Within에 격리되어 설치되므로, 다른 애플리케이션과의 충돌도방げる.

> 📢 **섹션 요약 비유**: 종속성 격리는"음식의 식재료 원산지 표시제"와 같다. 요리사가 만드는 요리(애플리케이션)에 어떤 식재료(종속성)가 사용되었는지 명시하면,식품안전감관당국(개발자/운영자)이 언제든 그것을검정에서き, 문제 발생 시 원인 파악이 용이하다. 만약 원산지를 밝히지 않으면(암시적 종속성) 문제 발생 시 추적이 불가능해진다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

종속성 격리를 효과적으로 구현하기 위해서는 각 프로그래밍 언어와 생태계에 맞는 패키지 관리자를 사용하고, 일관된 종속성 선언 및 격리 메커니즘을 채택해야 한다.

| 언어/플랫폼 | 패키지 관리자 | 종속성 선언 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) | 격리 메커니즘 |
|:---|:---|:---|:---|
| **Node.js** | npm, [yarn](/studynote/14_data_engineering/01_infrastructure/020_yarn/), pnpm | package.[json](/studynote/11_design_supervision/06_exam_summary/343_json/) | node_modules/, npm workspaces |
| **Python** | pip, poetry, conda | requirements.txt, pyproject.toml | venv, virtualenv |
| **Ruby** | Bundler | Gemfile, Gemfile.[lock](/studynote/05_database/04_transactions_concurrency/510_lock/) | .bundle/, vendor/ |
| **Java** | Maven, Gradle | pom.xml, build.gradle | .m2/, Gradle cache |
| **Go** | go mod | go.mod, go.sum | go modules |
| <strong><a href="/studynote/04_software_engineering/10_trends_pm_quality/782_memory_safety_rust_compiler_verification/">Rust</a></strong> | Cargo | Cargo.toml, Cargo.[lock](/studynote/05_database/04_transactions_concurrency/510_lock/) | target/ |
| **다중 언어** | Bazel, Pants | BUILD [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) | sandboxed execution |

아래는 종속성 격리의 내부 동작 메커니즘을 보여주는 [ASCII](/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램이다.

```text
[종속성 격리의 내부 동작 메커니즘]

1. 종속성 선언 ( Declarative Dependency)
+--------------------------------------+
|  package.json                        |
|  +--------------------------------+ |
|  | "dependencies": {              | |
|  |   "express": "^4.18.0",        | |
|  |   "mongoose": "^6.9.0"        | |
|  | }                              | |
|  | "devDependencies": {          | |
|  |   "jest": "^29.0.0",           | |
|  |   "eslint": "^8.0.0"           | |
|  | }                              | |
|  +--------------------------------+ |
+--------------------------------------+
           |
           | npm install / pip install
           v
2. 종속성 설치 및 격리 (Installation & Isolation)
+--------------------------------------+
|  애플리케이션 디렉토리                |
|  +------------------------------+    |
|  | my-app/                      |    |
|  | +-- node_modules/            |    | <- 격리된 종속성
|  | |   +-- express/             |    |   (전역 설치 아님)
|  | |   +-- mongoose/            |    |
|  | |   +-- [다른 종속성들...]    |    |
|  | +-- src/                     |    |
|  | +-- package.json             |    |
|  | +-- package-lock.json        |    | <- 정확한 버전 잠금
|  +------------------------------+    |
+--------------------------------------+
           |
           | 종속성 트랜잭션 (Dependency Resolution)
           v
3. 종속성 해석 및 검증 (Resolution & Verification)
+--------------------------------------+
|  종속성 트리 (Dependency Tree)       |
|  +--------------------------------+ |
|  | my-app                         | |
|  | +-- express@4.18.2            | |
|  | |   +-- accepts@1.3.7         | |
|  | |   |   +-- type-is@1.0.0    | |
|  | |   +-- body-parser@1.20.0    | |
|  | |   |   +-- raw-body@2.5.0   | |
|  | |   +-- ...                   | |
|  | +-- mongoose@6.9.1           | |
|  | |   +-- mongodb@4.13.0        | |
|  | |   +-- ...                   | |
|  | +-- jest@29.4.0               | |
|  |     +-- ...                   | |
|  +--------------------------------+ |
|                                      |
|  중복 종속성 자동 처리:               |
|  npm은 동일한 패키지의 다른 버전을     |
|  중첩된 node_modules에 설치하여       |
|  충돌을 방지                         |
+--------------------------------------+
```

> 📢 **섹션 요약 비유**: 종속성 격리는"음식의 반찬 관리"와 같다. 어떤 요리(애플리케이션)에 필요한 반찬(종속성)은 냉장고(시스템 전역)가 아닌 요리사 개인 냉장고(격리된 환경)에 별도로 보관한다. 그래야 다른 요리사와 냉장고 공간을 공유하면서도 서로의 반찬이 섞이지 않는다. 만약 누군가가 냉장고를 공유하면(전역 설치) 같은 밀가루를 놓고 다른 용도로 사용하다충돌이 발생할 수 있다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

종속성 격리는 다른 소프트웨어 개발 개념과 긴밀하게 연결되어 있으며, 그 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 이해하면より체계적な개발환경를 구축할 수 있다.

| 관련 개념 | 종속성 격리와의 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 시너지 효과 |
|:---|:---|:---|
| <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/">컨테이너</a>화 (<a href="/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/">Docker</a>)</strong> | [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)가 종속성을 격리하는기술제공 | Dockerfile에서 종속성 선언 -> 완전한 환경 격리 |
| <strong><a href="/studynote/12_it_management/02_itsm_itil/874_configuration_item/">CI</a>/CD <a href="/studynote/02_operating_system/02_process_thread/123_pipe/">파이프</a>라인</strong> | [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인에서 종속성 설치는Deterministic | 빌드Reproducibility 보장, [캐싱](/studynote/02_operating_system/08_storage_and_io_systems/456_caching/)으로 빌드 속도 향상 |
| <strong>보안 (<a href="/studynote/09_security/05_web_app_security/453_sca/">SCA</a>)</strong> | 종속성 스캔은 보안 취약점 발견 수단 | 취약한 종속성 예방적 발견/갱신 |
| <strong>모놀리식 -> <a href="/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a> 전환</strong> | [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 전환 시 공통 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 종속성 관리우위중요 | [공유 라이브러리](/studynote/02_operating_system/06_memory_management/333_shared_library/)의 판본 관리 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 수립 필요 |

특히 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)([Docker](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/))와의 결합은 종속성 격리의 완벽한 실현이다. Dockerfile에서 `RUN npm ci` 또는 `RUN pip install -r requirements.txt`를 사용하여 종속성을インストール하면, 그 이미지가 실행되는 모든 환경(개발자 laptop, [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/), 프로덕션)에서 동일한 종속성이 보장된다.

```text
[Docker와 종속성 격리의 결합]

Dockerfile
+-------------------------------------------------+
|  FROM node:18-alpine                            |
|                                                 |
|  WORKDIR /app                                  |
|                                                 |
|  # 종속성 선언 복사 (레이어 캐싱 최적화)          |
|  COPY package*.json ./                         |
|                                                 |
|  # 프로덕션 종속성만 설치 (devDependencies 제외) |
|  RUN npm ci --only=production                  |
|                                                 |
|  # 소스 코드 복사                               |
|  COPY ./ ./                                    |
|                                                 |
|  EXPOSE 3000                                   |
|  CMD ["node", "src/index.js"]                  |
+-------------------------------------------------+
              |
              | docker build
              v
+-------------------------------------------------+
|  Docker Image (불변하고 격리된 환경)              |
|  +-----------------------------------------+    |
|  | Layer 1: node:18-alpine (베이스)        |    |
|  | Layer 2: npm packages (종속성 격리)    |    |
|  | Layer 3: application source            |    |
|  +-----------------------------------------+    |
|                                                 |
|  이 이미지는 어떤 환경에서 실행해도                |
|  동일한 Node.js 버전과 동일한 npm 패키지를 사용  |
+-------------------------------------------------+
```

> 📢 **섹션 요약 비유**: Docker와 종속성 격리의 결합은"진공 포장 식재료"와 같다. 요리사(개발자)가 레시피(코드)와 함께 필요한 식재료(종속성)를진공 포장하여([컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지)중앙주방(프로덕션)에 전달하면, 그 식재료는 어디에서든 동일한품질을 유지한다. 중앙주방에서는 어떤 다른 식재료와 섞이지 않고(격리), 필요한 만큼만 사용하여(최적화) 요리를 만든다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

실무에서 종속성 격리를 적용할 때 흔히 직면하는문제와 해결 방안을シナリオ별로 분석한다.

**1. 실무 의사결정 시나리오**
- <strong>시나리오 A: 레거시 앱이 시스템 전역 <a href="/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/">라이브러리</a>에 의존하고 있어서 <a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/">컨테이너</a>화가곤난</strong>
  - **상황**: 10년 된 Python 2 앱이 시스템 전역에 설치된 특정 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)에 의존하고 있어, Docker화하면 동작하지 않음.
  - **판단**: 먼저 종속성을 정리하는 것이우선이다. `pip freeze`를 통해 현재 시스템에 설치된 모든 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)를추출し, 이를 기반으로 requirements.txt를 작성한다. 그 후 가상 환경에서 해당 종속성을 설치하여 테스트하고, 점진적으로 최신 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)으로천이한다. 만약 일부 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)가 더 이상 지원되지 않으면류사공능의 다른 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)로 교체해야 한다.

- **시나리오 B: 개발 환경에서는 되는데 프로덕션에서만 종속성 관련 에러가 발생**
  - **판단**: 이 문제는전형적인 종속성 격리 실패이다. package-[lock](/studynote/05_database/04_transactions_concurrency/510_lock/).[json](/studynote/11_design_supervision/06_exam_summary/343_json/) (또는 Pipfile.[lock](/studynote/05_database/04_transactions_concurrency/510_lock/), Gemfile.[lock](/studynote/05_database/04_transactions_concurrency/510_lock/)) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 프로덕션에 제대로 배포되지 않았거나, 프로덕션 환경에서 `npm install` 대신 `npm ci`를 사용하지 않았을 가능성이 높다. `npm ci`는 package-[lock](/studynote/05_database/04_transactions_concurrency/510_lock/).json을엄밀하게 사용하여 종속성을 설치하므로, 개발 환경과 프로덕션 환경의 종속성을일치시킬 수 있다.

```text
[종속성 관련 흔한 문제 및 해결책]

문제 1: "여기서는 되는데 저기서는 안 된다"
원인: 종속성 버전 불일치
해결: package-lock.json 등 Lock 파일을 항상 함께 배포
     -> `npm ci` (clean install) 사용

문제 2: 빌드할 때마다 다른 결과
원인: 종속성 순서 또는 transitive 종속성 차이
해결: Lock 파일의 해시로 무결성 검증
     -> npm: package-lock.json의 integrity 필드
     -> pip: pipenv 또는 poetry의 lock 파일

문제 3: 보안 취약점이 포함된 종속성
원인: 오래된 라이브러리 버전 사용
해결: SCA (Software Composition Analysis) 도구 활용
     -> npm audit, Snyk, Dependabot 등
```

> 📢 **섹션 요약 비유**: 종속성 문제는"가이드북 없는_foreign 음식 만들기"와 같다. 한국 셰프가 중국 요리 레시피를 보고 따라하려고 하는데, 재료의 원산지와 질감이 다르니(종속성 불일치) 결과물이완전불동해진다. 그러나 식재료의 브랜드와 원산지를 명시하면(종속성 선언) 어느 나라의 셰프든 동일한 요리를 만들 수 있다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

종속성 격리의 올바른 적용은 조직의 빌드 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)과 [보안성](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/)을 크게 향상시킨다.

| 관점 | 종속성 격리 미적용 ([AS-IS](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)) | 종속성 격리 적용 (TO-BE) | [핵심 성과 지표](/studynote/12_it_management/01_governance_strategy/018_kpi/) |
|:---|:---|:---|:---|
| <strong>빌드 <a href="/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a></strong> | 개발 OK, [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/) 실패 -> 이유 불명확 | 모든 환경에서 동일한 빌드 결과 | 빌드 실패율 감소 |
| **배포 Reproducibility** | "Production에서만 안 돼" 현상 | 환경 무관 일관된 동작 | 디버깅 시간 단축 |
| **보안** | 취약한 종속성 미인식 | SCA로 취약점 선제적 발견 | 보안 인시던트 감소 |
| **개발자 온보딩** | 새 개발자 [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)에 수일 소요 | `npm install` 한 번으로 즉시 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) | 온보딩 시간 80% 단축 |
| **인프라 비용** | 매 환경마다 수동 종속성 관리 | 선언적 관리로 자동화 | 관리 오버헤드 감소 |

**미래 전망 및 결론**:
종속성 관리의 미래는 더욱고도화되고 있다. 이제 단순히 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)을 맞추는 것을 넘어, 종속성의 투명성([Software Bill of Materials](/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/), [SBOM](/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/))과 보안([Software Composition Analysis](/studynote/04_software_engineering/11_testing_validation/887_sca_software_composition_analysis/), [SCA](/studynote/09_security/05_web_app_security/453_sca/))이 중요한 화두가 되고 있다. SolarWinds 등의 [공급망 공격](/studynote/09_security/15_malware_attack_vectors/764_supply_chain_attack/) 사례에서 볼 수 있듯이, 종속성 자체가 공격 경로가 될 수 있음을 인식해야 한다.

또한 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 코드 어시스턴트의 등장으로, 개발자가 명시적으로선언하지 않은 종속성도 AI가 자동으로 추가해주는 기능이 늘어나고 있다. 그러나 이것은 더 많은 종속성을 야기할 수 있으므로, 종속성 검토 프로세스의 중요성이 더 커지고 있다.

결론적으로, 종속성 격리는 12팩터 앱의 제2원칙으로 단순해 보이지만, 실무에서 이를 어겼을 때 발생하는 문제는 엄청나다."여기서는 되는데 저기서는 안 된다"는 말은 개발자와 운영자 모두에게 가장 귀찮은 문제 중 하나이며, 종속성 격리 원칙을 엄격히 준수하면 이러한 문제를 원천적으로방지할 수 있다. 모든 조직은 종속성을 명시적으로 선언하고, [Lock](/studynote/05_database/04_transactions_concurrency/510_lock/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 사용하여 불변성을 보장하며, 정기적으로 보안 취약점을검사해야 한다.

> 📢 **섹션 요약 비유**: 종속성 격리는"국제 요리 대회의 재료 통일 규정"과 같다. 대회에서는 각 나라의 셰프가 동일한 공급업체에서 받은 동일한 식재료(격리된 종속성)로 요리를 만들어야 한다. 그래야 셰프의 실력(코드 품질)만 평가대상가 되고, 식재료 차이(종속성 불일치)로 인한 불공정(예상 못한 에러)을 방지할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
|:---|:---|
| <strong><a href="/studynote/05_database/04_transactions_concurrency/510_lock/">Lock</a> <a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> (<a href="/studynote/05_database/04_transactions_concurrency/510_lock/">Lock</a> <a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">File</a>)</strong> | `package-lock.json`, `poetry.lock` 등으로 모든 하위 의존성 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)을 고정하여 빌드 재현성을 보장하는 메커니즘 |
| <strong>가상 환경 (Virtual <a href="/studynote/15_devops_sre/02_cicd_gitops/066_gitlab_flow_environment_branch_strategy/">Environment</a>)</strong> | 프로젝트별 격리된 런타임을 제공하여 전역 패키지 충돌을 방지하는 Python venv, Node nvm 등의 기술 |
| <strong><a href="/studynote/09_security/05_web_app_security/453_sca/">SCA</a> (<a href="/studynote/04_software_engineering/11_testing_validation/887_sca_software_composition_analysis/">Software Composition Analysis</a>)</strong> | 의존성 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)의 알려진 보안 취약점([CVE](/studynote/09_security/04_endpoint_security/409_cve_lifecycle/))을 자동으로 탐지하는 Snyk, Dependabot 등의 도구 |
| <strong><a href="/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/">SBOM</a> (<a href="/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/">Software Bill of Materials</a>)</strong> | 소프트웨어에 포함된 모든 [컴포넌트](/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) 목록을 기록한 [공급망](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 투명성 문서로, 미국 행정명령(EO 14028)에서 의무화 |
| <strong><a href="/studynote/06_ict_convergence/03_cloud_infrastructure/200_12_factor_app_cloud_native_principles/">12-Factor App</a></strong> | 12번째 원칙 "의존성 격리"를 포함하여 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 앱의 설계 기준을 제시하는 방법론 |

### 📈 관련 키워드 및 발전 흐름도

```text
[의존성 선언 (Dependency Declaration) — requirements.txt, package.json]
    |
    v
[의존성 잠금 (Lock File) — 버전 고정 불변성]
    |
    v
[가상 환경 격리 (venv / Docker) — 환경 재현성]
    |
    v
[소프트웨어 구성 분석 (SCA, Software Composition Analysis)]
    |
    v
[SBOM (Software Bill of Materials) — 공급망 보안]
```

DevOps에서 의존성 관리가 단순 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 선언에서 보안 취약점 분석과 [공급망](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 투명성 확보로 발전한 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명

1. 의존성 격리는 요리를 할 때 "어떤 재료를 얼마나 쓸지 정확히 적어둔 레시피"예요. 레시피가 없으면 매번 다른 요리가 나와요.
2. [Lock](/studynote/05_database/04_transactions_concurrency/510_lock/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 그 레시피를 봉인해두는 것 — 어떤 컴퓨터에서 만들어도 똑같은 맛이 나오게 해줘요.
3. SBOM은 모든 재료의 원산지를 기록한 성분표예요. 나쁜 재료(취약한 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/))가 몰래 들어왔는지 검사할 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 8 / 373

<- **이전**: [7. 코드베이스 (Codebase) - 버전 관리되는 하나의 코드베이스와 다양한 배포(Dev, Staging, Prod) 연계](/studynote/15_devops_sre/01_culture_methodology/007_codebase/)
**다음**: [9. 설정 (Config) - 환경 변수(Env Vars)에 설정을 저장하여 코드와 분리](/studynote/15_devops_sre/01_culture_methodology/009_config/) ->

---
