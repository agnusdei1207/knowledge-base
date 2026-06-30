---
title: "소프트웨어공학"
description: "컴퓨터시스템응용기술사 소프트웨어공학 과목의 1교시 단답형 기반 + 2~4교시 확장형 답안 구조"
sort_by: "weight"
weight: 94
---

# 04. 소프트웨어공학

소프트웨어공학 과목을 `스터디노트의 학습 흐름`에 맞춰 재구성했습니다. 각 페이지는 `1교시 단답형 기본 골격`과 `2~4교시 서술형 확장 프레임`을 함께 제공하며, 정의·구조·비교·실무 판단이 바로 답안으로 이어지도록 맞췄습니다.

## 답안 활용 기준

| 구분 | 활용 방식 |
|:---|:---|
| 1교시 | 정의 -> 목적 -> 핵심 요소/절차 -> 장단점/지표 -> 적용 판단 순으로 5~7줄 압축 |
| 2~4교시 | Ⅰ~Ⅴ 구조를 따라 배경, 메커니즘, 비교, 실무 판단, 결론까지 확장 |
| 묶음 학습 | 인접 주제를 함께 묶어 프로세스형, 아키텍처형, 품질형 문제에 대응 |

## 생명주기·프로세스·관리 기반

- 스터디노트 기반 축: `01_overview_principles, 10_trends_pm_quality`
- 출제 관점: 생명주기, 프로세스 성숙도, 형상·품질·원가·일정·위험 관리를 통합적으로 정리하는 축

