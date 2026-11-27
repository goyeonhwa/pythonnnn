import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import parse_sales, summarize
root = Path(__file__).resolve().parents[2]
rows = parse_sales((root / "data" / "sales.csv").read_bytes())
assert summarize(rows)["revenue"] == 31500
assert summarize(rows)["quantity"] == 7
assert summarize([])["revenue"] == 0
print("dashboard calculations OK")