---
title: "컴퓨터시스템응용기술사 핵심 트랙"
date: "2026-06-29"
tags:
  - "studynote-security"
weight: 91
---

## 컴퓨터시스템응용기술사 핵심 트랙

- 과목 총 노트 수: 1049개

### 왜 핵심인가
- 보안은 모든 시스템 설계 답안의 감점 방지 축이 아니라, 독립 득점 축으로 작동하는 필수 과목이다.
- 암호, 네트워크, 애플리케이션, IAM(Identity and Access Management, 통합 계정·권한 관리), 침해대응을 한 문제에서 엮어 내는 통합형 출제가 가능하다.
- 컴퓨터시스템응용기술사 답안은 "안전한 구조를 설계할 수 있는가"를 보기 때문에 제로 트러스트와 공급망 보안 관점이 강하게 반영된다.
- 최신 환경이 클라우드, API, AI로 이동하면서 보안은 별도 파트가 아니라 아키텍처 기본 조건이 되었다.

### 우선 학습 챕터
- `01_intro_principles`: CIA, 위험관리, 보안 모델, 기본 통제
- `02_crypto`: 대칭키, 비대칭키, 해시, 전자서명, 키관리
- `03_network_security`: TLS, VPN, Zero Trust, SASE
- `05_web_app_security`: OWASP, API 보안, 인증/세션, 공급망 취약점
- `11_iam_access_control`: AAA, RBAC, ABAC, MFA
- `13_secops_ir_forensics`: SIEM, SOAR, 사고대응, 포렌식
- `16_data_privacy`: 개인정보보호, DLP, 암호화, 비식별화
- `19_ai_advanced_security`: LLM 보안, 프롬프트 인젝션, 모델 악용

### 추천 핵심 키워드 목표 수
- 180개

### 단답형 분리 포인트
- 정의형: AES(Advanced Encryption Standard, 고급 암호화 표준), RSA(Rivest-Shamir-Adleman), TLS(Transport Layer Security), RBAC(Role-Based Access Control), DLP(Data Loss Prevention)
- 분류형: 대칭키 vs 비대칭키, 인증 vs 인가, IDS(Intrusion Detection System, 침입탐지시스템) vs IPS(Intrusion Prevention System, 침입방지시스템)
- 절차형: 인증 흐름, 키 교환, 사고대응 단계
- 공격형: SQL Injection, XSS(Cross-Site Scripting), SSRF(Server-Side Request Forgery), 랜섬웨어 특징

### 서술형 분리 포인트
- "자산-위협-취약점-통제-운영" 순으로 써야 보안 답안이 구조적으로 안정적이다.
- 암호나 프로토콜은 원리만 적지 말고 적용 위치, 성능, 키관리 이슈까지 함께 서술
- 제로 트러스트, 보안관제, IAM, 데이터보호를 계층형 방어 체계로 묶어 통합 설계 관점 제시
- 법/제도형 문제는 기술 통제, 관리 통제, 감사 증적을 분리해 답안 체계를 세우는 것이 유리하다.

### 최신 기술 동향 연결
- LLM Security(대규모 언어 모델 보안), Prompt Injection(프롬프트 인젝션), Model Leakage(모델 정보 유출)를 AI 서비스 보안 축으로 연결
- Software Supply Chain Security(소프트웨어 공급망 보안), SBOM(Software Bill of Materials, 소프트웨어 자재명세서), SLSA(Supply-chain Levels for Software Artifacts)를 개발 보안 체계와 연결
- Zero Trust Architecture(제로 트러스트 아키텍처), SASE(Secure Access Service Edge), CNAPP(Cloud-Native Application Protection Platform)를 클라우드 전환형 문제와 연결
- Post-Quantum Cryptography(양자내성암호), Data Security Posture Management(데이터 보안 태세 관리), AI 기반 SOC(Security Operations Center, 보안관제센터) 자동화를 차세대 운영 포인트로 정리
