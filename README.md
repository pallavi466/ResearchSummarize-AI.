# ResearchSummarize AI – Academic Paper Summarization Engine

## Project Description
ResearchSummarize AI is an AI-powered application designed to simplify the process of understanding lengthy academic research papers. It allows users to upload research papers in PDF format and automatically generates concise summaries.

## Features
- Upload academic research papers in PDF format.
- Extract text from PDF documents.
- Generate concise summaries using DistilBART.
- Extract important keywords using TF-IDF.
- Identify potential research gaps.
- Display results through an interactive Streamlit interface.

## Technologies Used
- Python
- Streamlit
- Natural Language Processing (NLP)
- Hugging Face Transformers
- DistilBART
- TF-IDF
- PDFplumber

## How to Run Locally
1. Install the required dependencies.
2. Run `pip install -r requirements.txt`.
3. Execute `streamlit run app.py`.
4. Open the local application in your browser.

## Deployment
Deployed using Hugging Face Spaces with Docker SDK.
