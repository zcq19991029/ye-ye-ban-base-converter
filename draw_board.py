from pathlib import Path
import re
root=Path(__file__).parent
p=root/'index.html'
h=p.read_text(encoding='utf-8-sig')
s=['<svg class="tx1-vector" viewBox="0 0 1500 800" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="GTX TX-1 元件与电路板矢量复刻"><defs><linearGradient id="pcb" x2="1" y2="1"><stop stop-color="#df152b"/><stop offset="1" stop-color="#a80019"/></linearGradient><linearGradient id="metal"><stop stop-color="#eceadf"/><stop offset=".5" stop-color="#8e989e"/><stop offset="1" stop-color="#e8eceb"/></linearGradient><filter id="ledglow"><feGaussianBlur stdDeviation="5"/></filter></defs><rect x="8" y="8" width="1484" height="784" rx="34" fill="url(#pcb)" stroke="#76101c" stroke-width="8"/>']
def rect(x,y,w,hh,fill,stroke='none',r=0): s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{hh}" rx="{r}" fill="{fill}" stroke="{stroke}"/>')
def text(x,y,t,size=16,fill='#fff0d5'): s.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-family="Consolas, monospace">{t}</text>')
def line(d,color='#831021',width=2): s.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"/>')
def chip(x,y,w,hh,label,pins=8):
    for i in range(pins):
        yy=y+8+i*(hh-16)/max(1,pins-1)
        rect(x-9,yy,10,5,'url(#metal)');rect(x+w-1,yy,10,5,'url(#metal)')
    rect(x,y,w,hh,'#171b21','#434951',4);text(x+7,y+hh/2,label,12,'#aeb5b8')
def header(x,y,n,label,vertical=False):
    rect(x-4,y-4,18 if vertical else n*17+6,n*17+6 if vertical else 18,'#292528','#616064',2)
    for i in range(n): rect(x if vertical else x+i*17,y+i*17 if vertical else y,9,9,'#090a0c','#a39d79',1)
    text(x,y-9,label,13)
def key(x,y,label,pin='',ident=''):
    s.append(f'<g class="pcb-key" {ident} tabindex="0" role="button" aria-label="{label} {pin}">')
    for dx,dy in [(0,0),(30,0),(0,29),(30,29)]:rect(x+dx,y+dy,5,8,'url(#metal)')
    rect(x,y+3,35,32,'#d7d8cd','#6b7377',3);s.append(f'<circle class="key-cap" cx="{x+17.5}" cy="{y+19}" r="11" fill="#15181c"/>');text(x,y+52,label,14);s.append('</g>')
# Copper fanouts follow the component groups and terminate at pads.
for i in range(20):
    yy=300+i*19
    line(f'M535 {yy} H{500-i*3} L{448-i*3} {yy-48} H395')
    line(f'M655 {yy} H{682+i*3} L{720+i*3} {yy-40} H820')
for i in range(8):line(f'M365 {55+i*33} H{390+i*3} V{270+i*5} H445')
for i in range(16):line(f'M{210+(i%4)*65} {475+(i//4)*68} H{475+i*2} V{320+i*17} H535')
for i in range(10):line(f'M{1080+i*14} 190 V{260+i*6} L{1140+i*14} {310+i*6} V430')
for x,y in [(32,35),(1460,35),(32,763),(1460,763)]:s.append(f'<circle cx="{x}" cy="{y}" r="19" fill="#d4cfaf"/><circle cx="{x}" cy="{y}" r="10" fill="#27252b"/>')
for d in ['M20 300 H1030 V20','M190 20 V780','M390 20 V780','M760 310 V780','M1040 20 V780','M20 450 H190','M190 710 H530','M760 450 H1490','M1040 620 H1490']:line(d,'#ffdfd6',3)
text(64,55,'GTX TX-1',27);text(64,79,'天祥 · 单片机实验板',13)
# Two USB/power areas and adjustment pots.
for x,y in [(20,130),(1340,22)]:
    rect(x,y,100,90,'url(#metal)','#5a6065',5);rect(x+17,y+22,66,47,'#343536','#eee9ca',3);rect(x+30,y+32,40,20,'#161a1e');text(x,y+112,'USB / 5V',14)
