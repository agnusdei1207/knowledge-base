---
title: 147. 추상 팩토리 (Abstract Factory) 패턴
date: '2026-04-19'
tags:
- studynote-design-supervision
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[255_abstract_factory_pattern_object_families|추상 팩토리]]([[255_abstract_factory_pattern_object_families|Abstract Factory]]) 패턴은 **서로 연관되거나 의존적인 객체군(Product Family)을 구체적인 클래스를 지정하지 않고 하나의 팩토리 인터페이스를 통해 일괄 [[087_process_state_transition|생성]]**하는 GoF(Gang of Four) [[252_creational_patterns_overview|생성 패턴]]이다.
> 2. **가치**: UI [[184_theme_agile_requirements|테마]] 변환([[673_mac_message_authentication_code|Mac]] UI ↔ Windows UI), [[002_database_definition|데이터베이스]] 드라이버 교체(MySQL ↔ PostgreSQL), OS별 렌더링 엔진 교체 등 **런타임에 제품군 전체를 [[194_consistency_database_integrity|일관성]] 있게 교체**할 수 있어, 코드 변경 없이 플랫폼·환경을 스위칭할 수 있다.
> 3. **판단 포인트**: [[254_factory_method_pattern_subclass_creation|팩토리 메서드]]([[254_factory_method_pattern_subclass_creation|Factory Method]])가 단일 객체 [[087_process_state_transition|생성]]을 위임하는 것과 달리, [[255_abstract_factory_pattern_object_families|추상 팩토리]]는 **연관된 복수의 객체군 전체**를 일관된 [[184_theme_agile_requirements|테마]]로 [[087_process_state_transition|생성]]하는 것이 핵심 차이다.

---

## Ⅰ. 개요 및 필요성

[[255_abstract_factory_pattern_object_families|추상 팩토리]] 패턴은 시스템이 다양한 제품 군(Product Family)에 독립적이어야 할 때 사용한다. 예를 들어 GUI 프레임워크가 Windows, macOS, Linux에서 각각 다른 UI [[603_component_independent_deployment_unit|컴포넌트]](버튼, 체크박스, 스크롤바)를 써야 한다면, 플랫폼마다 `if/else` 분기를 코드 전체에 뿌려두는 것은 유지보수 재앙이다.

[[255_abstract_factory_pattern_object_families|추상 팩토리]]는 이 문제를 해결한다:
- `GUIFactory` 인터페이스: `createButton()`, `createCheckbox()` 추상 메서드
- `WindowsFactory`: Windows 전용 구현 반환
- `MacFactory`: macOS 전용 구현 반환
- 클라이언트 코드: `GUIFactory`만 알고, 실제 어떤 공장(팩토리)인지는 모름

**[[255_abstract_factory_pattern_object_families|추상 팩토리]] 없으면 발생하는 문제**:
- 플랫폼별 `if/else` 분기가 비즈니스 로직 전체에 산재
- 새 플랫폼 추가 시 모든 분기문 수정 필요 → [[746_ocp|OCP]]([[244_ocp_open_closed_principle|Open-Closed Principle]]) 위반
- 서로 다른 제품군의 객체가 섞여 [[194_consistency_database_integrity|일관성]] 깨짐 (예: Windows 버튼 + [[673_mac_message_authentication_code|Mac]] 스크롤바)

- **📢 섹션 요약 비유**: [[255_abstract_factory_pattern_object_families|추상 팩토리]]는 **'가구 세트 공장'** 과 같습니다. "북유럽 스타일" 공장에 가면 소파·테이블·침대가 모두 북유럽 디자인으로 나오고, "클래식 스타일" 공장에 가면 모두 클래식 스타일로 나옵니다. 어떤 공장을 선택하느냐에 따라 제품군 전체가 일관된 [[184_theme_agile_requirements|테마]]로 바뀝니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. [[255_abstract_factory_pattern_object_families|추상 팩토리]] 구조

```text
추상 팩토리 패턴 구조

  ┌─────────────────────────────────────────────────────────────┐
  │                <<interface>>                                │
  │               AbstractFactory                              │
  │   + createButton(): AbstractButton                         │
  │   + createCheckbox(): AbstractCheckbox                     │
  └────────────────┬────────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
  ┌─────▼──────┐       ┌──────▼──────┐
  │  Win       │       │  Mac        │
  │  Factory   │       │  Factory    │
  │            │       │             │
  │createButton│       │createButton │
  │→WinButton  │       │→MacButton   │
  │createCheckb│       │createCheckb │
  │→WinCheckbox│       │→MacCheckbox │
  └────────────┘       └─────────────┘
        │                     │
  ┌─────▼──────┐       ┌──────▼──────┐
  │WinButton   │       │MacButton    │
  │WinCheckbox │       │MacCheckbox  │
  └────────────┘       └─────────────┘
```

