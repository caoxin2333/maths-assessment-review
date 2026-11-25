# Maths Assessment Review

An agent skill for maths teachers. It turns an assessment paper and class question-level analysis (QLA) into a large-text, 16:9 PDF for projection in SMART Notebook.

The pack opens with a four-question starter in a 2 × 2 grid. The skill picks assessment questions where the class has room to improve, pairs each original with a similar question on the next page, and closes with five mixed practice questions. Pages include blank working space.

## Install in Codex

Run this from the project where you want to use the skill.

```sh
git clone https://github.com/caoxin2333/maths-assessment-review.git .agents/skills/maths-assessment-review
```

For use across projects, put the repository in `~/.agents/skills/maths-assessment-review` instead. Start a new Codex session, then invoke `$maths-assessment-review`. [Codex skills documentation](https://developers.openai.com/codex/skills)

## Use the skill

Provide the test paper, class averages or anonymised question-level marks, and any mark scheme or existing review questions you want to use.

> Use Maths Assessment Review for this Year 9 paper and class QLA. Produce a widescreen review lesson and give me the starter answers separately.

If your ChatGPT account has skill uploads enabled, open **Plugins → Skills → Create → Upload from your computer** and upload a skill bundle containing `SKILL.md` and `scripts/`. [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)

## Repository contents

- [SKILL.md](SKILL.md) contains the question-selection, lesson-building and verification workflow.
- [scripts/review_pdf.py](scripts/review_pdf.py) provides the optional widescreen PDF layout. It uses Python, ReportLab and Matplotlib.
- [agents/openai.yaml](agents/openai.yaml) provides the skill name and example prompt shown in Codex.
