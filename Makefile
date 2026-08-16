# Install the skills in this repo into Claude Code so they can be tested.
#
#   make list                     show every skill and whether it is installed
#   make install                  symlink all skills into ~/.claude/skills
#   make install SKILL=grill-me   symlink just one
#   make uninstall                remove only the links this repo created
#   make check                    validate frontmatter before installing
#
# Overrides:
#   DEST=path/to/.claude/skills   install somewhere else (e.g. a project dir)
#   FORCE=1                       move a conflicting real directory to <name>.bak

SHELL := /bin/bash
SKILLS := ./scripts/skills.sh

DEST  ?= $(HOME)/.claude/skills
MODE  ?= link
SKILL ?=
FORCE ?= 0

export DEST MODE SKILL FORCE

.PHONY: help list install link copy uninstall reinstall check

help:
	@echo "ai-skills"
	@echo
	@echo "  make list             list skills and their install status"
	@echo "  make check            validate skill frontmatter"
	@echo "  make install          symlink all skills into $(DEST)"
	@echo "  make copy             copy instead of symlink (snapshot, not live)"
	@echo "  make uninstall        remove links created from this repo"
	@echo "  make reinstall        uninstall then install"
	@echo
	@echo "  SKILL=<name>          limit install/uninstall to one skill"
	@echo "  DEST=<dir>            install elsewhere (default ~/.claude/skills)"
	@echo "  FORCE=1               move a conflicting real dir aside to <name>.bak"

list:
	@$(SKILLS) list

check:
	@$(SKILLS) check

install:
	@$(SKILLS) install

# Explicit alias so "make link" reads clearly next to "make copy".
link: install

copy:
	@MODE=copy $(SKILLS) install

uninstall:
	@$(SKILLS) uninstall

reinstall: uninstall install
