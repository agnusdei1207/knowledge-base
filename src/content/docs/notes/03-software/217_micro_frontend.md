---
sidebar:
  order: 217
  label: "217. 마이크로프론트엔드 아키텍처 (Micro Frontend)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "마이크로프론트엔드 아키텍처 (Micro Frontend)"
date: "2026-08-14T06:50:00+09:00"
tags: ["notes-software"]
weight: 217
extra:
  question_no: "217"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "업무별 화면 분리와 독립 배포가 독립 설계축임"
---

## Ⅰ. 개요

<details>
<summary>용어 설명</summary>

- **독립 배포·화면 조합(Independent Deployment & UI Composition)**: 업무 도메인별 웹 앱을 각 목적 조직(팀)이 독립적으로 배포하고, 런타임에 애플리케이션 셸(Shell)을 통해 하나의 단일 화면(SPA)처럼 매끄럽게 조합하는 아키텍처 원칙.
- **마이크로프론트엔드(Micro Frontend, MFE)**: 모놀리식으로 구성되던 사용자 화면(Frontend)을 비즈니스 업무 경계(Domain)별로 분할하여, 서로 다른 팀이 독립적으로 개발·배포·운영할 수 있도록 분리한 뒤 최종적으로 하나의 화면으로 통합하는 아키텍처 패턴.

</details>

- 정의/개념: 화면을 업무 경계별 App으로 분리•조합하는 **Micro Frontend**
- 배경/필요성: Monolithic UI의 **배포 의존•Merge 충돌•Build 지연** 증가

#### 한줄 요약

- 방대한 웹 화면을 상품, 주문, 결제 등 비즈니스 도메인 단위로 분할하여 각 팀이 자율적으로 개발·배포하되, 사용자에게는 매끄러운 단일 서비스처럼 제공하는 화면 분할 아키텍처.

## Ⅱ. 특징

<details>
<summary>용어 설명</summary>

- **기술 자율성·공통 계약(Technical Autonomy & Common Contract)**: 각 마이크로 앱 팀이 리액트(React), 뷰(Vue) 등 구현 기술을 자율적으로 선택할 수 있는 권한과 함께, 셸(Shell)과의 라우팅·이벤트 통신·공유 상태 규약(Contract)은 엄격히 준수해야 한다는 양립 원칙.
- **업무 경계(Business Boundary)**: 함께 변경되는 화면, 비즈니스 로직, 규칙을 하나의 크로스펑셔널(Cross-functional) 팀이 엔드투엔드로 소유하도록 나누는 DDD(Domain-Driven Design) 기반의 기능 범위.
- **부분 독립 배포(Independent Deployment)**: 전체 프론트엔드 애플리케이션을 다시 빌드하지 않고, 변경이 발생한 특정 도메인의 마이크로 앱만 개별 파이프라인을 통해 즉시 배포하는 CI/CD 방식.

</details>

