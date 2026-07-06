#!/usr/bin/env python3
"""
Extract key technical terms from CSPE markdown files and replace
placeholder 1-term tables with proper 5-7 term tables.

Strategy:
1. Find all **bolded terms** with parenthetical explanations
2. Find terms defined with — or : patterns
3. Extract from tables (| **Term** | description |)
4. Use title + context to generate meaningful entries
"""
import os, re, sys

def extract_bold_terms(content):
    """Extract **Term (English)** patterns."""
    terms = []
    # Pattern: **한글 (English)** or **English**
    for m in re.finditer(r'\*\*([^*]{2,50})\*\*', content):
        term = m.group(1)
        # Skip generic terms
        if any(skip in term for skip in ['본질', '가치', '융합', '판단', '개념', '필요성', '비유', '배경', '시나리오', '정량', '정성', '기술적', '운영', '참고', '미래', '결론', '섹션 요약', '다이어그램']):
            continue
        if len(term) < 2 or len(term) > 40:
            continue
        terms.append(term)
    return terms

def extract_definitions(content):
    """Extract term — definition patterns."""
    defs = {}
    # Pattern: **Term**: definition or **Term** — definition
    for m in re.finditer(r'\*\*([^*]{2,40})\*\*\s*[:—]\s*(.{10,100}?)(?:\.|$)', content, re.MULTILINE):
        term = m.group(1).strip()
        defn = m.group(2).strip()
        if term not in defs:
            defs[term] = defn
    return defs

def extract_table_terms(content):
    """Extract terms from existing tables like component tables."""
    terms = {}
    # Find table rows with bolded first column
    for m in re.finditer(r'\|\s*\*\*([^*|]{2,40})\*\*\s*\|\s*([^|]{3,80})\s*\|', content):
        term = m.group(1).strip()
        desc = m.group(2).strip()
        if term and desc and not any(skip in term for skip in ['구분', '비교', '항목', '요소명', '단계', '구성', '용어']):
            terms[term] = desc
    return terms

def extract_parenthetical(content):
    """Extract terms with parenthetical English names."""
    terms = {}
    # Pattern: 한글용어(English Term)
    for m in re.finditer(r'(\w{2,15})\(([A-Z][a-zA-Z\s\-]{2,30})\)', content):
        kor = m.group(1)
        eng = m.group(2).strip()
        terms[f"{kor}({eng})"] = eng
    return terms

def generate_analogy(term, defn):
    """Generate a simple analogy based on term/definition keywords."""
    term_lower = (term + " " + defn).lower()

    analogies = {
        'cache': '"자주 쓰는 물건을 책상 위에"',
        'buffer': '"완충 지대"',
        'queue': '"줄 서기"',
        'stack': '"접시 쌓기"',
        'tree': '"가계도"',
        'graph': '"지하철 노선도"',
        'encrypt': '"자물쇠"',
        'decrypt': '"열쇠"',
        'hash': '"지문"',
        'token': '"입장권"',
        'auth': '"신분증 확인"',
        'firewall': '"건물 출입 경비원"',
        'proxy': '"대리인"',
        'load': '"교통 분산"',
        'virtual': '"가상의 칸막이"',
        'container': '"표준 화물 컨테이너"',
        'pipeline': '"공장 조립 라인"',
        'thread': '"한 사무실의 여러 직원"',
        'process': '"독립된 사무실"',
        'memory': '"작업 책상"',
        'disk': '"창고"',
        'cpu': '"두뇌"',
        'bus': '"고속도로"',
        'protocol': '"외교 의전"',
        'packet': '"택배 상자"',
        'routing': '"내비게이션"',
        'switch': '"우체국 분류기"',
        'gateway': '"국경 검문소"',
        'bandwidth': '"도로 차선 수"',
        'latency': '"배달 시간"',
        'throughput': '"시간당 처리량"',
        'redundancy': '"예비 타이어"',
        'failover': '"백업 발전기"',
        'cluster': '"팀 협업"',
        'scale': '"건물 증축"',
        'index': '"책의 목차"',
        'query': '"도서관 검색"',
        'transaction': '"은행 거래"',
        'lock': '"화장실 잠금"',
        'deadlock': '"좁은 골목 교착"',
        'api': '"식당 메뉴판"',
        'sdk': '"요리 도구 세트"',
        'framework': '"건축 골조"',
        'library': '"공구 상자"',
        'compiler': '"통번역사"',
        'interpreter': '"동시통역사"',
        'kernel': '"건물 관리실"',
        'driver': '"통역 어댑터"',
        'interrupt': '"긴급 전화벨"',
        'scheduler': '"일정 관리자"',
        'algorithm': '"요리 레시피"',
        'model': '"설계 도면"',
        'pattern': '"건축 양식"',
        'layer': '"건물 층"',
        'module': '"레고 블록"',
        'interface': '"리모컨 버튼"',
        'abstraction': '"자동차 핸들 (엔진 몰라도 운전)"',
        'cloud': '"전기처럼 빌려 쓰는 컴퓨팅"',
        'edge': '"현장 가까이에서 처리"',
        'ai': '"학습하는 기계"',
        'ml': '"경험으로 배우는 프로그램"',
        'deep': '"여러 층의 필터"',
        'neural': '"뇌 신경망 모방"',
        'attack': '"사이버 침입"',
        'vulnerability': '"건물 보안 허점"',
        'patch': '"구멍 메우기"',
        'scan': '"건강 검진"',
        'monitor': '"CCTV"',
        'log': '"일지 기록"',
        'backup': '"보험"',
        'recovery': '"응급 복구"',
        'test': '"품질 검사"',
        'deploy': '"출시"',
        'ci': '"자동 품질 검사 라인"',
        'cd': '"자동 배송 시스템"',
        'agile': '"단거리 반복 달리기"',
        'waterfall': '"폭포수처럼 순차 진행"',
        'devops': '"개발+운영 합체"',
        'microservice': '"독립 가게 모음"',
        'monolith': '"백화점 한 건물"',
        'soa': '"서비스 분업"',
        'rest': '"표준 주문 방식"',
        'grpc': '"고속 내부 통신"',
        'kafka': '"메시지 고속도로"',
        'blockchain': '"위변조 불가 장부"',
        'quantum': '"양자 세계의 규칙"',
        'iot': '"만물 인터넷"',
        '5g': '"초고속 무선 고속도로"',
        'zero trust': '"아무도 믿지 않는 보안"',
    }

    for keyword, analogy in analogies.items():
        if keyword in term_lower:
            return analogy

    return '"이 개념의 핵심"'