### 2. 코드 예시 (Python 스타일)

```python
# 추상 팩토리 인터페이스
class GUIFactory:
    def create_button(self) -> Button: ...
    def create_checkbox(self) -> Checkbox: ...

# 구체 팩토리
class WindowsFactory(GUIFactory):
    def create_button(self): return WindowsButton()
    def create_checkbox(self): return WindowsCheckbox()

class MacFactory(GUIFactory):
    def create_button(self): return MacButton()
    def create_checkbox(self): return MacCheckbox()

# 클라이언트 코드 — 팩토리 인터페이스만 의존
def render_ui(factory: GUIFactory):
    btn = factory.create_button()   # 어떤 버튼인지 모름
    chk = factory.create_checkbox() # 어떤 체크박스인지 모름
    btn.render()
    chk.render()

# 실행
factory = WindowsFactory()   # 여기서만 결정
render_ui(factory)            # 나머지 코드 변경 없음
```

### 3. 구성 요소 역할

| 역할 | 설명 | 예시 |
|:---|:---|:---|
| AbstractFactory | 제품군 [[087_process_state_transition|생성]] 메서드 선언 인터페이스 | `GUIFactory` |
| ConcreteFactory | 구체적 제품군 [[087_process_state_transition|생성]] 구현 | `WindowsFactory`, `MacFactory` |
| AbstractProduct | 개별 제품의 인터페이스 | `Button`, `Checkbox` |
| ConcreteProduct | 구체 제품 구현 | `WinButton`, `MacButton` |
| [[003_audit_stakeholders|Client]] | AbstractFactory·Product 인터페이스만 사용 | `render_ui()` |

- **📢 섹션 요약 비유**: [[255_abstract_factory_pattern_object_families|추상 팩토리]]는 **'음식 [[184_theme_agile_requirements|테마]] 박스 구독 [[090_service_kubernetes_network_load_balancing|서비스]]'** 와 같습니다. "한식 박스"를 구독하면 밥·된장국·김치가 모두 한식으로 오고, "이탈리안 박스"를 구독하면 파스타·브루스케타·티라미수가 옵니다. 어떤 박스를 선택하든 고객(클라이언트)은 "박스를 열어 음식을 꺼내 먹는" 행동만 합니다.

---

## Ⅲ. 비교 및 연결

### [[254_factory_method_pattern_subclass_creation|팩토리 메서드]] vs. [[255_abstract_factory_pattern_object_families|추상 팩토리]]

| 구분 | [[254_factory_method_pattern_subclass_creation|팩토리 메서드]] ([[254_factory_method_pattern_subclass_creation|Factory Method]]) | [[255_abstract_factory_pattern_object_families|추상 팩토리]] ([[255_abstract_factory_pattern_object_families|Abstract Factory]]) |
|:---|:---|:---|
| 목적 | 단일 제품 [[087_process_state_transition|생성]] 위임 | 연관 제품군 전체 일괄 [[087_process_state_transition|생성]] |
| [[087_process_state_transition|생성]] 단위 | 1개 객체 | 복수의 연관 객체 (제품군) |
| 확장 방법 | 서브클래스로 [[087_process_state_transition|생성]] 메서드 오버라이드 | 새 ConcreteFactory 추가 |
| [[083_relationship_in_er_model|관계]] | [[234_uml_class_relationships_generalization_dependency|상속]] 기반 | 구성(Composition) + 인터페이스 |
| 코드 관련 패턴 | 템플릿 메서드와 자주 결합 | [[254_factory_method_pattern_subclass_creation|팩토리 메서드]]를 내부 사용 |

### GoF [[252_creational_patterns_overview|생성 패턴]] 전체 맥락

