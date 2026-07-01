---
title: "AI 공급망 보안 (AI Supply Chain Security)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 156
---

# 📖 【암기용】 개념 완전 이해

> 목적: AI 공급망 보안을 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 데이터·모델·코드·패키지·학습환경·배포경로 전반의 변조와 취약점을 통제하는 보안 체계
- **왜 필요한가**: AI 서비스는 오픈소스 모델, 학습 데이터, 파이썬 패키지, 컨테이너, GPU 클러스터, 모델 레지스트리를 연결한다. 어느 한 지점의 변조가 전체 추론 결과와 고객 데이터에 영향을 준다.
- **핵심 직관**: AI 모델도 소프트웨어 제품처럼 원재료, 조립 과정, 서명, 출하 검사를 기록해야 한다.

## 깊이 이해
- **배경·문제의식**: 기존 SW 공급망은 소스코드와 빌드 산출물 중심이었다. AI는 여기에 데이터셋, pretrained model, fine-tuning adapter, prompt template, vector index, evaluation set이 추가되어 변조 지점이 늘어난다.
- **작동 원리**: 데이터 출처를 검증하고, 모델·패키지 SBOM/ML-BOM을 작성하며, 학습·빌드 provenance를 SLSA 방식으로 서명한다. 모델 레지스트리에서는 hash, 서명, 취약점 스캔, 라이선스, 평가 결과를 gate로 확인한다.
- **비유**: 의약품 생산처럼 원료 입고, 배합, 제조시설, 품질검사, 출하번호를 기록하는 방식이다. AI에서는 데이터와 모델이 원료이고 학습 파이프라인이 제조 공정이다.
- **구체 예시**: 오픈소스 LLM을 도입할 때 model hash, license, dataset card, 안전성 평가, dependency CVE, container image scan을 통과해야 운영 레지스트리에 승격한다.
- **흔한 오해·주의점**: 모델 파일만 스캔하면 끝이 아니다. poisoned dataset, malicious pickle, dependency confusion, backdoor adapter, vector DB 오염까지 공급망 범위에 포함해야 한다.

## 연결 개념
- SLSA·SBOM - 빌드 provenance와 구성요소 목록 관리
- 모델 보안 - backdoor, model stealing, prompt injection, evaluation poisoning
- MLOps 보안 - 학습·검증·배포 파이프라인 통제

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: AI 공급망 보안은 코드 취약점 관리가 아니라 데이터, 모델, 학습 파이프라인, 레지스트리, 추론 서비스를 하나의 provenance 체계로 묶는 문제임.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: AI 공급망 보안은 AI 생명주기 전반의 구성요소와 산출물에 대해 출처, 무결성, 취약점, 라이선스, 평가 결과를 검증하는 체계임.
> 2. **가치**: 데이터 오염, 모델 백도어, 악성 패키지, 레지스트리 변조가 운영 추론 결과로 확산되는 경로를 차단함.
> 3. **판단 포인트**: SBOM/ML-BOM, SLSA provenance, 서명 검증, 모델 레지스트리 gate, 데이터 lineage를 함께 구축해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| AI 공급망 공격면 식별 | 데이터, 모델, 코드, 패키지, 컨테이너, registry, vector index | 일반 SW 공급망만 설명하고 데이터·모델 누락 |
| 통제 기술 설계 | SBOM, ML-BOM, SLSA, Sigstore, model signing, lineage | 백신 스캔만 제시 |
| 운영 지표 판단 | provenance coverage, scan gate, eval gate, rollback | 학습·배포 승인 기준 누락 |

> 요약: 이 문제는 AI 산출물의 원재료부터 운영 배포까지 변조를 추적·검증하는 공급망 설계를 요구함.

---

## Ⅰ. 개요 및 필요성

- 개요: AI 구성요소 무결성 통제
- 배경: AI 시스템은 데이터셋, 오픈소스 모델, 패키지, 컨테이너, GPU 학습환경, 모델 레지스트리를 연결한다.
- 필요성: SLSA, SBOM/ML-BOM, 서명된 모델 아티팩트로 출처와 hash를 검증해 백도어·개인정보 유출·추론 오류를 차단해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Data Source -> Training Pipeline -> Model Artifact -> Model Registry -> Serving Runtime
                    +-> SBOM/ML-BOM
                    +-> Provenance/Signature
                    +-> Security/Eval Gate
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Data Lineage | 데이터 출처·동의·품질·오염 여부 추적 | datasheet, hash, PII scan |
| Build/Train Provenance | 학습 코드·환경·파라미터·실행자 기록 | SLSA, in-toto, attestation |
| Model Artifact Control | 모델 파일·adapter·tokenizer 무결성 검증 | SHA-256, Sigstore, safe format |
| Registry Gate | 취약점·라이선스·평가 기준 통과 여부 결정 | CVE scan, license policy, eval score |
| Serving Guard | 배포 후 drift·abuse·rollback 통제 | canary, audit log, model version |

