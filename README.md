# BambooHR Resume Review

A Python application that pulls resumes from BambooHR's Applicant Tracking System and uses Claude to review them against job requirements defined in a markdown file.

## Setup

1. Clone the repository and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy the environment template and configure your credentials:
   ```bash
   cp .env.example .env
   ```

3. Fill in your `.env` file:
   - `BAMBOOHR_DOMAIN` - Your BambooHR subdomain (e.g., "mycompany" from mycompany.bamboohr.com)
   - `BAMBOOHR_API_KEY` - Generate from BambooHR: User menu → API Keys
   - `ANTHROPIC_API_KEY` - Your Anthropic API key

4. Edit `job_requirements.md` with your job requirements

## Usage

```bash
python main.py
```

The application will:
1. Fetch all applications from BambooHR (optionally filtered by `JOB_ID`)
2. Download and extract text from resume PDFs
3. Send each resume to Claude for evaluation against your requirements
4. Output a review with match score, strengths, gaps, and recommendation

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `BAMBOOHR_DOMAIN` | Yes | Your BambooHR subdomain |
| `BAMBOOHR_API_KEY` | Yes | BambooHR API key |
| `ANTHROPIC_API_KEY` | Yes | Anthropic API key |
| `JOB_ID` | No | Filter applications by job ID |
| `REQUIREMENTS_FILE` | No | Path to requirements file (default: `job_requirements.md`) |

## Requirements File

Edit `job_requirements.md` to define what you're looking for in candidates. The LLM will evaluate resumes against these criteria.

## License

MIT License - see [LICENSE](LICENSE) for details.
