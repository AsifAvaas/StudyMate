# utils/segment_topics.py
import math
import numpy as np
from sqlalchemy.orm import Session
from sklearn.cluster import KMeans
from models.Topics import topics
from models.Chunks import chunks as ChunksModel
from utils.Extract_Keykords import extract_keywords

def _choose_k(n: int) -> int:
    # Heuristic: between 2 and 12, scales with corpus size
    if n < 2:
        return 1
    return max(2, min(12, int(round(math.sqrt(max(2, n // 2))))))

def auto_segment_topics(file_id: str, db: Session):
    # 1) Fetch chunks for this file
    rows = db.query(ChunksModel).filter(ChunksModel.file_id == file_id).all()
    if not rows:
        return

    # 2) Build embedding matrix (ensure float)
    try:
        X = np.vstack([np.array(r.embedding, dtype=float) for r in rows])
    except Exception:
        # if any embedding missing or malformed, skip
        return

    n = X.shape[0]
    if n == 1:
        # Single topic – label from the only chunk
        topic_name = extract_keywords(rows[0].chunk_text)
        new_topic = topics(file_id=file_id, user_id=rows[0].user_id, name=topic_name, is_manual=False)
        db.add(new_topic); db.commit(); db.refresh(new_topic)
        rows[0].topic_id = new_topic.id
        db.commit()
        return

    # 3) Cluster embeddings
    k = _choose_k(n)
    # If k > n, fix it
    k = min(k, n)
    if k <= 1:
        k = 1
    kmeans = KMeans(n_clusters=k, n_init="auto", random_state=42)
    labels = kmeans.fit_predict(X)

    # 4) For each cluster → extract keywords & save topic
    for cluster_id in sorted(set(labels)):
        cluster_texts = [rows[i].chunk_text for i in range(n) if labels[i] == cluster_id]
        combined_text = " ".join(cluster_texts)
        topic_name = extract_keywords(combined_text)

        new_topic = topics(
            file_id=file_id,
            user_id=rows[0].user_id,
            name=topic_name,
            is_manual=False
        )
        db.add(new_topic); db.commit(); db.refresh(new_topic)

        # 5) Link chunks → topic
        for i, row in enumerate(rows):
            if labels[i] == cluster_id:
                row.topic_id = new_topic.id
        db.commit()
