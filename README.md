# Mini DevNet Lab: **Pizza Ordering** (real‑world style)

A lightweight, “real‑world” flavored app so you can practice a clean workflow before we build a bigger service next week.

**You will:** create a venv → run tests with `pytest` → work on 2 branches (merge + tiny conflict + tags) → generate a **Menu & Sample Order** page and ship it via **GitHub Pages**.

---

## Step‑by‑Step (Student Guide)

### 0) Prereqs
- Python 3.10+ and Git installed
- GitHub account

### 1) Bootstrap
```bash
# unzip and cd into the folder
cd pizza-lab-starter

python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
pytest -q    # expect passing tests
```

### 2) Explore the app
- `data/menu.yaml` — sizes/toppings/prices, tax, promo codes
- `src/pizza.py` — pricing, validation, promo calculation
- `tests/test_pricing.py` — unit tests for real‑world rules
- `build_site.py` — builds `docs/index.html` to showcase menu + a sample order

### 3) Git workflow — Branch #1 (feature/twopizza-promo)
Implement or confirm BOGO‑style discount for two large pizzas with code `LARGE2`. Tests already cover this.
```bash
git init
git add .
git commit -m "Starter"

git checkout -b feature/twopizza-promo
pytest -q            # green
git add .
git commit -m "Confirm two-large promo logic"
git checkout main
git merge feature/twopizza-promo --no-ff -m "Merge feature/twopizza-promo"
git tag v1.0.0 -m "Baseline pizza app + tests"
```

### 4) Git workflow — Branch #2 (tiny conflict practice)
Change the **same YAML line** on a branch and on `main` to simulate a 1‑line conflict (e.g., tweak `tax_rate` or a price). Then resolve and tag.
```bash
git checkout -b feature/price-tweak
# edit data/menu.yaml: change a price or tax_rate
git add data/menu.yaml
git commit -m "Adjust price/tax"

git checkout main
# simulate conflicting change to the same line
git add data/menu.yaml
git commit -m "Simulate conflicting change on main"

git merge feature/price-tweak
# resolve the single conflict, keep the desired final value; remove markers
pytest -q
git add data/menu.yaml
git commit -m "Resolve price conflict; tests green"
git tag v1.1.0 -m "Resolved pricing conflict"
```

### 5) Build & Preview
```bash
python build_site.py
# open docs/index.html in your browser
```

### 6) Publish to GitHub Pages
1. Create a GitHub repo and push your code (include tags).
2. GitHub: **Settings → Pages → Build from branch → main /docs**.
3. Your site: `https://<username>.github.io/<repo-name>/`

### 7) Submit
- **GitHub Pages URL** (live site)
- **Repo URL**
- **Screenshot** showing tests passing and the site

---

## Rubric (10 pts)
- (2) venv + deps installed; tests run
- (3) Git workflow: 2 feature branches, merge commits, tags (`v1.0.0`, `v1.1.0`)
- (3) Pricing, tax, and promo rules pass tests
- (2) Site built and published to GitHub Pages
