---
title: "OAuth 2.0·OIDC (OAuth 2.0 OIDC)"
date: "2026-07-05"
tags:
  - "cspe-software"
weight: 203
---

## Ⅰ. 개요
- **정의**: OAuth 2.0은 제3자 앱에 자원 접근 권한을 위임하는 인가 프레임워크, OIDC는 그 위에 인증 계층을 추가한 프로토콜
- **배경/필요성**: 비밀번호 공유 없이 서비스 간 자원 접근 위임과 사용자 신원 확인을 분리할 필요
- **비유**: 호텔 카드키(Access Token)로 객실(자원)만 출입 허용, 신분증(ID Token)으로 투숙객 본인 확인

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 인가와 인증 구분 이해 | OAuth=인가, OIDC=인증, 토큰 종류 구분 | Authorization Code + PKCE 흐름 설명 필수 |

> 요약: OAuth 2.0이 인가를, OIDC가 인증을 담당하여 자원 위임·신원 확인을 분리함

## Ⅱ. 구성요소
```text
User --> Client App --AuthZ Request--> AuthZ Server
                                          |
                                   +------+------+
                                   |      |      |
                              Token EP  UserInfo  Resource Server
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Authorization Server | 인증·인가 수행 후 토큰 발급 서버 | 호텔 프런트 |
| Access Token | 자원 서버 접근 권한을 나타내는 단기 토큰 | 객실 카드키 |
| ID Token | 사용자 신원 정보를 담은 JWT(OIDC 전용) | 신분증 사본 |

> 요약: 인가 서버가 Access Token(인가)과 ID Token(인증)을 발급하여 역할 분리함

## Ⅲ. 절차
```text
인가 요청 --> 사용자 동의 --> 코드 교환 --> 토큰 발급
```
- 1단계: 클라이언트가 Authorization Server에 인가 요청(scope·redirect_uri 포함)
- 2단계: 사용자가 로그인 후 접근 범위에 대해 동의(Consent) 수행
- 3단계: Authorization Code를 클라이언트에 전달, 클라이언트가 Token Endpoint에 코드 교환
- 4단계: Access Token(+Refresh Token, ID Token) 발급, 클라이언트가 Resource Server 호출

> 요약: 인가 요청, 사용자 동의, 코드 교환, 토큰 발급 4단계로 권한 위임 완료함

## Ⅳ. 문제점
- 토큰 탈취: Access Token 유출 시 만료까지 무단 접근 가능 — 피해 범위 제한 곤란
- Redirect URI 위조: 검증 미흡 시 Authorization Code가 공격자에게 전달 — 계정 탈취
- 토큰 폐기 지연: JWT 기반 토큰은 서버 측 즉시 폐기 불가 — 유효기간까지 악용 가능

> 요약: 토큰 탈취, Redirect URI 위조, 폐기 지연이 주요 보안 문제임

## Ⅴ. 개선방안
1. 단기: 토큰 유효기간 단축(수 분)·Refresh Token Rotation 적용으로 탈취 영향 최소화
2. 중기: Redirect URI 정확 일치 검증·PKCE 적용으로 코드 가로채기 공격 차단
3. 장기: Token Introspection 엔드포인트·블랙리스트 연동으로 실시간 폐기 체계 구축

> 요약: 토큰 단기화, PKCE 적용, 실시간 폐기 체계로 단계적 보안 강화함

## Ⅵ. 전망
- 발전 방향: OAuth 2.1 표준화로 Implicit·ROPC 폐지, PKCE 필수화 추진 중
- 기술사적 판단: Zero Trust 아키텍처에서 토큰 기반 접근 제어의 핵심 기반 기술임
- 기술사 제언: API Gateway와 연동한 중앙 집중 토큰 검증 아키텍처 설계 권장
