"""LLM-based resume reviewer using Anthropic's Claude API."""

import anthropic
from pathlib import Path


class ResumeReviewer:
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def load_requirements(self, requirements_path: str) -> str:
        """Load job requirements from a markdown file."""
        return Path(requirements_path).read_text()

    def review_resume(self, resume_text: str, requirements: str, applicant_name: str = "Unknown") -> dict:
        """Review a resume against job requirements using Claude."""
        prompt = f"""You are a hiring assistant reviewing resumes against specific job requirements.

## Job Requirements
{requirements}

## Resume
{resume_text}

Please evaluate this resume against the requirements and provide:
1. **Match Score**: A score from 1-10 indicating how well the candidate matches
2. **Strengths**: Key qualifications that align with requirements
3. **Gaps**: Missing skills or experience
4. **Recommendation**: PROCEED, MAYBE, or PASS with brief justification

Format your response as structured output."""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        return {
            "applicant_name": applicant_name,
            "review": message.content[0].text,
        }
