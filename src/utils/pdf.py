import logging

import markdown_pdf

LOGGER = logging.getLogger(__name__)


def md_to_pdf(content: str, out_path: str) -> None:
    pdf = markdown_pdf.MarkdownPdf()
    pdf.add_section(markdown_pdf.Section(content))
    pdf.save(out_path)
