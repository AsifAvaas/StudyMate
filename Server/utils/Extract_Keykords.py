from typing import List
import re
from keybert import KeyBERT
import yake
# Primary: KeyBERT (semantic, best quality)
try:
    from sentence_transformers import SentenceTransformer
    _sb_model = SentenceTransformer("all-MiniLM-L6-v2")
    _kw_model = KeyBERT(model=_sb_model)
    _HAS_KEYBERT = True
except Exception:
    _HAS_KEYBERT = False

# Fallback: YAKE (no transformer needed)
try:
    # import yake
    _yake = yake.KeywordExtractor(n=1, top=10)
    _HAS_YAKE = True
except Exception:
    _HAS_YAKE = False


def _clean(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text


def extract_keywords(text: str, top_n: int = 5) -> str:
    """
    Returns a short, human-readable topic label from text.
    Tries KeyBERT first, then YAKE, then a very simple fallback.
    """
    text = _clean(text)
    if not text:
        return "General"

    # Try KeyBERT
    if _HAS_KEYBERT:
        try:
            # use MMR to avoid near-duplicates
            kws = _kw_model.extract_keywords(
                text,
                keyphrase_ngram_range=(1, 3),
                stop_words="english",
                top_n=top_n,
                use_mmr=True,
                diversity=0.5,
            )
            label = ", ".join([w for (w, score) in kws if w])
            return label or "General"
        except Exception:
            pass

    # Try YAKE
    if _HAS_YAKE:
        try:
            kws = _yake.extract_keywords(text)
            # sorted by score ascending (lower is better)
            kws = [k for (k, score) in sorted(kws, key=lambda x: x[1])[:top_n]]
            label = ", ".join(kws)
            return label or "General"
        except Exception:
            pass

    # Ultra-minimal fallback: top frequent nouns-ish tokens
    tokens = re.findall(r"[A-Za-z]{3,}", text.lower())
    if not tokens:
        return "General"
    from collections import Counter
    common = [w for (w, _) in Counter(tokens).most_common(top_n)]
    return ", ".join(common) or "General"