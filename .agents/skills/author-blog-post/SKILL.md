---
name: author-blog-post
description: >-
  Author, structure, and format engaging, light, tech-first, and startup-friendly blog posts
  for Gurple under docs/blog/posts/, adhering strictly to the Human Author Writing Style rule,
  NYT headline conventions, and MkDocs blog plugin requirements.
---

# Author Blog Post

This skill defines the guidelines, frontmatter specifications, structural templates, tone requirements, and quality standards for authoring blog posts for Gurple under `docs/blog/posts/`.

---

## 1. Role and Tone: Startup-Friendly, Technical, and Conversational

While the main Gurple book is a structured reference manual, the Gurple Blog is a conversational, fast-moving companion for immediate news, hands-on labs, open-source tools, and digestible technical breakdowns.

### Tone Principles
* **Personal First-Person Voice ("I / Me / Myself")**: The author is an individual researcher and builder. Always write from the first-person singular perspective (*"I built"*, *"I noticed"*, *"I wanted to test"*). Strictly prohibit the royal or collective *"we"* (*"we built"*, *"our team"*, *"we wanted to see"*).
* **Direct & Conversational**: Open with a compelling question or relatable engineering dilemma (such as *"What if you could hijack a neural network without running gradient descent...?"*).
* **Light & Startup-Savvy**: Keep prose punchy, active, and accessible without sacrificing technical depth. Avoid overly dense academic posturing and administrative corporate filler.
* **Concrete & Pragmatic**: Ground arguments in actual code, metrics, model identifiers (`Qwen/Qwen3.5-0.8B`, `gemini-3.8-flash`), parameter counts, and reproducible steps.
* **No Marketing Fluff**: Do not write promotional brochure prose. State verifiable facts, test results, and practical implications directly.

> [!IMPORTANT]
> All blog posts must strictly comply with [`.agents/rules/human-author-writing-style.md`](file:///Users/fcpenha/git/gurple/.agents/rules/human-author-writing-style.md).
> * Zero forbidden vocabulary words from the blacklist.
> * Zero trailing participial clauses (`-ing` tails at sentence ends).
> * Zero stacked noun compounds (chains of 3+ nouns).
> * Avoid em dashes (`—`) and parenthetical hype breaks; use natural commas or direct sentence structures.
> * Header capitalization strictly follows NYT style per [`.agents/rules/nyt-header.md`](file:///Users/fcpenha/git/gurple/.agents/rules/nyt-header.md).

---

## 2. File Naming and Frontmatter Specification

Every published post requires standardized file naming conventions and complete metadata frontmatter.

### File Location & Naming
Blog posts reside in:
```text
docs/blog/posts/YYYY-MM-DD-<slug>.md
```
* Example: `docs/blog/posts/2026-11-03-zero-gradient-model-weight-poisoning-wsp.md`

### Frontmatter Schema
Every blog post begins with YAML frontmatter:
```yaml
---
draft: false
date: YYYY-MM-DD
slug: <kebab-case-slug>
authors:
  - felipe
categories:
  - AI Security
  - Research
---
```
* **draft**: `false` for published posts, `true` for work-in-progress drafts.
* **date**: ISO date matching the filename prefix (`YYYY-MM-DD`).
* **slug**: URL slug matching the filename suffix.
* **authors**: Author key defined in `docs/blog/.authors.yml` (for example, `felipe`).
* **categories**: List of top-level tags (`AI Security`, `Research`, `Engineering`, `General`).

---

## 3. Post Structure and Excerpt Marker

Blog posts maintain a focused narrative progression from initial hook to hands-on reproduction links.

```markdown
---
draft: false
date: 2026-11-03
slug: example-slug
authors:
  - felipe
categories:
  - AI Security
---

# Title in NYT Headline Style

One or two punchy paragraphs setting up the hook, announcing the release or finding, and stating the practical significance.

<!-- more -->

## Subheading One in NYT Headline Style

Story background, paper origin, release context, or engineering challenge. State exact release dates, papers, and authors when referencing recent research.

## Subheading Two (Technical Execution / The Build)

Walk through how the tool, agent, or exploit works step-by-step:
1. First stage or setup.
2. Core mechanism or inspection.
3. Surgical action or implementation.
4. Measurable outcomes and test results.

## Subheading Three (Implications for Builders and Defenders)

Practical takeaways for engineers, startup teams, and security practitioners. Explain why conventional assumptions (such as file format safety or standard benchmarks) fail and what steps to take instead.

## Hands-On / Try It Yourself

Direct links to open-source repositories, runnable labs, and relevant threat catalog entries in Gurple.
```

### The Excerpt Delimiter
Always place `<!-- more -->` after the introductory hook. MkDocs Blog uses this delimiter to generate the summary card on `docs/blog/index.md` and the RSS/Atom feeds.

---

## 4. Cross-Linking Conventions

Blog posts connect directly to the broader catalog and external source repositories.

* **Link to Gurple Threat Catalog**: When discussing specific attack categories or threat variants, link using relative paths to the threat pages:
  ```markdown
  [Weight Poisoning](../../threats/model_tampering/weight_poisoning.md)
  ```
* **Link to External Repositories & Labs**: Provide bare or markdown links with full context:
  ```markdown
  [github.com/felipepenha/pi-weight-space-programming](https://github.com/felipepenha/pi-weight-space-programming/)
  ```

---

## 5. Math and Formula Rendering in Blog Posts

Pandoc converts markdown files into GFM during the build pipeline. In blog posts, complex inline LaTeX like `$\nabla_\theta L = 0$` or nested sub-equations can get transformed into backtick math artifacts (`$``\nabla...``$`).
* **Best Practice**: For standalone variables or simple inline equations, prefer clean, code-styled Unicode or backticks:
  * Use ``(`∇_θ L = 0`)`` instead of `($\nabla_\theta L = 0$)`.
  * Use `bfloat16`, `<0.0018%`, and `$d_{\text{model}} = 1024$`.

---

## 6. Verification and Build Workflow

When authoring or modifying a blog post, follow this quality check sequence:

1. **Audit Writing Style**:
   ```bash
   uv run python .agents/skills/audit-writing-style/scripts/audit_writing_style.py docs/blog/posts/<filename>.md
   ```
   Ensure the score is **100.0/100** with zero errors or warnings.

2. **Compile and Build Documentation**:
   ```bash
   make build
   ```
   Verify that Pandoc transforms the post into `processed/blog/posts/` and that `mkdocs build` finishes with exit code 0.

3. **Check HTML Output**:
   Verify that the rendered post HTML exists under `site/blog/YYYY/MM/DD/<slug>/index.html` and that headings, code blocks, and math characters render without formatting artifacts.
