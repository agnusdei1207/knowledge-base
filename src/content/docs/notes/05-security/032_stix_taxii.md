---
sidebar:
  order: 32
  label: "032. STIX•TAXII 위협 공유 (STIX TAXII)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "STIX•TAXII 위협 공유 (STIX TAXII)"
date: "2026-08-13T18:56:00+09:00"
tags:
  - "notes-security"
weight: 32
extra:
  question_no: "032"
  source_status: "기출"
  source_history: "123회, 138회"
  priority: 70
  priority_note: "123•138회 반복된 구조화 공유 표준 핵심 주제임"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **구조화 위협 정보 표현(Structured Threat Information eXpression, STIX)**: 사이버 위협 객체와 연관 관계를 기계가 판독할 수 있는 JSON 형태로 정형화 표현하는 국제 표준.
- **신뢰 정보 자동 교환(Trusted Automated eXchange of Intelligence Information, TAXII)**: STIX 형태의 위협 객체를 HTTPS 기반 API를 통해 조회•게시•동기화하는 전송 프로토콜 규약.

</details>

- 정의/개념: 위협 표현 **STIX**와 자동 교환 **TAXII** 연계
- 배경/필요성: 비정형 문서 교환으로는 **장비 간 자동 연동** 불가

#### 한줄 요약

- STIX는 위협 객체•관계 표현 형식을 정의하고, TAXII는 지표의 조회•게시•동기화 전송 절차를 제공함.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **사이버 위협 인텔리전스(Cyber Threat Intelligence, CTI)**: 위협 데이터에 공격자•의도•TTP•신뢰도 맥락을 부여한 실행 가능한 정형 정보.
- **TAXII 컬렉션(TAXII Collection)**: 접근 권한 및 주제별 분류에 따라 STIX 객체들을 그룹화하여 관리하는 논리적 데이터 저장소.
- **표식•철회(Marking & Revocation)**: 정보의 민감도 취급 등급(TLP) 및 더 이상 유효하지 않은 지표의 폐기 상태를 명시하는 메타데이터.

</details>

- **STIX** 객체•연관 관계 모델 기반 **CTI** 위협 맥락 정밀 표현.
- **TAXII 컬렉션(TAXII Collection)** 자원 구성을 통한 객체 조회•게시•실시간 동기화.
- 객체 버전 정보 및 **표식•철회(Marking & Revocation)** 메타데이터를 활용한 수명주기 및 보안 취급 통제.

#### 한줄 요약

- 위협 객체의 버전과 표식•철회 메타데이터를 추적하여 검증된 신뢰 정보만 방어 장비에 연동함.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **응용 프로그래밍 인터페이스(Application Programming Interface, API)**: TAXII 컬렉션 내 STIX 객체를 프로그래밍 방식으로 조회•등록하기 위한 RESTful 규약.

</details>

```text
STIX•TAXII 공유 구조
├─ 생산자•소비자 정책
├─ STIX 객체•관계
├─ 버전•표식•철회
├─ TAXII 자원
└─ 목록•객체•상태
```

가지의 의미: 공유 정책 아래 표현과 교환 영역의 정적 포함 관계를 표현.

| 구성요소 | 책임 |
|:---|:---|
| STIX 객체•관계 | **STIX** 기반 지표•악성코드•공격자 관계 표현 |
| 버전•표식•철회 | **표식**•**철회** 기반 변경 이력•취급 등급•폐기 상태 전달 |
| TAXII 자원 | **API** 루트 및 **TAXII 컬렉션** 저장소 구성 |
| 목록•객체•상태 | **TAXII** 프로토콜 기반 객체 데이터 및 게시 상태 교환 |
| 생산자•소비자 정책 | 신뢰 수준•접근 권한•필터링 정책 정의 |

#### 한줄 요약

- 타임스탬프 기반 변경분 및 철회 객체를 확인하여 최신 보안 정책으로 자동 반영함.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **변경분 조회(Delta Query)**: 객체 식별자와 수정 타임스탬프를 이용해 변경•철회된 최신 객체만 효율적으로 동기화하는 절차.
- **STIX 프로파일(STIX Profile)**: 상호 운용성을 위해 검증 객체•관계•필드 규격을 사전에 정의한 프로파일 아키텍처.
- **STIX 객체•프로파일 검증(STIX & Profile Validation)**: 객체 및 스키마 구조가 합의된 프로파일 명세에 부합하는지 검증하는 단계.
- **권한 검증•객체 저장(Authorization & Object Persistence)**: 생산자의 게시 권한 및 스키마 유효성 검증 후 객체를 컬렉션에 저장하는 단계.
- **변경•철회 객체 선별(Delta & Revocation Extraction)**: 동기화 타임스탬프 이후 수정되거나 철회 처리된 STIX 객체만 추출하는 단계.
- **검증 객체 적용(Validated Object Enforcement)**: 중복•철회 상태 및 자사 자산 적합성을 확인한 객체를 보안 통제 장비에 배포하는 단계.

