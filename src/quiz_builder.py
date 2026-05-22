"""Quiz builder — generates offline self-contained HTML quiz from flashcard data."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import List

from .llm_client import LLMClient
from .flashcard_builder import FlashcardRow


class QuizError(Exception):
    """Raised when quiz generation fails validation."""


@dataclass
class QuizQuestion:
    question_type: str   # "translation" | "fill-in-the-blank"
    prompt: str          # question text shown to user
    options: List[str]   # exactly 4 options
    correct_index: int   # index into options (0–3)


QUIZ_PROMPT = """You are an Italian language teacher creating a multiple-choice quiz for an A1-level beginner.

Flashcard data (JSON):
{flashcard_json}

Italian reading passage:
{passage_text}

Generate exactly 12 multiple-choice questions.
- At least 6 must be Italian-to-English TRANSLATION questions (show an Italian word/phrase, ask for the English meaning)
- At least 4 must be FILL-IN-THE-BLANK sentence completion questions (show a sentence with a blank, ask which word fits)
- Every question must have exactly 4 answer options
- Use only vocabulary from the flashcards or passage
- Do NOT use grammar terminology
- Make wrong answers plausible but clearly incorrect to a learner
- correct_index is 0-based (0, 1, 2, or 3)

Return JSON only:
{{
  "questions": [
    {{
      "question_type": "translation",
      "prompt": "What does 'mangiare' mean?",
      "options": ["to drink", "to eat", "to sleep", "to walk"],
      "correct_index": 1
    }},
    {{
      "question_type": "fill-in-the-blank",
      "prompt": "Io ___ la pizza ogni giorno.",
      "options": ["bevo", "mangio", "dormo", "cammino"],
      "correct_index": 1
    }}
  ]
}}"""


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{week_title} — Italian Quiz</title>
<style>
  :root {{
    --bg: #f0f4f8;
    --card: #ffffff;
    --primary: #4f46e5;
    --primary-hover: #4338ca;
    --correct: #16a34a;
    --correct-bg: #dcfce7;
    --incorrect: #dc2626;
    --incorrect-bg: #fee2e2;
    --reveal: #d97706;
    --reveal-bg: #fef3c7;
    --text: #1e293b;
    --muted: #64748b;
    --border: #e2e8f0;
    --radius: 12px;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
  }}
  .container {{ max-width: 640px; width: 100%; }}
  h1 {{ font-size: 1.4rem; font-weight: 700; margin-bottom: 4px; color: var(--primary); }}
  .subtitle {{ font-size: 0.9rem; color: var(--muted); margin-bottom: 24px; }}
  .progress-bar-wrap {{
    background: var(--border);
    border-radius: 99px;
    height: 8px;
    margin-bottom: 24px;
    overflow: hidden;
  }}
  .progress-bar {{
    height: 100%;
    background: var(--primary);
    border-radius: 99px;
    transition: width 0.3s ease;
  }}
  .card {{
    background: var(--card);
    border-radius: var(--radius);
    padding: 28px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    margin-bottom: 16px;
  }}
  .question-counter {{ font-size: 0.8rem; color: var(--muted); margin-bottom: 8px; }}
  .question-text {{ font-size: 1.15rem; font-weight: 600; margin-bottom: 20px; line-height: 1.5; }}
  .options {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
  .option-btn {{
    background: var(--bg);
    border: 2px solid var(--border);
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 0.95rem;
    cursor: pointer;
    text-align: left;
    transition: border-color 0.15s, background 0.15s;
    line-height: 1.4;
  }}
  .option-btn:hover:not(:disabled) {{ border-color: var(--primary); background: #eef2ff; }}
  .option-btn.correct {{ background: var(--correct-bg); border-color: var(--correct); color: var(--correct); font-weight: 600; }}
  .option-btn.incorrect {{ background: var(--incorrect-bg); border-color: var(--incorrect); color: var(--incorrect); }}
  .option-btn:disabled {{ cursor: default; }}
  .feedback {{
    margin-top: 16px;
    padding: 12px 16px;
    border-radius: 8px;
    font-size: 0.95rem;
    display: none;
  }}
  .feedback.correct {{ background: var(--correct-bg); color: var(--correct); }}
  .feedback.incorrect {{ background: var(--incorrect-bg); color: var(--incorrect); }}
  .feedback.reveal {{ background: var(--reveal-bg); color: var(--reveal); margin-top: 8px; }}
  .next-btn {{
    display: none;
    margin-top: 16px;
    background: var(--primary);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    width: 100%;
    transition: background 0.15s;
  }}
  .next-btn:hover {{ background: var(--primary-hover); }}
  .score-screen {{
    display: none;
    text-align: center;
    padding: 40px 28px;
  }}
  .score-emoji {{ font-size: 3rem; margin-bottom: 16px; }}
  .score-number {{ font-size: 2.5rem; font-weight: 800; color: var(--primary); }}
  .score-label {{ font-size: 1rem; color: var(--muted); margin-top: 4px; margin-bottom: 24px; }}
  .score-bar-wrap {{ background: var(--border); border-radius: 99px; height: 12px; margin-bottom: 24px; overflow: hidden; }}
  .score-bar {{ height: 100%; border-radius: 99px; background: var(--primary); transition: width 1s ease; }}
  .restart-btn {{
    background: var(--primary);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 32px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
  }}
  .restart-btn:hover {{ background: var(--primary-hover); }}
  @media (max-width: 480px) {{
    .options {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>
<div class="container">
  <h1>🇮🇹 {week_title}</h1>
  <p class="subtitle">Italian vocabulary quiz — A1 level</p>
  <div class="progress-bar-wrap">
    <div class="progress-bar" id="progressBar" style="width:0%"></div>
  </div>

  <div class="card" id="quizCard">
    <div class="question-counter" id="questionCounter"></div>
    <div class="question-text" id="questionText"></div>
    <div class="options" id="optionsGrid"></div>
    <div class="feedback" id="feedbackCorrect">✅ Correct!</div>
    <div class="feedback" id="feedbackIncorrect">❌ Incorrect.</div>
    <div class="feedback reveal" id="feedbackReveal"></div>
    <button class="next-btn" id="nextBtn" onclick="nextQuestion()">Next →</button>
  </div>

  <div class="card score-screen" id="scoreScreen">
    <div class="score-emoji" id="scoreEmoji"></div>
    <div class="score-number" id="scoreNumber"></div>
    <div class="score-label" id="scoreLabel"></div>
    <div class="score-bar-wrap"><div class="score-bar" id="scoreBar" style="width:0%"></div></div>
    <button class="restart-btn" onclick="restartQuiz()">Try Again</button>
  </div>
</div>

<script>
const QUESTIONS = {questions_json};

let shuffled = [];
let current = 0;
let score = 0;

function shuffle(arr) {{
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {{
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }}
  return a;
}}

function prepareQuestions() {{
  shuffled = shuffle(QUESTIONS).map(q => {{
    // Shuffle options while tracking correct answer
    const indexed = q.options.map((opt, i) => ({{ opt, isCorrect: i === q.correct_index }}));
    const shuffledOpts = shuffle(indexed);
    return {{
      question_type: q.question_type,
      prompt: q.prompt,
      options: shuffledOpts.map(o => o.opt),
      correct_index: shuffledOpts.findIndex(o => o.isCorrect)
    }};
  }});
}}

function renderQuestion() {{
  const q = shuffled[current];
  const total = shuffled.length;

  document.getElementById('progressBar').style.width = (current / total * 100) + '%';
  document.getElementById('questionCounter').textContent = 'Question ' + (current + 1) + ' of ' + total;
  document.getElementById('questionText').textContent = q.prompt;

  const grid = document.getElementById('optionsGrid');
  grid.innerHTML = '';
  q.options.forEach((opt, i) => {{
    const btn = document.createElement('button');
    btn.className = 'option-btn';
    btn.textContent = opt;
    btn.onclick = () => selectAnswer(i);
    grid.appendChild(btn);
  }});

  document.getElementById('feedbackCorrect').style.display = 'none';
  document.getElementById('feedbackIncorrect').style.display = 'none';
  document.getElementById('feedbackReveal').style.display = 'none';
  document.getElementById('nextBtn').style.display = 'none';
}}

function selectAnswer(selectedIndex) {{
  const q = shuffled[current];
  const buttons = document.querySelectorAll('.option-btn');

  // Disable all buttons immediately
  buttons.forEach(b => b.disabled = true);

  const isCorrect = selectedIndex === q.correct_index;

  if (isCorrect) {{
    score++;
    buttons[selectedIndex].classList.add('correct');
    document.getElementById('feedbackCorrect').style.display = 'block';
    // Auto-advance after 1 second on correct
    setTimeout(nextQuestion, 1000);
  }} else {{
    buttons[selectedIndex].classList.add('incorrect');
    buttons[q.correct_index].classList.add('correct');
    document.getElementById('feedbackIncorrect').style.display = 'block';
    const reveal = document.getElementById('feedbackReveal');
    reveal.textContent = 'The correct answer is: ' + q.options[q.correct_index];
    reveal.style.display = 'block';
    document.getElementById('nextBtn').style.display = 'block';
  }}
}}

function nextQuestion() {{
  current++;
  if (current >= shuffled.length) {{
    showScore();
  }} else {{
    renderQuestion();
  }}
}}

function showScore() {{
  document.getElementById('quizCard').style.display = 'none';
  const screen = document.getElementById('scoreScreen');
  screen.style.display = 'block';

  const total = shuffled.length;
  const pct = Math.round(score / total * 100);

  let emoji = '😊';
  if (pct >= 90) emoji = '🏆';
  else if (pct >= 70) emoji = '⭐';
  else if (pct >= 50) emoji = '👍';
  else emoji = '📚';

  document.getElementById('scoreEmoji').textContent = emoji;
  document.getElementById('scoreNumber').textContent = score + ' / ' + total;
  document.getElementById('scoreLabel').textContent = pct + '% correct';
  document.getElementById('progressBar').style.width = '100%';

  setTimeout(() => {{
    document.getElementById('scoreBar').style.width = pct + '%';
  }}, 100);
}}

function restartQuiz() {{
  current = 0;
  score = 0;
  prepareQuestions();
  document.getElementById('scoreScreen').style.display = 'none';
  document.getElementById('quizCard').style.display = 'block';
  renderQuestion();
}}

// Init
prepareQuestions();
renderQuestion();
</script>
</body>
</html>"""


