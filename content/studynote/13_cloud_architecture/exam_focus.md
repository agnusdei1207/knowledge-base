---
title: "컴퓨터시스템응용기술사 핵심 트랙"
date: "2026-06-29"
tags:
  - "studynote-cloud-architecture"
weight: 91
---

## 컴퓨터시스템응용기술사 핵심 트랙

- 기준: 컴퓨터시스템응용기술사 관점만 반영
- 과목 총 노트 수: 372개
- 과목 필요성:
  - 클라우드 아키텍처는 현대 컴퓨터시스템의 표준 운영 기반으로, 인프라 설계 문제를 시스템 확장성·가용성·비용 구조와 함께 묻는 출제와 직결된다.
  - 단순 서비스 모델 비교보다 가상화, 컨테이너, 쿠버네티스(Kubernetes), 마이크로서비스 아키텍처(Microservices Architecture, MSA) 간 연결 구조를 설명할 수 있어야 한다.
  - 기술사는 장애 대응, 멀티 클라우드, 벤더 종속성, 보안 경계, 운영 자동화까지 포함한 아키텍처 판단력을 본다.
  - 따라서 정의 암기보다 "왜 이 구조를 선택하는가"와 "어떤 트레이드오프를 감수하는가"를 답안 골격으로 훈련해야 한다.
- 우선 학습 챕터:
  - `01_virtualization`
  - `02_iaas_paas_saas`
  - `03_msa_serverless`
  - `04_devops_observability`
  - `07_container_k8s`
  - `05_data_engineering`
- 추천 핵심 키워드 목표 수: 90개
- 단답형 포인트:
  - IaaS(Infrastructure as a Service), PaaS(Platform as a Service), SaaS(Software as a Service), FaaS(Function as a Service), Service Mesh, Circuit Breaker, HPA(Horizontal Pod Autoscaler)처럼 구조와 기능을 2~4문장 내로 정의
  - 쿠버네티스 제어 평면(Control Plane), CSI(Container Storage Interface), CNI(Container Network Interface), mTLS(Mutual Transport Layer Security) 등 구성요소 역할 구분
  - Rehost, Replatform, Refactor 등 클라우드 전환 전략 차이 정리
- 서술형 포인트:
  - 클라우드 네이티브 전환 로드맵, MSA 분해 기준, 서버리스 적용 한계, 멀티 클라우드 운영모델을 비교형 답안으로 전개
  - 확장성, 복원력, 비용, 보안, 운영복잡도를 동시에 평가하는 의사결정형 문제가 핵심
  - 장애 전파 차단, 데이터 중력(Data Gravity), 벤더 종속성, 운영 자동화 수준을 함께 언급해야 고득점 가능
- 최신 기술 동향 연결:
  - 클라우드 네이티브: 컨테이너, 쿠버네티스, 서비스 메시(Service Mesh), GitOps와 연계
  - 플랫폼 엔지니어링(Platform Engineering): 개발자 셀프서비스 플랫폼, 내부 개발자 플랫폼(Internal Developer Platform, IDP) 설계 관점으로 확장
  - 데이터 파이프라인: 객체 스토리지 기반 데이터 플랫폼과 애플리케이션 플랫폼의 결합 관점 정리
  - AIOps(Artificial Intelligence for IT Operations): 관측성 데이터 기반 자동 확장·자동 복구 시나리오와 연결
  - 레이크하우스(Lakehouse): 클라우드 데이터 플랫폼을 위한 스토리지-컴퓨트 분리 구조와 접점 이해