| 패턴 | 핵심 | 언제 |
|:---|:---|:---|
| 싱글턴([[253_singleton_pattern_single_instance|Singleton]]) | 인스턴스 1개 보장 | 공유 자원, [[009_config|설정]] 객체 |
| [[254_factory_method_pattern_subclass_creation|팩토리 메서드]] | 단일 객체 [[087_process_state_transition|생성]] 위임 | 어떤 클래스 [[087_process_state_transition|생성]]할지 서브클래스 결정 |
| **[[255_abstract_factory_pattern_object_families|추상 팩토리]]** | **연관 객체군 일괄 [[087_process_state_transition|생성]]** | **플랫폼·[[184_theme_agile_requirements|테마]]별 제품군 교체** |
| [[256_builder_pattern_step_by_step_creation|빌더]]([[256_builder_pattern_step_by_step_creation|Builder]]) | 복잡한 객체 단계별 구성 | [[087_process_state_transition|생성]] 과정이 복잡한 객체 |
| [[257_prototype_pattern_object_cloning|프로토타입]]([[257_prototype_pattern_object_cloning|Prototype]]) | 기존 객체 [[016_replication_factor|복제]] | 객체 [[087_process_state_transition|생성]] 비용이 높을 때 |

- **📢 섹션 요약 비유**: [[254_factory_method_pattern_subclass_creation|팩토리 메서드]]는 **'주문서 한 장에 제품 하나 생산'**, [[255_abstract_factory_pattern_object_families|추상 팩토리]]는 **'[[184_theme_agile_requirements|테마]] [[394_catalog_metadata|카탈로그]] 전체를 선택하면 관련 제품 세트 전체가 나오는 것'** 입니다. 소파 한 개만 주문([[254_factory_method_pattern_subclass_creation|팩토리 메서드]])하는 것과, "북유럽 거실 세트 전체"를 주문([[255_abstract_factory_pattern_object_families|추상 팩토리]])하는 것의 차이입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 적용 판단 [[435_checklist_based_testing|체크리스트]]

- **복수의 연관 객체가 같은 [[184_theme_agile_requirements|테마]]로 사용되어야 함**: 버튼+체크박스+스크롤바 모두 동일 플랫폼 스타일
- **제품군 전체를 런타임에 교체해야 함**: DB 드라이버, UI [[184_theme_agile_requirements|테마]], 렌더링 엔진
- **새로운 제품군이 주기적으로 추가됨**: 새 플랫폼/[[184_theme_agile_requirements|테마]] 추가 시 기존 코드 무수정

### 실무 적용 사례

1. **Java JDBC**: `Connection`, `Statement`, `ResultSet`을 MySQL·[[188_pl_sql_t_sql_procedural|Oracle]]·PostgreSQL별 드라이버 팩토리가 [[194_consistency_database_integrity|일관성]] 있게 제공
2. **Android UI**: 머티리얼 디자인 vs. 커스텀 [[184_theme_agile_requirements|테마]]별 [[603_component_independent_deployment_unit|컴포넌트]] 일괄 [[087_process_state_transition|생성]]
3. **게임 엔진**: DirectX vs. OpenGL vs. Vulkan 렌더링 [[603_component_independent_deployment_unit|컴포넌트]] 팩토리

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

**제품군 간 혼용**: 클라이언트가 두 팩토리에서 각각 객체를 가져와 섞어 쓰면 [[194_consistency_database_integrity|일관성]]이 깨진다. "WindowsButton + MacScrollbar" 조합은 [[184_theme_agile_requirements|테마]] [[194_consistency_database_integrity|일관성]] 위반이다. 팩토리를 [[337_dependency_injection|의존성 주입]]([[190_enterprise_di_framework_lifecycle|DI]])으로 단 하나만 제공하고, 클라이언트는 해당 팩토리만 사용하도록 강제해야 한다.

- **📢 섹션 요약 비유**: 제품군 혼용은 **'한식 코스 요리에 이탈리아 파스타를 중간에 끼워 넣는 것'** 과 같습니다. 음식이 따로 먹으면 다 맛있어도, 코스 흐름([[194_consistency_database_integrity|일관성]])이 무너집니다.

---

## Ⅴ. 기대효과 및 결론

[[255_abstract_factory_pattern_object_families|추상 팩토리]] 패턴은 [[746_ocp|OCP]]([[244_ocp_open_closed_principle|Open-Closed Principle]], [[356_process|개방-폐쇄 원칙]])와 [[247_dip_dependency_inversion_principle|DIP]]([[247_dip_dependency_inversion_principle|Dependency Inversion Principle]], [[359_process|의존 역전 원칙]])를 동시에 실현하는 대표적 패턴이다. 새로운 제품군(플랫폼, [[184_theme_agile_requirements|테마]])이 추가될 때 **기존 코드를 수정하지 않고** 새 ConcreteFactory 클래스만 추가하면 된다.