class QuizBuilder:
    """Generates quiz questions via LLM and renders a self-contained HTML quiz."""

    def __init__(self, llm: LLMClient) -> None:
        self._llm = llm

    def build_questions(
        self, flashcard_rows: List[FlashcardRow], passage_text: str
    ) -> List[QuizQuestion]:
        """Call LLM to generate quiz questions. Validates count and structure."""
        flashcard_json = json.dumps(
            [
                {
                    "italian_form": r.italian_form,
                    "english_translation": r.english_translation,
                    "source_word": r.source_word,
                    "word_type": r.word_type,
                    "tense_label": r.tense_label,
                    "italian_example": r.italian_example,
                }
                for r in flashcard_rows
            ],
            ensure_ascii=False,
            indent=2,
        )

        prompt = QUIZ_PROMPT.format(
            flashcard_json=flashcard_json,
            passage_text=passage_text,
        )

        data = self._llm.call(prompt)
        raw_questions = data.get("questions", [])

        if len(raw_questions) < 10:
            raise QuizError(
                f"Quiz generation returned {len(raw_questions)} questions. Expected at least 10."
            )

        questions = []
        for i, q in enumerate(raw_questions):
            opts = q.get("options", [])
            if len(opts) != 4:
                raise QuizError(
                    f"Question {i+1} has {len(opts)} options. Expected exactly 4."
                )
            questions.append(
                QuizQuestion(
                    question_type=str(q.get("question_type", "translation")),
                    prompt=str(q.get("prompt", "")),
                    options=[str(o) for o in opts],
                    correct_index=int(q.get("correct_index", 0)),
                )
            )

        # Validate at least 2 question types
        types = {q.question_type for q in questions}
        if len(types) < 2:
            raise QuizError(
                f"Quiz must include at least 2 question types. Got: {types}"
            )

        return questions

    def to_html(self, questions: List[QuizQuestion], week_title: str) -> str:
        """Render questions into a fully self-contained offline HTML file."""
        questions_data = [
            {
                "question_type": q.question_type,
                "prompt": q.prompt,
                "options": q.options,
                "correct_index": q.correct_index,
            }
            for q in questions
        ]
        questions_json = json.dumps(questions_data, ensure_ascii=False)

        return HTML_TEMPLATE.format(
            week_title=week_title,
            questions_json=questions_json,
        )
