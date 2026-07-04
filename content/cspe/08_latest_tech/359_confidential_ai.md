---
title: "Confidential AI 기밀 AI (Confidential AI)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 359
---

# 📖 【암기용】 개념 완전 이해

> 목적: Confidential AI를 AI 학습·추론 과정에서 데이터와 모델을 사용 중에도 보호하는 보안 아키텍처로 이해하게 만든다.

## 한눈에
- **개요**: TEE와 암호 기술로 AI 데이터·모델·추론을 보호하는 방식
- **왜 필요한가**: AI는 입력 데이터, 모델 가중치, 프롬프트, 추론 결과가 메모리에서 평문으로 처리되는 시간이 있다. 이 구간은 저장·전송 암호화만으로 보호되지 않는다.
- **핵심 직관**: 금고에 보관할 때와 운반할 때만 잠그는 것이 아니라, 계산하는 순간에도 외부 관리자와 호스트 OS가 내용을 보지 못하게 격리한다.

## 깊이 이해
- **배경·문제의식**: 기업은 민감 데이터와 독점 모델을 클라우드 GPU에서 처리하려 하지만 인프라 운영자, 하이퍼바이저, 다른 tenant에 대한 노출 우려가 있다.
- **작동 원리**: Trusted Execution Environment가 코드와 데이터를 격리하고, remote attestation으로 실행 환경을 검증한 뒤 키를 주입해 학습 또는 추론을 수행한다.
- **비유**: 요리 재료와 레시피를 투명 주방에 두지 않고, 검증된 잠금 주방 안에서만 조리하고 완성품만 내보내는 방식이다.
- **구체 예시**: 의료기관은 환자 데이터를 confidential VM 또는 TEE 기반 추론 환경에 암호화 전송하고, attestation 성공 후에만 복호화 키를 제공한다.
- **흔한 오해·주의점**: Confidential AI가 모델 출력 유출, prompt injection, 학습 데이터 추론 공격을 모두 해결하지 않는다. TEE는 사용 중 데이터 보호 축이며 AI 보안 통제와 함께 써야 한다.

## 연결 개념
- Confidential Computing — 사용 중 데이터 보호 기술
- TEE — 하드웨어 기반 격리 실행환경
- Remote Attestation — 실행 환경 무결성 검증

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: Confidential AI는 TEE, attestation, key release, model/data governance로 AI 처리 중 데이터와 모델 노출을 줄이는 구조다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Confidential AI는 AI 학습·추론을 검증된 TEE에서 실행해 데이터와 모델을 사용 중에도 격리하는 아키텍처다.
> 2. **가치**: 민감 데이터, 독점 모델, 프롬프트, 추론 결과를 클라우드·공동 환경에서 처리할 때 관리자 접근 위험을 줄인다.
> 3. **판단 포인트**: remote attestation, key release, GPU TEE 지원, side-channel, 출력 정책, 감사로그를 검토한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 사용 중 데이터 보호 이해 확인 | TEE, attestation, key release | 저장·전송 암호화로만 설명 |
| AI 보안 적용 판단 확인 | 데이터·모델·프롬프트 보호 범위 | hallucination 해결책으로 오해 |
| 운영 리스크 확인 | side-channel, 공급망, 출력 유출 | TEE를 완전 격리로 단정 |

> 요약: 이 문제는 AI 처리 중 보호와 AI 애플리케이션 보안 통제를 구분하는 것이 핵심이다.

---

## Ⅰ. 개요 및 필요성

- 개요: 기밀 실행 AI
- 배경: AI 학습·추론은 메모리와 GPU에서 평문 데이터와 모델을 처리하므로 저장·전송 암호화만으로 노출면을 줄일 수 없음.
- 필요성: TEE와 remote attestation으로 검증된 실행환경에서만 키를 제공해 민감 데이터와 모델을 처리해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Encrypted Data / Model -> Confidential VM / TEE -> AI Runtime
                         -> Remote Attestation -> Key Release
                         +-> Policy / Audit / Output Filter
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| TEE/Confidential VM | 실행 중 데이터 격리 | CPU/GPU 지원 확인 |
| remote attestation | 코드·환경 무결성 검증 | measurement 검증 |
| key broker | attestation 성공 시 키 제공 | policy-based release |
| AI runtime | 학습·추론 수행 | model serving |

