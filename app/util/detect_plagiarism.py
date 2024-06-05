from typing import List, Any, Tuple
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


def detect_plagiarism(files: List[str], allowable_limit: float):
    """
    A function to detect plagiarism among given list of files as well as the threshold of the similarity between files
    :param files: List of files which should be checked for plagiarism
    :param allowable_limit: Percentage limit of allowable similarity
    :return: Complete list of similarity scores between each pair of files
    """
    plagiarism_pairs = []
    embeddings = []
    similarity_scores = []
    for file in files:
        embeddings.append(model.encode(file))
    for i in range(len(embeddings)):
        for j in range(i+1, len(embeddings)):
            similarity_score = cosine_similarity(embeddings[i].reshape(1, -1), embeddings[j].reshape(1, -1))
            print("Similarity between pairs", i, " and ", j, " is: ", similarity_score[0][0])
            similarity_scores.append((i, j, similarity_score[0][0]))
            if similarity_score[0][0] > allowable_limit:
                plagiarism_pairs.append((i, j, similarity_score[0][0]))
    return plagiarism_pairs, similarity_scores
