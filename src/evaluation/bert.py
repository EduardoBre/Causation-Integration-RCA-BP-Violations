from torch import Tensor
from transformers import BertTokenizer, BertModel
import torch.nn as nn

# Load Model and Tokenizer form BERT-base pretrained model:
# On the choice of model, it's all about  efficiency vs complexity
# 'bert-base-uncased' more efficiency, less accuracy
# 'bert-large-uncased' more complexity (about 3x), more accuracy
PRETRAINED_MODEL: str = 'bert-large-uncased'
TOKENIZER = BertTokenizer.from_pretrained(PRETRAINED_MODEL)
MODEL = BertModel.from_pretrained(PRETRAINED_MODEL)


def encode_text(text: str) -> Tensor:
    """
    Preprocess a text and encode it using BERT's tokenizer and model.
    :param text: The text to encode.
    :returns: Torch's tensor of the encoding.
    """

    encoded_dict = TOKENIZER.encode_plus(
        text,
        add_special_tokens=True,  # Add '[CLS]' (start) and '[SEP]' (end) of sentence
        max_length=64,  # Pad & truncate all sentences (64 was chosen here as sentence strings are all small)
        padding=True,  # All encoded texts are padded to the same length (consistent input size for BERT)
        return_attention_mask=True,  # Instructs the tokenizer to generate attention masks
        return_tensors='pt',  # Output as PyTorch tensors (required for input to BERT's model)
    )

    # Extract input (token) ids and attention masks from encoded dictionary and pass to BERT model
    input_ids = encoded_dict['input_ids']
    attention_mask = encoded_dict['attention_mask']
    outputs = MODEL(input_ids, attention_mask=attention_mask)

    # (Tensor object type) Extract the last hidden state and return the mean of the embeddings (Tensor object type)
    return outputs.last_hidden_state.squeeze(0).mean(dim=0)


def get_cosine_similarity(subject_text: Tensor, object_text: Tensor) -> float:
    """
    Helper function to calculate cosine similarity
    :param subject_text: The sentence to be teste for similarity.
    :param object_text: The Gold-Standard sentence.
    :return: Float type similarity between [-1, 1], no further roundings.
    """
    return nn.functional.cosine_similarity(subject_text, object_text, dim=0).item()
