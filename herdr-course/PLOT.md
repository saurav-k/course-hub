# PLOT - Herdr from Zero

The reading order below is the true order. The course map (`index.html`) and this file
are two views of one sequence and have to agree; when they disagree one of them is wrong
and it gets fixed before anything new is added.

## Written, in order

| # | File | Module | Name | Rung |
|---|---|---|---|---|
| 01 | `lessons/0001-what-is-herdr.html` | 01 Herdr in one picture | What is Herdr | foundation |
| 02 | `lessons/0002-the-always-on-server.html` | 02 How it works | The always-on server | working |
| 03 | `lessons/0003-sessions-workspaces-panes.html` | 02 How it works | Sessions, workspaces, panes | working |
| 04 | `lessons/0004-knowing-which-agent-is-stuck.html` | 02 How it works | Knowing which agent is stuck | working |
| 05 | `lessons/0005-install-and-first-run.html` | 03 Getting it running | Install and first run | foundation |
| 06 | `lessons/0006-configuring-herdr.html` | 03 Getting it running | Configuring Herdr | working |
| 07 | `lessons/0007-remote-updates-and-deployment.html` | 03 Getting it running | Remote, updates and deployment | working |
| 08 | `lessons/0008-what-people-use-it-for.html` | 04 What it is for | What people use it for | foundation |
| 09 | `lessons/0009-what-a-plugin-is.html` | 05 Plugin development | What a plugin is | foundation |
| 10 | `lessons/0010-the-plugin-contract.html` | 05 Plugin development | The plugin contract | working |
| 11 | `lessons/0011-build-your-first-plugin.html` | 05 Plugin development | Build your first plugin | working |
| 12 | `lessons/0012-plugin-lifecycle-and-api.html` | 05 Plugin development | Plugin lifecycle and API | working |
| 13 | `lessons/0013-testing-and-publishing.html` | 05 Plugin development | Testing and publishing | working |

## Why this order and no other

Module 01 is the whole idea before any machinery, so a reader can stop after one page
and still know what Herdr is. Module 02 explains the mechanism while the reader still
has no installation to fiddle with - concepts before commands. Module 03 is hands-on and
depends on 01-02 for its vocabulary; a reader who installs first has no words for what
they are installing. Module 04 answers "why bother" once the reader can judge the answer.
Module 05 is the largest module by design: the plugin track (09-13) reads as one
continuous build - concept, contract, worked example, runtime behaviour, then shipping -
and nothing in it needs anything after it.

## Reserved, unwritten

- **Reference: glossary of Herdr terms.** Planned as `reference/glossary.html`, linked
  from every lesson foot. Not written yet; the course map carries it as a `.roadmap`
  entry until it exists.

Nothing else is planned. New numbers go at the end of the sequence above; nothing
already published is renumbered or renamed.
