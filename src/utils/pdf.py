import logging
import pathlib

import markdown_pdf

LOGGER = logging.getLogger(__name__)


def md_to_pdf(
    content: str,
    out_path: str | pathlib.Path,
    css: str | None = None
) -> None:
    pdf = markdown_pdf.MarkdownPdf()
    pdf.add_section(markdown_pdf.Section(content), user_css=css)
    pdf.save(out_path)
