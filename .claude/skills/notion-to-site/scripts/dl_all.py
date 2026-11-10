import json, re, os, sys, urllib.request, time
from concurrent.futures import ThreadPoolExecutor
# 사용: python dl_all.py <fetch결과파일.json> <tag> <작업폴더>
src, tag = sys.argv[1], sys.argv[2]
SP = sys.argv[3].rstrip("/\\") + "/"
j = json.load(open(src, encoding="utf-8"))
txt = j["text"]; refs = j["references"]
open(SP+f"{tag}_raw.txt","w",encoding="utf-8").write(txt)
json.dump(refs, open(SP+f"{tag}_refs.json","w",encoding="utf-8"))
order = re.findall(r'<image source="([^"]+)"', txt)
os.makedirs(SP+tag, exist_ok=True)
t0 = time.time()
def get(i):
    o = order[i-1]
    for attempt in range(2):
        try:
            d = urllib.request.urlopen(refs[o], timeout=100).read()
            open(SP+f"{tag}/raw{i:02d}.bin","wb").write(d)
            print(f"{tag} {i:02d} ok {len(d)//1024}KB {time.time()-t0:.0f}s", flush=True); return True
        except Exception as e:
            print(f"{tag} {i:02d} retry {e}", flush=True)
    return False
with ThreadPoolExecutor(10) as ex:
    res = list(ex.map(get, range(1, len(order)+1)))
print(tag, "done", sum(res), "/", len(order), "| title:", j.get("title"), "| edited:", j.get("page_last_edited_at"), flush=True)
