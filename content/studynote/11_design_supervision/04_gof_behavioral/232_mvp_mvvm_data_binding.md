---
title: 232. MVP/MVVM 데이터 바인딩 (MVP/MVVM Data Binding)
date: '2026-05-10'
tags:
- studynote-design-supervision
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[036_mvp|MVP]] ([[211_mvp_mvvm_architecture_frontend|Model-View-Presenter]]) 는 Presenter가 View를 직접 참조해 [[008_단방향_반이중_전이중|단방향]] 제어하고, MVVM (Model-[[151_sql_view_virtual_table|View]]-ViewModel) 은 [[001_dikw_pyramid|데이터]] 바인딩([[001_dikw_pyramid|Data]] Binding)으로 View와 ViewModel이 자동 [[212_synchronization_mechanisms|동기화]]된다.
> 2. **가치**: 두 패턴 모두 비즈니스 로직을 View에서 분리하여 테스트 가능성([[285_testability_tactics|Testability]])을 높이지만, 바인딩 방식의 차이로 UI 복잡도와 테스트 전략이 달라진다.
> 3. **판단 포인트**: 단순 폼 처리는 [[036_mvp|MVP]], 실시간 [[001_dikw_pyramid|데이터]] 반응형 UI (User Interface) 는 MVVM이 적합하며, 선택 기준은 "View가 ViewModel을 아는가"의 의존 방향이다.

---

## Ⅰ. 개요 및 필요성
전통적인 MVC ([[405_mvc_m_v_c|Model-View-Controller]]) 패턴에서 Controller가 비대해지면 테스트와 유지보수가 어렵다. [[036_mvp|MVP]] ([[211_mvp_mvvm_architecture_frontend|Model-View-Presenter]]) 와 MVVM (Model-[[151_sql_view_virtual_table|View]]-ViewModel) 은 이 문제를 해결하기 위해 프레젠테이션 로직을 [[151_sql_view_virtual_table|View]] 바깥으로 추출한다.

두 패턴의 등장 배경:

- **[[036_mvp|MVP]]**: 서버 사이드 웹 프레임워크(ASP.NET Web Forms, Android [[459_quic_fec_forward_error_correction|초기]]) 에서 View가 인터페이스로만 존재할 때 유용
- **MVVM**: WPF (Windows Presentation Foundation), Angular, Vue.js, Jetpack Compose 같은 반응형 UI 프레임워크에서 [[001_dikw_pyramid|데이터]] 바인딩 엔진을 활용

공통 목표는 **UI 로직과 비즈니스 로직의 완전한 분리**이지만, 그 방법이 다르다.

| 연도 | 패턴 | 맥락 |
|:---:|:---|:---|
| [[098_md5|1996]] | [[036_mvp|MVP]] | Taligent 설계, 마틴 파울러 정리 |
| 2004 | PM (Presentation Model) | [[036_mvp|MVP]] 진화 형태 |
| 2005 | MVVM | Microsoft WPF 팀 (켄 쿠퍼, 존 고스만) |
| 2010~ | MVVM 대중화 | AngularJS, Knockout.js, 이후 모든 SPA 프레임워크 |

```text
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Problem      │──▶│ Core Idea    │──▶│ Expected Gain │
└──────────────┘    └──────────────┘    └──────────────┘
```