> 요약: AI 공급망은 데이터 lineage에서 serving guard까지 provenance와 gate를 연결해야 함.

---

## Ⅲ. 동작원리 및 흐름도

```text
구성요소 수집 -> hash/SBOM 생성 -> 학습 provenance 서명
-> 보안·품질 gate -> registry 승격 -> 배포·감시 -> rollback
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 데이터·코드·모델·패키지 수집 | 출처, license, hash, PII scan |
| 2 | 학습·빌드 환경 재현 정보 기록 | container digest, GPU image, parameter |
| 3 | SBOM/ML-BOM과 provenance 서명 | SLSA attestation, Sigstore |
| 4 | 보안·품질 gate 수행 | critical CVE 0건, backdoor test, eval threshold |
| 5 | 레지스트리 승격·배포·감시 | signed artifact only, canary, rollback |

> 요약: AI 공급망 보안은 산출물 생성 시 증적을 만들고 배포 전 gate에서 검증한 뒤 운영 감시로 폐쇄 루프를 구성함.

---

## Ⅳ. 특징

| 구분 | 일반 SW 공급망 | AI 공급망 보안 | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 구성요소 | 소스코드, 패키지, 이미지 | 데이터, 모델, tokenizer, adapter, vector index | SBOM+ML-BOM |
| 공격 | dependency confusion, tampering | data poisoning, model backdoor, pickle RCE | OWASP ML/LLM risks |
| 검증 | 빌드 provenance 중심 | 학습 provenance+평가 gate | SLSA, in-toto, Sigstore |
| 운영 | 버전 배포 | 모델 drift, abuse, rollback | critical CVE 0건, signed only |

> 요약: AI 공급망은 SW 공급망 통제에 데이터·모델 lineage와 평가 gate가 추가된 형태임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | DevSecOps SBOM | MLOps SBOM+ML-BOM | 외부 모델·데이터 사용 시 필수 |
| 무결성 | 이미지 서명 | 데이터·모델·adapter 서명 | 모델 registry 운영 조직 |
| 품질 | 단위 테스트 | 안전성 eval, backdoor test, drift test | 고객 영향 모델, 규제 대상 모델 |
| 운영 | 수동 승인 | policy-as-code gate | 배포 빈도 주 1회 이상 |

> 요약: 외부 모델과 데이터가 포함되면 일반 SBOM만으로 부족하며 ML-BOM과 평가 gate가 필요함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Data Poisoning | 학습 데이터 오염·라벨 조작 | lineage, anomaly scan, holdout eval | 오염 샘플 탐지율 95% 이상 |
| Model Backdoor | pretrained model·adapter 변조 | signed model, trigger test, safe format | backdoor test 통과율 100% |
| Malicious Dependency | typosquatting, dependency confusion | private registry, lockfile, CVE scan | critical CVE 0건 |
| Registry Tampering | 모델 교체·권한 남용 | RBAC, MFA, immutable version, audit log | 미서명 배포 0건 |

> 요약: AI 공급망 리스크는 데이터 오염, 모델 백도어, 악성 의존성, 레지스트리 변조로 나누어 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| provenance coverage | 배포 모델 100% attestation 보유 | registry query, CI/CD gate |
| 취약점 기준 | critical CVE 0건, high CVE 예외승인 100% | SBOM scan, ticket audit |
| 모델 무결성 | signed artifact only, hash mismatch 0건 | Sigstore verify, registry policy |
| 평가 gate | 안전성·정확도·편향 기준 통과율 100% | eval report, approval workflow |

> 요약: 공급망 성숙도는 provenance 보유율, CVE 기준, 서명 검증, 평가 gate 통과로 측정함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. AI BOM 구축: 데이터셋, 모델, tokenizer, adapter, 패키지, 컨테이너 digest를 SBOM/ML-BOM으로 관리
2. 서명·증적 gate 적용: SLSA provenance, in-toto attestation, Sigstore 서명을 CI/CD와 모델 레지스트리 승격 조건으로 설정
3. 보안 평가 운영: data poisoning scan, backdoor trigger test, critical CVE 0건, 안전성 eval 통과를 배포 승인 기준으로 적용

**결론 (2줄):**
- 기술사 판단: 내부 모델만 쓰면 lineage와 registry gate를 우선하고, 외부 pretrained model 사용 시 서명·라이선스·backdoor test를 필수로 둠
- 향후 방향: AI 공급망 보안은 DevSecOps, MLOps, AI governance를 결합한 signed AI artifact 운영체계로 발전함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "AI 공급망 보안을 설명하시오", "기술하시오" | 수집, provenance, gate, registry, 배포 흐름 | 일반 SW 공급망과 AI 공급망 차이 |
| 요구사항 명시형 | "도입 방안을 제시하시오", "설계하시오" | SBOM/ML-BOM, SLSA, Sigstore, eval gate | CVE 0건, signed only, provenance 100% |

> 요약: 설명형은 생명주기와 공격면을, 설계형은 증적·서명·평가 gate 지표를 중심으로 작성함.
