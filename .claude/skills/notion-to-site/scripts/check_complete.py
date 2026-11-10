import re, os, html as H, sys
SP=sys.argv[1].rstrip("/\\")+"/"   # 작업 폴더(<tag>_raw.txt가 있는 곳)
PROJ=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "topics")).replace("\\", "/")+"/"
def norm(s):
    s=s.replace("\<","&lt;").replace("\>","&gt;")
    s=re.sub(r"^\s*(?:>|####)\s+","",s)
    s=re.sub(r'<span discussion-urls="[^"]+">','',s)
    s=re.sub(r"<[^>]+>"," ",s)
    s=H.unescape(s)
    for ch in r"\~^*[]()<>:_-.!#+|$%&":
        s=s.replace("\\"+ch,ch)
    s=re.sub(r"^\s*-\s+","",s)
    s=re.sub(r"\s+","",s)
    return s
SKIP={"<p />","---","<ul>","</ul>","<li>","</li>","<p>","</p>","<columns>","</columns>","</column>","</callout>","<quote>","</quote>"}
pairs=[a.split(":") for a in sys.argv[2:]]   # 사용: python check_complete.py <작업폴더> d4:thein-day4 d5:thein-day5
for tag,pid in pairs:
    t=open(SP+f"{tag}_raw.txt",encoding="utf-8").read()
    c=t.split("<content>",1)[1].split("</content>",1)[0]
    body=open(PROJ+pid+"/index.html",encoding="utf-8").read().split('<main id="top"',1)[1]
    hay=norm(body); miss=[]; total=0
    for ln in c.split("\n"):
        s=ln.strip()
        if not s or s in SKIP or s.startswith(("<image ","<column","<callout")): continue
        n=norm(s)
        if not n: continue
        total+=1
        if n not in hay: miss.append(s)
    print(f"{pid}: checked {total} lines, missing {len(miss)}")
    for m in miss[:25]: print("   MISSING:", m[:150])
