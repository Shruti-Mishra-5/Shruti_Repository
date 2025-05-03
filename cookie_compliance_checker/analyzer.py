import re
import string
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
from bs4 import BeautifulSoup

# Load SBERT model globally
sbert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # Consider using LegalBERT for legal texts

### ─────────────────────────────
### TEXT CLEANING & NORMALIZATION
### ─────────────────────────────

def clean_text(text):
    if not text or not isinstance(text, str): return ""
    
    # Remove HTML and JavaScript
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text()
    text = re.sub(r'<.*?>', '', text)  # Remove HTML tags
    text = re.sub(r'function.*?\{.*?\}', '', text, flags=re.DOTALL)  # Remove JS functions
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r'\s+', ' ', text)
    
    return text.lower().strip()

def normalize_length(text, max_words=200):
    words = text.split()
    return ' '.join(words[:max_words]) if len(words) > max_words else text


### ─────────────────────────────
### SIMILARITY COMPUTATION
### ─────────────────────────────

def compute_similarity_tfidf(text1, text2):
    text1 = clean_text(text1)
    text2 = clean_text(text2)
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform([text1, text2])
    return cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

def compute_semantic_similarity(text1, text2):
    embeddings1 = sbert_model.encode(text1, convert_to_tensor=True)
    embeddings2 = sbert_model.encode(text2, convert_to_tensor=True)
    return util.pytorch_cos_sim(embeddings1, embeddings2).item()

def compute_similarity(text1, text2, use_semantic=True, weight_semantic=0.7):
    text1 = normalize_length(clean_text(text1))
    text2 = normalize_length(clean_text(text2))

    tfidf_sim = compute_similarity_tfidf(text1, text2)
    if use_semantic:
        semantic_sim = compute_semantic_similarity(text1, text2)
        return round(weight_semantic * semantic_sim + (1 - weight_semantic) * tfidf_sim, 4)
    else:
        return round(tfidf_sim, 4)


### ─────────────────────────────
### PARAGRAPH-LEVEL SECTION MATCHING
### ─────────────────────────────

def find_best_matching_policy_section(cookie_banner, privacy_policy_text):
    banner_clean = normalize_length(clean_text(cookie_banner), max_words=150)
    if not banner_clean or len(banner_clean) < 10:
        return 0.0, ""

    banner_embed = sbert_model.encode(banner_clean, convert_to_tensor=True)

    # Use paragraph chunks or full sentences
    paragraphs = re.split(r'\n+|(?<=[.!?])\s{2,}', privacy_policy_text)

    best_score = 0.0
    best_chunk = ""

    for para in paragraphs:
        para_clean = normalize_length(clean_text(para), max_words=150)
        if len(para_clean.split()) < 10:
            continue
        chunk_embed = sbert_model.encode(para_clean, convert_to_tensor=True)
        score = util.pytorch_cos_sim(banner_embed, chunk_embed).item()

        if score > best_score:
            best_score = score
            best_chunk = para.strip()

    return round(best_score, 4), best_chunk


### ─────────────────────────────
### KEYWORD-BASED SECTION EXTRACTION
### ─────────────────────────────

def extract_section(text, keyword):
    pattern = re.compile(rf"[^.]*\b{keyword}\b[^.]*\.", re.IGNORECASE)
    matches = pattern.findall(text)
    return ' '.join(matches) if matches else ''

def fine_grained_analysis(cookie_banner, privacy_policy, keywords=None):
    if keywords is None:
        keywords = ['cookies', 'data collection', 'third-party', 'consent', 'personal data']

    results = {}
    for keyword in keywords:
        banner_section = extract_section(cookie_banner, keyword)
        policy_section = extract_section(privacy_policy, keyword)

        if banner_section and policy_section:
            score = compute_similarity(banner_section, policy_section)
        else:
            score = 0.0
        results[keyword] = round(score, 4)
    return results


### ─────────────────────────────
### INTERPRETATION HELPER
### ─────────────────────────────

def interpret_similarity(score):
    if score >= 0.75:
        return "✅ Strong contextual match"
    elif score >= 0.5:
        return "🟡 Moderate similarity"
    elif score >= 0.3:
        return "⚠️ Weak similarity — may be loosely related"
    else:
        return "❌ No meaningful contextual match"


### ─────────────────────────────
### MAIN COMPARISON FUNCTION
### ─────────────────────────────

def compare_banner_to_policy(cookie_banner, privacy_policy_text):
    print("🔎 Performing full comparison...")

    overall_score = compute_similarity(cookie_banner, privacy_policy_text)
    print(f"\n📊 Overall Similarity Score: {overall_score}")
    print(f"🧠 Interpretation: {interpret_similarity(overall_score)}")

    print("\n🔍 Finding best matching section from privacy policy...")
    best_score, best_match = find_best_matching_policy_section(cookie_banner, privacy_policy_text)
    print(f"\n📌 Best Matching Section Score: {best_score}")
    print(f"🧩 Matching Text Snippet:\n\"{best_match.strip()}\"")
    print(f"🧠 Interpretation: {interpret_similarity(best_score)}")

    print("\n📑 Fine-Grained Keyword-Based Analysis:") 
    keyword_results = fine_grained_analysis(cookie_banner, privacy_policy_text)
    for kw, sc in keyword_results.items():
        print(f"  - {kw.title():<20}: {sc} → {interpret_similarity(sc)}")

    return {
        "overall_similarity": overall_score,
        "best_section_score": best_score,
        "best_section_text": best_match.strip(),
        "keyword_analysis": keyword_results
    }

### Additional Notes:

# 1. **Dynamically Loaded or Non-Textual Content**:
#    This approach assumes that the text has already been fully rendered in the HTML content. If the page uses JavaScript to load the cookie banner or privacy policy dynamically (e.g., with AJAX), this approach will not capture those elements.
#    **To address this limitation**: Use tools like **Selenium** or **Puppeteer** to render the page and extract the fully-loaded HTML content.

# 2. **Specialized or Legal Language**:
#    The current model uses **Sentence-BERT** for semantic similarity, which is general-purpose and may not fully capture the nuances of specialized or legal language. For better performance with legal texts, you could use a model like **LegalBERT**, which is specifically fine-tuned for legal text.
#    **To address this limitation**: Consider using domain-specific models for legal texts or training custom models with a corpus of legal documents to improve accuracy.