def build_term_table(content, title):
    """Build a proper 5-7 term table from file content."""
    bold_terms = extract_bold_terms(content)
    definitions = extract_definitions(content)
    table_terms = extract_table_terms(content)
    paren_terms = extract_parenthetical(content)

    # Merge all sources, preferring those with definitions
    all_terms = {}

    # Add terms with definitions first
    for term, defn in definitions.items():
        if len(all_terms) < 7:
            all_terms[term] = defn

    # Add table terms
    for term, desc in table_terms.items():
        if term not in all_terms and len(all_terms) < 7:
            all_terms[term] = desc

    # Add bold terms without definitions
    for term in bold_terms:
        clean = term.split('(')[0].strip() if '(' in term else term
        if clean not in all_terms and len(all_terms) < 7:
            # Try to find context
            idx = content.find(f'**{term}**')
            if idx >= 0:
                context = content[idx:idx+200]
                # Get text after the bold term
                after = re.search(r'\*\*[^*]+\*\*\s*[:—은는이가을를]?\s*(.{10,80}?)(?:[.\n])', context)
                if after:
                    all_terms[term] = after.group(1).strip()
                else:
                    all_terms[term] = f"{term} 관련 핵심 개념"

    # Ensure at least 3 terms
    if len(all_terms) < 3:
        # Extract from title
        short = title.split('(')[0].strip().split('—')[0].strip()
        if short not in all_terms:
            all_terms[short] = f"{title}의 핵심 개념"

    # Limit to 7
    items = list(all_terms.items())[:7]

    if not items:
        return None

    # Build table
    rows = []
    for term, defn in items:
        # Clean up definition
        defn = defn.replace('|', '/').replace('\n', ' ').strip()
        if len(defn) > 80:
            defn = defn[:77] + "..."
        analogy = generate_analogy(term, defn)
        rows.append(f"| **{term}** | {defn} | {analogy} |")

    table = """### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
""" + "\n".join(rows) + "\n\n---\n\n"

    return table

def process_file(fpath):
    """Process a single file: replace placeholder with proper terms."""
    with open(fpath, 'r') as f:
        content = f.read()

    # Check if it has a placeholder (1-term table)
    table_match = re.search(r'### 🔑 핵심 용어 정리\n\n\| 용어.*?\n\|:---.*?\n(\|.*?\n)+\n---\n', content, re.DOTALL)
    if not table_match:
        return False

    old_table = table_match.group()
    term_count = old_table.count('\n| **')

    # Only replace if it's a placeholder (1 term)
    if term_count > 2:
        return False  # Already proper

    # Extract title
    title_match = re.search(r'title:\s*"([^"]+)"', content)
    title = title_match.group(1) if title_match else os.path.basename(fpath)

    # Generate proper table
    new_table = build_term_table(content, title)
    if not new_table:
        return False

    # Replace
    content = content.replace(old_table, new_table)

    with open(fpath, 'w') as f:
        f.write(content)

    return True

def process_directory(base):
    count = 0
    for fname in sorted(os.listdir(base)):
        if not fname.endswith('.md') or not fname[0].isdigit():
            continue
        fpath = os.path.join(base, fname)
        if process_file(fpath):
            count += 1
    return count

if __name__ == '__main__':
    area = sys.argv[1] if len(sys.argv) > 1 else None
    if area:
        base = f"content/cspe/{area}"
        n = process_directory(base)
        print(f"{area}: {n} files updated")
    else:
        areas = ["02_hardware", "03_software", "04_network", "05_security",
                 "06_evaluation", "07_law_policy", "08_latest_tech"]
        total = 0
        for a in areas:
            base = f"content/cspe/{a}"
            n = process_directory(base)
            print(f"{a}: {n} files updated")
            total += n
        print(f"TOTAL: {total}")
