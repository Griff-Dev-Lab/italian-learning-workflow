# Tech Stack

## Language & Runtime
- Python 3.10+
- macOS (primary platform)

## Dependencies (`requirements.txt`)
- `openai>=1.0.0` — LLM API client (used for Ollama, OpenAI, and Gemini via OpenAI-compatible interface)
- `pyyaml>=6.0` — config and theme file parsing
- `python-dotenv>=1.0` — loads `OPENAI_API_KEY` from `.env`

## AI / LLM
- Default: Ollama running locally (`http://localhost:11434/v1`) with the `mistral` model
- The OpenAI SDK is used for all providers — Ollama, OpenAI, and Gemini all expose an OpenAI-compatible API
- Provider is switched by editing `config.yaml` (model name + base URL)
- `OPENAI_API_KEY` is always required; for Ollama it is set to the literal string `ollama`

## Configuration Files
- `config.yaml` — LLM provider, model, base URL, output directory, max retries
- `themes.yaml` — theme definitions (id, label, description); no code changes needed to add themes
- `.env` — API key (copied from `.env.example`)

## Common Commands

```bash
# Run the workflow for a theme
python run.py --theme food

# Run with a custom output directory
python run.py --theme travel --output ./my_output

# List all available themes
python run.py --list-themes

# First-time setup
cp .env.example .env
pip install -r requirements.txt

# Start Ollama (must be running before executing the workflow)
ollama serve

# Pull the default model (one-time)
ollama pull mistral
```

## No Build Step
There is no compilation, bundling, or build process. The project runs directly with `python run.py`.

## No Test Framework
There is currently no automated test suite in the project.
