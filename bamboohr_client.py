"""BambooHR API client for fetching applicant data and resumes."""

import requests
from requests.auth import HTTPBasicAuth


class BambooHRClient:
    def __init__(self, company_domain: str, api_key: str):
        self.base_url = f"https://{company_domain}.bamboohr.com/api/gateway.php/{company_domain}/v1"
        self.auth = HTTPBasicAuth(api_key, "x")
        self.headers = {"Accept": "application/json"}

    def get_applications(self, job_id: int | None = None, status_id: int | None = None) -> list[dict]:
        """Fetch job applications with optional filters."""
        url = f"{self.base_url}/applicant_tracking/applications"
        params = {}
        if job_id:
            params["jobId"] = job_id
        if status_id:
            params["statusId"] = status_id

        response = requests.get(url, auth=self.auth, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json().get("applications", [])

    def get_application_details(self, application_id: int) -> dict:
        """Fetch detailed information for a specific application."""
        url = f"{self.base_url}/applicant_tracking/applications/{application_id}"
        response = requests.get(url, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_resume_file(self, application_id: int, file_id: int) -> bytes:
        """Download a resume file for an application."""
        url = f"{self.base_url}/applicant_tracking/applications/{application_id}/files/{file_id}"
        response = requests.get(url, auth=self.auth)
        response.raise_for_status()
        return response.content

    def get_job_summaries(self) -> list[dict]:
        """Fetch all job openings."""
        url = f"{self.base_url}/applicant_tracking/jobs"
        response = requests.get(url, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        return response.json()
