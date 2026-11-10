from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


def generate_report(summary, keywords, gaps):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "ResearchSummarize AI Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            "<b>Summary:</b><br/>" +
            escape(summary).replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            "<b>Important Keywords:</b><br/>" +
            escape(", ".join(keywords)),
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            "<b>Research Gap Indicators:</b><br/>" +
            escape(", ".join(gaps)),
            styles["BodyText"]
        )
    )

    doc.build(content)

    buffer.seek(0)

    return buffer.getvalue()
 