> 요약: Confidential AI는 TEE 자체보다 attestation과 키 제공 정책이 결합될 때 보호 경계가 형성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
이미지/런타임 측정 -> attestation 검증 -> 키 제공
-> 데이터/모델 복호화 -> TEE 내부 추론 -> 출력 정책·감사 기록
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | AI runtime 이미지와 TEE 측정값을 생성함 | measurement hash |
| 2 | verifier가 attestation evidence를 검증함 | trusted TCB |
| 3 | key broker가 정책 충족 시 복호화 키를 제공함 | key release log |
| 4 | 추론 결과를 출력 필터와 감사로그에 반영함 | output policy |

> 요약: Confidential AI는 검증된 실행환경 확인 후 키를 주입하는 순서가 보안 경계를 만든다.

---

## Ⅳ. 특징

| 구분 | 일반 AI Serving | Confidential AI | 판단 기준 |
|:---|:---|:---|:---|
| 데이터 보호 | 저장·전송 암호화 | 사용 중 격리 추가 | 민감도 |
| 신뢰 대상 | 클라우드 관리자 포함 | TEE TCB로 축소 | threat model |
| 검증 | 배포 승인 | remote attestation | 런타임 무결성 |
| 비용 | 표준 인스턴스 | confidential CPU/GPU | 지연·가격 |

> 요약: Confidential AI는 인프라 운영자 신뢰를 TEE와 attestation으로 줄이지만 TCB와 성능 비용을 검토해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 개인정보 처리 | 익명화·마스킹 | TEE 내부 처리 | 원본 필요 여부 |
| 공동 분석 | 데이터 반출 | confidential collaboration | 기관 간 데이터 공유 |
| 모델 보호 | 접근통제 | 암호화 모델+attestation | 모델 IP 보호 |

> 요약: Confidential AI는 원본 데이터 또는 모델을 외부 환경에서 처리해야 할 때 검토한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| side-channel | 캐시·메모리 접근 패턴 | 패치, TCB 업데이트, workload 분리 | CVE status |
| 출력 유출 | 모델이 민감정보 반환 | output filtering, DLP | leakage finding |
| attestation 우회 | 검증 정책 오류 | allowlist measurement, key broker policy | failed attestation |

> 요약: Confidential AI 리스크는 TEE 취약점, 출력 데이터 통제, attestation 정책 오류에서 발생한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 무결성 | 승인된 measurement만 실행 | attestation log |
| 보호범위 | 데이터·모델·프롬프트 분류 | data flow review |
| 성능 | 추론 지연 SLA 충족 | benchmark |

> 요약: Confidential AI는 암호화 여부보다 승인된 실행환경, 보호 대상 흐름, 지연 영향을 측정해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 보호 대상을 학습 데이터, 추론 입력, 모델 가중치, 프롬프트, 출력으로 분류하고 threat model을 작성함.
2. confidential VM/GPU 지원, remote attestation 검증, key broker 정책, TCB 업데이트 절차를 구축함.
3. TEE 보호와 별도로 prompt injection, output DLP, model access control, audit log를 AI 보안 정책에 포함함.

**결론 (2줄):**
- 기술사 판단: 민감 원본 데이터나 독점 모델을 외부 인프라에서 처리해야 하면 Confidential AI를 적용하고, 공개 데이터 추론은 일반 serving이 단순함.
- 향후 방향: Confidential AI는 GPU TEE, federated learning, privacy-enhancing technology와 결합해 규제 산업의 AI 활용 기반이 됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Confidential AI를 설명하시오" | attestation-key release-추론 흐름 | 일반 AI serving과 차이 |
| 요구사항 명시형 | "민감정보 AI 활용 방안을 제시하시오" | 보호 대상 분류와 TEE 적용 | side-channel·출력 유출 통제 |

> 요약: 설명형은 기밀 실행 구조를, 방안형은 데이터 흐름과 정책 검증을 중심으로 작성한다.