**한계**: 새로운 종류의 제품(새 메서드)이 추가되면 AbstractFactory 인터페이스 자체를 수정해야 하므로, 모든 ConcreteFactory를 수정해야 한다. [[255_abstract_factory_pattern_object_families|추상 팩토리]]는 제품군 수는 쉽게 늘릴 수 있지만(새 플랫폼), **제품의 종류(버튼, 체크박스 등)를 새로 추가하기는 어렵다**.

**미래 방향**: ① [[337_dependency_injection|의존성 주입]] 프레임워크(Spring [[190_enterprise_di_framework_lifecycle|DI]], Guice)와 결합한 팩토리 관리, ② 코드 [[087_process_state_transition|생성]] 도구(Lombok, 어노테이션 프로세서)로 보일러플레이트 자동화.

[[255_abstract_factory_pattern_object_families|추상 팩토리]]는 "객체를 만드는 법"이 아니라 **"어떤 세계관(제품군)에서 객체를 만들지를 결정하는 선택 체계"** 라는 관점으로 이해해야 한다.

- **📢 섹션 요약 비유**: [[255_abstract_factory_pattern_object_families|추상 팩토리]]는 **'영화 세트장 선택'** 과 같습니다. "조선 시대 세트"를 선택하면 모든 소품(버튼·체크박스·스크롤바)이 한국 전통 스타일로 나오고, "미래 도시 세트"를 선택하면 SF 스타일로 나옵니다. 배우(클라이언트)는 세트 선택만 바꾸면 되고, 연기 방식(비즈니스 로직)은 그대로입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[254_factory_method_pattern_subclass_creation|팩토리 메서드]] ([[254_factory_method_pattern_subclass_creation|Factory Method]])** | 단일 제품 [[087_process_state_transition|생성]] 위임; [[255_abstract_factory_pattern_object_families|추상 팩토리]] 내부에서 사용 |
| **[[746_ocp|OCP]] ([[244_ocp_open_closed_principle|Open-Closed Principle]])** | [[255_abstract_factory_pattern_object_families|추상 팩토리]]가 구현하는 [[242_solid_object_oriented_design_principles|SOLID]] 원칙; 확장에 열리고 수정에 닫힘 |
| **[[247_dip_dependency_inversion_principle|DIP]] ([[247_dip_dependency_inversion_principle|Dependency Inversion Principle]])** | 클라이언트가 추상에만 의존; 구체 팩토리는 주입 |
| **[[380_builder_pattern_summary|빌더 패턴]] ([[148_builder_pattern|Builder Pattern]])** | 단계별 복잡한 객체 [[087_process_state_transition|생성]]; [[255_abstract_factory_pattern_object_families|추상 팩토리]]와 상보적 [[083_relationship_in_er_model|관계]] |
| **[[337_dependency_injection|의존성 주입]] ([[190_enterprise_di_framework_lifecycle|DI]], [[337_dependency_injection|Dependency Injection]])** | [[255_abstract_factory_pattern_object_families|추상 팩토리]]를 런타임에 주입하는 현대적 구현 방식 |

### 📈 관련 키워드 및 발전 흐름도

```text
단순 직접 생성 (new ConcreteClass())
    │
    ▼
팩토리 메서드 — 단일 객체 생성 위임
    │
    ▼
추상 팩토리 — 연관 제품군 전체 일괄 생성
    │
    ├─► OCP / DIP SOLID 원칙 실현
    │
    ├─► 의존성 주입 (Spring DI, Guice)
    │
    └─► 서비스 로케이터 패턴과 비교
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[255_abstract_factory_pattern_object_families|추상 팩토리]]는 **'가구 [[184_theme_agile_requirements|테마]] 패키지 공장'** 이에요. "북유럽 공장"에 가면 소파·책상·침대가 모두 북유럽 스타일로 딱 맞게 나오고, "클래식 공장"에 가면 모두 클래식 스타일로 나와요!
2. 소비자(클라이언트 코드)는 어떤 공장에 가느냐만 선택하면 되고, 각 가구(버튼·체크박스)가 어떻게 만들어지는지는 알 필요가 없어요.
3. 새로운 "미니멀 스타일 공장"을 추가해도 기존 소비자 코드를 **한 줄도 바꾸지 않아도 된다는 것**이 이 패턴의 가장 큰 장점이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 203 / 530

← **이전**: [[146_factory_method_pattern|146. 팩터리 메서드 패턴 (Factory Method Pattern)]]
**다음**: [[148_builder_pattern|148. 빌더 (Builder) 패턴 - 복잡한 인스턴스의 생성 과정과 표현 분리]] →

---
