# ai-skills

My list of AI skills that I have collected, either made myself or gathered from others.

## Installing them for testing

`make install` symlinks every skill in this repo into `~/.claude/skills/`, so Claude
Code picks them up in any project. Because they are symlinks, editing a `SKILL.md`
here takes effect in the next session — no re-install step.

```sh
make list                     # every skill, its source dir, and install status
make check                    # validate frontmatter before installing
make install                  # symlink all of them into ~/.claude/skills
make install SKILL=grill-me   # just one
make uninstall                # remove only the links this repo created
make reinstall                # uninstall then install
```

The install name comes from the `name:` in each `SKILL.md`, not the directory — so
`linear-issue/` installs as `linear-issue-creator` and `zero-to-hero/files/` installs
as `zero-to-hero`.

### Options

| Variable | Effect |
| --- | --- |
| `SKILL=<name>` | Limit install/uninstall to one skill (matches the skill name or its directory) |
| `DEST=<dir>` | Install somewhere else, e.g. `DEST=../myproject/.claude/skills` for a project-local install |
| `FORCE=1` | Move a conflicting real directory aside to `<name>.bak` instead of skipping it |

`make copy` copies instead of symlinking — use it to hand someone a snapshot, not for
testing, since copies go stale as soon as you edit the source.

### Safety

`install` never overwrites a real directory in the destination (it skips and warns,
unless `FORCE=1`), and `uninstall` only removes symlinks that point back into this
repo. Skills installed from elsewhere are left alone.
