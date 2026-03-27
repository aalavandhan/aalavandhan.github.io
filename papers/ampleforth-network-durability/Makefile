PAPER_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
VENV      := $(PAPER_DIR)sims/.venv
PYTHON    := $(VENV)/bin/python
FIGURES   := $(PAPER_DIR)figures

CHARTS := $(FIGURES)/price_over_time.pdf \
          $(FIGURES)/price_supply_overlay.pdf \
          $(FIGURES)/price_deviation_dist.pdf \
          $(FIGURES)/supply_change_dist.pdf \
          $(FIGURES)/log_supply_change_dist.pdf \
          $(FIGURES)/daily_vol_ampl.pdf \
          $(FIGURES)/daily_vol_comparison.pdf \
          $(FIGURES)/monthly_vol_ampl.pdf \
          $(FIGURES)/monthly_vol_comparison.pdf \
          $(FIGURES)/max_neg_rebase.pdf

.PHONY: all pdf charts venv clean open

all: pdf

# ---------- Python environment ----------
venv: $(VENV)/bin/activate

$(VENV)/bin/activate: sims/requirements.txt
	python3.13 -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r sims/requirements.txt
	touch $(VENV)/bin/activate

# ---------- Charts ----------
charts: $(CHARTS)

$(CHARTS): sims/generate_charts.py $(VENV)/bin/activate
	$(PYTHON) sims/generate_charts.py

# ---------- PDF ----------
pdf: main.pdf

main.pdf: main.tex $(CHARTS)
	tectonic main.tex

# ---------- Open ----------
open: pdf
	open main.pdf

# ---------- Clean ----------
clean:
	rm -rf main.pdf figures $(VENV)
