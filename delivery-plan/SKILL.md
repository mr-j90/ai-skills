---
name: delivery-plan
description: Delivery plan for a client engagement — print-ready HTML built on a spine date, a workstream Gantt, and dependency gates. Use when the user asks for a delivery plan, engagement plan, or client project timeline, or wants an SOW, kickoff notes, or a scoping call turned into a plan to send a client.
---

# Delivery Plan

A delivery plan is not a task list with dates on it. It is an argument that a **spine**
date will be met, and an honest account of what could stop that.

Build it by copying [`TEMPLATE.html`](TEMPLATE.html) — a complete, self-contained,
SkipForward-branded plan — and rewriting its content. The CSS is finished work.

Write the output to the working directory as `<client>-delivery-plan.html` unless the
user names a path.

## 1. Find the spine

The **spine** is the one date that cannot move — UAT opening, a contract expiring, a
system going dark, a season starting. Every other date in the plan is derived by
working backwards from it.

State it in the hero sub-line, in the opening `.ask`, and on the `.ms.spine` card.

**Done when** you can write this sentence with real values: *"{date} is when {event}
begins, which means this has to be live and carrying data by then, not merely built."*
If no date in the engagement is genuinely immovable, say so to the user and ask which
one is — a plan without a spine has nothing to work backwards from.

## 2. Map the gates

A **gate** is a dependency owned by someone other than you that blocks downstream work.
Collector access, network time, a signed field list, an environment someone else
provisions. Gates are the reason plans slip, so the plan names them before the client
discovers them.

Each gate carries an owner, a by-when, and the consequence if it slips — in days, against
a named date.

**Done when** every gate appears in all three places: its own Gantt row with an amber
diamond, a `tr.critical` row in the ask table, and a sentence of prose *before* the chart
that tells the reader to look for it. A dependency in only one of the three is not yet a
gate — put it in the other two or drop it.

## 3. Lay the timeline

One column per week. Components run concurrently wherever the dependency graph allows,
and the plan says why: concurrency is a **risk decision**, not a schedule fact. Write it
as *"That is deliberate: it is what protects {spine} if {gate} takes longer than expected."*

Place work you do not own on its own row — `.client` hatched for client-owned, `.joint`
hatched for shared, `.ghost` dashed for not-yet-started.

**Done when** every component in section 02 has a bar, the spine lands in the final
column, and each bar's text says what happens in it rather than repeating the row label.

## 4. Compose the sections

Reach for the block that fits; drop any section with nothing real in it.

| Block | Classes | Reach for it when |
|---|---|---|
| Section band | `.page` + `.pageband` | Every numbered section |
| Headline claim | `.ask` | Opening a section with the one thing that matters |
| Comparison grid | `table.ft` | Workstreams side by side; any what/when/why table |
| Boundary | `.twocol` + `.box.good` / `.box.out` | We build vs we do not |
| Date strip | `.msrow` + `.ms`, `.spine` on the immovable one | The four or five dates that matter |
| Timeline | `.gantt` | Always — this is the centrepiece |
| Legend | `.gkey` | Always, directly under the Gantt |
| Component detail | `.compstack` + `.comp.c1`–`.c4` | Expanding each Gantt row into what it actually is |
| The ask | `table.ft` + `tr.critical` | What we need from you; `.critical` marks date-movers |
| Module cards | `.mods` + `.mod`, `.pend` if not yet detailed | A second workstream, or anything deferred |
| Candour callout | `.named` | A gap you would rather name now than have discovered later |
| Numbered steps | `ul.steps` | Next steps, each with an owner and a date |

The **boundary** section earns its place through the *right* column. "We do not touch your
production data — you execute the promotion, we are not members of that workspace" is
worth more to a client than five lines of what you will build.

**Done when** every section carries content specific to this engagement, and the nav
numbers match the page bands.

## 5. Write the ask

Three columns: what / by when / why it matters. The third column names the **consequence**
— what breaks, and which date moves. It never restates the first.

> Later than end of January and the ingestion build compresses against 19 February.

**Done when** each row's third column would change the client's behaviour if it were the
only cell they read.

## 6. Name it now

Somewhere in every honest plan there is a gap: partial coverage, a deferred workstream, a
risk you are carrying. Put it in a `.named` block, in plain words, with the phrase that
makes it land — *"We would rather say that now than have it discovered in April."*

**Done when** a reader who dislikes the plan learns it here rather than in month four.

## 7. Render and verify

Open the file in a browser, then screenshot it and look at it. Check:

- Every sentence names this client, this system, these dates.
- The nav anchors jump to their sections.
- The Gantt bars sit inside the column count, and the legend lists only classes actually used.
- Print holds: `Cmd-P` shows the nav hidden, the Gantt fitting the page width, and hero and
  bar colours intact.

**Done when** you have looked at the rendered page, not only the markup.

## Colour

The palette is validated — adjacent-pair CVD ΔE 16.1 deutan, every bar clearing 4.5:1
against its white label. Use it as-is:

- Workstream bars take `.c1 .c2 .c3 .c4` **in order, never cycled**. A fifth workstream
  folds into an existing bar or takes the neutral `.ops`.
- `--risk` (red diamond, hard dates) and `--gate` (amber diamond) are **reserved status
  colours** — never a workstream.
- `--brand #A4B885` is a fill with ink on top. On white it reads at 2.15:1, so text accents
  take `--brand-strong #5F763D`.

Changing a bar colour means re-running the validator in the `dataviz` skill
(`scripts/validate_palette.js`) before shipping.

## Voice

Second person for the client, first person plural for us. Short declaratives. Dates as
`19 Feb`. Bold carries the load-bearing clause, not whole sentences.

Give an indicative effort in hours so the plan reads against a size — and say the committed
number sits in the Statement of Work.
