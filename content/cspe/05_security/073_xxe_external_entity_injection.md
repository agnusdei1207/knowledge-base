---
title: "XXE 외부 엔티티 인젝션 (XXE External Entity Injection)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 73
---

# 📖 【암기용】 개념 완전 이해

> 목적: XXE를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: XML 파서가 외부 엔티티를 해석해 내부 파일·네트워크 자원에 접근하는 취약점
- **왜 필요한가**: XML은 문서 안에서 다른 파일이나 URL을 참조하는 DTD와 entity 기능을 제공한다. 서버 파서가 이를 허용하면 공격 입력이 서버 내부 자원을 읽거나 호출하는 경로가 된다.
- **핵심 직관**: 서버가 XML 문서를 읽는 과정에서 공격자가 심어둔 "대신 이 파일도 읽어라" 지시를 실행하는 문제임.

## 깊이 이해
- **배경·문제의식**: SOAP, SAML, Office 문서, XML 업로드 기능은 XML 파서를 사용한다. 기본 파서 설정이 DTD와 외부 엔티티를 허용하면 애플리케이션 권한으로 파일, 내부 HTTP, DNS 요청이 발생한다.
- **작동 원리**: 요청 XML에 DTD와 external entity가 포함되고, 파서가 이를 확장(resolve)한다. 결과로 `/etc/passwd` 같은 로컬 파일 읽기, 내부 관리자 API 호출, DNS 기반 데이터 유출, Billion Laughs DoS가 가능해진다.
- **비유**: 접수 서류에 "첨부 A는 금고 안 문서로 대체"라고 적었는데, 접수 직원이 확인 없이 금고 문서를 꺼내 붙이는 상황임.
- **구체 예시**: SAML 응답 검증 전에 XML parser가 외부 엔티티를 허용하면 인증 서버 내부 메타데이터 URL이나 파일 경로 접근이 발생할 수 있다.
- **흔한 오해·주의점**: XML 서명 검증과 XXE 방어는 별개이다. 서명 검증 전에 파서가 외부 엔티티를 해석하면 검증 이전 단계에서 이미 접근이 발생한다.

## 연결 개념
- XML Parser Hardening — DTD, external general entity, external parameter entity 비활성화
- SSRF — XML 외부 엔티티가 내부 URL 호출로 이어질 때 연결
- SAML 보안 — XML 서명 검증, canonicalization, parser 설정 동시 필요

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: XXE 답안은 XML 문법 설명이 아니라 파서 설정, DTD 금지, 외부 리소스 접근 차단, 검증 순서를 연결해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: XXE는 XML 파서가 신뢰되지 않은 DTD와 외부 엔티티를 해석해 서버 권한으로 파일·네트워크 자원에 접근하는 취약점이다.
> 2. **가치**: DTD 금지와 external entity 비활성화는 파일 유출, 내부망 호출, XML bomb DoS를 동시에 줄이는 parser hardening이다.
> 3. **판단 포인트**: XML 파서 설정, 스키마 검증 순서, egress 통제, 파서 로그를 함께 설계해야 재발 방지가 가능하다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| XML 처리 취약점 이해 확인 | DTD, external entity, entity expansion | 단순 인젝션으로만 설명하고 파서 설정 누락 |
| 방어 설정 판단 확인 | `disallow-doctype-decl`, external entity disable | 입력 필터링만으로 방어 가능하다고 서술 |
| 운영 통제 연결 확인 | 파일 접근, 내부 HTTP, DNS egress 차단 | SSRF·DoS·로그 지표 연결 누락 |

> 요약: XXE는 XML 파서의 기능을 줄이고 외부 접근을 차단하는 설정형 취약점 문제이다.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **개요** | XML 파서가 외부 엔티티를 해석해 내부 파일·네트워크 자원에 접근하는 취약점 | "경험으로 배우는 프로그램" |
| **왜 필요한가** | XML은 문서 안에서 다른 파일이나 URL을 참조하는 DTD와 entity 기능을 제공한다 | "경험으로 배우는 프로그램" |
| **핵심 직관** | 서버가 XML 문서를 읽는 과정에서 공격자가 심어둔 "대신 이 파일도 읽어라" 지시를 실행하는 문제임 | "경험으로 배우는 프로그램" |
| **배경·문제의식** | SOAP, SAML, Office 문서, XML 업로드 기능은 XML 파서를 사용한다 | "경험으로 배우는 프로그램" |
| **작동 원리** | 요청 XML에 DTD와 external entity가 포함되고, 파서가 이를 확장(resolve)한다 | "경험으로 배우는 프로그램" |
| **비유** | 접수 서류에 "첨부 A는 금고 안 문서로 대체"라고 적었는데, 접수 직원이 확인 없이 금고 문서를 꺼내 붙이는 상황임 | "핵심 기술 요소" |
| **구체 예시** | SAML 응답 검증 전에 XML parser가 외부 엔티티를 허용하면 인증 서버 내부 메타데이터 URL이나 파일 경로 접근이 발생할 수 있다 | "경험으로 배우는 프로그램" |

---


## Ⅰ. 개요 및 필요성

- 개요: XML 외부 엔티티 취약점
- 배경: XML 업로드, SOAP, SAML, 문서 변환 서버에서 파서가 DTD와 외부 엔티티를 허용하면 파일 읽기와 내부망 요청이 발생할 수 있음.
- 필요성: OWASP ASVS와 CWE-611 기준으로 파서 생성 지점에서 DTD, external entity, XInclude를 비활성화하고 XML 입력 크기를 제한해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
XML Input -> Parser -> DTD Processing -> Entity Resolver -> File/HTTP/DNS Access
             / Schema Validation
             / Signature Validation
