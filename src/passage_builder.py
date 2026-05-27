"""Passage builder — generates structured example sentences for an Italian verb."""

from __future__ import annotations

from .llm_client import LLMClient
from .verb_conjugator import ConjugationData


class PassageError(Exception):
    """Raised when example sentence generation fails."""


SENTENCES_PROMPT = """You are an Italian language teacher creating example sentences for A1–A2 learners.

Verb: {infinitive}

Use exactly these conjugated forms — do not change them:
- Present (io):      {present_io}
- Present (tu):      {present_tu}
- Present (lui/lei): {present_lui_lei}
- Present (noi):     {present_noi}
- Present (voi):     {present_voi}
- Present (loro):    {present_loro}
- Past (io):         {past_io}
- Future (io):       {future_io}

Generate exactly 8 sentences using these exact templates. Choose appropriate objects that make semantic sense with "{infinitive}":

Templates:
1. Io {present_io} _____.
2. Tu {present_tu} _____.
3. Lui {present_lui_lei} _____.
4. Noi {present_noi} _____.
5. Voi {present_voi} _____.
6. Loro {present_loro} _____.
7. Ieri io {past_io} _____.
8. Domani io {future_io} _____.

Object selection rules:
- Choose simple A1-A2 level nouns that logically work with "{infinitive}"
- Always use the correct Italian definite article (il/la/l'/i/gli/le)
- Use common, everyday objects that native speakers would naturally use
- Avoid unusual or unnatural combinations
- Each object should be 1-3 words maximum (article + noun, e.g. "la pizza", "gli spaghetti")

Examples of good article usage:
- il (masc. sing): il libro, il pane, il treno
- la (fem. sing): la pizza, la casa, la macchina  
- l' (before vowel): l'acqua, l'auto, l'orologio
- i (masc. plural): i libri, i biscotti
- gli (masc. plural before vowel/s+cons): gli spaghetti, gli studenti
- le (fem. plural): le scarpe, le verdure

Rules:
- Use each template exactly once
- Fill each blank with ONE appropriate object (article + noun)
- Do not change the conjugated forms
- Do not add extra words beyond the template + object
- Write only the 8 completed sentences, numbered 1–8
- No translations, no labels, no extra text
"""

TRANSLATION_PROMPT = """Translate each of these Italian sentences into English.

Write only the 8 English translations, one per line, numbered 1–8. No extra text.

Italian sentences:
{italian_sentences}
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Example Sentences — {infinitive}</title>
<style>
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    max-width: 620px;
    margin: 60px auto;
    padding: 0 24px;
    background: #fafaf8;
    color: #1a1a1a;
    line-height: 1.7;
  }}
  h1 {{
    font-size: 1.4rem;
    font-weight: 700;
    color: #2d2d2d;
    margin-bottom: 4px;
  }}
  .subtitle {{
    font-size: 0.9rem;
    color: #888;
    margin-bottom: 36px;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
  }}
  thead th {{
    text-align: left;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: #aaa;
    padding: 0 12px 10px 0;
    border-bottom: 1px solid #e5e5e5;
  }}
  tbody tr {{
    border-bottom: 1px solid #f0f0f0;
  }}
  tbody tr:last-child {{
    border-bottom: none;
  }}
  td {{
    padding: 14px 12px 14px 0;
    vertical-align: top;
  }}
  .label {{
    font-size: 0.78rem;
    color: #aaa;
    white-space: nowrap;
    padding-right: 20px;
    padding-top: 16px;
  }}
  .italian {{
    font-size: 1.05rem;
    font-weight: 500;
    color: #1a1a1a;
  }}
  .english {{
    font-size: 0.92rem;
    color: #666;
    font-style: italic;
    margin-top: 3px;
  }}
</style>
</head>
<body>
  <h1>🇮🇹 {infinitive_title}</h1>
  <p class="subtitle">Example sentences · A1–A2 level</p>

  <table>
    <thead>
      <tr>
        <th>Tense</th>
        <th>Italian</th>
      </tr>
    </thead>
    <tbody>
      {rows}
    </tbody>
  </table>
</body>
</html>"""

ROW_TEMPLATE = """      <tr>
        <td class="label">{label}</td>
        <td>
          <div class="italian">{italian}</div>
          <div class="english">{english}</div>
        </td>
      </tr>"""


def _parse_numbered_lines(text: str) -> list[str]:
    """Extract lines from a numbered list (1. ... 2. ... etc.)."""
    lines = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        # Strip leading number and punctuation e.g. "1. " or "1) "
        if len(line) > 2 and line[0].isdigit() and line[1] in ".):":
            line = line[2:].strip()
        elif len(line) > 3 and line[0].isdigit() and line[1].isdigit() and line[2] in ".):":
            line = line[3:].strip()
        lines.append(line)
    return lines


class PassageBuilder:
    """Generates structured example sentences for a verb as a clean HTML file."""

    LABELS = [
        "present (io)",
        "present (tu)",
        "present (lui/lei)",
        "present (noi)",
        "present (voi)",
        "present (loro)",
        "past (io)",
        "future (io)",
    ]

    def __init__(self, llm: LLMClient) -> None:
        self._llm = llm

    def build(self, data: ConjugationData) -> str:
        """Generate an HTML example-sentences page. Returns the HTML string."""

        # Step 1: Generate Italian sentences
        it_prompt = SENTENCES_PROMPT.format(
            infinitive=data.infinitive,
            present_io=data.present_io,
            present_tu=data.present_tu,
            present_lui_lei=data.present_lui_lei,
            present_noi=data.present_noi,
            present_voi=data.present_voi,
            present_loro=data.present_loro,
            past_io=data.past_io,
            future_io=data.future_io,
        )
        italian_raw = self._llm.call_text(it_prompt).strip()
        italian_lines = _parse_numbered_lines(italian_raw)

        if len(italian_lines) < 8:
            raise PassageError(
                f"Expected 8 Italian sentences, got {len(italian_lines)}. "
                f"Raw output: {italian_raw!r}"
            )
        italian_lines = italian_lines[:8]

        # Step 2: Translate
        en_prompt = TRANSLATION_PROMPT.format(
            italian_sentences="\n".join(f"{i+1}. {s}" for i, s in enumerate(italian_lines))
        )
        english_raw = self._llm.call_text(en_prompt).strip()
        english_lines = _parse_numbered_lines(english_raw)

        # Pad translations if short
        while len(english_lines) < 8:
            english_lines.append("")

        # Step 3: Build HTML rows
        rows = []
        for i, (label, italian, english) in enumerate(
            zip(self.LABELS, italian_lines, english_lines)
        ):
            rows.append(ROW_TEMPLATE.format(
                label=label,
                italian=italian,
                english=english,
            ))

        print(f"      Generated {len(rows)} example sentences.")

        return HTML_TEMPLATE.format(
            infinitive=data.infinitive,
            infinitive_title=data.infinitive.capitalize(),
            rows="\n".join(rows),
        )
