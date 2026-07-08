---
title: "LLM03 Supply Chain (LLM03 Supply Chain)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 199
extra:
  question_no: "199"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- LLM03는 모델과 데이터와 라이브러리와 플러그인 등 외부 AI 부품 전체를 공급망 위험으로 본 항목임
- AI 공급망은 코드뿐 아니라 가중치 파일과 데이터셋이 공격 표면이라는 점이 전통 소프트웨어와 다름
- 파일 포맷 안전성과 provenance와 AI-SBOM이 핵심 통제 수단임

## Ⅰ. 개요

- **정의/개념**: LLM03 Supply Chain은 외부 모델과 데이터셋과 라이브러리와 플러그인 같은 서드파티 AI 컴포넌트의 취약점과 변조와 악성 행위가 애플리케이션 전체로 전이되는 OWASP 공급망 위험 항목임
- **배경/필요성**: 대부분의 기업은 공개 허브와 오픈소스 패키지와 외부 데이터에 의존해 생성형 AI를 구축하므로, 외부 자산의 무결성과 출처를 검증하지 않으면 시스템 전체가 침해될 수 있음

## Ⅱ. 특징

- 코드 취약점뿐 아니라 모델 가중치와 데이터셋 자체가 공격 벡터가 됨
- 오염된 파일 하나가 로드 시점부터 RCE와 백도어와 성능 훼손을 동시에 일으킬 수 있음
- 공급망 리스크는 기술 문제와 라이선스·거버넌스 문제를 함께 수반함
- 반입 전 검증과 내부 레지스트리 운영이 실무 방어의 핵심임

## Ⅲ. 종류 및 비교

| 판단 기준 | Traditional SW Supply Chain | AI Model Supply Chain | AI Data Supply Chain |
|:---|:---|:---|:---|
| 주요 자산 | 코드, 패키지 | 가중치, 체크포인트 | 데이터셋, 문서, 피드백 |
| 대표 위협 | 취약 라이브러리, typosquatting | poisoned weights, unsafe serialization | poisoning, license, provenance 문제 |
| 대표 방어 | SBOM, signing | AI-SBOM, signed registry, safetensors | lineage, data approval gate |
| 탐지 난도 | 상대적으로 성숙 | 높음 | 높음 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| External Model, Dataset Source | 허브와 저장소와 벤더가 공급하는 외부 자산 원천으로 신뢰 평가가 필요함 |
| Package, Plugin Dependency | 프레임워크와 확장 도구가 런타임 취약점과 권한 오남용 경로가 될 수 있음 |
| Ingestion Sandbox, Scanner | 모델 포맷과 악성 행위와 라이선스를 반입 전 검사하는 격리 검증 계층임 |
| Registry, Provenance Ledger | 승인된 자산만 내부 레지스트리에 등록하고 해시와 버전과 출처를 추적함 |
| Runtime Policy, AI-SBOM | 운영 중 사용 중인 자산 관계를 가시화해 사고 시 영향 범위를 빠르게 좁힘 |

```text
+-------------------+      +-------------------+      +-------------------+
| External Sources  | ---> | Sandbox / Scanner | ---> | Trusted Registry  |
+-------------------+      +-------------------+      +-------------------+
                                                           |
                                                           v
                                                   +-------------------+
                                                   | Runtime / AI-SBOM |
                                                   +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 외부 자산 반입    | --> | 무결성/포맷 검사 | --> | 승인 레지스트리 등록 | --> | 런타임 추적/감사 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **외부 자산 반입**: 모델과 데이터와 패키지를 외부에서 가져옴
2. **무결성 및 포맷 검사**: 해시와 serialization과 라이선스를 점검함
3. **승인 레지스트리 등록**: 검증된 자산만 내부 허용 목록에 올림
4. **런타임 추적 및 감사**: 실제 사용 버전과 의존성을 운영 중 계속 추적함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 안전하지 않은 직렬화 포맷과 검증 없는 체크포인트 로딩은 모델 반입 순간부터 RCE나 백도어 위험을 열 수 있음
   - 해결방안: safetensors 우선 정책과 sandbox loading을 적용하고 unsafe format usage rate와 malicious load detection rate로 검증함
2. 문제: 어떤 모델과 데이터와 패키지가 서비스에 쓰였는지 가시성이 없으면 사고 발생 시 영향 범위와 원인 파악이 느려질 수 있음
   - 해결방안: AI-SBOM과 provenance registry를 적용하고 dependency trace completeness와 incident triage time으로 검증함
3. 문제: 오픈소스 허브 의존이 높은데 내부 승인 없이 개발자가 임의로 자산을 반입하면 공급망 거버넌스가 무력화될 수 있음
   - 해결방안: private registry와 approval workflow를 적용하고 unapproved asset usage rate와 onboarding lead time으로 검증함

## Ⅶ. 적용 사례

- 기업 생성형 AI 플랫폼이 외부 모델 반입을 내부 레지스트리와 safetensors 정책으로 통제하며 확인 지표는 unsafe format usage rate와 approval compliance임
- 금융권 AI 서비스가 AI-SBOM과 모델 provenance를 운영해 사고 대응을 단축하며 확인 지표는 dependency trace completeness와 incident triage time임
- RAG 서비스가 외부 플러그인과 라이브러리를 샌드박스 검증 후 사용하며 확인 지표는 malicious dependency detection rate와 runtime integrity score임

## Ⅷ. 결론

LLM03는 생성형 AI를 구성하는 외부 자산 전체가 신뢰 경계 밖에 있음을 보여주므로 내부 레지스트리와 AI-SBOM 중심의 공급망 통제가 필수임.