- [001. 소프트웨어 개발 생명주기 (SDLC)](001_sdlc.md)
- [002. 전통 SW 개발 모델 (폭포수·V-모델·나선형·프로토타입)](002_sw-process-models.md)
- [003. CMMI 성숙도 5단계 (CMMI)](003_cmmi.md)
- [004. 형상관리 (SCM)](004_software-configuration-management.md)
- [005. 기술부채 (Technical Debt)](005_technical-debt.md)
- [006. WBS·CPM·PERT](006_wbs-cpm-pert.md)
- [007. 획득가치관리 (EVM)](007_earned-value-management.md)
- [008. COCOMO·기능점수 (COCOMO·FP)](008_cocomo-function-point.md)
- [009. 델파이 기법 (Delphi)](009_delphi-technique.md)
- [010. 브룩스의 법칙 (Brooks's Law)](010_brooks-law.md)
- [011. 위험관리 4단계 (Risk Management)](011_risk-management.md)

## 애자일·DevOps·지속적 전달

- 스터디노트 기반 축: `02_requirements_analysis, 05_devops_ci_cd`
- 출제 관점: 애자일 실행체계와 DevOps 자동화를 연결해 빠른 전달과 운영 피드백을 묻는 축

- [012. 애자일 선언문 (Agile Manifesto)](012_agile-manifesto.md)
- [013. 스크럼 (Scrum)](013_scrum.md)
- [014. 번다운 차트 (Burndown Chart)](014_burndown-chart.md)
- [015. 익스트림 프로그래밍 (XP)](015_extreme-programming.md)
- [016. 칸반 (Kanban)](016_kanban.md)
- [017. 린·MVP (Lean·MVP)](017_lean-mvp.md)
- [018. 대규모 애자일 (SAFe·LeSS)](018_safe-less.md)
- [019. 데브옵스 (DevOps)](019_devops.md)
- [020. 코드형 인프라 (IaC)](020_infrastructure-as-code.md)
- [021. 지속적 통합·배포 (CI/CD)](021_continuous-delivery.md)
- [022. 사이트 신뢰성 엔지니어링 (SRE)](022_site-reliability-engineering.md)
- [023. 데브섹옵스 (DevSecOps)](023_devsecops.md)
- [024. MLOps·LLMOps](024_mlops-llmops.md)
- [025. 플랫폼 엔지니어링 (IDP)](025_platform-engineering.md)
- [026. 옵저버빌리티 (Observability)](026_observability.md)
- [027. 카오스 엔지니어링 (Chaos Engineering)](027_chaos-engineering.md)
- [028. 배포 전략 (카나리·블루그린·롤링)](028_deployment-strategies.md)
- [029. 깃옵스 (GitOps)](029_gitops.md)
- [030. 12-Factor App](030_twelve-factor-app.md)
- [031. 행위주도개발 (BDD)](031_behavior-driven-development.md)

## 요구공학·분석·명세

- 스터디노트 기반 축: `02_requirements_analysis, 03_design_architecture`
- 출제 관점: 요구 도출, 우선순위, 명세, 추적성으로 프로젝트 실패를 줄이는 분석 축

- [032. 요구공학 (Requirements Engineering)](032_requirements-engineering.md)
- [033. 기능·비기능 요구사항 (Functional·Non-functional)](033_functional-nonfunctional-requirements.md)
- [034. 유스케이스 다이어그램 (Use Case Diagram)](034_use-case-diagram.md)
- [035. DFD·자료사전 (Data Flow Diagram·Data Dictionary)](035_dfd-data-dictionary.md)
- [036. 요구사항 명세서 (SRS)](036_software-requirements-specification.md)
- [037. 검증과 확인 (V&V)](037_verification-validation.md)
- [038. 인스펙션·워크쓰루 (Inspection·Walkthrough)](038_inspection-walkthrough.md)
- [039. 요구사항 추적성 (RTM)](039_requirements-traceability-matrix.md)
- [040. 범위 크리프 (Scope Creep)](040_scope-creep.md)
- [041. 골드 플래팅 (Gold Plating)](041_gold-plating.md)
- [042. MoSCoW 우선순위 기법](042_moscow-prioritization.md)
- [043. 카노 모델 (Kano Model)](043_kano-model.md)
- [044. 품질기능전개 (QFD)](044_quality-function-deployment.md)
- [045. 유저스토리 맵·에픽 (User Story Map·Epic)](045_user-story-map-epic.md)

## 아키텍처·설계·코드 품질

- 스터디노트 기반 축: `03_design_architecture, 06_software_architecture, 07_object_oriented`
- 출제 관점: 모듈성, 설계 원칙, 아키텍처 스타일, 패턴, 품질속성을 판단하는 축

- [046. 응집도·결합도 (Cohesion·Coupling)](046_cohesion-coupling.md)
- [047. 추상화·정보은닉 (Abstraction·Information Hiding)](047_abstraction-information-hiding.md)
- [048. 4+1 뷰 아키텍처 모델](048_4plus1-view-model.md)
- [049. 계층형 아키텍처 (Layered Architecture)](049_layered-architecture.md)
- [050. 파이프-필터 아키텍처 (Pipe-Filter)](050_pipe-filter-architecture.md)
- [051. 이벤트 기반 아키텍처 (EDA)](051_event-driven-architecture.md)
- [052. MVC·MVP·MVVM](052_mvc-mvp-mvvm.md)
- [053. 서비스 지향 아키텍처 (SOA)](053_service-oriented-architecture.md)
- [054. 마이크로서비스 아키텍처 (MSA)](054_microservices-architecture.md)
- [055. 헥사고날·클린 아키텍처 (Hexagonal·Clean)](055_hexagonal-clean-architecture.md)
- [056. 도메인 주도 설계 (DDD)](056_domain-driven-design.md)
- [057. CQRS·이벤트 소싱 (CQRS·Event Sourcing)](057_cqrs-event-sourcing.md)
- [058. 아키텍처 트레이드오프 분석 (ATAM)](058_atam.md)
- [059. 통합 모델링 언어 (UML)](059_uml.md)
- [060. SOLID 원칙](060_solid-principles.md)
- [061. DRY·KISS·YAGNI](061_dry-kiss-yagni.md)
- [062. 싱글톤 패턴 (Singleton)](062_singleton-pattern.md)
- [063. 팩토리 패턴 (Factory Method)](063_factory-pattern.md)
- [064. 옵저버 패턴 (Observer)](064_observer-pattern.md)
- [065. 전략 패턴 (Strategy)](065_strategy-pattern.md)
- [066. 데코레이터 패턴 (Decorator)](066_decorator-pattern.md)
- [067. 프록시 패턴 (Proxy)](067_proxy-pattern.md)
- [068. 어댑터 패턴 (Adapter)](068_adapter-pattern.md)
- [069. 퍼사드 패턴 (Facade)](069_facade-pattern.md)
- [070. 객체지향 4대 특징 (OOP)](070_oop-features.md)
- [071. 함수형 프로그래밍 (Functional Programming)](071_functional-programming.md)
- [072. 제어역전·의존성주입 (IoC·DI)](072_ioc-di.md)
- [073. 관점지향 프로그래밍 (AOP)](073_aspect-oriented-programming.md)
- [074. 클린코드·코드스멜 (Clean Code·Code Smell)](074_clean-code-code-smell.md)
- [075. 정적·동적 분석 (Static·Dynamic Analysis)](075_static-dynamic-analysis.md)
- [076. ISO 25010 품질모델 (SQuaRE)](076_iso-25010-square.md)
- [077. 맥케이브 순환복잡도 (Cyclomatic Complexity)](077_cyclomatic-complexity.md)
- [078. 가용성 (MTBF·MTTR)](078_availability-mtbf-mttr.md)

## 품질공학·검증·테스팅

- 스터디노트 기반 축: `04_testing_quality, 11_testing_validation, 12_testing_maintenance`
- 출제 관점: 검증·확인, 테스트 설계, 커버리지, 성능, 회귀 전략을 묻는 축

- [079. 테스팅 7원리 (Testing Principles)](079_testing-principles.md)
- [080. 블랙박스 테스트 (Black-box Testing)](080_black-box-testing.md)
- [081. 화이트박스 커버리지 (White-box Coverage)](081_white-box-coverage.md)
- [082. 테스트 레벨 (단위·통합·시스템·인수)](082_test-levels.md)
- [083. 회귀 테스트 (Regression Testing)](083_regression-testing.md)
- [084. 테스트 더블 (Mock·Stub·Spy·Fake)](084_test-double.md)
- [085. 성능 테스트 (부하·스트레스·스파이크)](085_performance-testing.md)
- [086. 테스트 주도 개발 (TDD)](086_test-driven-development.md)

## 클라우드 네이티브·분산 아키텍처 운영

- 스터디노트 기반 축: `05_devops_ci_cd, 09_cloud_native_ai_architecture, 11_testing_validation`
- 출제 관점: 컨테이너, 서비스 통신, 분산 트랜잭션, 관측성과 복원력을 묻는 운영형 축

- [087. 컨테이너·쿠버네티스 (Container·Kubernetes)](087_container-kubernetes.md)
- [088. 서비스 메시 (Service Mesh)](088_service-mesh.md)
- [089. API 게이트웨이·BFF (API Gateway·Backend for Frontend)](089_api-gateway-bff.md)
- [090. 서비스 디스커버리 (Service Discovery)](090_service-discovery.md)
- [091. 회복탄력성 패턴 (서킷브레이커·벌크헤드·재시도)](091_resilience-patterns.md)
- [092. 사가 패턴 (Saga)](092_saga-pattern.md)
- [093. 2단계 커밋 한계 (2PC)](093_two-phase-commit.md)
- [094. 분산 추적 (Distributed Tracing)](094_distributed-tracing.md)
- [095. 서버리스·콜드스타트 (Serverless·Cold Start)](095_serverless-cold-start.md)
- [096. 모듈러 모놀리스 (Modular Monolith)](096_modular-monolith.md)
- [097. 스트랭글러 피그 패턴 (Strangler Fig)](097_strangler-fig.md)

## 보안 내재화·공급망 신뢰

- 스터디노트 기반 축: `08_security_compliance_devsecops, 11_testing_validation`
- 출제 관점: Secure SDLC, 위협 모델링, OSS 공급망 통제를 예방 관점으로 정리하는 축

- [098. 시큐어 SDLC (Secure SDLC)](098_secure-sdlc.md)
- [099. STRIDE 위협 모델링 (STRIDE)](099_stride-threat-modeling.md)
- [100. SCA·SBOM·공급망 보안 (SCA·SBOM·Supply Chain)](100_sca-sbom-supply-chain.md)
- [101. 시크릿 관리 (Secret Management·Vault)](101_secret-management-vault.md)

## 최신 실행기술·AI 기반 공학

- 스터디노트 기반 축: `09_cloud_native_ai_architecture, 10_trends_pm_quality`
- 출제 관점: 런타임 혁신과 AI 기반 공학을 도입 효과와 제약까지 묶어 설명하는 축

- [102. 가상 스레드 (Virtual Threads)](102_virtual-threads.md)
- [103. 웹어셈블리 (WebAssembly·WASM)](103_webassembly.md)
- [104. AI 활용 소프트웨어공학 (AI4SE)](104_ai4se.md)