for x,y in [(115,105),(1155,26)]:rect(x,y,45,48,'#e7e5d7','#69727b',4);rect(x+10,y+7,26,30,'#1779c2','#07528f',3)
for x,y,l in [(205,35,'RP3'),(258,35,'RP2'),(72,375,'ADC'),(1080,485,'光敏')]:
    rect(x,y,39,40,'#207cc1','#15507c',3);s.append(f'<circle cx="{x+20}" cy="{y+20}" r="9" fill="#a4afb5"/>');line(f'M{x+13} {y+20} H{x+27}','#414b56',3);text(x,y+58,l,13)
chip(130,235,36,70,'CH340',12);chip(60,330,43,43,'ADC',8);chip(270,340,40,53,'DAC',8);text(20,290,'USB转串口＆电源',13)
# Physical D1..D8 column. Numbering displayed without asserting an unverified bit order.
for i in range(8):
    y=45+i*33;rect(332,y,31,16,'url(#metal)','#e8b9a2',2)
    s.append(f'<rect class="pcb-led" data-led-bit="{i}" x="341" y="{y+3}" width="13" height="10" rx="2" fill="#64544b"/>');text(368,y+13,f'D{i+1}',14)
chip(325,318,50,88,'LED驱动',14)
# Six common-anode displays, segment shapes instead of text glyphs.
for i in range(6):
    x=422+i*91;rect(x,84,86,166,'#20222a','#a6a9a5',5)
    for xx,yy,ww,hh in [(15,12,52,8),(12,20,8,53),(65,20,8,53),(15,75,52,8),(12,83,8,53),(65,83,8,53),(15,138,52,8)]:rect(x+xx,84+yy,ww,hh,'#6c6862',r=3)
    s.append(f'<circle cx="{x+76}" cy="234" r="4" fill="#6c6862"/>')
header(435,47,26,'LCD1602 / LCD12864');text(816,280,'六位共阳数码管',18)
chip(790,327,72,95,'74HC573',10);chip(917,327,72,95,'74HC573',10)
# Central DIP and real expansion headers.
chip(548,343,107,366,'STC89C52RC',20);text(542,323,'STC89C52RC',20)
header(510,340,20,'P7 / P9',True);header(686,340,20,'P6 / P8',True)
rect(561,728,83,27,'url(#metal)','#666e73',13);text(550,778,'Y1 · 12 MHz',14)
for i in range(4):
    for j in range(4):key(212+j*64,452+i*63,f'S{6+i*4+j}')
