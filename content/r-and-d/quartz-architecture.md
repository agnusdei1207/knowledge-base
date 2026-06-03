---
title: 🔧 Quartz v5 아키텍처 분석 — 백링크·그래프 뷰·빌드 한계
tags:
- r-and-d
- quartz
- knowledge-base
---

[ 🌌 [[index|종합 지식 포털]] ] > [[r-and-d/index|🔬 R&D]] > **🔧 Quartz 분석**

---

이 문서는 Knowledge Base가 채택한 **Quartz v5** 정적 사이트 생성기의 핵심 기능, 강점, 한계를 기술적으로 분석한다.

---

## 1. 백링크(Backlink)와 그래프 뷰(Graph View)

### 1.1 백링크 — 데이터

**백링크**는 "이 문서를 언급(링크)한 다른 문서 목록"이다.

<div style="display:flex; flex-direction:column; gap:8px; padding:16px; border:1px solid var(--lightgray, #E5DEC9); border-radius:8px; background:var(--highlight, rgba(166,91,50,0.08)); font-size:0.9rem;">
  <div style="padding:10px 14px; border-radius:6px; border-left:3px solid var(--secondary, #A65B32);">
    <strong>A.md</strong> 내용: <code>"이 개념은 [[B]]에서 파생된 것이다."</code>
  </div>
  <div style="text-align:center; font-size:1.2rem;">⬇️</div>
  <div style="padding:10px 14px; border-radius:6px; border-left:3px solid var(--tertiary, #73826F);">
    <strong>B.md</strong> 하단 자동 표시: <em>"Backlinks: A가 이 문서를 링크함"</em>
  </div>
</div>

- **본질**: 텍스트 기반 역참조 인덱스
- **표시 위치**: 페이지 하단에 리스트 형태
- **데이터 흐름**: 빌드타임에 전체 파일 간 `[[wikilink]]`를 스캔 → 역방향 매핑 생성
- **용도**: "이 개념이 어디서 쓰이고 있는가?" — 지식 탐색의 핵심

### 1.2 그래프 뷰 — 시각화

**그래프 뷰**는 백링크(+포워드 링크) 관계를 **노드(문서)와 엣지(링크)**로 시각화한 것이다.

<div style="display:grid; grid-template-columns:1fr 1fr; gap:4px; max-width:260px; padding:16px; border:1px solid var(--lightgray, #E5DEC9); border-radius:8px; text-align:center; font-weight:600; font-size:0.95rem;">
  <div style="padding:8px; border-radius:6px; border:2px solid var(--secondary, #A65B32);">A</div>
  <div style="padding:8px; border-radius:6px; border:2px solid var(--secondary, #A65B32);">B</div>
  <div style="grid-column:1/3; display:flex; justify-content:space-between; font-size:0.8rem; color:var(--gray, #8E8575); padding:0 20px;">↑ &nbsp;&nbsp;&nbsp;&nbsp; → &nbsp;&nbsp;&nbsp;&nbsp; ↓</div>
  <div style="padding:8px; border-radius:6px; border:2px solid var(--tertiary, #73826F);">D</div>
  <div style="padding:8px; border-radius:6px; border:2px solid var(--tertiary, #73826F);">C</div>
  <div style="grid-column:1/3; font-size:0.8rem; color:var(--gray, #8E8575);">← 노드(문서)와 엣지(링크)의 시각적 관계</div>
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