Defense -> DTD Disable -> External Entity Disable -> Egress Control -> Parser Log
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| XML 입력 | SOAP, SAML, 업로드 문서 수신 | 신뢰 경계 밖 문서 |
| DTD 처리 | 엔티티 정의와 확장 수행 | XXE와 XML bomb 원인 |
| Entity Resolver | 파일·URL 참조를 실제 자원으로 해석 | 서버 권한으로 접근 |
| 파서 설정 | DTD와 외부 엔티티 사용 여부 결정 | 언어·라이브러리별 기본값 상이 |

> 요약: XXE 구조는 XML 입력보다 파서의 DTD 처리와 entity resolver 설정이 공격면을 결정한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
XML 요청 수신 -> 파서 생성 -> DTD 허용 -> 외부 엔티티 해석
-> 로컬 파일 또는 내부 URL 접근 -> 응답 포함/외부 전송 -> 로그·egress 확인
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | XML 문서가 API 또는 업로드 기능에 도착 | Content-Type, 업로드 경로 식별 |
| 2 | 파서가 DTD와 entity를 처리 | DTD 금지 옵션 적용 여부 |
| 3 | Entity Resolver가 파일·URL을 호출 | outbound HTTP/DNS 차단 정책 |
| 4 | 결과가 응답, 오류, DNS로 노출 | 파서 오류 로그와 egress 로그 상관분석 |

> 요약: XXE는 XML 수신, DTD 허용, entity resolve, 내부 자원 접근 순서로 발생한다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | XXE 대응 | 수치·기술 판단 |
|:---|:---|:---|:---|
| 파서 기능 | DTD 허용 | DTD 전면 금지 | OWASP XXE Prevention Cheat Sheet 기준 |
| 엔티티 처리 | 외부 general/parameter entity 허용 | external entity resolve 비활성화 | file, http, ftp scheme 차단 |
| 네트워크 | 애플리케이션 outbound 자유 | egress allowlist | metadata, RFC 1918 대역 차단 |
| 검증 순서 | 서명 검증 전 파싱 | 안전 파서 생성 후 스키마·서명 검증 | SAML, SOAP 처리 전제 |

> 요약: XXE 대응은 파서 기능 축소, 외부 접근 차단, 안전한 검증 순서가 함께 적용되어야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | XML 파서 기본값 사용 | DTD와 외부 엔티티 비활성화 | 외부 XML 입력 처리 기능 전체 적용 |
| 비용/성능 | 네트워크 접근 허용 | outbound allowlist와 timeout | 외부 schema 참조 필요 시 내부 캐시 사용 |
| 운영/위험 | 오류 로그 미수집 | parser exception, egress 로그 수집 | XXE 테스트 payload 재현 0건 |

> 요약: 외부 XML 입력은 안전 파서 설정을 기본값으로 하고, 필요한 외부 참조는 내부 캐시로 대체한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 파일 유출 | `file` scheme entity resolve | external entity disable, OS 권한 최소화 | 민감 파일 접근 로그 0건 |
| 내부망 호출 | entity URL이 내부 API 지시 | egress allowlist, RFC 1918 차단 | 내부 IP outbound 0건 |
| XML bomb DoS | 재귀 entity expansion | DTD 금지, entity expansion limit | XML 파싱 CPU·메모리 임계치 |

> 요약: XXE 리스크는 파일, 내부망, DoS 세 갈래이며 파서와 네트워크 통제로 나누어 막는다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 파서 설정 | DTD·external entity 100% disable | 설정 리뷰, 단위 테스트 |
| 외부 통신 | XML 처리 프로세스 outbound allowlist 적용 | 방화벽, service mesh egress 로그 |
| 회귀 검증 | XXE 재현 테스트 0건 | DAST, SAST, 보안 단위 테스트 |

> 요약: 도입 후에는 파서 설정 적용률, outbound 로그, 회귀 테스트 결과로 통제 여부를 확인한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 파서 생성: Java `DocumentBuilderFactory`에서 `disallow-doctype-decl`, external general/parameter entity disable, XInclude 비활성화 적용
2. 아키텍처: XML 처리 컨테이너의 outbound를 사내 schema cache와 필수 API로 제한, metadata IP와 RFC 1918 대역 차단
3. 검증: SAML·SOAP·업로드 경로별 XXE 단위 테스트, 파서 예외 로그, DNS/HTTP egress 로그를 릴리스마다 점검

**결론 (2줄):**
- 기술사 판단: 외부 XML 입력은 DTD 금지를 기본값으로 하며, 외부 schema가 필요하면 내부 캐시와 allowlist로 대체함
- 향후 방향: XML 사용 기능은 JSON 전환 여부를 평가하되, SAML·SOAP 잔존 구간은 parser hardening을 표준 설정으로 관리함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "XXE를 설명하시오", "기술하시오" | XML 파서, DTD, entity resolver 흐름 | 파일·내부망·DoS 리스크와 방어 |
| 요구사항 명시형 | "방안을 제시하시오", "설계하시오", "비교하시오" | 파서 설정값과 egress 검증 절차 | DTD 금지, allowlist, 회귀 테스트 선택 기준 |

> 요약: 설명형은 파서 동작 원리를, 방안형은 파서 설정과 네트워크 차단을 중심으로 목차를 전환한다.
