#!/usr/bin/env bash
#
# Install/manage the skills in this repo so they can be tested in Claude Code.
#
# Usage: scripts/skills.sh <list|install|uninstall|check>
#
# Environment overrides (set by the Makefile):
#   DEST   destination skills dir   (default: ~/.claude/skills)
#   MODE   link | copy              (default: link)
#   SKILL  install/uninstall only this skill (matches name or source dir)
#   FORCE  1 = replace a real directory in DEST, moving it aside to <name>.bak
#
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${DEST:-$HOME/.claude/skills}"
MODE="${MODE:-link}"
SKILL="${SKILL:-}"
FORCE="${FORCE:-0}"

if [ -t 1 ]; then
  BOLD=$'\033[1m'; DIM=$'\033[2m'; RED=$'\033[31m'; GREEN=$'\033[32m'
  YELLOW=$'\033[33m'; BLUE=$'\033[34m'; RESET=$'\033[0m'
else
  BOLD=""; DIM=""; RED=""; GREEN=""; YELLOW=""; BLUE=""; RESET=""
fi

warn() { printf '%s\n' "${YELLOW}warn${RESET}  $*" >&2; }
fail() { printf '%s\n' "${RED}error${RESET} $*" >&2; exit 1; }

# Read a single frontmatter key from a SKILL.md (first match wins, value trimmed).
frontmatter() {
  awk -v key="$2" '
    NR == 1 && /^---[[:space:]]*$/ { in_fm = 1; next }
    in_fm && /^---[[:space:]]*$/   { exit }
    in_fm && index($0, key ":") == 1 {
      value = substr($0, length(key) + 2)
      sub(/^[[:space:]]+/, "", value)
      sub(/[[:space:]]+$/, "", value)
      gsub(/^["'"'"']|["'"'"']$/, "", value)
      print value
      exit
    }
  ' "$1"
}

# Emit "<source dir>\t<installed name>" for every skill in the repo, sorted by name.
discover() {
  find "$REPO_ROOT" -name SKILL.md -not -path "*/.git/*" -not -path "$DEST/*" -print |
  while IFS= read -r skill_md; do
    src="$(dirname "$skill_md")"
    name="$(frontmatter "$skill_md" name || true)"
    if [ -z "$name" ]; then
      # No declared name: fall back to the directory, stepping up out of a
      # generic wrapper dir like zero-to-hero/files.
      name="$(basename "$src")"
      case "$name" in
        files|skill|src) name="$(basename "$(dirname "$src")")" ;;
      esac
    fi
    name="$(printf '%s' "$name" | tr '[:upper:]' '[:lower:]')"
    printf '%s\t%s\n' "$src" "$name"
  done | sort -t"$(printf '\t')" -k2,2
}

# Does $1 match the SKILL filter (by installed name or source dir basename)?
selected() {
  [ -z "$SKILL" ] && return 0
  [ "$2" = "$SKILL" ] && return 0
  [ "$(basename "$1")" = "$SKILL" ] && return 0
  return 1
}

