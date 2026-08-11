# Course Hub

Free, self-paced technical courses as plain static HTML.
No build step, no framework, no tracking - open a lesson in a browser and start reading.

**Live site:** http://aqi-course-hub-149536460784.s3-website.ap-south-2.amazonaws.com/

## Courses

| Course | Lessons | What it covers |
|---|---|---|
| [`llm-papers-course/`](llm-papers-course/index.html) | 38 | The LLM research canon, in teaching order: attention, the GPT and LLaMA lines, scaling laws, positional encodings, FlashAttention, alignment (RLHF, DPO, GRPO), efficient fine-tuning, reasoning, and mixture-of-experts. |
| [`llm-inference-course/`](llm-inference-course/index.html) | 16 | Running LLMs in production: vLLM and SGLang, continuous batching, KV-cache management, speculative decoding, quantization, routing, Kubernetes, observability, load testing, and unit economics. |

Every lesson is one idea, mental model first, with active-recall quizzes built in. Retrieval practice beats re-reading, so the quizzes are the point rather than decoration.

## Reading a course

There is no server and nothing to install.

```bash
git clone git@github.com:saurav-k/course-hub.git
cd course-hub
open index.html                       # macOS
xdg-open index.html                   # Linux
```

Or just use the live site above.

## Repository layout

```
index.html                    the hub landing page; every course is a card here
assets/                       shared CSS and JS for the landing page only
scripts/validate_site.py      structure and link checker that gates every pull request
.github/workflows/            validate on pull request, publish on merge to main

<course-name>/
  index.html                  the course map; every lesson is linked from here
  assets/                     CSS and JS owned by that course
  lessons/NNNN-kebab.html     the lessons, zero-padded and in teaching order
  reference/*.html            print-friendly cheat sheets and glossaries
  learning-records/*.md       progress notes; never published to the site
  MISSION.md                  why the course exists and what is out of scope
  NOTES.md                    teaching style and working notes
  RESOURCES.md                the high-trust sources the lessons cite
  BUILDER-SPEC.md             the authoring spec for that course
```

Courses are siblings under one bucket root, so cross-course links are relative - `../../llm-papers-course/index.html`. Absolute paths break the site.

## How publishing works

`main` is protected. Nobody pushes to it and nobody deploys from a laptop.

```
branch -> pull request -> checks pass -> review -> merge to main -> GitHub Actions syncs to S3
```

- [`.github/workflows/validate.yml`](.github/workflows/validate.yml) runs on every pull request: the structure and link checker.
- [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) runs on merge to `main`: it re-runs validation, assumes a scoped AWS role over OpenID Connect, and mirrors the hub into the bucket.

There are no long-lived AWS keys in this repository, and no deploy script or bucket configuration either. The destination lives in the repository's Actions settings, so contributors need no AWS access, no credentials, and no setup. The workflow mints a short-lived token per run, and the role it assumes trusts only this repository's `main` branch and can write only that one bucket.

## Contributing

Contributions are welcome - a typo fix, a corrected explanation, a new lesson, or a whole new course.

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) first. The short version:

```bash
git checkout -b lesson/my-new-lesson
# write the lesson, register it in the course index.html
python3 scripts/validate_site.py
# open a pull request into main
```

Coding agents: read [`AGENTS.md`](AGENTS.md) as well. It is the contract for automated contributors, and `CLAUDE.md` points at the same file.

By taking part you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).

## Licence

Dual-licensed so both halves are covered properly:

- **Code** - `scripts/`, the workflows, and the course CSS and JS - is under the [MIT License](LICENSE).
- **Course content** - lessons, reference sheets, glossaries, and prose - is under [CC BY 4.0](LICENSE-CONTENT).

Both let anyone use, modify, redistribute, and build on this work, commercially included. The content licence asks only for attribution.

Lessons summarise published papers and vendor documentation. Those upstream works stay under their own licences and belong to their authors.
