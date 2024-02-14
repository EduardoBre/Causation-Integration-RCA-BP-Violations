from sentence_transformers import SentenceTransformer
import torch.nn as nn
from torch import Tensor
from scipy.spatial.distance import euclidean, cityblock
from scipy.stats import pearsonr, spearmanr

"""
This .py file was mainly use for preliminary manual testing on typical LLM output regarding the thesis' objective.
It has no further use, besides manual testing.
"""

# Load Model and Tokenizer form S-BERT-base pretrained model
# 'all-MiniLM-L6-v2' has a model size of 80MB
# 'all-MiniLM-L12-v2' has a model size of 120MB
model = SentenceTransformer('all-MiniLM-L6-v2')

# The subject sentence (e.g., from mined constraints)
subject_sentence_1 = "eventually follows"
subject_sentence_2 = "sequentially follows"
# The object sentence (from Gold-Standard)
gs_sentence = "directly follows"


def encode_text(text: str) -> Tensor:
    """
    Preprocess a text and encode it using BERT's tokenizer and model.
    :param text: The text to encode.
    :returns: Encoded sentence converted to Torch's Tensor.
    """
    return model.encode(text, convert_to_tensor=True)


def get_cosine_similarity(subject_text: Tensor, object_text: Tensor) -> float:
    """
    Helper function to calculate cosine similarity
    :param subject_text: The sentence to be teste for similarity.
    :param object_text: The Gold-Standard sentence.
    :return: Float type similarity between [-1, 1], no further roundings.
    """
    return nn.functional.cosine_similarity(subject_text, object_text, dim=0).item()


# Encode the sentence strings using S-BERT model
encoded_subject_sentence_1 = encode_text(subject_sentence_1)
encoded_subject_sentence_2 = encode_text(subject_sentence_2)
encoded_object_sentence = encode_text(gs_sentence)

# Calculate cosine similarity
similarity = get_cosine_similarity(encoded_subject_sentence_1, encoded_object_sentence)
print(f"Similarity between the 'eventually follows' and 'directly follows' using Cosine Similarity: {similarity}")
similarity = get_cosine_similarity(encoded_subject_sentence_2, encoded_object_sentence)
print(f"Similarity between the 'sequentially follows' and 'directly follows' using Cosine Similarity: {similarity}")

# Evaluation: Euclidean Distance
euclidean_dist = euclidean(encoded_subject_sentence_1, encoded_object_sentence)
print("Similarity between the 'eventually follows' and 'directly follows' using Euclidean Distance:", euclidean_dist)
euclidean_dist = euclidean(encoded_subject_sentence_2, encoded_object_sentence)
print(f"Similarity between the 'sequentially follows' and 'directly follows' using Euclidean Distance: {similarity}")

# Evaluation: Manhattan (Cityblock) Distance
manhattan_dist = cityblock(encoded_subject_sentence_1, encoded_object_sentence)
print("Similarity between the 'eventually follows' and 'directly follows' using Manhattan Distance:", manhattan_dist)
manhattan_dist = cityblock(encoded_subject_sentence_2, encoded_object_sentence)
print(f"Similarity between the 'sequentially follows' and 'directly follows' using Manhattan Distance: {similarity}")

# Evaluation: Pearson Correlation Coefficient (.flatten() needed to reshape the embeddings from 2D to 1D arrays for
# correlation)
pearson, _ = pearsonr(encoded_subject_sentence_1.flatten(), encoded_object_sentence.flatten())
print("Similarity between the 'eventually follows' and 'directly follows' using Pearson Correlation:", pearson)
pearson, _ = pearsonr(encoded_subject_sentence_2.flatten(), encoded_object_sentence.flatten())
print(f"Similarity between the 'sequentially follows' and 'directly follows' using Pearson Correlation: {similarity}")

# Evaluation: Spearman's Correlation (.flatten() needed to reshape the embeddings from 2D to 1D arrays for correlation)
spearman, _ = spearmanr(encoded_subject_sentence_1.flatten(), encoded_object_sentence.flatten())
print("Similarity between the 'eventually follows' and 'directly follows' using Spearman's Correlation:", spearman)
spearman, _ = spearmanr(encoded_subject_sentence_2.flatten(), encoded_object_sentence.flatten())
print(f"Similarity between the 'sequentially follows' and 'directly follows' using Spearman's Correlation: {similarity}")
