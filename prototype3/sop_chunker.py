import re
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def split_into_sentences(text):
    
    sentences = re.split(r'[.!?]+', text.strip())

    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

def get_embeddings(sentences, model):

    embeddings = model.encode(sentences)
    return embeddings

def find_most_similar_sentences(para1_sentences, para2_sentences, para1_embeddings, para2_embeddings):

    results = []
    
    for i, sentence1 in enumerate(para1_sentences):

        similarities = cosine_similarity([para1_embeddings[i]], para2_embeddings)[0]

        most_similar_idx = np.argmax(similarities)
        max_similarity = similarities[most_similar_idx]
        most_similar_sentence = para2_sentences[most_similar_idx]
        
        results.append({
            'para1_sentence': sentence1,
            'para2_sentence': most_similar_sentence,
            'similarity_score': max_similarity
        })
    
    return results

def check_semantic_subset(similarity_results, threshold=0.9):

    high_similarity_count = sum(1 for result in similarity_results if result['similarity_score'] > threshold)
    total_sentences = len(similarity_results)
    
    is_subset = high_similarity_count == total_sentences
    
    return is_subset, high_similarity_count, total_sentences

def comparison_func(para1, para2):

    # print("Loading sentence transformer model...")
    model = SentenceTransformer('Qwen/Qwen3-Embedding-0.6B')
    

    # para1 = """
    # Machine learning is a subset of artificial intelligence. It enables computers to learn patterns from data. 
    # These algorithms can make predictions on new data without being explicitly programmed for each task.
    # """
    
    # para2 = """
    # Artificial intelligence encompasses various technologies including machine learning. Machine learning is a 
    # powerful subset of AI that allows computers to automatically learn and improve from experience. It involves 
    # algorithms that can identify patterns in data and make predictions or decisions on new, unseen data without 
    # being explicitly programmed for every specific task. This capability makes it valuable for many applications.
    # """
    
    print("Paragraph 1:")
    print(para1.strip())
    print("\nParagraph 2:")
    print(para2.strip())
    print("\n" + "="*80 + "\n")
    
    # Split paragraphs into sentences
    para1_sentences = split_into_sentences(para1)
    para2_sentences = split_into_sentences(para2)
    
    print("Paragraph 1 sentences:")
    for i, sentence in enumerate(para1_sentences, 1):
        print(f"{i}. {sentence}")
    
    print(f"\nParagraph 2 sentences:")
    for i, sentence in enumerate(para2_sentences, 1):
        print(f"{i}. {sentence}")
    
    print("\n" + "="*80 + "\n")
    

    print("Generating embeddings...")
    para1_embeddings = get_embeddings(para1_sentences, model)
    para2_embeddings = get_embeddings(para2_sentences, model)
    
    # Find most similar sentences
    similarity_results = find_most_similar_sentences(
        para1_sentences, para2_sentences, para1_embeddings, para2_embeddings
    )
    

    print("Similarity Analysis:")
    print("-" * 80)
    for i, result in enumerate(similarity_results, 1):
        print(f"\nSentence {i} from Paragraph 1:")
        print(f"'{result['para1_sentence']}'")
        print(f"Most similar sentence in Paragraph 2:")
        print(f"'{result['para2_sentence']}'")
        print(f"Similarity Score: {result['similarity_score']:.4f}")
    
    print("\n" + "="*80 + "\n")
    

    is_subset, high_similarity_count, total_sentences = check_semantic_subset(similarity_results, threshold=0.9)
    
    print("SEMANTIC SUBSET ANALYSIS:")
    print(f"Threshold for high similarity: 0.9")
    print(f"Sentences with high similarity: {high_similarity_count}/{total_sentences}")
    print(f"Average similarity score: {np.mean([r['similarity_score'] for r in similarity_results]):.4f}")
    
    if is_subset:
        print("\nCONCLUSION: Paragraph 1 appears to be a SEMANTIC SUBSET of Paragraph 2")
        print("   All sentences in Paragraph 1 have very high similarity (>0.9) with sentences in Paragraph 2")
    else:
        print("\nCONCLUSION: Paragraph 1 is NOT a complete semantic subset of Paragraph 2")
        print(f"   Only {high_similarity_count} out of {total_sentences} sentences have high similarity (>0.9)")
    

    print(f"\nDetailed similarity scores:")
    for i, result in enumerate(similarity_results, 1):
        status = "High" if result['similarity_score'] > 0.9 else "Low"
        print(f"Sentence {i}: {result['similarity_score']:.4f} ({status})")
