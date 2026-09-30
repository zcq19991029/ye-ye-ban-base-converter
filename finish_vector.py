from pathlib import Path
import re, subprocess, tarfile, json, sys, base64
root=Path(__file__).parent
if len(sys.argv)>1 and sys.argv[1]=='publish':
    import getpass
    c=json.loads(getpass.getpass('Sites credential JSON (hidden): '))
    header='Authorization: Bearer '+c['token']
    proc=subprocess.run(['git','-c','http.extraHeader='+header,'push',c['remote_url'],'HEAD:main'],cwd=root,capture_output=True,text=True)
    if proc.returncode: raise SystemExit('Sites source push failed')
    archive=root/'vector-release.tar'
    with tarfile.open(archive,'w') as t:
        t.add(root/'.openai/hosting.json',arcname='.openai/hosting.json')
        for p in (root/'dist').rglob('*'):
            if p.is_file():t.add(p,arcname=p.relative_to(root).as_posix())
    print(json.dumps({'archive':str(archive),'sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()}))
else:
    h=(root/'index.html').read_text(encoding='utf-8')
    h=h.replace('D${i+1}<br>P1.${7-i}','D${8-i}<br>P1.${7-i}')
    h=h.replace('const btn=$("[data-tx1-key=\'"+k+"\']");if(btn)btn.classList.toggle("pressed",state.keys[k]);','document.querySelectorAll("[data-tx1-key=\'"+k+"\']").forEach(btn=>btn.classList.toggle("pressed",state.keys[k]));')
    h=h.replace('["S2","S3"].forEach(k=>','["S2","S3","S4","S5"].forEach(k=>')
    h=h.replace('红点</b> 实物热点','元件</b> 矢量绘制').replace('蓝字</b> 课堂引脚','标注</b> 课堂引脚')
    h=h.replace('1 静音','1 静音')
    (root/'index.html').write_text(h,encoding='utf-8');(root/'dist/index.html').write_text(h,encoding='utf-8')
    svg=re.search(r'<svg class="tx1-vector".*?</svg>',h,re.S).group(0)
    (root/'assets/tx1-board-vector.svg').write_text(svg,encoding='utf-8')
    (root/'dist/assets/tx1-board-vector.svg').write_text(svg,encoding='utf-8')
    scripts=re.findall(r'<script[^>]*>(.*?)</script>',h,re.S)
    js='\n'.join('new Function('+json.dumps(s)+');' for s in scripts)
    temp=root/'_check.cjs';temp.write_text(js,encoding='utf-8')
    subprocess.run([r'C:\Users\25466\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe',str(temp)],check=True);temp.unlink()
    print('All scripts parse; vector artwork exported')
