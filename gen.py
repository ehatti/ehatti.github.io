import os

for fn in os.listdir('output'):
    if '.html' in fn:
        os.system(f'rm output/{fn}')

with open('pages/table-of-contents.md', 'w') as f:
    lines = []
    for fn in os.listdir('pages'):
        if fn == 'table-of-contents.md': continue
        fn, _ = os.path.splitext(fn)
        with open(f'pages/{fn}.md') as p:
            t = p.readlines()[1][7:-1]
            lines.append(f'- [{t}]({fn}.html)\n')
    lines.insert(0, '---\n')
    lines.insert(1, 'title: Table of Contents\n')
    lines.insert(2, 'publish: true\n')
    lines.insert(3, '---\n')
    f.writelines(lines)

for fn in os.listdir('pages'):
    print(f'Converting {fn}...')
    fn, _ = os.path.splitext(fn)
    with open(f'pages/{fn}.md', 'r', encoding = 'utf-8') as f:
        if 'publish: true' not in f.read():
            continue
    os.system(f'pandoc pages/{fn}.md --mathml -o output/{fn}.html --template template.html')
    with open(f'output/{fn}.html', 'r', encoding = 'utf-8') as f:
        t = f.read()
        t = t.replace('.md', '.html')
    with open(f'output/{fn}.html', 'w', encoding = 'utf-8') as f:
        f.write(t)