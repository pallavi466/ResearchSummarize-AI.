 
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from xml.sax.saxutils import escape


def generate_report(filename, summary, keywords, gaps):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    # Report Title
    content.append(
        Paragraph(
            "ResearchSummarize AI Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 20))

    # Summary
    content.append(
        Paragraph(
            "<b>Summary:</b><br/>" +
            escape(summary).replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 20))

    # Keywords
    content.append(
        Paragraph(
            "<b>Important Keywords:</b><br/>" +
            escape(", ".join(keywords)),
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 20))

    # Research Gaps
    content.append(
        Paragraph(
            "<b>Research Gap Indicators:</b><br/>" +
            escape(", ".join(gaps)),
            styles["BodyText"]
        )
    )

    # Generate PDF
    doc.build(content)
