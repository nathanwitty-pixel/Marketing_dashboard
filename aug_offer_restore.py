"""One-off: restore August's Offer Type figures into monthly_report_history.json
from report_2026_august.html (the dated archive generated before the offer-parse
bug corrupted the re-archived snapshot). Run once, then push_to_supabase + history."""
import json, re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

rep = open("report_2026_august.html", encoding="utf-8").read()
RPT = json.loads(re.search(r"const RPT\s*=\s*(\{.*?\});\s*</script>", rep, re.S).group(1))
o = RPT["offer"]
ke = o.get("items", [])
su = lambda a: sum(int(x.get("units") or 0) for x in a)
combos = [x for x in ke if x.get("type") == "combo"]
deals  = [x for x in ke if x.get("type") == "deal"]

offer_type = {
    "combos": 10, "powerDeals": 10,
    "kenya": {"comboUnits": su(combos), "comboValue": 0, "comboAvg": 0,
              "dealUnits": su(deals), "dealValue": 2599700, "dealAvg": 2025,
              "offers": ke},
    "sinza":  {"units": 206, "value": 49500, "cleared": 42.2, "offers": o.get("sinza", [])},
    "uganda": {"units": 78,  "value": 36,    "cleared": 10.3, "offers": o.get("uganda", [])},
}

hist = json.load(open("monthly_report_history.json", encoding="utf-8"))
hist["2026-08"]["offerType"] = offer_type
json.dump(hist, open("monthly_report_history.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"Restored Aug offerType: combos {offer_type['kenya']['comboUnits']} units, "
      f"deals {offer_type['kenya']['dealUnits']}, Sinza {offer_type['sinza']['units']}, "
      f"Uganda {offer_type['uganda']['units']}  ({len(ke)} Kenya offers, "
      f"{len(o.get('sinza', []))} Sinza, {len(o.get('uganda', []))} Uganda)")
