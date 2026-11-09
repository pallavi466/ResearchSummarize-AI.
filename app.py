import os
import tempfile
import warnings
import streamlit as st

# Suppress Hugging Face transformers warnings across the app
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")

from modules.pdf_reader import extract_text
from modules.text_cleaner import clean_text
from modules.section_extractor import extract_sections
from modules.summarizer import summarize_text
from modules.keyword_extractor import extract_keywords
from modules.research_gap_detector import detect_research_gap
from modules.report_generator import generate_report

st.set_page_config(
    page_title="ResearchSummarize AI",
    layout="wide"
)
st.title("ResearchSummarize AI")

uploaded_file = st.file_uploader(
    "Upload Research Paper",
    type=["pdf"]
)

if uploaded_file:
    # Key optimization: Prevents reloading models every time a button is clicked
    file_key = f"{uploaded_file.name}_{uploaded_file.size}"

    if st.session_state.get("current_file") != file_key:
        
        temp_pdf_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
                temp_pdf_path = tmp_file.name

            text = extract_text(temp_pdf_path)
            cleaned_text = clean_text(text)

            st.success("PDF Successfully Processed")

            with st.spinner("Generating Summary..."):
                summary = summarize_text(cleaned_text)
                keywords = extract_keywords(cleaned_text)
                gaps = detect_research_gap(cleaned_text)
                sections = extract_sections(cleaned_text)

                # Process section summaries safely without triggering warnings on short texts
                section_summaries = {}
                if sections and isinstance(sections, dict):
                    for section, content in sections.items():
                        clean_content = content.strip()
                        # Only summarize sections that have enough body text (>150 characters)
                        if len(clean_content) > 150:
                            section_summaries[section] = summarize_text(clean_content[:3000])
                        elif len(clean_content) > 0:
                            section_summaries[section] = clean_content

                report_file = "generated_report.pdf"
                generate_report(
                    report_file,
                    summary,
                    keywords,
                    gaps
                )

                st.session_state.current_file = file_key
                st.session_state.summary = summary
                st.session_state.keywords = keywords
                st.session_state.gaps = gaps
                st.session_state.section_summaries = section_summaries
                st.session_state.report_file = report_file

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.stop()

        finally:
            if temp_pdf_path and os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)

    # --- Render Output ---

    st.header("Full Summary")
    st.write(st.session_state.get("summary", ""))

    st.header("Keywords")
    st.write(st.session_state.get("keywords", []))

    st.header("Research Gap Indicators")
    st.write(st.session_state.get("gaps", []))

    st.header("Section Summaries")
    for section, short_summary in st.session_state.get("section_summaries", {}).items():
        st.subheader(section)
        st.write(short_summary)

    if st.session_state.get("report_file") and os.path.exists(st.session_state.report_file):
        with open(st.session_state.report_file, "rb") as pdf:
            st.download_button(
                "Download Report",
                pdf,
                file_name="Research_Report.pdf",
                mime="application/pdf"
            )