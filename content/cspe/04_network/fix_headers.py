import os
import glob
import re

files = ["028_tcp_flow_control.md", "029_tcp_congestion_control.md", "030_tcp_udp_sctp_comparison.md", "031_udp_characteristics.md"]

for file in files:
    if not os.path.exists(file): continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Ensure "## 핵심 용어 정리 (내부에 등장하는 것들)" exists right after "## 한눈에" if not present
    if "## 핵심 용어 정리 (내부에 등장하는 것들)" not in content:
        content = re.sub(r'(## 한눈에.*?)(## 깊이 이해)', r'\1\n## 핵심 용어 정리 (내부에 등장하는 것들)\n- 별도 용어 정리 내용\n\n\2', content, flags=re.DOTALL)
    
    # Replace roman numeral headers if they don't exactly match
    content = re.sub(r'## Ⅰ\.\s+.*', '## Ⅰ. 개요 및 필요성', content)
    content = re.sub(r'## Ⅱ\.\s+.*', '## Ⅱ. 구조 및 구성요소', content)
    content = re.sub(r'## Ⅲ\.\s+.*', '## Ⅲ. 동작원리 및 흐름도', content)
    content = re.sub(r'## Ⅳ\.\s+.*', '## Ⅳ. 특징', content)
    content = re.sub(r'## Ⅴ\.\s+.*', '## Ⅴ. 심화 비교 및 적용 판단', content)
    content = re.sub(r'## Ⅵ\.\s+.*', '## Ⅵ. 실무 적용 및 결론', content)
    
    if "### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)" not in content:
        content = re.sub(r'(> 💡 \*\*작성 팁.*)', r'### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)\n\1', content)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

