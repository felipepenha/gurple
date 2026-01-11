import re
import os

def extract_citations(file_path):
    citations = []
    if not os.path.exists(file_path):
        return citations
    with open(file_path, 'r') as f:
        content = f.read()
        # Find citations starting with @ (Pandoc style)
        matches = re.findall(r'@([a-zA-Z0-9_:.-]+)', content)
        citations.extend(matches)
    return citations

def main():
    # 1. Get valid keys from Gurple.bib
    valid_keys = set()
    if os.path.exists('Gurple.bib'):
        with open('Gurple.bib', 'r') as f:
            content = f.read()
            valid_keys = set(re.findall(r'@\w+\{([^,]+),', content))
    
    # 2. Get file order from mkdocs.yml
    if not os.path.exists('mkdocs.yml'):
        return
    with open('mkdocs.yml', 'r') as f:
        mkdocs_content = f.read()
    
    # regex for .md files in nav
    files = re.findall(r'[:\s]-?\s*([a-zA-Z0-9_/.-]+\.md)', mkdocs_content)
    
    docs_dir = 'docs'
    all_citations = []
    seen = set()
    
    # 3. Process files in order of invocation
    for f in files:
        if f == 'bibliography/index.md':
            continue
        full_path = os.path.join(docs_dir, f)
        file_citations = extract_citations(full_path)
        for c in file_citations:
            if c in valid_keys and c not in seen:
                all_citations.append(c)
                seen.add(c)
    
    # 4. Append remaining valid keys alphabetically (optional)
    remaining_keys = sorted([k for k in valid_keys if k not in seen])
    for k in remaining_keys:
        all_citations.append(k)
            
    # 5. Write the documentation file
    with open(os.path.join(docs_dir, 'bibliography/index.md'), 'w') as f:
        f.write('---\n')
        f.write('title: Bibliography\n')
        f.write('---\n\n')
        f.write('<div style="display:none">\n\n')
        for cite in all_citations:
            f.write(f'[@{cite}]\n')
        f.write('\n</div>\n')

if __name__ == '__main__':
    main()
