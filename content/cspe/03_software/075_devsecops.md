---
title: "DevSecOps (DevSecOps)"
date: "2026-07-05"
tags:
  - "cspe-software"
weight: 75
---

## Ⅰ. 개요
- **정의**: DevOps 파이프라인 전 단계에 보안(Sec)을 내재화한 개발·운영 체계임
- **배경/필요성**: 배포 후 보안 점검 방식은 수정 비용이 100배 이상 증가하므로 Shift-Left 방식의 보안 통합이 필요함
- **비유**: 건물 완공 후 소방 점검이 아닌, 설계 단계부터 방화벽을 포함하는 것과 동일함

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| DevOps 대비 보안 내재화 차이점 | Shift-Left, Security as Code, 자동화 게이트 | DevOps(074 참조)와 단순 보안 도구 추가로 설명하지 말 것 |

> 요약: DevSecOps는 보안을 파이프라인 초기부터 자동화·내재화한 개발 운영 체계임

## Ⅱ. 구성요소
```text
Plan --> Code --> Build --> Test --> Release --> Deploy --> Operate
  |       |        |         |         |          |          |
Threat  SAST     SCA/DAST  Pen-Test  Sign      Policy    RASP/WAF
Model   Lint     Scan      Gate      Verify    Enforce   Monitor
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| SAST | 소스코드 정적 분석으로 코딩 단계 취약점 탐지 | 원고 맞춤법 검사기 |
| SCA | 오픈소스 라이브러리의 알려진 CVE 스캔 | 식재료 원산지 검증 |
| DAST | 실행 중 애플리케이션에 공격 시뮬레이션 수행 | 완성 건물 침투 테스트 |
| Security as Code | 보안 정책을 OPA/Rego 등 코드로 정의·버전 관리 | 법규를 프로그래밍 |

> 요약: SAST/SCA/DAST와 Security as Code로 파이프라인 전 구간 보안을 자동화함

## Ⅲ. 절차
```text
Threat Model --> SAST --> SCA --> DAST --> Sign --> Deploy --> Monitor
     |             |       |       |        |                   |
   설계 보안    코드 보안  의존성  런타임   무결성              RASP
```
- 1단계: 설계 단계에서 위협 모델링(STRIDE 등)으로 공격 표면 식별함
- 2단계: 코드 커밋 시 SAST·SCA가 자동 실행되어 취약점 포함 빌드를 차단함
- 3단계: 스테이징에서 DAST·퍼즈 테스트로 런타임 취약점 탐지함
- 4단계: 이미지 서명(cosign) 검증 후 배포하고 RASP·WAF로 런타임 보호함

> 요약: 위협 모델링-정적 분석-동적 분석-런타임 보호 4단계로 보안을 Shift-Left함

## Ⅳ. 문제점
- 파이프라인 지연: 보안 스캔 추가로 빌드 시간이 증가하여 개발 속도 저하됨
- 오탐(False Positive) 과다: SAST 도구의 오탐률로 개발자 피로도 증가함
- 보안 역량 부족: 개발자에게 보안 책임 이관 시 전문성 부족으로 형식적 대응 발생함

> 요약: 빌드 지연, 오탐 과다, 보안 역량 부족이 주요 문제임

## Ⅴ. 개선방안
1. 단기: 스캔을 병렬화·증분 분석으로 전환하여 파이프라인 지연 최소화함
2. 중기: 오탐 학습 기반 튜닝·우선순위 필터링으로 의미 있는 취약점만 리포트함
3. 장기: Security Champion 프로그램 운영으로 팀별 보안 전문가 육성함

> 요약: 병렬 스캔, 오탐 튜닝, 보안 인력 육성으로 개선 가능함

## Ⅵ. 전망
- 발전 방향: AI 기반 코드 취약점 탐지와 자동 패치 생성이 보안 자동화를 가속할 전망임
- 기술사적 판단: DevOps(074 참조)와 차별화하여 보안 Shift-Left 구체 사례를 서술해야 함
- 기술사 제언: SBOM + Supply Chain Security 체계와 연계한 종합 보안 파이프라인 설계를 권고함
