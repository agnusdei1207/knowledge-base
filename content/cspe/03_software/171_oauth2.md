---
title: "OAuth 2.0 (OAuth2)"
date: "2026-07-05"
tags:
  - "cspe-software"
weight: 171
---

## Ⅰ. 개요
- **정의**: 제3자 애플리케이션에 자원 접근 권한을 위임하는 인가 프레임워크
- **배경/필요성**: 사용자 비밀번호를 외부 앱에 직접 제공하면 탈취 위험이 증가하므로, 토큰 기반 권한 위임 체계가 필요함
- **비유**: 호텔 프런트에서 객실 카드키를 발급받아 마스터키 없이 특정 방만 출입하는 구조와 유사함

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 인증과 인가의 구분 이해 | OAuth 2.0은 인가 프레임워크이며 인증은 별도 계층 | Grant Type 4가지를 혼동하지 않아야 함 |

> 요약: 비밀번호 노출 없이 제3자에게 자원 접근 권한을 위임하는 토큰 기반 인가 프레임워크임

## Ⅱ. 구성요소
```text
Resource Owner ---> Client App ---> Authorization Server
                                        |
                                   Access Token
                                        |
                                        v
                                  Resource Server
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Resource Owner | 자원에 대한 접근 권한을 소유한 사용자 | 집 주인 |
| Client | 자원 접근을 요청하는 제3자 애플리케이션 | 배달 기사 |
| Authorization Server | 인가 코드·토큰을 발급하는 서버 | 프런트 데스크 |
| Resource Server | 보호 자원을 제공하는 API 서버 | 금고실 |
| Access Token | 자원 접근 권한을 증명하는 단기 토큰 | 임시 출입증 |
| Refresh Token | Access Token 갱신용 장기 토큰 | 출입증 재발급 쿠폰 |

> 요약: 자원 소유자·클라이언트·인가 서버·자원 서버 4개 역할과 토큰 2종으로 구성됨

## Ⅲ. 절차
```text
Owner -> Client -> Auth Server -> Owner(동의) -> Auth Server
  |                                                   |
  |              Authorization Code                   |
  |<--------------------------------------------------+
  |         Code+Secret -> Auth Server -> Token
  |         Token -> Resource Server -> Data
```
- 1단계: Client가 Authorization Server에 인가 요청을 전송함
- 2단계: Resource Owner가 동의하면 Authorization Code가 Client에 전달됨
- 3단계: Client가 Code와 Client Secret으로 Access Token을 교환함
- 4단계: Client가 Access Token으로 Resource Server에 자원을 요청함

> 요약: 인가 코드 발급 후 토큰 교환을 거쳐 자원에 접근하는 4단계 흐름임

## Ⅳ. 문제점
- Token 탈취: 전송 구간 암호화 미흡 시 Access Token이 중간자에게 노출됨
- Scope 과다 부여: 최소 권한 원칙 미적용 시 불필요한 자원까지 접근 가능해짐
- Redirect URI 변조: 검증 미흡 시 인가 코드가 공격자 서버로 전달됨

> 요약: 토큰 탈취·과다 권한·URI 변조가 주요 보안 위협임

## Ⅴ. 개선방안
1. 단기: TLS 필수 적용 및 토큰 만료 시간 단축으로 탈취 영향 최소화
2. 중기: Scope를 자원 단위로 세분화하여 최소 권한 원칙 적용
3. 장기: PKCE(Proof Key for Code Exchange) 도입으로 Redirect URI 기반 공격 차단

> 요약: 전송 암호화·Scope 세분화·PKCE 적용으로 단계적 보안 강화가 필요함

## Ⅵ. 전망
- 발전 방향: OAuth 2.1로 표준 통합, 불안전한 Grant Type 폐기 추세임
- 기술사적 판단: API 경제 확산에 따라 인가 표준의 중요성이 지속 증가함
- 기술사 제언: Zero Trust 아키텍처와 연계하여 토큰 검증 강도를 높이는 설계가 필요함
