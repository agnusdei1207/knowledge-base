---
title: "서브리소스 무결성 SRI (Subresource Integrity)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 89
---

# 📖 【암기용】 개념 완전 이해

> 목적: 서브리소스 무결성 SRI를 처음 봐도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 브라우저가 외부 script·style 파일의 해시를 검증해 변조된 리소스 실행을 차단하는 표준
- **왜 필요한가**: 웹 페이지는 CDN과 외부 라이브러리에 의존한다. CDN 계정 탈취, 중간자 변조, 배포 오류로 script가 바뀌면 사용자 브라우저에서 악성 코드가 실행된다.
- **핵심 직관**: SRI는 택배 상자에 적힌 봉인 번호와 실제 내용물의 봉인 번호가 같은지 브라우저가 확인하는 절차임

## 깊이 이해
- **배경·문제의식**: 외부 리소스 도메인을 신뢰해도 파일 내용이 항상 같다는 보장은 없다. SRI는 HTML에 기대 해시를 적고 브라우저가 다운로드 후 계산한 해시와 비교한다.
- **작동 원리**: 외부 `script` 또는 `link` 태그에 `integrity`와 `crossorigin` 속성을 지정한다. 브라우저는 리소스를 받은 뒤 SHA-256/384/512 해시를 계산하고 일치하지 않으면 실행하지 않는다.
- **비유**: 계약서 원본의 지문을 미리 받아두고, 배송된 문서의 지문이 다르면 서명을 거부하는 방식과 같다.
- **구체 예시**: CDN의 jQuery 파일에 `sha384` 해시를 넣으면 CDN 파일이 1바이트만 바뀌어도 브라우저가 script 실행을 차단하고 콘솔 오류를 남긴다.
- **흔한 오해·주의점**: SRI는 리소스 버전이 바뀌면 해시도 갱신해야 한다. 동적으로 자주 바뀌는 파일에는 적용이 어렵고, CORS 설정과 `crossorigin` 속성이 필요할 수 있다.

## 연결 개념
- CSP - 허용 출처 제한과 위반 보고
- 공급망 보안 - CDN·패키지·빌드 산출물 변조 통제
- 해시 함수 - SHA-256/384/512 기반 무결성 검증

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: SRI를 해시 속성 암기가 아니라 CDN 신뢰 경계에서 리소스 내용 변조를 브라우저가 검증하는 통제로 설명한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SRI는 `integrity` 속성에 지정한 SHA 해시와 다운로드 리소스 해시를 브라우저가 비교해 변조된 script·style 실행을 차단하는 표준임
> 2. **가치**: CDN 변조, 외부 라이브러리 교체, 중간자 공격을 브라우저 실행 직전에 탐지하며 CSP와 결합해 공급망 위험을 줄임
> 3. **판단 포인트**: 해시 생성·버전 고정·crossorigin·배포 자동 갱신·차단 로그 확인을 함께 설계해야 함

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| CDN 리소스 변조 통제 이해 | `integrity`, SHA-256/384/512, browser hash compare | HTTPS만으로 내용 무결성 검증 가능하다고 설명 |
| 브라우저 보안 정책 연계 | SRI+CSP, crossorigin, version pinning | CSP와 SRI의 역할을 혼동 |
| 운영 실패 모드 판단 | 해시 미갱신 시 리소스 차단, 배포 파이프라인 반영 | 라이브러리 자동 업데이트와 해시 고정을 동시에 요구 |

> 요약: 이 문제는 외부 리소스의 출처가 아니라 파일 내용이 기대한 해시와 같은지 브라우저가 검증하는지를 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: 외부 리소스 무결성 검증
- 배경: CDN과 오픈소스 JavaScript 라이브러리는 배포 경로를 외부에 맡기므로 파일 변조 시 사용자 브라우저에서 악성 코드가 실행될 수 있음.
- 필요성: W3C SRI의 `integrity` 해시와 `crossorigin` 속성을 HTML에 명시해 다운로드한 리소스가 기대 SHA-256/384/512 해시와 일치하는지 검증해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Build Pipeline -> Hash 생성 -> HTML integrity 속성
Browser -> CDN Resource Download -> Hash Compare -> Execute or Block
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| integrity 속성 | 기대 해시 알고리즘과 값 저장 | `sha256`, `sha384`, `sha512` |
| crossorigin 속성 | CORS 모드와 응답 검증 연계 | `anonymous`, `use-credentials` |
| 브라우저 검증기 | 다운로드 파일 해시 계산·비교 | 불일치 시 실행 차단 |
| 배포 파이프라인 | 파일 버전 고정과 해시 갱신 | lockfile, asset manifest |