- **📢 섹션 요약 비유**: MVC가 "주방장이 요리도 하고 서빙도 하는" 구조라면, [[036_mvp|MVP]]/MVVM은 "요리사(Model)와 웨이터([[151_sql_view_virtual_table|View]])를 완전히 분리하고 중간에 매니저를 둔" 구조다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
┌─────────────────────────────────────────────────────┐
│                    MVP 구조                          │
│                                                     │
│  ┌──────────┐  interface  ┌──────────────────────┐  │
│  │   View   │◀────────────│     Presenter        │  │
│  │(UI 컴포넌트│  직접 참조  │(프레젠테이션 로직 전담)│  │
│  │ 수동 업데이)│────────────▶│                      │  │
│  └──────────┘  이벤트 전달 └──────────┬───────────┘  │
│                                      │ Model 조작   │
│                              ┌───────▼───────────┐  │
│                              │      Model        │  │
│                              │ (데이터 + 비즈니스)  │  │
│                              └───────────────────┘  │
└─────────────────────────────────────────────────────┘
```

**[[036_mvp|MVP]] 핵심**: Presenter가 IView 인터페이스를 통해 View를 갱신한다. View는 수동적(Passive [[151_sql_view_virtual_table|View]])이며 스스로 아무것도 결정하지 않는다.

```
┌──────────────────────────────────────────────────────┐
│                   MVVM 구조                           │
│                                                      │
│  ┌─────────┐    데이터 바인딩    ┌──────────────────┐ │
│  │  View   │◀═══════════════════▶│   ViewModel      │ │
│  │ (UI 템플) │  양방향 자동 동기화 │ (관찰 가능 상태)  │ │
│  └─────────┘                    └────────┬─────────┘ │
│  View는 ViewModel을                      │           │
│  직접 알지 못함                    ┌──────▼─────────┐  │
│  (바인딩 엔진이 연결)               │    Model       │  │
│                                   │ (도메인 로직)    │  │
│                                   └────────────────┘  │
└──────────────────────────────────────────────────────┘
```

**MVVM 핵심**: ViewModel은 Observable (관찰 가능한) [[082_attribute_types_er_model|속성]]을 노출하고, 바인딩 엔진이 View를 자동으로 갱신한다. Presenter처럼 View를 직접 호출하지 않는다.

| [[082_attribute_types_er_model|속성]] | [[036_mvp|MVP]] | MVVM |
|:---|:---|:---|
| [[151_sql_view_virtual_table|View]] 업데이트 방식 | Presenter가 [[151_sql_view_virtual_table|view]].setText() 직접 호출 | ViewModel [[082_attribute_types_er_model|속성]] 변경 → 바인딩 엔진 자동 반영 |
| 의존 방향 | Presenter → IView ([[008_단방향_반이중_전이중|단방향]]) | ViewModel ↔ [[151_sql_view_virtual_table|View]] (양방향 가능) |
| 테스트 | Presenter [[397_unit_test|단위 테스트]] 용이 | ViewModel [[397_unit_test|단위 테스트]] 용이 |
| 코드량 | 보일러플레이트 많음 | 바인딩으로 코드 간소화 |

- **📢 섹션 요약 비유**: MVP는 매니저가 직원에게 "지금 당장 이렇게 바꿔"라고 지시하는 방식이고, MVVM은 공유 화이트보드에 숫자를 적으면 모든 직원이 자동으로 확인하는 방식이다.

---

## Ⅲ. 비교 및 연결
| 항목 | MVC ([[405_mvc_m_v_c|Model-View-Controller]]) | [[036_mvp|MVP]] ([[211_mvp_mvvm_architecture_frontend|Model-View-Presenter]]) | MVVM (Model-[[151_sql_view_virtual_table|View]]-ViewModel) |
|:---|:---|:---|:---|
| [[151_sql_view_virtual_table|View]] → 비즈니스 로직 | 직접 접근 가능 | 금지 (인터페이스만) | 금지 (바인딩만) |
| 테스트 난이도 | 높음 ([[151_sql_view_virtual_table|View]] 의존) | 낮음 (인터페이스 목킹) | 낮음 (Observable [[395_verification_process_review|검증]]) |
| 학습 곡선 | 낮음 | 중간 | 중간~높음 |
| 반응형 UI 지원 | 제한적 | 제한적 | 네이티브 지원 |
| 주요 프레임워크 | Spring MVC, Rails | Android (구버전), WinForms | Angular, Vue, WPF, Compose |

MVVM의 양방향 [[001_dikw_pyramid|데이터]] 바인딩은 코드를 줄여주지만 **[[001_dikw_pyramid|데이터]] 흐름 추적이 어려워질 수 있다**. 이를 위해 React는 [[008_단방향_반이중_전이중|단방향]] [[001_dikw_pyramid|데이터]] 흐름(Flux/Redux)을 강제한다. Angular는 `[(ngModel)]`로 양방향 바인딩을 지원하면서도 `@Input`/`@Output`으로 [[008_단방향_반이중_전이중|단방향]]을 권장한다.

- **📢 섹션 요약 비유**: 양방향 바인딩은 전화 통화처럼 편리하지만, 누가 먼저 말했는지 헷갈릴 수 있다. [[008_단방향_반이중_전이중|단방향]]은 라디오처럼 명확하지만 응답하려면 별도 채널이 필요하다.

---

## Ⅳ. 실무 적용 및 기술사 판단
- **Android** 레거시 코드: Activity가 [[151_sql_view_virtual_table|View]] 역할, Presenter를 JUnit으로 테스트
- **ASP.NET WebForms**: Code-behind를 IView 인터페이스 뒤로 숨겨 Presenter 테스트 가능

- **Vue.js / Angular**: `v-model`, `[(ngModel)]`로 폼 상태 자동 [[212_synchronization_mechanisms|동기화]]
- **WPF**: INotifyPropertyChanged ([[082_attribute_types_er_model|속성]] 변경 알림 인터페이스) 구현으로 바인딩
- **Jetpack Compose**: `State<T>`, `StateFlow`로 선언적 UI ([[219_declarative_yaml|Declarative]] UI)

```
// MVP Presenter
class LoginPresenter(val view: ILoginView, val model: UserModel) {
    fun onLoginClick(id: String, pw: String) {
        val result = model.login(id, pw)
        if (result.success) view.navigateHome()
        else view.showError(result.message)
    }
}

