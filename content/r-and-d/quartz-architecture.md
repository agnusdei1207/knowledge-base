+++
title = "Quartz v5 아키텍처 분석 — 백링크·그래프 뷰·빌드 한계"

[taxonomies]
tags = ["r-and-d", "quartz", "knowledge-base"]

[extra]
tags = ["r-and-d", "quartz", "knowledge-base"]
+++

[ 종합 지식 포털 ] > R&D > **Quartz 분석**

---

이 문서는 Knowledge Base가 채택한 **Quartz v5** 정적 사이트 생성기의 핵심 기능, 강점, 한계를 기술적으로 분석한다.

---

## 1. 백링크(Backlink)와 그래프 뷰(Graph View)

### 1.1 백링크 — 데이터

<strong>백링크</strong>는 "이 문서를 언급(링크)한 다른 문서 목록"이다.


<div class="rd-backlink-container">
  <div class="card-a">
    A.md 내용: &ldquo;이 개념은 B에서 파생된 것이다.&rdquo;
  </div>
  <div class="arrow">⬇️</div>
  <div class="card-b">
    B.md 하단 자동 표시: <em>&ldquo;Backlinks: A가 이 문서를 링크함&rdquo;</em>
  </div>
</div>


- **본질**: 텍스트 기반 역참조 인덱스
- **표시 위치**: 페이지 하단에 리스트 형태
- **데이터 흐름**: 빌드타임에 전체 파일 간 `wikilink`를 스캔 → 역방향 매핑 생성
- **용도**: "이 개념이 어디서 쓰이고 있는가?" — 지식 탐색의 핵심

### 1.2 그래프 뷰 — 시각화

<strong>그래프 뷰</strong>는 백링크(+포워드 링크) 관계를 <strong>노드(문서)와 엣지(링크)</strong>로 시각화한 것이다.


<div class="rd-graph-container">
  <div class="node-sec">A</div>
  <div class="node-sec">B</div>
  <div class="arrows">↑ &nbsp;&nbsp;&nbsp;&nbsp; → &nbsp;&nbsp;&nbsp;&nbsp; ↓</div>
  <div class="node-tert">D</div>
  <div class="node-tert">C</div>
  <div class="caption">노드(문서)와 엣지(링크)의 시각적 관계</div>
</div>


- **본질**: 백링크 데이터를 기반으로 렌더링하는 UI (D3.js 등)
- **표시 위치**: 사이드바 또는 전용 페이지
- **용도**: 문서 간 관계 구조를 직관적으로 탐색, 고립 문서 발견

### 1.3 핵심 구분

| 구분 | 백링크 | 그래프 뷰 |
|------|--------|-----------|
| **성격** | 데이터 (역참조 인덱스) | UI (시각화 렌더러) |
| **없으면?** | 그래프 뷰도 못 그림 | 백링크 리스트만 표시 |
| **구현 비용** | 낮음 (텍스트 파싱) | 높음 (D3.js, WebGL 등) |
| **대표 조합** | MkDocs Material: 백링크만 ✅, 그래프 ❌ | 일부 도구: 그래프만 ✅, 백링크 리스트 ❌ |
| **Quartz** | ✅ 있음 | ✅ 있음 — **둘 다 지원이 강점** |

> **백링크가 데이터이고, 그래프 뷰는 그걸 시각화한 것이다.**
> 이 둘을 혼동하면 도구 선택 시 판단이 흐려진다.

---

## 2. Quartz v5 아키텍처

### 2.1 빌드 파이프라인