> 요약: SRI는 빌드 시 해시를 만들고 브라우저가 다운로드 리소스 해시와 비교해 실행 여부를 결정한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
리소스 버전 고정 -> SHA 해시 생성 -> HTML 태그 반영
-> 브라우저 다운로드 -> 해시 비교 -> 일치 실행 / 불일치 차단
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 외부 라이브러리 버전 고정 | semver exact version, lockfile |
| 2 | 해시 생성 | SHA-384 권장, Base64 인코딩 |
| 3 | HTML 태그에 integrity/crossorigin 지정 | script, link rel=stylesheet |
| 4 | 브라우저 해시 비교 | 기대 해시와 실제 해시 일치 |
| 5 | 차단 로그 확인 | console error, RUM, CSP report 연계 |

> 요약: SRI는 버전 고정, 해시 생성, 브라우저 비교, 차단 로그 확인 순서로 동작한다.

---

## Ⅳ. 특징

| 구분 | 기존/미적용 | 본 키워드 적용 | 수치/판단 포인트 |
|:---|:---|:---|:---|
| 검증 대상 | CDN 도메인 신뢰 | 파일 내용 해시 검증 | 1바이트 변경도 해시 불일치 |
| 브라우저 처리 | 다운로드 후 즉시 실행 | integrity 불일치 시 실행 차단 | script/style 태그 적용 |
| 운영 방식 | floating latest 사용 | exact version+hash pinning | lockfile 변경 리뷰 |
| 한계 | 동적 파일 대응 없음 | 정적 외부 리소스 중심 | 자주 변하는 광고 script 제외 검토 |

> 요약: SRI는 외부 정적 리소스의 내용 변조를 차단하지만, 자주 변하는 동적 리소스에는 운영 부담이 생긴다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 전송 보호 | HTTPS | HTTPS+SRI | 전송 암호화와 내용 무결성 동시 필요 |
| 출처 제한 | CSP source allowlist | SRI integrity hash | 허용 CDN 내부 파일 변조 대응 |
| 배포 관리 | 자동 최신 버전 | 고정 버전+해시 갱신 | 결제·인증 화면 외부 script |

> 요약: SRI는 HTTPS와 CSP를 대체하지 않고 허용된 외부 파일의 내용 변조를 추가로 검증한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 리소스 차단 | 해시 갱신 누락 | asset manifest 자동 생성, 배포 전 browser test | integrity error 0건 |
| 공급망 변조 | CDN 파일 교체 | exact version, SRI, 내부 mirror | hash mismatch 이벤트 |
| CORS 오류 | crossorigin/응답 헤더 불일치 | CDN CORS 헤더 점검, anonymous 모드 | failed resource load 수 |

> 요약: SRI 운영 리스크는 해시 누락, CDN 변조, CORS 오류이며 배포 테스트와 로드 실패 지표로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 적용 범위 | 외부 script/style 100% integrity 지정 | HTML scan, CSP report |
| 무결성 검증 | SHA-384 이상 사용 | build artifact 검사 |
| 운영 장애 | integrity mismatch, load failure 추적 | RUM, browser console collection |

> 요약: 적용 효과는 외부 리소스 커버리지, 해시 알고리즘, 브라우저 차단 이벤트로 확인한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 리소스 관리: 외부 script/style은 exact version으로 고정하고 빌드 단계에서 SHA-384 해시와 `integrity` 속성을 asset manifest에 기록
2. 브라우저 설정: CDN 리소스 태그에 `crossorigin="anonymous"`를 적용하고 CSP `script-src` allowlist와 함께 운영
3. 검증 운영: 배포 전 Playwright로 리소스 로드 테스트, RUM에서 integrity mismatch와 failed resource load를 수집

**결론 (2줄):**
- 기술사 판단: 결제·인증·개인정보 화면의 외부 정적 script는 CSP allowlist만으로 부족하므로 SRI 해시 검증을 병행해야 함
- 향후 방향: SRI, lockfile 검증, SBOM, CDN mirror를 연결해 프런트엔드 공급망 무결성을 추적해야 함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "SRI를 설명하시오" | 해시 생성, 브라우저 비교, 차단 흐름 | HTTPS·CSP와 역할 차이, 적용 한계 |
| 요구사항 명시형 | "CDN 변조 대응 방안을 제시하시오", "공급망 보안을 설계하시오" | integrity/crossorigin 적용과 배포 파이프라인 | lockfile, RUM 지표, mismatch 대응 |

> 요약: 설명형은 브라우저 해시 검증 원리를, 방안형은 CDN 변조 탐지와 배포 자동화 지표를 중심으로 쓴다.
