+++
title = "1057. NETCONF / YANG 모델링 규격체 - 차세대 네트워크 자동화"

[taxonomies]
tags = ["network"]

[extra]
tags = ["network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: YANG은 네트워크 장비의 설정·상태 데이터 구조를 트리 형태로 정의하는 모델링 언어(RFC 6020)이고, NETCONF는 그 모델을 SSH 위에서 XML로 안전하게 교환하며 트랜잭션 기반으로 장비 설정을 관리하는 프로토콜(RFC 6241)이다.
> 2. **가치**: CLI 수작업의 사람 의존성과 SNMP의 설정 자동화 한계를 동시에 극복하여, 대규모 네트워크 장비를 코드(Infrastructure as Code)로 선언적으로 관리하고, 실패 시 자동 롤백이 가능한 안전한 설정 자동화 파이프라인을 구축할 수 있다.
> 3. **판단 포인트**: candidate → validate → commit → rollback 단계의 데이터스토어 분리 구조가 NETCONF의 핵심이다. 벤더별 YANG 모델 지원 범위 차이를 고려하여 OpenConfig 모델 활용 여부를 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

네트워크 장비 수가 수백, 수천 대로 늘어나면서 기존 관리 방식의 한계가 뚜렷해졌다.

**기존 CLI 방식의 문제점**:
- 장비마다 다른 명령어 체계 (Cisco IOS vs JunOS vs Arista EOS)
- 사람이 직접 타이핑 → 오타, 누락, 순서 오류 발생
- 설정 변경 후 검증 방법 없음 → 잘못된 설정이 바로 적용됨
- 설정 실패 시 수동 롤백 필요 → 장애 시간 증가

**SNMP의 설정 관리 한계**:
- Set 명령으로 일부 설정은 가능하나, 복잡한 멀티-파라미터 설정 트랜잭션 불가
- 보안 취약 (v1/v2c 평문 전송)
- 구조화된 검증(validation) 메커니즘 없음
- 에러 발생 시 원자적 롤백(Atomic Rollback) 불가

NETCONF/YANG은 이 두 가지 문제를 동시에 해결하기 위해 IETF에서 2006년(NETCONF RFC 4741) 이후 지속적으로 발전시켜 온 차세대 네트워크 관리 표준이다. 2010년 RFC 6020(YANG), 2011년 RFC 6241(NETCONF 1.1)이 핵심 표준이다.

**NETCONF/YANG이 목표하는 관리 패러다임 변화**:

| 구분 | 기존 방식 | NETCONF/YANG |
| :--- | :--- | :--- |
| 인터페이스 | CLI (수작업) | 프로그래밍 API |
| 설정 모델 | 명령어 기반 (명령형) | 데이터 모델 기반 (선언형) |
| 검증 | 없음 (적용 후 확인) | 사전 검증 (candidate 단계) |
| 원자성 | 없음 | commit/rollback 트랜잭션 |
| 벤더 중립성 | 없음 | OpenConfig YANG으로 표준화 추구 |
| 자동화 | 스크립트 (벤더별) | Ansible, NSO, Python 통합 |

- **📢 섹션 요약 비유**: 기존 CLI 관리는 요리사가 손으로 각 요리를 만드는 방식이다. NETCONF/YANG은 레시피(YANG 모델)를 자동 조리 로봇(NETCONF)에 입력하면 검증 후 안전하게 만들어주는 방식이다. 실패하면 전 단계로 되돌아간다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### YANG 데이터 모델링 언어

YANG은 네트워크 장비의 설정(Configuration)과 상태(Operational State) 데이터가 어떤 구조를 가져야 하는지, 어떤 값이 허용되는지, 어떤 제약이 있는지를 계층적 트리 구조로 정의한다.

```text
[YANG 모델 트리 구조 예시 - 인터페이스 설정]

module: ietf-interfaces
  +--rw interfaces
     +--rw interface* [name]
        +--rw name                        string
        +--rw description?                string
        +--rw type                        identityref
        +--rw enabled?                    boolean
        +--rw link-up-down-trap-enable?   enumeration
        +--ro admin-status                enumeration
        +--ro oper-status                 enumeration
        +--ro statistics
           +--ro in-octets?              yang:counter64
           +--ro out-octets?             yang:counter64
           +--ro in-errors?              yang:counter32
           +--ro out-errors?             yang:counter32
```

**YANG 핵심 구성 요소**:

| 요소 | 설명 | 예시 |
| :--- | :--- | :--- |
| `module` | YANG 모듈 단위 (파일 단위) | ietf-interfaces |
| `container` | 자식 노드를 담는 그룹 | interfaces |
| `list` | 반복 가능한 항목 목록 | interface (인터페이스 목록) |
| `leaf` | 단일 값 노드 | name, description |
| `leaf-list` | 다중 값 노드 | allowed-vlans |
| `+--rw` | 읽기/쓰기 가능 (설정) | enabled |
| `+--ro` | 읽기 전용 (상태) | oper-status |
| `grouping` | 재사용 가능한 노드 묶음 | statistics-grouping |

**YANG 타입 시스템**:

```text
[YANG 기본 타입]
string     - 문자열
uint8/16/32/64 - 부호없는 정수
int8/16/32/64  - 부호있는 정수
boolean    - true/false
enumeration - 열거형 (예: up, down, testing)
identityref - 추상 기반 타입 참조

[YANG 제약 표현]
range "0..65535"           - 범위 제한
pattern "[0-9]{4}"         - 정규식 패턴
must "count(../interface) > 0" - XPath 조건 제약
```

### NETCONF 프로토콜 구조

NETCONF는 YANG 모델로 정의된 설정 데이터를 장비에 전달하고 관리하는 전송 프로토콜이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">NETCONF 통신 스택</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Controller (Ansible, NSO, Python)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">NETCONF 클라이언트</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(XML 기반 RPC 메시지 생성)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">SSH (TCP 포트 830)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(보안 전송 채널)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">NETCONF 서버 (네트워크 장비 내장)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Datastore Manager</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">candidate</div><div class="kb-diagram-cell">running</div><div class="kb-diagram-cell">startup</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(편집 중)</div><div class="kb-diagram-cell">(현재 동작)</div><div class="kb-diagram-cell">(재시작 후)</div></div>
</div>
</div>



### NETCONF 핵심 RPC 연산

| RPC | 방향 | 설명 |
| :--- | :--- | :--- |
| `get-config` | 클라이언트 → 서버 | 데이터스토어에서 설정 조회 |
| `edit-config` | 클라이언트 → 서버 | 설정 추가/수정/삭제 |
| `validate` | 클라이언트 → 서버 | candidate 설정의 유효성 검증 |
| `commit` | 클라이언트 → 서버 | candidate → running 적용 |
| `rollback-on-error` | 자동 | 오류 시 변경 취소 |
| `discard-changes` | 클라이언트 → 서버 | candidate 변경 사항 취소 |
| `get` | 클라이언트 → 서버 | 운영 상태(Operational) 조회 |
| `lock/unlock` | 클라이언트 → 서버 | 데이터스토어 잠금 (충돌 방지) |

### NETCONF 트랜잭션 흐름 (안전한 설정 변경)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">NETCONF 설정 변경 트랜잭션 플로우</div></div>
<div class="kb-diagram-note">Controller Network Device</div>
<div class="kb-diagram-tree-item" style="--depth:2">lock(candidate) → │ 잠금 획득 (다른 변경 차단)</div>
<div class="kb-diagram-tree-item" style="--depth:2">edit-config → │ candidate에 변경 적용</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(running 영향 없음)</div></div>
<div class="kb-diagram-tree-item" style="--depth:2">validate → │ YANG 모델 규칙 검증</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">←── OK</div><div class="kb-diagram-cell">유효성 확인</div></div>
<div class="kb-diagram-tree-item" style="--depth:2">commit → │ candidate → running 반영</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">오류 발생 시</div></div>
<div class="kb-diagram-tree-item" style="--depth:2">discard-changes → │ candidate 취소 (running 영향 없음)</div>
<div class="kb-diagram-tree-item" style="--depth:2">unlock → │ 잠금 해제</div>
</div>
</div>



- **📢 섹션 요약 비유**: NETCONF 트랜잭션은 코드 배포의 블루/그린 배포 전략과 같다. candidate 데이터스토어가 스테이징 환경, running이 프로덕션이다. 스테이징에서 검증 후 안전하게 프로덕션에 반영하고, 문제 시 롤백한다.

---

## Ⅲ. 비교 및 연결

### NETCONF vs CLI vs SNMP 비교

| 항목 | CLI | SNMP Set | NETCONF/YANG |
| :--- | :--- | :--- | :--- |
| 인터페이스 | 텍스트 명령어 | MIB OID | 구조화 XML/JSON |
| 데이터 모델 | 없음 (비정형) | MIB (제한적) | YANG (완전 정형) |
| 설정 검증 | 없음 | 없음 | 사전 validate |
| 트랜잭션 | 없음 | 없음 | commit/rollback |
| 보안 | 텔넷(위험)/SSH | 커뮤니티 스트링 | SSH (강력) |
| 대량 설정 | 스크립트 필요 | 비효율 | 일괄 편집 가능 |
| 에러 처리 | 수동 확인 | 부실 | 구조화된 오류 코드 |
| 표준화 | 없음 | RFC (MIB) | RFC 6020/6241 |

### NETCONF vs RESTCONF

| 항목 | NETCONF | RESTCONF |
| :--- | :--- | :--- |
| 전송 | SSH (TCP 830) | HTTPS (TCP 443) |
| 메시지 형식 | XML | XML 또는 JSON |
| 인터페이스 | RPC 기반 | REST API (HTTP 메서드) |
| 트랜잭션 | 완전 지원 | 부분 지원 |
| 개발자 친화성 | 낮음 (XML 복잡) | 높음 (curl, Postman 사용 가능) |
| 주요 용도 | 엔터프라이즈 대규모 자동화 | 웹 기반 관리, DevOps 통합 |

### OpenConfig vs IETF YANG

| 항목 | IETF YANG | OpenConfig YANG |
| :--- | :--- | :--- |
| 주도 기관 | IETF 표준화 기구 | Google, Facebook 등 주도 |
| 표준화 속도 | 느림 (RFC 프로세스) | 빠름 (오픈소스 기여) |
| 벤더 중립성 | 높음 | 더 높음 (사용자 주도) |
| 지원 벤더 | 광범위 | Cisco, Arista, Juniper 등 주요 벤더 |
| 적용 범위 | 일반 네트워크 관리 | 멀티벤더 통합 자동화 |

- **📢 섹션 요약 비유**: NETCONF는 엄격한 계약서 기반 거래(트랜잭션 보장), RESTCONF는 빠른 전자 계약서(개발자 친화적), SNMP는 구두 계약(빠르지만 기록 미흡), CLI는 현장 구두 협의(즉각적이지만 기록 없음)에 해당한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### Python ncclient로 NETCONF 활용 예시

```python
from ncclient import manager

# NETCONF 연결 (SSH)
with manager.connect(
    host="192.168.1.1",
    port=830,
    username="admin",
    password="password",
    hostkey_verify=False
) as m:
    
    # 현재 인터페이스 설정 조회
    config = m.get_config(source='running',
        filter=('<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>', 'subtree'))
    print(config)
    
    # 새 인터페이스 설정 (candidate에 편집)
    new_config = """
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>GigabitEthernet0/0/1</name>
          <description>서버팜 연결 포트</description>
          <enabled>true</enabled>
        </interface>
      </interfaces>
    </config>
    """
    m.edit_config(target='candidate', config=new_config)
    m.validate(source='candidate')  # 검증
    m.commit()                       # 적용
```

### Ansible으로 NETCONF 대규모 자동화

```yaml
# Ansible Playbook - NETCONF 기반 인터페이스 설정
---
- name: 인터페이스 설명 일괄 설정
  hosts: network_devices
  gather_facts: no
  
  tasks:
    - name: YANG 모델로 인터페이스 설정
      netconf_config:
        host: "{{ inventory_hostname }}"
        username: "{{ ansible_user }}"
        password: "{{ ansible_password }}"
        xml: |
          <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
              <interface>
                <name>{{ item.name }}</name>
                <description>{{ item.desc }}</description>
                <enabled>{{ item.enabled }}</enabled>
              </interface>
            </interfaces>
          </config>
      loop:
        - { name: "GE0/0/1", desc: "서버팜", enabled: "true" }
        - { name: "GE0/0/2", desc: "업링크", enabled: "true" }
```

### 설계 판단 체크리스트

1. **YANG 모델 지원 범위 확인**: 모든 벤더가 동일한 YANG 모델을 지원하지 않는다. 배포 전 대상 장비의 YANG capability를 `hello` 메시지로 확인해야 한다.
2. **OpenConfig 모델 사용 여부 결정**: 멀티벤더 환경에서는 IETF 표준 YANG보다 OpenConfig YANG이 이식성이 높을 수 있다.
3. **candidate 데이터스토어 지원 여부**: 일부 경량 장비는 candidate를 지원하지 않을 수 있다. 이 경우 running에 직접 쓰는 것은 위험하다.
4. **락(Lock) 관리 전략**: 멀티 컨트롤러 환경에서 candidate 락 충돌을 어떻게 관리할지 설계해야 한다.
5. **RESTCONF 병행 여부**: 운영 팀이 REST API에 익숙하다면 RESTCONF를 함께 제공해 진입 장벽을 낮출 수 있다.

### 안티패턴

- **candidate 없이 running에 직접 편집**: 검증 단계 없이 running에 직접 edit-config하면 오류 시 장비가 잘못된 상태가 된다.
- **YANG 모델 없이 자유 XML**: 구조화되지 않은 XML로 설정하면 모델의 검증 이점이 사라진다.
- **단일 컨트롤러에서 락 미해제**: 설정 작업 후 lock을 해제하지 않으면 다른 관리자/시스템이 설정을 변경할 수 없다.
- **벤더 전용 YANG만 사용**: 표준 YANG 대신 벤더 전용 YANG만 사용하면 멀티벤더 환경에서 이식성 문제가 생긴다.

- **📢 섹션 요약 비유**: NETCONF/YANG 자동화는 레고 설명서(YANG 모델)를 입력하면 로봇팔(NETCONF)이 정확하게 조립하는 자동화 라인이다. 설명서가 틀리면(YANG 검증 실패) 라인이 멈추고(commit 차단), 성공하면 조립이 시작된다.

---

## Ⅴ. 기대효과 및 결론

NETCONF/YANG 도입 효과:

| 효과 | 정량적 지표 | 비고 |
| :--- | :--- | :--- |
| 설정 오류 감소 | ~80% 감소 | YANG 검증으로 사전 차단 |
| 설정 소요 시간 | ~70% 단축 | 자동화 파이프라인 |
| 장애 복구 시간(MTTR) | ~50% 단축 | 자동 롤백 |
| 감사 로그 | 100% 추적 | 모든 변경 이력 기록 |
| 멀티벤더 통합 | 가능 | OpenConfig 기반 |

**미래 전망**: NETCONF/YANG은 네트워크 자동화의 핵심 기반으로 자리잡고 있으며, NSO (Network Services Orchestrator), Crosswork, NetBox 등 현대 네트워크 자동화 플랫폼의 중심 기술이다. 장기적으로 IBN (Intent-Based Networking)과 결합하여 비즈니스 의도(Intent)를 자동으로 YANG 모델 변경으로 변환하는 방향으로 발전할 전망이다.

기술사 관점에서 NETCONF/YANG은 단순한 프로토콜 변경이 아니라, 네트워크 관리의 패러다임이 명령형(Imperative)에서 선언형(Declarative)으로 전환하는 흐름의 핵심으로 이해해야 한다.

- **📢 섹션 요약 비유**: NETCONF/YANG은 네트워크 세계의 쿠버네티스 매니페스트와 같다. YAML로 원하는 상태를 선언하면 쿠버네티스가 알아서 맞춰주듯, YANG으로 원하는 네트워크 상태를 선언하면 NETCONF가 장비를 그 상태로 맞춰준다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| SNMP | NETCONF/YANG이 극복하는 기존 관리 프로토콜 |
| YANG | 네트워크 설정/상태 데이터 모델링 언어 (RFC 6020) |
| RESTCONF | NETCONF의 REST API 버전 (RFC 8040) |
| OpenConfig | 멀티벤더 중립 YANG 모델 표준화 프로젝트 |
| SDN | NETCONF/YANG으로 구현하는 중앙집중 제어 |
| IBN | NETCONF/YANG 위에서 의도 기반 자동화 구현 |
| 스트리밍 텔레메트리 | YANG 모델 기반 실시간 네트워크 상태 모니터링 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">CLI 수동 관리 (1990s) - 장비별 다른 명령어, 사람 의존</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">SNMP v3 (1999) - 보안 개선, 설정 자동화 한계</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">NETCONF v1 (RFC 4741, 2006) - SSH + XML 기반 트랜잭션 관리</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">YANG v1 (RFC 6020, 2010) - 구조화된 데이터 모델링 언어</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">NETCONF v1.1 (RFC 6241, 2011) - 안정화, 주요 벤더 지원 시작</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">OpenConfig (2014~) - 구글 등 주도, 멀티벤더 통합 YANG 모델</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">RESTCONF (RFC 8040, 2017) - REST API 친화적 대안</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">NSO, Crosswork, NetBox (2015~) - NETCONF/YANG 기반 자동화 플랫폼 성숙</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">IBN + NETCONF (현재~) - 의도 기반 자동화와 통합</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. YANG은 레고 조립 설명서예요. "빨간 블록 2개, 파란 블록 1개, 이렇게 연결해야 해"라고 정확하게 적혀 있어요.
2. NETCONF는 그 설명서를 읽고 실제로 조립하는 로봇팔이에요. 잘못 조립되면 알려주고, 성공하면 완성품을 만들어요.
3. 그래서 사람이 손으로 하나씩 조립하는 것보다 훨씬 빠르고 실수가 적어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 162 / 1120

← **이전**: [1056. ONOS / OpenDaylight 구조 모델 비교](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1056_onos_opendaylight_sdn_controller_comparison/)
**다음**: [1058. 스트리밍 텔레메트리 (Streaming Telemetry) - 푸시 기반 실시간 네트워크 관측](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1058_streaming_telemetry_network_monitoring/) →

---