# Where does the symlink at $1 point? (absolute; empty if not a symlink)
link_target() {
  [ -L "$1" ] || return 0
  local t; t="$(readlink "$1")"
  case "$t" in
    /*) printf '%s' "$t" ;;
    *)  printf '%s' "$(cd "$(dirname "$1")" && pwd -P)/$t" ;;
  esac
}

# Is the path at $1 a symlink owned by this repo?
owned_by_repo() {
  local t; t="$(link_target "$1")"
  [ -n "$t" ] && case "$t" in "$REPO_ROOT"/*) return 0 ;; esac
  return 1
}

cmd_list() {
  printf '%s\n' "${BOLD}skills in $REPO_ROOT${RESET}"
  printf '%s\n' "${DIM}destination: $DEST${RESET}"
  echo
  printf '  %-34s %-30s %s\n' "NAME" "SOURCE" "STATUS"
  local count=0
  while IFS="$(printf '\t')" read -r src name; do
    count=$((count + 1))
    local target="$DEST/$name" status
    if owned_by_repo "$target"; then
      if [ "$(link_target "$target")" = "$src" ]; then
        status="${GREEN}linked${RESET}"
      else
        status="${YELLOW}linked elsewhere in repo${RESET}"
      fi
    elif [ -L "$target" ]; then
      status="${YELLOW}symlink to $(link_target "$target")${RESET}"
    elif [ -d "$target" ]; then
      status="${BLUE}copied / external dir${RESET}"
    else
      status="${DIM}not installed${RESET}"
    fi
    printf '  %-34s %-30s %b\n' "$name" "${src#$REPO_ROOT/}" "$status"
  done < <(discover)
  echo
  printf '%s\n' "${DIM}$count skill(s) found${RESET}"
}

cmd_install() {
  mkdir -p "$DEST"
  local installed=0 skipped=0 matched=0
  while IFS="$(printf '\t')" read -r src name; do
    selected "$src" "$name" || continue
    matched=$((matched + 1))
    local target="$DEST/$name"

    # An existing real directory is someone else's skill - never clobber silently.
    if [ -d "$target" ] && [ ! -L "$target" ]; then
      if [ "$FORCE" = "1" ]; then
        if [ -e "$target.bak" ]; then
          warn "$name: $target.bak already exists, skipping"
          skipped=$((skipped + 1)); continue
        fi
        mv "$target" "$target.bak"
        printf '  %s %s %s\n' "${YELLOW}moved${RESET}" "$name" "${DIM}-> $name.bak${RESET}"
      else
        warn "$name: $target is a real directory (not from this repo); re-run with FORCE=1 to move it aside"
        skipped=$((skipped + 1)); continue
      fi
    fi

    # A symlink is safe to replace whether it points here or elsewhere.
    [ -L "$target" ] && rm "$target"

    if [ "$MODE" = "copy" ]; then
      cp -R "$src" "$target"
      printf '  %s %-32s %s\n' "${GREEN}copied${RESET}" "$name" "${DIM}${src#$REPO_ROOT/}${RESET}"
    else
      ln -s "$src" "$target"
      printf '  %s %-32s %s\n' "${GREEN}linked${RESET}" "$name" "${DIM}${src#$REPO_ROOT/}${RESET}"
    fi
    installed=$((installed + 1))
  done < <(discover)

  if [ -n "$SKILL" ] && [ "$matched" -eq 0 ]; then
    fail "no skill matching SKILL=$SKILL (run 'make list' to see the names)"
  fi
  echo
  printf '%s\n' "${BOLD}$installed installed${RESET}${skipped:+, $skipped skipped} -> $DEST"
  printf '%s\n' "${DIM}restart Claude Code (or start a new session) to pick them up${RESET}"
}

cmd_uninstall() {
  [ -d "$DEST" ] || { echo "nothing to do: $DEST does not exist"; return 0; }
  local removed=0
  # Only ever remove symlinks that point back into this repo.
  for target in "$DEST"/*; do
    [ -e "$target" ] || [ -L "$target" ] || continue
    owned_by_repo "$target" || continue
    local name; name="$(basename "$target")"
    local src; src="$(link_target "$target")"
    selected "$src" "$name" || continue
    rm "$target"
    printf '  %s %s\n' "${RED}removed${RESET}" "$name"
    removed=$((removed + 1))
  done
  echo
  printf '%s\n' "${BOLD}$removed link(s) removed${RESET} ${DIM}(copies and external skills left untouched)${RESET}"
}

cmd_check() {
  local errors=0 warnings=0 names="" count=0

  while IFS="$(printf '\t')" read -r src name; do
    count=$((count + 1))
    local rel="${src#$REPO_ROOT/}"
    local skill_md="$src/SKILL.md"
    local declared; declared="$(frontmatter "$skill_md" name || true)"
    local desc;     desc="$(frontmatter "$skill_md" description || true)"

    if [ -z "$declared" ]; then
      printf '  %s %s: no "name" in frontmatter (falling back to "%s")\n' "${RED}FAIL${RESET}" "$rel" "$name"
      errors=$((errors + 1))
    elif ! printf '%s' "$declared" | grep -Eq '^[a-z0-9]+(-[a-z0-9]+)*$'; then
      printf '  %s %s: name "%s" must be lowercase kebab-case\n' "${RED}FAIL${RESET}" "$rel" "$declared"
      errors=$((errors + 1))
    fi

    if [ -z "$desc" ]; then
      printf '  %s %s: no "description" in frontmatter\n' "${RED}FAIL${RESET}" "$rel"
      errors=$((errors + 1))
    elif [ "${#desc}" -lt 20 ]; then
      printf '  %s %s: description is only %s chars - too thin to trigger reliably\n' \
        "${YELLOW}WARN${RESET}" "$rel" "${#desc}"
      warnings=$((warnings + 1))
    fi

    if [ -n "$declared" ] && [ "$(basename "$src")" != "$declared" ]; then
      printf '  %s %s: directory name differs from skill name "%s"\n' "${YELLOW}WARN${RESET}" "$rel" "$declared"
      warnings=$((warnings + 1))
    fi

    case " $names " in
      *" $name "*)
        printf '  %s %s: duplicate skill name "%s" - installs would collide\n' "${RED}FAIL${RESET}" "$rel" "$name"
        errors=$((errors + 1)) ;;
    esac
    names="$names $name"
  done < <(discover)

  # Top-level dirs that look like skills but have no SKILL.md anywhere inside.
  for dir in "$REPO_ROOT"/*/; do
    dir="${dir%/}"
    case "$(basename "$dir")" in scripts|.*) continue ;; esac
    if [ -z "$(find "$dir" -name SKILL.md -print -quit)" ]; then
      printf '  %s %s/: no SKILL.md anywhere inside - not installable\n' \
        "${YELLOW}WARN${RESET}" "$(basename "$dir")"
      warnings=$((warnings + 1))
    fi
  done

  echo
  printf '%s\n' "${BOLD}$count skill(s) checked${RESET} - ${errors} error(s), ${warnings} warning(s)"
  [ "$errors" -eq 0 ] || exit 1
}

case "${1:-}" in
  list)      cmd_list ;;
  install)   cmd_install ;;
  uninstall) cmd_uninstall ;;
  check)     cmd_check ;;
  *)         fail "usage: $(basename "$0") <list|install|uninstall|check>" ;;
esac
