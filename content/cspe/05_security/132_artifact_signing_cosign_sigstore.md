---
title: "아티팩트 서명 - Cosign·Sigstore (Artifact Signing)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 132
---

# 📖 【암기용】 개념 완전 이해

> 목적: 아티팩트 서명을 처음 봐도 컨테이너·SBOM·provenance 검증까지 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 아티팩트 서명은 이미지·바이너리·SBOM이 승인된 주체에서 생성됐고 중간에 바뀌지 않았음을 암호학적으로 증명하는 기법임
- **왜 필요한가**: 레지스트리 태그는 재사용 가능하고 CI 산출물은 복사·교체될 수 있음. digest와 서명을 검증해야 배포 대상이 빌드한 결과물과 동일한지 판단 가능함.
- **핵심 직관**: 택배 상자에 봉인 스티커와 발송자 증명서를 붙이고, 도착지에서 봉인 훼손과 발송자 신원을 확인하는 과정임.

## 깊이 이해
- **배경·문제의식**: 컨테이너 기반 배포에서는 `latest` 태그, 임시 레지스트리 토큰, CI 권한이 공격면이 됨. 악성 이미지를 같은 태그로 밀어 넣으면 배포 시스템이 구분하지 못함.
- **작동 원리**: Cosign은 아티팩트 digest를 대상으로 서명하고, Sigstore는 OIDC identity, Fulcio 인증서, Rekor 투명 로그를 통해 장기 개인키 관리 부담을 줄임.
- **비유**: 주민등록증으로 공증 사무소에서 문서에 전자서명을 남기고, 공증 기록부에 시간과 서명 정보를 등록하는 방식과 유사함.
- **구체 예시**: CI가 `ghcr.io/org/app@sha256:9b1c2d3e4f5a6789` 이미지를 빌드한 뒤 Cosign keyless signing을 수행하고, Kubernetes admission 단계에서 OIDC issuer와 subject를 검증함.
- **흔한 오해·주의점**: 서명은 취약점 제거가 아님. 서명된 취약 이미지도 존재할 수 있으므로 SCA, SBOM, CVE 정책과 함께 운영해야 함.

## 연결 개념
- Sigstore: Fulcio, Rekor, Cosign으로 구성된 서명 생태계
- SLSA provenance: 서명 대상이 되는 빌드 출처 증거
- Admission Control: 미서명·검증 실패 이미지를 배포 전에 차단하는 지점

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 아티팩트 서명 답안은 "서명 생성"이 아니라 "digest 기준 검증, identity 확인, 배포 차단"까지 써야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 아티팩트 서명 (Artifact Signing)은 컨테이너 이미지·바이너리·SBOM의 digest에 전자서명을 부여해 출처와 무결성을 검증하는 통제임.
> 2. **가치**: Cosign·Sigstore는 OIDC, Fulcio, Rekor, OCI registry를 결합해 장기 개인키 보관 없이 서명·투명 로그·검증을 수행함.
> 3. **판단 포인트**: tag가 아니라 digest를 서명하고, certificate identity·issuer·transparency log inclusion을 배포 정책에 연결해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 컨테이너 공급망 무결성 이해 확인 | digest 서명, keyless signing, Rekor 투명 로그 | 이미지 태그 서명으로 설명하거나 digest 누락 |
| Sigstore 구성요소 판단 확인 | Cosign, Fulcio, Rekor, OIDC issuer, OCI registry | Cosign을 단순 CLI 도구로만 설명 |
| 운영 통제 설계 확인 | CI 서명, admission 검증, 정책 불일치 배포 거부 | 서명 생성 후 검증·차단 절차 누락 |

> 요약: 이 문제는 서명 알고리즘 설명보다 CI 신원 기반 서명과 배포 시 검증 정책을 연결하는 역량을 확인함.

---

## Ⅰ. 개요 및 필요성

아티팩트 서명은 배포 산출물의 출처·무결성 증명 기법임.
컨테이너 이미지, Helm chart, SBOM, provenance는 레지스트리와 CI 경로에서 교체될 수 있으므로 배포 전 암호학적 검증이 필요함.
Cosign·Sigstore는 OIDC 기반 keyless signing과 투명 로그를 제공해 공급망 위조를 배포 전 차단하게 함.

---

## Ⅱ. 구조 및 구성요소

