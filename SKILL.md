---
name: maths-assessment-review
description: Create or revise maths assessment review lessons for SMART Notebook, using an assessment paper, question-level analysis (QLA), and any mark scheme or supplied review questions. Use for AW2-style review packs, test corrections with matched questions, and "same format" review lessons for another year group or class.
---

# Maths Assessment Review

## Choose the questions

- Read the current assessment paper and any supplied mark scheme, review questions and QLA. Accept a pasted table or spreadsheet. Match the QLA to the paper by number, subpart, topic and maximum marks. If numbering differs, use the topic and actual question to establish the match. Distinguish a zero score from missing marks. Check questionable totals against the mark limits and supplied averages before using them.
- Prioritise questions with a class average above zero and below full marks. When individual marks are available, favour questions where several students earned part marks. Look at the subparts too: a low-scoring final step can make a question valuable even when earlier parts went well. Balance the skills across the lesson. Use about eight pairs by default and adjust to the available evidence, class and lesson.
- Keep the selected originals faithful to the paper. Retain the actual numbers, notation, domain, task, relevant givens, diagram labels and marks. Reflow text or redraw diagrams for projection. Verify formulas and diagrams visually when PDF extraction or Word equation objects lose signs, powers, fractions or labels.
- Pair each original with a question that uses the same method at comparable difficulty. Prefer a suitable question in the supplied review document. Check its maths, wording and diagram independently. Write a new equivalent when a close match is unavailable. Keep student-level marks and identifiers out of the lesson PDF.

## Build the widescreen lesson

- Use a large-text, 16:9 landscape PDF for SMART Notebook. Default to 960 × 540 pt, 22–28 pt question text, wide margins and generous unruled working space. Use a light background, high contrast and consistent marks and page numbers. For a long question, use the width to put the diagram or givens beside the subparts and keep all of the question on one page.
- Open with a five-minute starter of four short prerequisite or retrieval questions on one page, arranged in a 2 × 2 grid. Align the questions to the class and upcoming review.
- Put one numbered test question on a page and its matching practice question on the very next page. Keep subparts together and label the original question number on both pages. Use the paper's order by default.
- End with five additional mixed questions on one page. Revisit the weaker skills and keep these questions short enough for working space. Honour any later instructions for a different layout, count, level or answer format.
- Solve all new questions and check the originals against the mark scheme where available. Render and inspect the PDF. Verify page order, the starter grid, the five final questions, notation, diagram accuracy, visible marks and margins.
- Deliver the PDF using the usual file-saving workflow. Give the starter answers in the reply for quick marking. Keep the projected pages student-facing. Provide worked answers or another answer artifact when requested, using the current contents of the lesson.

## Optional PDF layout helper

Use [scripts/review_pdf.py](scripts/review_pdf.py) to reuse the widescreen page design, text and equation sizing, starter grid and mixed-practice columns. It imports ReportLab and Matplotlib. Use the workspace's bundled Python when available. Write a small builder for the current questions and import the helper by adding its scripts directory to the Python import path. Each question in the starter or closing page is a list of lines. A line is a string or a tuple of text and Math fragments. Math fragments use Matplotlib's LaTeX-style syntax without dollar delimiters. Put longer or diagram-heavy questions on a custom page using the canvas and line methods.

~~~python
from review_pdf import Math, ReviewPDF

pdf = ReviewPDF("Y7_AW2_Review_Lesson.pdf", "Year 7", "AW2", pages=18)
# pdf.starter(starter_questions)
pdf.page("Solving equations", "Original question 12")
pdf.line(390, "Solve   ", Math("2x=24"), label="(a)", points=1)
# Add the rest of the question, its matching page and the other pairs.
# pdf.mixed_practice(final_questions)
# pdf.save()
~~~
