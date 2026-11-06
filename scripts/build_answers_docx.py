"""Writes the answer to every peer-graded question directly under its question screenshot in the
assignment Word file (Doc1.docx): links for URL questions, saved command outputs for TEXT questions
and the screenshot for UPLOAD questions.

    python scripts/build_answers_docx.py <Doc1.docx> [--out <file.docx>]
"""
import argparse
import shutil
from pathlib import Path

from docx import Document
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent
REPO = 'https://github.com/jsowkw1/Django-React-Car-Dealership-Capstone'
BLOB = f'{REPO}/blob/main'
OUTPUTS = ROOT / 'submission' / 'outputs'
UPLOAD = ROOT / 'submission' / 'upload'

# (question number, type, value) in the order the questions appear in the form.
# Question 3 has no screenshot in the document; its answer is placed after Question 2.
ANSWERS = [
    (1, 'URL', f'{BLOB}/README.md'),
    (2, 'TEXT', 'django_server'),
    (3, 'URL', f'{BLOB}/server/frontend/static/About.html'),
    (4, 'URL', f'{BLOB}/server/frontend/static/Contact.html'),
    (5, 'TEXT', 'loginuser'),
    (6, 'TEXT', 'logoutuser'),
    (7, 'URL', f'{BLOB}/server/frontend/src/components/Register/Register.jsx'),
    (8, 'TEXT', 'getdealerreviews'),
    (9, 'TEXT', 'getalldealers'),
    (10, 'TEXT', 'getdealerbyid'),
    (11, 'TEXT', 'getdealersbyState'),
    (12, 'UPLOAD', 'admin_login.png'),
    (13, 'UPLOAD', 'admin_logout.png'),
    (14, 'TEXT', 'getallcarmakes'),
    (15, 'TEXT', 'analyzereview'),
    (16, 'UPLOAD', 'get_dealers.png'),
    (17, 'UPLOAD', 'get_dealers_loggedin.png'),
    (18, 'UPLOAD', 'dealersbystate.png'),
    (19, 'UPLOAD', 'dealer_id_reviews.png'),
    (20, 'UPLOAD', 'dealership_review_submission.png'),
    (21, 'UPLOAD', 'added_review.png'),
    (22, 'TEXT', 'CI-CD'),
    (23, 'TEXT', 'deploymentURL'),
    (24, 'UPLOAD', 'deployed_landingpage.png'),
    (25, 'UPLOAD', 'deployed_loggedin.png'),
    (26, 'UPLOAD', 'deployed_dealer_detail.png'),
    (27, 'UPLOAD', 'deployed_add_review.png'),
]
Q3_TEXT = ('Question 3 | URL — Task 3: Submit the public GitHub URL of the server/frontend/static/About.html file '
           'showing the updated "About Us" page with correct CSS links, images, team member names, roles, '
           'brief details, and email IDs.')

GREEN = RGBColor(0x0B, 0x6B, 0x3A)


def add_hyperlink(paragraph, url):
    rel = paragraph.part.relate_to(url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink',
                                   is_external=True)
    link = OxmlElement('w:hyperlink')
    link.set(qn('r:id'), rel)
    run = OxmlElement('w:r')
    props = OxmlElement('w:rPr')
    for tag, attr in (('w:color', '0563C1'), ('w:u', 'single')):
        el = OxmlElement(tag)
        el.set(qn('w:val'), attr)
        props.append(el)
    run.append(props)
    text = OxmlElement('w:t')
    text.text = url
    run.append(text)
    link.append(run)
    paragraph._p.append(link)


class Inserter:
    """Creates paragraphs at the end of the document and moves them after the current anchor."""

    def __init__(self, doc, anchor):
        self.doc = doc
        self.anchor = anchor

    def para(self, space_after=4):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.space_before = Pt(0)
        self.anchor.addnext(p._p)
        self.anchor = p._p
        return p

    def label(self, text):
        run = self.para(2).add_run(text)
        run.bold = True
        run.font.size = Pt(11)
        run.font.color.rgb = GREEN

    def note(self, text):
        run = self.para().add_run(text)
        run.italic = True
        run.font.size = Pt(9)

    def code(self, text):
        p = self.para(10)
        shade = OxmlElement('w:shd')
        shade.set(qn('w:val'), 'clear')
        shade.set(qn('w:color'), 'auto')
        shade.set(qn('w:fill'), 'F2F4F7')
        p._p.get_or_add_pPr().append(shade)
        lines = text.rstrip('\n').split('\n')
        for i, line in enumerate(lines):
            run = p.add_run(line)
            run.font.name = 'Consolas'
            run._r.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), 'Consolas')
            run.font.size = Pt(8)
            if i < len(lines) - 1:
                run.add_break(WD_BREAK.LINE)


def write_answer(ins, number, kind, value):
    ins.label(f'Answer to Question {number} ({kind}):')
    if kind == 'URL':
        add_hyperlink(ins.para(10), value)
    elif kind == 'TEXT':
        ins.note(f'Saved in file: submission/outputs/{value}  ({BLOB}/submission/outputs/{value})')
        ins.code((OUTPUTS / value).read_text(encoding='utf-8'))
    else:
        ins.note(f'File to upload: submission/upload/{value}')
        ins.para(10).add_run().add_picture(str(UPLOAD / value), width=Inches(6.2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('docx')
    parser.add_argument('--out')
    args = parser.parse_args()
    out = Path(args.out or args.docx)
    if out == Path(args.docx):
        backup = Path(args.docx).with_name(Path(args.docx).stem + '_original.docx')
        if not backup.exists():
            shutil.copy(args.docx, backup)
        source = backup  # always rebuild from the untouched original
    else:
        source = Path(args.docx)

    doc = Document(str(source))
    # The question screenshots are runs inside a single paragraph: give each its own paragraph.
    question_paras = []
    for p in [p for p in doc.paragraphs if 'graphicData' in p._p.xml]:
        anchor = p._p
        for run in [r for r in p._p.findall(qn('w:r')) if r.find('.//' + qn('w:drawing')) is not None]:
            for stale in run.findall(qn('w:lastRenderedPageBreak')):
                run.remove(stale)
            new_p = OxmlElement('w:p')
            new_p.append(run)
            anchor.addnext(new_p)
            anchor = new_p
            question_paras.append(new_p)
        if not p.text.strip() and p._p.find('.//' + qn('w:drawing')) is None:
            p._p.getparent().remove(p._p)
    answers = [a for a in ANSWERS if a[0] != 3]
    assert len(question_paras) == len(answers), (len(question_paras), len(answers))

    for p, (number, kind, value) in zip(question_paras, answers):
        ins = Inserter(doc, p)
        write_answer(ins, number, kind, value)
        if number == 2:  # Question 3 is missing from the screenshots: add its text and answer here
            q3 = ins.para(2).add_run(Q3_TEXT)
            q3.bold = True
            q3.font.size = Pt(11)
            write_answer(ins, 3, 'URL', ANSWERS[2][2])
        page_break = ins.para(0)
        page_break.add_run().add_break(WD_BREAK.PAGE)

    doc.save(str(out))
    print('saved', out)


if __name__ == '__main__':
    main()
