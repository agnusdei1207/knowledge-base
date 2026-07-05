---
title: 자바 엔터프라이즈 에디션 Java EE / Jakarta EE (Java EE)
date: 2026-07-05
tags: [cspe-software]
weight: 211
---

## Ⅰ. 개요
- 자바를 이용한 다계층(Multi-tier) 엔터프라이즈 애플리케이션 개발 표준 플랫폼임
- 오라클에서 Eclipse Foundation으로 이관되며 Jakarta EE로 명칭이 변경됨
| 구분 | 내용 | 비유 |
| --- | --- | --- |
| 출제의도 | Java EE 스택(Servlet, JSP, EJB, JPA, JMS), Jakarta EE 전환 배경 | 국가 표준 건축 규격 |

## Ⅱ. 구성요소
- 웹 계층, 비즈니스 계층, 데이터 계층을 위한 다양한 API 세트임
[Web Container: JSP/Servlet] <-> [EJB Container: EJB/JPA]
- 구성요소 표
| 구성요소 | 설명 | 비유 |
| --- | --- | --- |
| Servlet / JSP | 동적 웹 페이지 생성 및 요청 처리를 위한 표준 기술 | 웹사이트의 요리사 |
| JPA | 자바 객체와 관계형 데이터베이스를 매핑하는 표준 (ORM) | 자동 번역 저장 장치 |
| JTA / JMS | 분산 트랜잭션 관리(JTA) 및 비동기 메시지 서비스(JMS) | 금융 결제 및 우편 시스템 |
> 요약: 대규모 시스템의 안정성, 확장성, 보안을 보장하는 API 표준의 집합체임

## Ⅲ. 절차
- 표준 규격 준수 기반의 다계층 개발 및 배포 절차임
[표준 API 선정] -> [컴포넌트 개발] -> [패키징(WAR/EAR)] -> [WAS 배포]
- 4단계 설명
1) 사양 선택: 프로젝트 규모에 따라 Full Profile 또는 Web Profile 선정함
2) 표준 구현: 특정 WAS에 의존하지 않도록 표준 인터페이스 중심으로 코딩함
3) 아카이브 생성: 웹 자원(WAR)과 비즈니스 자원(JAR)을 통합한 EAR 생성함
4) 컨테이너 실행: 인증된 WAS(Jeus, WebSphere, WildFly 등)에서 서비스 구동함
> 요약: 한 번 작성하면 어디서든 실행되는(WORA) 엔터프라이즈 환경을 지향함

## Ⅳ. 문제점
- 과거의 무거운 구조로 인해 클라우드 네이티브 및 MSA 대응 속도가 느림 (원인: 거대 아키텍처)
- 명칭 변경(javax -> jakarta)에 따른 기존 코드의 호환성 문제 발생함 (원인: 패키지 변경)

## Ⅴ. 개선방안
- (단기) MicroProfile을 병행 도입하여 클라우드 환경의 기술 스택(Circuit Breaker 등) 보완함
- (중기) 가벼운 런타임인 Quarkus, Helidon 등 Jakarta EE 지원 경량 프레임워크 활용함
- (장기) 클라우드 환경에 최적화된 서버리스 자바(GraalVM 기반) 체계로 전환함

## Ⅵ. 전망
- Jakarta EE 10/11은 클라우드 네이티브를 핵심 가치로 삼아 모듈화 및 현대화를 지속할 것임
- AI 애플리케이션 개발을 위한 자바 표준 API(Jakarta AI 등) 논의가 새로운 성장 동력이 될 것임
