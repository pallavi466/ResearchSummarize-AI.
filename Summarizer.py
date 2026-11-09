
import warnings
from functools import lru_cache
from transformers import pipeline

warnings.filterwarnings("ignore", category=UserWarning, module="transformers")


# Load the model only once
@lru_cache(maxsize=1)
def load_summarizer():

    try:
        print("Loading BART summarization model...")

        model = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-12-6"
        )

        print("BART model loaded successfully!")

        return model

    except Exception as e:
        raise RuntimeError(
            f"Unable to load BART model: {e}"
        ) from e


def summarize_chunk(text, summarizer):

    if not text or not text.strip():
        return ""

    tokenizer = summarizer.tokenizer

    token_ids = tokenizer.encode(
        text,
        add_special_tokens=False
    )

    if len(token_ids) < 35:
        return text.strip()

    max_length = min(
        130,
        max(40, int(len(token_ids) * 0.5))
    )

    min_length = min(
        30,
        max(10, max_length // 3)
    )

    result = summarizer(
        text,
        max_length=max_length,
        min_length=min_length,
        do_sample=False,
        truncation=True
    )

    return result[0]["summary_text"]


def summarize_text(text: str) -> str:

    if not text or not text.strip():
        return ""

    # Load model
    summarizer = load_summarizer()

    tokenizer = summarizer.tokenizer

    # Convert text into tokens
    token_ids = tokenizer.encode(
        text,
        add_special_tokens=False
    )

    # Split large PDF text into manageable chunks
    chunk_size = 850

    chunks = []

    for i in range(0, len(token_ids), chunk_size):

        chunk_ids = token_ids[i:i + chunk_size]

        chunk_text = tokenizer.decode(
            chunk_ids,
            skip_special_tokens=True
        )

        if chunk_text.strip():
            chunks.append(chunk_text)

    # Generate summaries for each chunk
    summaries = []

    for chunk in chunks:

        summary = summarize_chunk(
            chunk,
            summarizer
        )

        if summary:
            summaries.append(summary)

    if not summaries:
        return ""

    combined_summary = " ".join(summaries)

    # Generate a final summary if multiple chunks exist
    if len(summaries) > 1:

        final_tokens = tokenizer.encode(
            combined_summary,
            add_special_tokens=False
        )

        if len(final_tokens) <= chunk_size:
            combined_summary = summarize_chunk(
                combined_summary,
                summarizer
            )

    return combined_summary
