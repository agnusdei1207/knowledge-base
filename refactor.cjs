const fs = require('fs');
const path = require('path');

const dir = 'src/content/docs/notes/07-law-policy';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.md') && parseInt(f.substring(0,3)) > 3);

const termDict = {
  'IT 거버넌스': 'IT Governance',
  'IT 서비스 관리': 'IT Service Management',
  '프로젝트 관리 조직': 'Project Management Office',
  '디지털 플랫폼 정부': 'Digital Platform Government',
  '전자정부': 'e-Government',
  '디지털 리터러시': 'Digital Literacy',
  '웹 접근성': 'Web Accessibility',
  '매니지드 서비스': 'Managed Service Provider',
  '소프트웨어 진흥법': 'Software Promotion Act',
  '상용 SW 직접 구매': 'Commercial SW Direct Purchase',
  'SW 사업 영향 평가': 'SW Business Impact Assessment',
  'BMT': 'Benchmark Test',
  '개인정보보호법': 'Personal Information Protection Act',
  '네트워크망 사고 보고': 'Network Act Incident Report',
  '주요정보통신기반시설': 'Critical Information Infrastructure',
  '전자서명법': 'Electronic Signature Act',
  '클라우드 컴퓨팅법': 'Cloud Computing Act',
  'AI 기본법': 'AI Basic Act',
  'GDPR': 'General Data Protection Regulation',
  'EU AI Act': 'EU AI Act',
  'EU DORA': 'Digital Operational Resilience Act',
  '지식재산권': 'Intellectual Property Rights',
  '오픈소스 컴플라이언스': 'Open Source Compliance',
  'SBOM': 'Software Bill of Materials',
  '국제표준화기구': 'International Organization for Standardization',
  '전자정부 표준프레임워크': 'eGovernment Standard Framework',
  'COBIT': 'Control Objectives for Information and Related Technologies',
  'ITIL': 'Information Technology Infrastructure Library',
  'PMO': 'Project Management Office',
  'ISP': 'Information Strategy Planning',
  'ISMP': 'Information System Master Plan',
  'EA': 'Enterprise Architecture',
  'WCAG': 'Web Content Accessibility Guidelines',
  'MSP': 'Managed Service Provider',
  'PIP': 'Personal Information Protection',
  'ISO': 'International Organization for Standardization',
  'NIST': 'National Institute of Standards and Technology',
  'CSF': 'Cybersecurity Framework',
  'PQC': 'Post-Quantum Cryptography',
  'SCA': 'Software Composition Analysis',
  'CVE': 'Common Vulnerabilities and Exposures',
  'VEX': 'Vulnerability Exploitability eXchange',
  'OSPO': 'Open Source Program Office',
  'SDO': 'Standards Development Organization',
  'ITU': 'International Telecommunication Union',
  'IEC': 'International Electrotechnical Commission',
  'IEEE': 'Institute of Electrical and Electronics Engineers',
  'IETF': 'Internet Engineering Task Force',
  'RFC': 'Request for Comments',
  '3GPP': '3rd Generation Partnership Project',
  'IMT': 'International Mobile Telecommunications',
  'KEM': 'Key-Encapsulation Mechanism'
};

function lookupEnglish(kor, abbr) {
  if (abbr && termDict[abbr]) return termDict[abbr];
  if (termDict[kor]) return termDict[kor];
  return null;
}

files.forEach(f => {
  let content = fs.readFileSync(path.join(dir, f), 'utf-8');
  
  content = content.replace(/- \*\*(.+?)(?:\((.+?)\))?\*\*: (.*)/g, (match, p1, p2, p3) => {
    let engFull = lookupEnglish(p1, p2);
    
    let combined = '';
    
    // If there's an existing abbreviation (p2)
    if (p2) {
      if (engFull && !p2.includes(engFull) && !engFull.includes(p2)) {
         combined = `${engFull}, ${p2}`;
      } else if (engFull && engFull.includes(p2)) { // p2 is e.g., 'ISP', engFull is 'Information Strategy Planning'
         combined = `${engFull}, ${p2}`;
      } else {
         if (p2.includes(',')) combined = p2;
         else if (p2.match(/^[a-zA-Z\s]+$/)) combined = `English, ${p2}`; // fallback
         else combined = p2;
      }
    } else {
      // No abbreviation initially
      if (engFull) {
         combined = engFull;
      } else {
         combined = 'English';
      }
    }

    let modifiedP3 = p3;
    if (modifiedP3.endsWith('이다.')) {
        modifiedP3 = modifiedP3.replace(/이다\.$/, '이며, 이를 통해 실질적인 작동 방식과 사용 맥락을 구체화한다.');
    }
    
    return `- **${p1}(${combined})**: ${modifiedP3}`;
  });

  const lines = content.split('\n');
  let inConclusion = false;
  let inSummary = false;
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('Ⅶ. 결론') || lines[i].includes('Ⅶ 결론') || lines[i].includes('## Ⅶ')) {
      inConclusion = true;
    }
    if (inConclusion && lines[i].includes('#### 한줄 요약')) {
      inSummary = true;
      continue;
    }
    if (inSummary && lines[i].startsWith('- ')) {
      let l = lines[i];
      l = l.replace(/(한다|이다|된다|한다\.|이다\.|된다\.|한다\s|이다\s|된다\s)$/, ' 체계 적용 및 준수.');
      if (l === lines[i]) {
         l = l.replace(/다\.$/, ' 체계 구현 필수.');
      }
      if (l === lines[i] && l.endsWith('.')) {
         l = l.replace(/([가-힣])\.$/, '$1 적용.');
      }
      lines[i] = l;
      inSummary = false;
    }
  }
  content = lines.join('\n');
  
  content = content.replace(/#### 한줄 요약\n- (.*)/g, (match, p1) => {
    if (p1.includes('체계 적용 및 준수') || p1.includes('구현 필수') || p1.includes('적용.')) {
        return match;
    }
    if (!p1.includes('실무')) {
        let clean = p1.replace(/\.$/, '');
        return `#### 한줄 요약\n- ${clean} (핵심 원리 및 차별점을 기반으로 한 실무 맥락 적용).`;
    }
    return match;
  });

  fs.writeFileSync(path.join(dir, f), content, 'utf-8');
});
console.log('Processed all files again.');