</details>

```text
생산자 게시 흐름
1. STIX 객체•프로파일 검증
        │
        └─ STIX 객체 게시 요청
                │
                ▼
2. 권한 검증•객체 저장
        └─ 게시 상태 반환

소비자 동기화 흐름
TAXII 변경분 조회
        │
        ▼
3. 변경•철회 객체 선별
        └─ 변경•철회 객체 반환
                │
                ▼
4. 검증 객체 적용
        └─ 활용 효과를 생산자에게 환류
```

### 동작 원리

1. STIX 객체•프로파일 검증: **STIX 프로파일** 기반 스키마 및 속성 유효성 검증.
2. 권한 검증•객체 저장: 게시 권한 확인 후 TAXII 컬렉션 데이터 저장.
3. 변경•철회 객체 선별: **변경분 조회**를 통한 최신 변경 및 철회 객체 추출.
4. 검증 객체 적용: 유효성 및 적합성 검증 완료 객체의 차단 통제 반영.

#### 한줄 요약

- 식별자와 수정 시각을 파악하여 변경분만 선택적으로 수신함으로써 교환 효율성을 극대화함.

## Ⅴ. 종류 및 비교

| 표준 | 역할 | 연계 결과 |
|:---|:---|:---|
| STIX 2.1 | 위협 객체•관계 표현 | 도구가 해석할 공통 위협 정보 생성 |
| TAXII 2.1 | 컬렉션 기반 조회•게시 | 권한에 맞는 STIX 객체 자동 전송 |

> 요약: STIX 표준의 위협 데이터 표현과 TAXII 프로토콜의 안전한 전송 연계.

#### 한줄 요약

- **STIX 문법•TAXII 권한**의 상호운용성 확보

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **구조화 정보 표준 발전 기구(Organization for the Advancement of Structured Information Standards, OASIS)**: STIX/TAXII 등 글로벌 개방형 정보 기술 표준을 제정 및 관리하는 국제 컨소시엄.
- **OASIS STIX 2.1 Errata 01**: 위협 객체(SDO), 관계 객체(SRO) 등의 JSON 구조 및 연관성을 정률 정의한 표준 스펙.
- **OASIS TAXII 2.1**: RESTful API 기반 위협 정보 교환 서비스 및 엔드포인트를 정의한 명세서.
- **하이퍼텍스트 전송 프로토콜 보안(Hypertext Transfer Protocol Secure, HTTPS)**: TAXII 통신 채널을 암호화하여 기밀성을 보장하는 전송 프로토콜.
- **전송 계층 보안 상호 인증(Transport Layer Security Mutual Authentication, TLS Mutual Authentication / mTLS)**: 클라이언트와 서버 간 양방향 인증으로 무단 접근을 통제하는 보안 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| CTI 객체•관계 | **OASIS** **STIX 2.1 Errata 01** 적용 | 의미•버전 상호운용성 확보 |
| 자동 교환 API | **OASIS** **TAXII 2.1** 적용 | 컬렉션 교환 일관화 |
| 지표 철회•권한 | **표식**•**철회**•접근정책 검증 | 오차단•정보 노출 억제 |
| API 도청•무단 접근 | **HTTPS**•**TLS 상호 인증** | 교환 정보의 기밀성•무결성 보호 |

#### 한줄 요약

- SOC는 TAXII 서버에서 STIX 형식의 악성 IP•도메인을 받아 유효성과 자사 로그 적중 여부를 검증한 뒤 탐지 규칙으로 변환한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **신뢰 검증(Trust Verification)**: 표준 형식 연동과 별개로 수신된 인텔리전스의 출처 신뢰성, 유효기간, 자사 환경 적합성을 종합 검증하는 프로세스.

</details>

- **신뢰 검증** 절차를 병행하고, 위협 데이터 표현에는 **STIX**, 자동 공유 통신에는 **TAXII**, 취급•수명 통제에는 **표식**•**철회** 적용.

#### 한줄 요약

- **출처•권한•유효기간** 검증 후 수신 객체 적용