<div style="display:flex; flex-direction:column; gap:6px; padding:16px; border:1px solid var(--lightgray, #E5DEC9); border-radius:8px; font-size:0.88rem;">
  <div style="padding:10px; border-radius:6px; background:var(--highlight, rgba(166,91,50,0.08)); text-align:center; font-weight:600;">📄 content/*.md (9,600+)</div>
  <div style="text-align:center; color:var(--gray, #8E8575);">▼</div>
  <div style="padding:8px 12px; border-radius:6px; border-left:3px solid #4A90D9;"><strong>①</strong> remark-parse: Markdown → MDAST (추상 구문 트리)</div>
  <div style="text-align:center; color:var(--gray, #8E8575);">▼</div>
  <div style="padding:8px 12px; border-radius:6px; border-left:3px solid #7B68EE;"><strong>②</strong> rehype: MDAST → HAST (HTML AST)</div>
  <div style="text-align:center; color:var(--gray, #8E8575);">▼</div>
  <div style="padding:10px 12px; border-radius:6px; border-left:3px solid var(--secondary, #A65B32);">
    <strong>③ 플러그인 체인</strong>
    <ul style="margin:6px 0 0 0; padding-left:18px; line-height:1.6;">
      <li>obsidian-flavored-markdown: <code>[[wikilink]]</code> 해석</li>
      <li>crawl-links: 전체 링크 그래프 구성</li>
      <li>backlinks: 역참조 인덱스 생성</li>
      <li>content-index: FlexSearch 전문 검색 인덱스</li>
      <li>graph: D3.js 그래프 데이터 생성</li>
      <li><s>og-image: OG 이미지 렌더링</s> <span style="color:var(--tertiary, #73826F);">(비활성화 완료)</span></li>
    </ul>
  </div>
  <div style="text-align:center; color:var(--gray, #8E8575);">▼</div>
  <div style="padding:8px 12px; border-radius:6px; border-left:3px solid #2ECC71;"><strong>④</strong> Preact SSR: JSX → 정적 HTML</div>
  <div style="text-align:center; color:var(--gray, #8E8575);">▼</div>
  <div style="padding:10px; border-radius:6px; background:var(--highlight, rgba(166,91,50,0.08)); text-align:center; font-weight:600;">📁 public/ 출력</div>
</div>

### 2.2 강점

| 기능 | 상세 |
|------|------|
| **Obsidian 네이티브 호환** | `[[wikilink]]`, 캘러스, 캔버스, 프로퍼티 등 그대로 사용 |
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

<div style="padding:16px; border:1px solid var(--lightgray, #E5DEC9); border-radius:8px;">
  <div style="font-weight:600; margin-bottom:10px; font-size:0.9rem;">메모리 사용 패턴</div>
  <div style="display:flex; align-items:flex-end; gap:3px; height:120px; padding-bottom:4px; border-bottom:2px solid var(--gray, #8E8575); border-left:2px solid var(--gray, #8E8575); position:relative;">
    <div style="flex:1; background:var(--tertiary, #73826F); border-radius:3px 3px 0 0; height:15%; opacity:0.7;" title="0분: 시작"></div>
    <div style="flex:1; background:var(--tertiary, #73826F); border-radius:3px 3px 0 0; height:25%;" title="AST 파싱"></div>
    <div style="flex:1; background:var(--secondary, #A65B32); border-radius:3px 3px 0 0; height:40%;" title="플러그인 처리"></div>
    <div style="flex:1; background:var(--secondary, #A65B32); border-radius:3px 3px 0 0; height:60%;" title="링크 그래프 구성"></div>
    <div style="flex:1; background:#c0392b; border-radius:3px 3px 0 0; height:80%;" title="검색 인덱스 생성"></div>
    <div style="flex:1; background:#c0392b; border-radius:3px 3px 0 0; height:95%; position:relative;" title="피크: 8GB">
      <span style="position:absolute; top:-18px; right:-10px; font-size:0.7rem; font-weight:600; white-space:nowrap;">⚠️ 피크 ~8GB</span>
    </div>
    <div style="flex:1; background:var(--secondary, #A65B32); border-radius:3px 3px 0 0; height:70%;" title="SSR 렌더링"></div>
    <div style="flex:1; background:var(--tertiary, #73826F); border-radius:3px 3px 0 0; height:30%;" title="출력"></div>
  </div>
  <div style="display:flex; justify-content:space-between; font-size:0.7rem; color:var(--gray, #8E8575); margin-top:4px; padding-left:2px;">
    <span>0분</span><span>1분</span><span>2분</span><span>3분</span><span>4분</span>
  </div>
  <div style="display:flex; gap:12px; margin-top:10px; font-size:0.75rem; flex-wrap:wrap;">
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
> Quartz의 강점은 **기능의 풍부함**이고, 약점은 **빌드 성능**이다.
> "옮길 것인가"보다 "언제 옮길 것인가"의 판단 기준을 미리 세워두는 것이 핵심이다.
