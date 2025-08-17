from database import LocalSession
from utils.Segment_Topics import auto_segment_topics
from models.Chunks import chunks
from utils.Chunker import chunk_text
from utils.embedder import get_embedding

def process_chunks(file_id: str, user_id: str, text: str):
    db = LocalSession()  # open a fresh session
    try:
        Chunk_data = chunk_text(text, max_words=200)
        for ch in Chunk_data:
            embedding = get_embedding(ch)
            new_chunk = chunks(
                file_id=file_id,
                user_id=user_id,
                chunk_text=ch,
                embedding=embedding
            )
            db.add(new_chunk)
        db.commit()

        # Call auto segment
        auto_segment_topics(file_id, db)
    finally:
        db.close()  # always close the session