// MVVM ViewModel
class LoginViewModel(val model: UserModel) {
    val isLoading = MutableStateFlow(false)
    val errorMsg  = MutableStateFlow("")
    fun login(id: String, pw: String) {
        isLoading.value = true
        // 비동기 처리 후 errorMsg 자동 바인딩
    }
}
```

### 판단 [[435_checklist_based_testing|체크리스트]]
1. 해결하려는 변화 축이 분명한가?
2. [[198_abstraction_control_data_process|추상화]] 비용보다 변경 절감 효과가 큰가?
3. 테스트·[[568_logs_distributed_logging_elk_fluentd|로그]]·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: [[036_mvp|MVP]] 매니저는 직접 전화해서 지시하고, MVVM 매니저는 공유 구글 시트에 상태를 업데이트하면 팀원들이 알아서 확인한다.

---

## Ⅴ. 기대효과 및 결론
두 패턴 모두 "[[525_fat_file_allocation_table|Fat]] [[151_sql_view_virtual_table|View]] (뚱뚱한 뷰)" 안티 패턴을 해소한다. 선택 기준을 정리하면:

- **[[036_mvp|MVP]]** 선택: 바인딩 프레임워크가 없거나, [[151_sql_view_virtual_table|View]] 교체(웹→앱)가 잦고, 엄격한 [[397_unit_test|단위 테스트]]가 필요한 경우
- **MVVM** 선택: [[001_dikw_pyramid|데이터]] 반응형 UI, 선언적 [[603_component_independent_deployment_unit|컴포넌트]], 실시간 상태 [[212_synchronization_mechanisms|동기화]]가 필요한 현대 SPA (Single [[286_page_frame|Page]] Application) / 모바일

기술사 관점에서는 **"왜 View와 비즈니스 로직을 분리하는가"** 라는 근본 질문에 답하는 것이 핵심이다. 분리를 통해 테스트 가능성, 재사용성, 유지보수성이 모두 향상된다.

확장 방향은 ① 선언형 API와의 결합, ② [[111_observability_metrics_logs_traces|관측 가능성]]([[642_observability_telemetry|Observability]]) 내장, ③ [[136_variance|분산]] 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: [[036_mvp|MVP]]/MVVM은 "요리사와 홀 직원을 분리"한 레스토랑이다. 홀이 바뀌어도 주방은 그대로 운영된다.

---

### 📌 관련 개념 맵
| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | MVC ([[405_mvc_m_v_c|Model-View-Controller]]) | [[036_mvp|MVP]]/MVVM의 원조 패턴 |
| 하위 개념 | Passive [[151_sql_view_virtual_table|View]] | MVP에서 View의 역할 (수동적) |
| 하위 개념 | Observable / StateFlow | MVVM [[001_dikw_pyramid|데이터]] 바인딩의 기술 구현체 |
| 연관 개념 | Flux / Redux | [[008_단방향_반이중_전이중|단방향]] [[001_dikw_pyramid|데이터]] 흐름 패턴 (React 생태계) |
| 연관 개념 | [[217_clean_architecture_dependency_rule|Clean Architecture]] | [[036_mvp|MVP]]/MVVM을 레이어 아키텍처에 통합 |
| 연관 개념 | [[337_dependency_injection|Dependency Injection]] ([[337_dependency_injection|의존성 주입]]) | Presenter/ViewModel [[087_process_state_transition|생성]] 시 활용 |

### 📈 관련 키워드 및 발전 흐름도
MVC 분리 → [[036_mvp|MVP]]/MVVM [[001_dikw_pyramid|데이터]] 바인딩 → 선언형 UI 상태 관리

### 👶 어린이를 위한 3줄 비유 설명
1. MVP는 선생님(Presenter)이 학생([[151_sql_view_virtual_table|View]])에게 직접 "이렇게 써"라고 지시하는 거야.
2. MVVM은 칠판(ViewModel)에 답을 쓰면 학생들이 자기 노트에 자동으로 따라 적는 거야.
3. 두 방법 모두 학생이 스스로 생각하지 않아도 되니까, 시험(테스트)이 훨씬 쉬워져!
