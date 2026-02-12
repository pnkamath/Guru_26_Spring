SHELL := /bin/bash
GIT_ROOT := $(shell git rev-parse --show-toplevel 2>/dev/null)
HERE := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

DATA = page_blocks_dirty.csv

help: ## show help.
	@gawk 'BEGIN { FS=":.*##"; \
		printf "\nUsage:\n  make \033[36m<target>\033[0m\n\ntargets:\n" } \
	/^[~a-zA-Z0-9_%./-]+:.*##/ { \
		printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 | "sort" \
	}' $(MAKEFILE_LIST) 

banner:
	@printf '\033[36m'
	@printf '%s\n' \
	'   ░██    ░██        ░██           ░██                            ░██' \
	'   ░██    ░██                      ░██                            ░██' \
	'░████████ ░████████  ░██░████████  ░██    ░██     ░██       ░████████  ░███████' \
	'   ░██    ░██    ░██ ░██░██    ░██ ░██   ░██    ░██████    ░██    ░██ ░██    ░██' \
	'   ░██    ░██    ░██ ░██░██    ░██ ░███████       ░██      ░██    ░██ ░██    ░██' \
	'   ░██    ░██    ░██ ░██░██    ░██ ░██   ░██               ░██   ░███ ░██    ░██' \
	'    ░████ ░██    ░██ ░██░██    ░██ ░██    ░██               ░█████░██  ░███████'
	@printf '\033[0m\n'

sh: ## run my shell
	@$(MAKE) -s banner
	@-HERE=$(HERE) bash --init-file $(HERE)/etc/ell -i

push: ## save to cloud
	@read -p "Reason? " msg; git commit -am "$$msg"; git push; git status

~/tmp/%.html: %.py ~/tmp Makefile
	mkdir -p ~/tmp
	pycco -d ~/tmp $<
	echo 'p {text-align: right}' >> ~/tmp/pycco.css

date: ## show date
	@echo $(shell date)

files: ## show files
	@ls

all: out/S1 out/S2 out/S4

out/S1: $(DATA); mkdir -p out; gawk -f S1.awk $< > $@
out/S2: $(DATA); mkdir -p out; gawk -f S2.awk $< > $@

out/S4: $(DATA); mkdir -p out; gawk -f S4.awk $< > $@