<div class="rd-pipeline-container">
  <div class="pipeline-step-head">📄 content/*.md (9,600+)</div>
  <div class="pipeline-arrow">▼</div>
  <div class="step-parse"><strong>①</strong> remark-parse: Markdown → MDAST (추상 구문 트리)</div>
  <div class="pipeline-arrow">▼</div>
  <div class="step-rehype"><strong>②</strong> rehype: MDAST → HAST (HTML AST)</div>
  <div class="pipeline-arrow">▼</div>
  <div class="step-plugins">
    <strong>③ 플러그인 체인</strong>
    <ul>
      <li>obsidian-flavored-markdown: wikilink 해석</li>
      <li>crawl-links: 전체 링크 그래프 구성</li>
      <li>backlinks: 역참조 인덱스 생성</li>
      <li>content-index: FlexSearch 전문 검색 인덱스</li>
      <li>graph: D3.js 그래프 데이터 생성</li>
      <li><del>og-image: OG 이미지 렌더링</del> (비활성화 완료)</li>
    </ul>
  </div>
  <div class="pipeline-arrow">▼</div>
  <div class="step-ssr"><strong>④</strong> Preact SSR: JSX → 정적 HTML</div>
  <div class="pipeline-arrow">▼</div>
  <div class="pipeline-step-head">📁 public/ 출력</div>
</div>


### 2.2 강점

| 기능 | 상세 |
|------|------|
| **Obsidian 네이티브 호환** | `wikilink`, 캘러스, 캔버스, 프로퍼티 등 그대로 사용 |
| **백링크 + 그래프 뷰** | 둘 다 빌드타임 자동 생성 — 별도 설정 불필요 |
| **SPA 네비게이션** | `enableSPA: true`로 페이지 전환 시 전체 리로드 없음 |
| **FlexSearch** | 한국어 포함 전문 검색 지원 |
| **테마 커스터마이징** | SCSS 변수 기반 색상/폰트/레이아웃 변경 용이 |
| **플러그인 생태계** | quartz-community 플러그인 30+ 종 |

### 2.3 구조적 한계

| 한계 | 원인 | 영향 |
|------|------|------|
| **메모리 폭발** | 전체 파일 AST를 Node.js 힙에 동시 보유 | 9,600파일 → 8GB 필요 |
| **빌드 시간** | 파일 수에 초선형(superlinear) 증가 | 10K파일 ≈ 5분 |
| **증분 빌드 미지원** | 1개 파일 수정 → 전체 리빌드 | CI 비용 증가 |
| **검색 인덱스 일체형** | FlexSearch 인덱스를 빌드 중 생성 → 추가 메모리 | 분리 불가 (Pagefind 대체 불가) |


<div class="rd-memory-container">
  <div class="title">메모리 사용 패턴</div>
  <div class="chart">
    <div class="bar-tert" style="height: 15%; opacity: 0.7;" title="0분: 시작"></div>
    <div class="bar-tert" style="height: 25%;" title="AST 파싱"></div>
    <div class="bar-sec" style="height: 40%;" title="플러그인 처리"></div>
    <div class="bar-sec" style="height: 60%;" title="링크 그래프 구성"></div>
    <div class="bar-danger" style="height: 80%;" title="검색 인덱스 생성"></div>
    <div class="bar-danger" style="height: 95%; position: relative;" title="피크: 8GB">
      <span class="warning-badge">⚠️ 피크 ~8GB</span>
    </div>
    <div class="bar-sec" style="height: 70%;" title="SSR 렌더링"></div>
    <div class="bar-tert" style="height: 30%;" title="출력"></div>
  </div>
  <div class="x-axis">
    <span>0분</span><span>1분</span><span>2분</span><span>3분</span><span>4분</span>
  </div>
  <div class="legend">
    <span>🟢 AST 파싱</span>
    <span>🟠 플러그인 + 링크 그래프</span>
    <span>🔴 검색 인덱스 (피크)</span>
  </div>
</div>


### 2.4 적용한 최적화

| 최적화 | 효과 | 적용일 |
|--------|------|--------|
| `NODE_OPTIONS=8192` | OOM 방지, 힙 한도 8GB 확보 | 2026-06-03 |
| `--concurrency 2` | 피크 메모리 ~30% 감소 | 2026-06-03 |
| `og-image: false` | 9,600개 이미지 렌더링 생략 | 2026-06-03 |
| `llms.txt` 자동 생성 | AI 에이전트 접근성 강화 | 2026-06-03 |

---

## 3. 타 SSG 대비 포지셔닝

| SSG | 빌드 (10K) | 메모리 | 백링크 | 그래프 뷰 | Obsidian 호환 |
|-----|------------|--------|--------|-----------|---------------|
| **Quartz v5** | ~5분 | ~8GB | ✅ | ✅ | ✅✅ 네이티브 |
| Hugo | ~3초 | ~200MB | ⚠️ 테마 의존 | ⚠️ 테마 의존 | ⚠️ 변환 필요 |
| Zola | ~10초 | ~200MB | ❌ 수동 구현 | ❌ 수동 구현 | ⚠️ 변환 필요 |
| Astro | ~60초 | ~1GB | ❌ 수동 구현 | ❌ 수동 구현 | ⚠️ 변환 필요 |
| MkDocs Material | ~30초 | ~500MB | ✅ 플러그인 | ❌ | ⚠️ 변환 필요 |

> **결론**: 빌드 성능은 약하지만, "Obsidian 네이티브 호환 + 백링크 + 그래프 뷰" 3종 세트를 기본 제공하는 유일한 도구가 Quartz다.

---

## 4. 스케일 전략 — 언제 이탈할 것인가

| 콘텐츠 규모 | 전략 |
|-------------|------|
| **~15,000** | 현 Quartz 유지 (8GB + concurrency 2로 커버 가능) |
| **15,000~25,000** | CI 러너 메모리 상향 (16GB) 또는 빌드 머신 분리 검토 |
| **25,000+** | Hugo/Zola 이전 검토 (백링크·그래프를 별도 구현해야 하는 비용 발생) |

---

## 5. AX 시대 대응 현황

| 항목 | 현재 상태 | 비고 |
|------|-----------|------|
| **MCP 서버** | ✅ `search_docs`, `get_doc`, `list_docs` | AI 에이전트 실시간 접근 |
| **llms.txt** | ✅ 빌드 후 자동 생성 | AI 사이트맵 표준 |
| **구조화된 마크다운** | ✅ YAML frontmatter + 위키링크 | 기계 가독성 높음 |
| **벡터 검색 / RAG** | ❌ 미구현 | 향후 연구 과제 |
| **AI 쓰기 권한** | ❌ 읽기 전용 | AGENTS.md로 에이전트 행동 가이드 |

---

> [!TIP]
> Quartz의 강점은 <strong>기능의 풍부함</strong>이고, 약점은 <strong>빌드 성능</strong>이다.
> "옮길 것인가"보다 "언제 옮길 것인가"의 판단 기준을 미리 세워두는 것이 핵심이다.
