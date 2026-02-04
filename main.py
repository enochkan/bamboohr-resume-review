"""Main application for BambooHR resume review."""

import os
import io
from dotenv import load_dotenv
from PyPDF2 import PdfReader

from bamboohr_client import BambooHRClient
from llm_reviewer import ResumeReviewer


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text content from PDF bytes."""
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def main():
    load_dotenv()

    # Initialize clients
    bamboo_client = BambooHRClient(
        company_domain=os.getenv("BAMBOOHR_DOMAIN"),
        api_key=os.getenv("BAMBOOHR_API_KEY"),
    )
    reviewer = ResumeReviewer(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Load job requirements
    requirements_path = os.getenv("REQUIREMENTS_FILE", "job_requirements.md")
    requirements = reviewer.load_requirements(requirements_path)

    # Optional: filter by job ID
    job_id = os.getenv("JOB_ID")
    job_id = int(job_id) if job_id else None

    # Fetch applications
    print("Fetching applications from BambooHR...")
    applications = bamboo_client.get_applications(job_id=job_id)
    print(f"Found {len(applications)} applications")

    reviews = []
    for app in applications:
        app_id = app.get("id")
        print(f"\nProcessing application {app_id}...")

        # Get application details
        details = bamboo_client.get_application_details(app_id)
        applicant_name = f"{details.get('firstName', '')} {details.get('lastName', '')}".strip()

        # Extract resume text
        resume_text = ""

        # Check for resume file in application
        resume_file = details.get("resumeFile") or details.get("resume")
        if resume_file and isinstance(resume_file, dict):
            file_id = resume_file.get("id") or resume_file.get("fileId")
            if file_id:
                try:
                    pdf_bytes = bamboo_client.get_resume_file(app_id, file_id)
                    resume_text = extract_text_from_pdf(pdf_bytes)
                except Exception as e:
                    print(f"  Could not download resume: {e}")

        # Fallback to any text fields in application
        if not resume_text:
            resume_text = details.get("coverLetter", "") or details.get("resumeText", "")

        if not resume_text:
            print(f"  No resume found for {applicant_name}, skipping...")
            continue

        # Review the resume
        print(f"  Reviewing resume for {applicant_name}...")
        review = reviewer.review_resume(resume_text, requirements, applicant_name)
        reviews.append(review)

        print(f"  Review complete for {applicant_name}")
        print("-" * 50)
        print(review["review"])
        print("-" * 50)

    # Summary
    print(f"\n{'='*50}")
    print(f"Reviewed {len(reviews)} resumes")
    for r in reviews:
        print(f"  - {r['applicant_name']}")


if __name__ == "__main__":
    main()
