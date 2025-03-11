import logging

import markdown_pdf
import mistralai

LOGGER = logging.getLogger(__name__)


def save_cover_letter(content: str, out_path: str) -> None:
    pdf = markdown_pdf.MarkdownPdf()
    pdf.add_section(markdown_pdf.Section(content))
    pdf.save(out_path)


def generate_cover_letter(
        mistral_client: mistralai.Mistral,
        job_description: str,
        resume_md: str,
        mistral_model: str ="mistral-large-latest"
) -> str:
    chat_response = mistral_client.chat.complete(
        model=mistral_model,
        messages=[
            {
                "role": "system",
                "content": "You are a writer hired to craft cover letters for a job applicant. You have a copy of the applicant's resume and a template structure for a cover letter. Given a decription of a job, you will write a cover letter for the applicant. The cover letter must be no longer than one page and must be ready for submission as-is without requiring any changes by the applicant."
            },
            {
                "role": "system",
                "content": "The Cover Letter Template:\n\nDear Hiring Manager of <COMPANY_NAME>,\n\n<CONTENT>\n\nSincerely,\n\n<APPLICANT_NAME>\n\n<APPLICANT_EMAIL>\n\n<APPLICANT_PROFILE_URL>\n\n<APPLICANT_LOCATION>\n"
            },
            {
                "role": "system",
                "content": f"The Applicant's Resume:\n\n{resume_md}"
            },
            {
                "role": "user",
                "content": f"The Job Description:\n\n{job_description}",
            },
        ]
    )
    logging.debug("%s", chat_response.choices[0].message.content)
    return chat_response.choices[0].message.content
