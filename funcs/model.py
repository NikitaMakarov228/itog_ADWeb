from create_bot import summarizer
import asyncio


def split_text_into_chunks(text, max_chunk_size) -> list:
    chunks = []
    while len(text) > max_chunk_size:
        split_index = text[:max_chunk_size].rfind(". ")
        if split_index == -1:
            split_index = max_chunk_size
        chunks.append(text[: split_index + 1])
        text = text[split_index + 1 :]
    if text:
        chunks.append(text)
    return chunks


async def summarize_large_text(
    text, progress_callback, max_length=1024, min_length=15
) -> str:

    has_pass = True if len(text) < 8000 else False

    while len(text) > 3500:
        chunks = split_text_into_chunks(text, max_chunk_size=int(max_length / 2))
        summarized_chunks = []
        for i, chunk in enumerate(chunks):
            if progress_callback:
                await progress_callback(i + 1, len(chunks) * 1.2)
            summary = await asyncio.to_thread(
                summarizer,
                chunk,
                max_length=int(max_length / 2),
                min_length=min_length,
                do_sample=False,
            )
            summarized_chunks.append(summary[0]["summary_text"])

        text = " ".join(summarized_chunks)
    if has_pass:
        final_summary = await asyncio.to_thread(
            summarizer,
            text,
            max_length=int(max_length / 2),
            min_length=300,
            do_sample=False,
        )
        text = final_summary[0]["summary_text"]
    return text
