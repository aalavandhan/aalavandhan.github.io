"""Download Berkshire Hathaway's 13F-HR information tables (XML era, report dates 2013-06-30 onward)
from SEC EDGAR into data/raw/edgar/ and write data/berkshire_13f_holdings.csv.
Run:  python -I fetch_13f.py
About 3 requests a second. Original 13F-HR filings only (amendments ignored).

STATUS (2026-11-19): NOT RUN TO COMPLETION. data.sec.gov served the filing list to a generic
User-Agent, but www.sec.gov/Archives returned HTTP 403. The SEC asks automated clients to identify
themselves with contact details in the User-Agent; this script will not invent one. To run it, set
the environment variable SEC_USER_AGENT to your own declared identity.
"""
import json, os, time, urllib.request, csv, collections
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "data", "raw", "edgar")
UA = {"User-Agent": os.environ.get("SEC_USER_AGENT", "research-script/1.0")}
CIK = "1067983"


def get(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return open(path, "rb").read()
    time.sleep(0.35)
    data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
    open(path, "wb").write(data)
    return data


def filings():
    j = json.loads(get(f"https://data.sec.gov/submissions/CIK{int(CIK):010d}.json", os.path.join(RAW, "submissions.json")))
    blocks = [j["filings"]["recent"]]
    for f in j["filings"]["files"]:
        blocks.append(json.loads(get("https://data.sec.gov/submissions/" + f["name"], os.path.join(RAW, f["name"]))))
    out = []
    for r in blocks:
        for i, form in enumerate(r["form"]):
            if form == "13F-HR" and r["reportDate"][i] >= "2013-06-30":
                out.append((r["reportDate"][i], r["filingDate"][i], r["accessionNumber"][i]))
    return sorted(set(out))


def local(tag):
    return tag.split("}")[-1]


def main():
    rows = []
    fl = filings()
    seen = collections.Counter(f[0] for f in fl)
    print(len(fl), "original 13F-HR filings;", "duplicate report dates:", [k for k, v in seen.items() if v > 1])
    for rep, filed, acc in fl:
        nodash = acc.replace("-", "")
        base = f"https://www.sec.gov/Archives/edgar/data/{CIK}/{nodash}/"
        idx = json.loads(get(base + "index.json", os.path.join(RAW, f"{acc}_index.json")))
        xmls = [it["name"] for it in idx["directory"]["item"] if it["name"].lower().endswith(".xml") and it["name"] != "primary_doc.xml"]
        if len(xmls) != 1:
            print("unexpected file list", rep, acc, xmls); continue
        data = get(base + xmls[0], os.path.join(RAW, f"{acc}_infotable.xml"))
        root = ET.fromstring(data)
        n = 0
        for it in root:
            if local(it.tag) != "infoTable":
                continue
            d = {}
            for ch in it.iter():
                d[local(ch.tag)] = (ch.text or "").strip()
            rows.append(dict(report_date=rep, filed=filed, accession=acc, issuer=d.get("nameOfIssuer"), title=d.get("titleOfClass"),
                             cusip=d.get("cusip", "").upper(), value=d.get("value"), shares=d.get("sshPrnamt"),
                             sh_type=d.get("sshPrnamtType"), put_call=d.get("putCall", "")))
            n += 1
        print(rep, filed, acc, n)
    with open(os.path.join(HERE, "data", "berkshire_13f_holdings.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)


if __name__ == "__main__":
    main()