```text
CI Identity -> Cosign Sign -> Fulcio Certificate -> Rekor Log
Artifact Digest -> OCI Registry Signature
Deploy Request -> Cosign Verify -> Admission Allow / Deny
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Cosign | 컨테이너 이미지·blob·attestation 서명 및 검증 | digest 기준 서명, OCI registry 저장 |
| Fulcio | OIDC identity 기반 단기 인증서 발급 | GitHub Actions, GitLab CI 등 issuer 확인 |
| Rekor | 서명과 metadata를 투명 로그에 기록 | inclusion proof, tamper-evident log |
| Policy Engine | 배포 전 서명·신원·issuer 검증 | Kyverno, OPA, Sigstore policy-controller |

> 요약: Sigstore 구조는 CI 신원, 단기 인증서, 투명 로그, 레지스트리 서명을 결합해 장기 키 관리 리스크를 줄임.

---

## Ⅲ. 동작원리 및 흐름도

```text
Build Artifact -> Calculate Digest -> Request OIDC Token
-> Fulcio Cert Issue -> Cosign Signature -> Rekor Upload
-> Registry Store -> Verify Identity / Issuer / Digest -> Deploy Decision
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | CI가 이미지 digest 계산 | SHA256 digest와 build output 일치 |
| 2 | OIDC 토큰으로 Fulcio 인증서 요청 | issuer, subject, workflow ref 확인 |
| 3 | Cosign이 digest 서명 후 Rekor 기록 | signature, certificate, log index 존재 |
| 4 | 서명과 아티팩트 레지스트리 저장 | tag가 아닌 digest reference 사용 |
| 5 | 배포 시 정책 검증 | identity allowlist, issuer, Rekor inclusion |

> 요약: 아티팩트 서명은 빌드 신원에서 시작해 배포 정책 검증으로 끝나며, digest 불일치 시 배포를 거부함.

---

## Ⅳ. 특징

| 구분 | 기존 방식 | Cosign·Sigstore 적용 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 신원 관리 | 장기 개인키 파일·KMS 의존 | OIDC 기반 keyless signing | 단기 인증서, CI identity 바인딩 |
| 검증 대상 | 이미지 태그·수동 승인 | SHA256 digest·certificate identity | tag 재사용 공격 차단 |
| 감사 근거 | CI 로그 보관 | Rekor transparency log | 서명 포함 여부와 시간 추적 |
| 한계 | 키 유출 대응 복잡 | OIDC issuer 신뢰와 정책 설계 필요 | issuer allowlist 오설정 방지 |

> 요약: Cosign·Sigstore는 키 보관보다 신원 기반 증명과 투명 로그에 초점을 두며, 운영 핵심은 배포 검증 정책임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | GPG key, KMS 서명 | Sigstore keyless signing | CI OIDC 신원 활용 가능 시 |
| 비용/성능 | 키 생성·보관·회전 운영 | Fulcio·Rekor 연동, 검증 자동화 | 릴리스 월 50회 이상이면 keyless 선호 |
| 운영/위험 | 키 파일 유출·공유 | issuer·subject 정책 오류 | 조직별 workflow subject 표준화 필요 |

> 요약: CI 신원 체계가 준비된 조직은 장기키 관리보다 keyless signing과 정책 검증을 우선 적용함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 잘못된 대상 서명 | tag 기준 서명, mutable tag 사용 | digest pinning, immutable tag policy | tag 서명 비율 0% |
| 신원 오용 | OIDC subject 범위 과다 | repo·branch·workflow allowlist | denied issuer/subject 건수 |
| 검증 우회 | admission controller 미적용 namespace | namespace label 강제, policy audit | 서명 검증 누락 namespace 0개 |

> 요약: 서명 운영의 주요 위험은 태그 서명, OIDC 범위 과다, 검증 우회이며 정책 지표로 상시 확인해야 함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 서명 적용률 | 운영 배포 이미지 100% cosign 서명 | registry scan, CI artifact metadata |
| 검증 실패 차단 | identity·issuer 불일치 100% deny | admission audit log |
| 감사 추적 | digest에서 CI run과 Rekor entry 5분 내 조회 | SIEM, Rekor, CI log |

> 요약: 아티팩트 서명 품질은 서명률, 차단률, 추적 시간으로 측정해야 하며 서명 파일 존재만으로 판단하지 않음.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. CI 단계: `cosign sign --identity-token` 또는 keyless workflow로 이미지 digest, SBOM, SLSA provenance를 모두 서명함.
2. 정책 단계: issuer, subject, repo, branch, workflow ref를 allowlist로 관리하고 production namespace는 미검증 이미지 admission deny 적용.
3. 감사 단계: Rekor log index, certificate identity, image digest, deployment revision을 SIEM에 저장해 사고 artifact 역추적 5분 목표 설정.

**결론 (2줄):**
- 기술사 판단: 컨테이너 배포 조직은 digest 서명과 admission 검증을 기본 통제로 두고, 고위험 업무는 private Fulcio·Rekor 또는 KMS 서명까지 검토함.
- 향후 방향: SBOM, VEX, SLSA attestation, Sigstore policy-controller가 결합되어 "서명된 산출물만 실행"하는 기본 정책으로 이동함.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "아티팩트 서명을 설명하시오", "Sigstore를 기술하시오" | Cosign-Fulcio-Rekor 서명·검증 흐름 | keyless signing 장점과 digest 검증 |
| 요구사항 명시형 | "컨테이너 배포 보안 방안을 제시하시오", "설계하시오" | CI 서명, registry 저장, admission 차단 흐름 | issuer 정책, namespace 통제, 감사 지표 |

> 요약: 설명형은 Sigstore 구성요소를 넓게 쓰고, 설계형은 digest·identity·admission deny를 중심으로 답안을 전환함.