- **업무 경계(Business Boundary)**와 크로스펑셔널 팀의 소유권을 일치시켜 콘웨이의 법칙(Conway's Law)에 부합하는 조직 구조 실현.
- **부분 독립 배포(Independent Deployment)**를 통해 배포 리드 타임을 단축하고, 특정 화면의 렌더링 실패가 전체 시스템으로 전파되지 않도록 장애 범위를 축소(Blast Radius Reduction).
- **기술 자율성·공통 계약(Technical Autonomy & Common Contract)** 기반의 화면 조합으로 레거시 마이그레이션이나 점진적 기술 스택 전환(Strangler Fig)에 유리.

#### 한줄 요약

- 팀별 변경과 배포는 완전히 격리되어 자율성이 높아지지만, 과도한 분할은 라이브러리 중복 로딩과 화면 상태 동기화 비용을 증가시키므로 적절한 도메인 경계 설정이 핵심.

## Ⅲ. 구조 및 구성요소

<details>
<summary>용어 설명</summary>

- **애플리케이션 셸(Application Shell)**: 글로벌 내비게이션(GNB), 라우팅 체계 등 공통 화면의 뼈대를 제공하고, URL 경로(Route)에 맞는 도메인별 마이크로 앱을 동적으로 로드하여 화면을 조합하는 부트스트랩 컨테이너.
- **통합 계약(Integration Contract)**: 셸과 마이크로 앱, 혹은 마이크로 앱 간의 느슨한 결합을 유지하기 위한 라우팅 규칙, 커스텀 이벤트(Custom Events), 글로벌 공유 상태(Auth 등)의 통신 인터페이스 규약.
- **디자인 시스템(Design System)**: 각기 다른 팀이 개발한 앱들이 조합되었을 때 이질감을 주지 않도록 공통 UI 컴포넌트(버튼, 모달 등)와 디자인 토큰(Design Token)을 중앙에서 제공하는 표현 체계.
- **오류 경계(Error Boundary)**: 특정 마이크로 앱에서 자바스크립트 런타임 오류가 발생했을 때, 브라우저 전체가 멈추는 것을 방지하고 해당 앱의 DOM 영역만 격리하여 대체(Fallback) 화면을 렌더링하는 안정성 기법.
- **업무별 마이크로 앱(Business Micro App)**: 하나의 비즈니스 하위 도메인(예: 장바구니, 리뷰)을 전담 팀이 소유하고 코드를 독립적으로 관리·배포하는 기능적 화면 단위.

</details>

```text
[Micro Frontend]
 ├── [Application Shell]
 ├── [Integration Contract]
 ├── [Business Micro App]
 ├── [Design System]
 └── [Error Boundary]
```

| 구성요소 | 책임 |
|:---|:---|
| Application Shell | 전역 Routing•Layout•**App Lifecycle** 관리 |
| Integration Contract | Event•인증•공유 상태의 **통신 규약** 정의 |
| Business Micro App | Domain UI•Logic과 **독립 CI/CD** 소유 |
| Design System | Component•Token으로 **UX 일관성** 제공 |
| Error Boundary | App Crash를 DOM 영역에 **격리** |


#### 한줄 요약

- 셸이 웹의 기본 레이아웃 뼈대를 잡고 계약에 맞춰 도메인 앱을 동적 로딩하며, 디자인 시스템과 오류 경계가 파편화되기 쉬운 UI 일관성과 안정성을 보완.

## Ⅳ. 흐름도

<details>
<summary>용어 설명</summary>

- **1. 업무 앱 적재(Micro App Loading)**: 사용자의 라우팅 변경(URL 이동) 감지 시, 웹팩 모듈 페더레이션(Webpack Module Federation) 등을 통해 원격 서버에서 필요한 자바스크립트 번들을 비동기로 가져오는(Fetch) 단계.
- **2. 통합 계약 연결(Contract Integration)**: 로드된 앱이 셸의 DOM 트리에 마운트(Mount)되며, 글로벌 스토어 구독 및 셸과의 브라우저 커스텀 이벤트(Custom Event) 리스너를 설정하는 단계.
- **3. 부분 오류 격리(Partial Error Isolation)**: 앱 렌더링 도중 예외가 발생할 경우, 최상위 컴포넌트에서 에러를 캐치(Catch)하여 다른 앱의 동작에 영향을 주지 않고 안전한 폴백(Fallback) UI로 교체하는 단계.

</details>

```text
화면 요청 (라우팅 변경)
    |
    v
1. 업무 앱 적재 (Module Fetch)
    |
    v
2. 통합 계약 연결 (Mount & Event Binding)
    |
    +-- 앱 실행 성공 ---- 조합 화면(DOM) 렌더링 반환
    |
    `-- 앱 실행 (런타임) 실패
             |
             v
      3. 부분 오류 격리 (Error Catch)
             |
             `-- 폴백(Fallback) 화면 반환
```

### 동작 원리

1. **업무 앱 적재**: URL 경로에 매핑된 업무 앱의 원격 모듈(JS 번들)을 브라우저가 동적으로 다운로드(Lazy Loading).
2. **통합 계약 연결**: 앱을 셸의 지정된 영역에 마운트(Mount)하고, 셸이 제공하는 인증 정보나 글로벌 이벤트를 수신할 수 있도록 바인딩.
3. **부분 오류 격리**: 렌더링 중 크래시 발생 시 Error Boundary 트리거를 통해 해당 영역만 '서비스를 불러올 수 없습니다' 등의 대체 화면으로 격리.


#### 한줄 요약

- 사용자가 메뉴를 클릭해 URL이 변경되면 셸이 해당 업무 앱 번들을 비동기 로드하여 화면에 결합하며, 앱 렌더링에 실패하더라도 해당 영역만 오류 화면으로 대체되어 나머지 서비스는 정상 작동.

## Ⅴ. 종류 및 비교

<details>
<summary>용어 설명</summary>

- **빌드 시 조합(Build-Time Composition)**: NPM 패키지 형태로 각 마이크로 앱을 셸에 의존성으로 추가하여, 최종적으로 하나의 빌드 산출물로 결합해 배포하는 가장 단순한 조합 방식.
- **런타임 조합(Runtime Composition)**: 셸 실행 중(클라이언트 사이드)에 iframe, Web Components, 또는 Webpack Module Federation 등을 활용해 업무별 앱을 브라우저에서 동적으로 결합하는 진정한 의미의 독립 배포 방식.
- **엣지/서버 조합(Edge-Side Composition)**: 리버스 프록시(Nginx 등)나 CDN 엣지(Edge) 서버(SSI, ESI 기술 활용)에서 사용자 요청을 가로채 여러 화면 조각을 HTML로 사전 조립하여 브라우저로 응답하는 서버 사이드(SSR) 방식.

</details>

| 마이크로프론트엔드 조합 방식 | **빌드 시 조합(Build-Time Composition)** | **런타임 조합(Runtime Composition)** | **엣지/서버 조합(Edge-Side Composition)** |
|:---|:---|:---|:---|
| 적용 기준 | 팀 간 결합도는 높으나 단순한 운영 환경이 우선일 때 | 진정한 프론트엔드 독립 배포와 동적 로딩이 필수일 때 | 서버 사이드 렌더링(SSR) 및 빠른 초기 렌더링(SEO)이 필요할 때 |
| 핵심 특징 | 셸 빌드 시점에 NPM 패키지 기반으로 정적 결합 | 브라우저가 실행 중(Client-side)에 원격 JS 모듈을 비동기 로딩 | 웹 서버/CDN 수준에서 마크업 조각을 하나의 HTML 문서로 결합 |
| 한계/단점 | 특정 앱 업데이트 시 셸 전체를 재빌드·재배포해야 함 | 초기 JS 로딩 지연 발생 및 공통 라이브러리 관리(의존성) 복잡성 | 서버 인프라 구성 복잡도 증가 및 캐싱 전략 난이도 상승 |

> 요약: 성능과 SEO가 중요하면 **엣지/서버 조합(Edge-Side Composition)**, 팀별 완벽한 독립 배포를 원하면 **런타임 조합(Runtime Composition)**, 팀 규모가 작고 레포지토리가 분리된 수준이라면 **빌드 시 조합(Build-Time Composition)**을 선택함.

#### 한줄 요약

- 배포 파이프라인에서 한 번에 묶는 정적 방식(빌드 시), 브라우저가 사용자 화면에서 실시간으로 합치는 동적 방식(런타임), 중간 서버에서 조립해 내려주는 서버 측 방식(엣지)으로 나뉨.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>용어 설명</summary>

- **경험 불일치(UX Inconsistency)**: 서로 다른 팀이 별도 기술이나 CSS 프레임워크를 사용함으로써 폰트, 버튼 크기, 애니메이션 등 사용자 인터페이스(UI)의 시각적·동작적 일관성이 깨지는 현상.
- **사용자 인터페이스(User Interface, UI)**: 사용자가 서비스 기능을 인지하고 물리적·논리적으로 상호작용(조작)하는 모든 시각적 화면 접점.
- **디자인 토큰(Design Token)**: 컬러(Hex), 타이포그래피, 간격(Spacing) 등 시각적 디자인 결정을 플랫폼(Web/iOS/AOS)에 구애받지 않도록 코드 변수(Variable)화하여 재사용하는 원자적(Atomic) 디자인 단위.
- **폴백(Fallback)**: 부분 앱이 네트워크 지연이나 코드 오류로 렌더링에 실패할 경우, 전체 앱 크래시를 방지하기 위해 사용자에게 표시하는 대체(대기) 화면이나 기본 기능.

</details>

| 실무 문제점 | 해결 대책 | 기대 효과 |
|:---|:---|:---|
| 중복 라이브러리(React 등) 로딩으로 인한 번들 용량 증가 | Webpack Module Federation의 `shared` 옵션 등 공통 의존성 공유 정책 적용 | 클라이언트 초기 적재 용량(Payload) 절감 및 TTI(Time To Interactive) 개선 |
| **사용자 인터페이스(UI)**의 시각적 **경험 불일치(UX Inconsistency)** | 중앙 집중형 디자인 시스템 구축 및 **디자인 토큰(Design Token)** 배포 | 브랜드 가이드라인 준수 및 사용자 경험(UX)의 매끄러운 일관성 확보 |
| 특정 앱의 자바스크립트 런타임 장애 전파 | Error Boundary 컴포넌트 적용 및 우아한 **폴백(Fallback)** UI 구성 | 런타임 오류 격리(Isolation)를 통한 전체 애플리케이션 가용성 보호 |
| 과도한 세분화로 인한 통신 오버헤드 | 콘웨이의 법칙에 따른 정확한 **업무 경계(Business Boundary)** 설정 및 도메인 주도 설계(DDD) | 팀 간 화면 의존도(Coupling) 최소화 및 릴리즈 조정 비용 감소 |

#### 한줄 요약

- 상품(Catalog) 팀과 결제(Checkout) 팀이 독립된 파이프라인으로 각자의 화면을 배포함으로써, UI 기능 추가 시 타 팀의 빌드 대기나 병합 충돌 없이 빠른 시장 출시(Time-to-Market)가 가능함.

## Ⅶ. 결론

<details>
<summary>용어 설명</summary>

- **조합 방식 선택 기준(Composition Strategy Selection)**: 조직의 구조, 독립 배포의 필요성, 초기 렌더링 성능(SEO), 그리고 운영 인프라의 복잡도를 종합적으로 트레이드오프(Trade-off) 분석하여 빌드 타임, 런타임, 또는 서버 사이드 조합 방식을 결정하는 아키텍처 판단 기준.

</details>

- 독립 배포는 **Runtime 조합**, 단순 Version 통제는 Build-Time 조합

#### 한줄 요약

- 화면을 단순히 조직도에 맞춰 물리적으로 분할하기 전에, 함께 변경되는 비즈니스 도메인(업무 범위)과 독립 배포의 실익을 우선 평가한 후 최적의 아키텍처 조합 방식 채택 필수.