text(215,727,'4×4 矩阵键盘',18)
for i in range(4):key(215+i*64,737,f'S{i+2}',f'P3.{i+4}',f'data-tx1-key="S{i+2}"')
# EEPROM, reset and buzzer.
text(800,477,'天 祥',33);chip(790,535,53,48,'AT24C02',4);key(786,649,'S22','复位','id="tx1BoardReset"')
s.append('<g id="tx1BoardBuzzer"><circle cx="929" cy="586" r="57" fill="#151a21" stroke="#6d7179" stroke-width="5"/><circle cx="929" cy="586" r="10" fill="#06090d"/><text x="909" y="619" fill="#8d9699" font-size="12">BUZZER</text><circle class="pcb-sound" cx="929" cy="586" r="66" fill="none" stroke="#ffcb59" stroke-width="5" opacity="0"/></g>')
text(866,680,'5V有源蜂鸣器',17);text(875,704,'P2.3 · 低电平有效',13)
# Serial connector, headers and right extension zone.
rect(20,500,103,176,'url(#metal)','#1d2028',7);rect(36,527,73,120,'#14181e',r=12)
for i in range(9):s.append(f'<circle cx="{55+(i%2)*29}" cy="{542+(i//2)*22}" r="4" fill="#cab79a"/>')
header(1070,241,4,'DHT11 / P3');header(1060,327,4,'蓝牙 / P2');header(1060,399,4,'RGB / P15')
for x,y,l in [(1070,555,'步进电机'),(1070,625,'直流电机')]:rect(x,y,96,40,'#f4efe0','#b2b4ad',4);text(x,y+62,l,14)
header(1080,714,3,'舵机 P12');header(1320,202,8,'扩展口 P1');header(1340,170,4,'超声波');chip(1300,320,65,73,'STC8H8K',16);chip(1210,546,45,72,'驱动',8)
text(1220,622,'扩展区域',29);header(1300,702,11,'16×16点阵 P11')
for i in range(4):key(1200+i*61,737,f'扩展{i+1}')
key(1093,43,'P3.2');text(1115,767,'GTX TX-1',16)
s.append('</svg>')
svg=''.join(s)
h=re.sub(r'<img class="tx1-photo"[^>]*>',lambda m:svg,h,count=1)
h=re.sub(r'\s*<button class="tx1-hotspot".*?</button>','',h,flags=re.S)
h=h.replace('底图来自 GTX TX-1 实物资料；点击红色标记查看对应位置，按住 S2～S5 才算按下。','按 GTX TX-1 实物布局绘制：红色 PCB、元件封装、排针与走线均为矢量图形。按住板上 S2～S5 操作。')
h=h.replace('照片资料：GTX TX-1 板卡说明','布局依据：用户提供的 GTX TX-1 实物资料').replace('照片对应位置','板上对应位置').replace('板上真实铜箔走线仍以照片和原理图为准','铜箔示意按元件分区绘制；电气连接以对应型号原理图为准').replace('实物照片','矢量板图').replace('实物图上的','矢量板图上的')
h=h.replace('const buz=state.keys.S2,','const buz=false,')
h=h.replace('if(strip) strip.innerHTML=', 'document.querySelectorAll(".pcb-led").forEach(el=>{const on=((p1>>Number(el.dataset.ledBit))&1)===0;el.setAttribute("fill",on?"#ffed6b":"#64544b");el.style.filter=on?"drop-shadow(0 0 7px #ffea5a)":"none";});\n    if(strip) strip.innerHTML=')
h=h.replace('$("#tx1Reset")?.addEventListener("click",()=>{state.p1=255;Object.keys(state.keys).forEach(k=>state.keys[k]=false);render();});','["#tx1Reset","#tx1BoardReset"].forEach(sel=>$(sel)?.addEventListener("click",()=>{state.p1=255;Object.keys(state.keys).forEach(k=>state.keys[k]=false);render();}));')
h=h.replace('if(page!==\'p1\'&&codeRunning)stopCode();','if(page!==\'p1\'&&page!==\'board\'&&codeRunning)stopCode();')
h=h.replace('</head>','<style>.tx1-vector{display:block;width:100%;height:100%}.pcb-key{cursor:pointer;touch-action:none}.pcb-key:hover .key-cap{fill:#424c59}.pcb-key.pressed .key-cap{fill:#ffd15b}.tx1-photo-wrap{aspect-ratio:1500/800}.tx1-board-card{min-width:0}.tx1-layout{grid-template-columns:minmax(0,1fr)}.tx1-side{grid-template-columns:repeat(4,minmax(0,1fr))}@media(max-width:1000px){.tx1-side{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:650px){.tx1-side{grid-template-columns:1fr}.tx1-photo-wrap{overflow-x:auto}.tx1-vector{min-width:850px}.tx1-photo-wrap{aspect-ratio:auto}} </style></head>')
# Remove the obsolete prototype handler.
h=re.sub(r'<script>\s*\(function\(\)\{const keys=\{S2:false.*?</script>','',h,flags=re.S)
p.write_text(h,encoding='utf-8')
(root/'dist/index.html').write_text(h,encoding='utf-8')
print('SVG components drawn; source and dist synchronized')
