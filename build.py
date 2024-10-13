import os

def proc(path, style, template):
    os.system(f'pandoc --standalone --mathjax --metadata style-path="{style}.css" --template {template}.html {path}.md -o {path}.html')

proc('index', 'style', 'template')

os.chdir('blog')

for f in os.listdir():
    f, _ = os.path.splitext(f)
    proc(f, '../style', '../template')