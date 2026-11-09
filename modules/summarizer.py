from transformers import pipeline

summarizer =pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)

def summarize_text(text):

    chunks = []

    max_chunk = 1000

    for i in range(0, len(text), max_chunk):

        chunks.append(text[i:i+max_chunk])

    summaries = []

    for chunk in chunks:

        result = summarizer(
            chunk,
            max_length=200,
            min_length=40,
            do_sample=False
        )

        summaries.append(
            result[0]["summary_text"]
        )

    return " ".join(summaries)
