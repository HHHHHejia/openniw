.PHONY: ui check test sync-skill build release

ui:
	sh scripts/build_ui.sh

test:
	python3 -m pytest tests/ -q

sync-skill:
	python3 scripts/sync_skill.py

check: test
	python3 scripts/sync_skill.py --check
	@# UI bundle freshness: fail if frontend/ changed since the committed stamp
	@stamp=$$(python3 -c "import json;print(json.load(open('src/openniw/ui/ui-build.json'))['frontend_tree'])" 2>/dev/null || echo missing); \
	tree=$$(git rev-parse "HEAD:frontend" 2>/dev/null || echo unknown); \
	if [ "$$stamp" != "$$tree" ]; then \
	  echo "UI bundle stale (stamp $$stamp != HEAD:frontend $$tree) — run 'make ui' and commit"; exit 1; \
	fi

build: check
	python3 -m pip install -q build && python3 -m build

release: build
	@echo "Now: python3 -m twine upload dist/*  (needs your PyPI token)"
