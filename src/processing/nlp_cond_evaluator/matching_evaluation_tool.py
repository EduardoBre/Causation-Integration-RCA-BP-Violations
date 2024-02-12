import json

from processing.constraint_kb.c_populator import ConstraintKnowledgeBase
from processing.knowledge_graph.ekg_populator import EventKnowledgeGraph
from torch import Tensor
from transformers import BertTokenizer, BertModel
import torch.nn as nn
import operator
import re


class MatchingEvaluationTool:

    def __init__(self, ckb: ConstraintKnowledgeBase,
                 ekg: EventKnowledgeGraph,
                 threshold: float = 0.8,
                 num_penalty: float = 0.4):
        """

        :param ckb: The Constraint Knowledge Base
        :param ekg: The Event Knowledge Graph
        """
        self.__c_kb = ckb
        self.__e_kg = ekg
        self.violations = {}

        # Load Model and Tokenizer form BERT-base pretrained model:
        # On the choice of model, it's all about  efficiency vs complexity
        # 'bert-base-uncased' more efficiency, less accuracy
        # 'bert-large-uncased' more complexity (about 3x), more accuracy
        pretrained_model = 'bert-large-uncased'
        self.tokenizer = BertTokenizer.from_pretrained(pretrained_model)
        self.model = BertModel.from_pretrained(pretrained_model)
        # The cosine similarity threshold to be applied for the embedding comparison
        self.threshold = threshold
        # The numeral penalty
        self.num_penalty = num_penalty
        # Dict to collect cache of measured labels
        self.similarity_cache = {}

        # Pre defined operators for evaluation
        self.operators = {
            '>': operator.gt,
            '<': operator.lt,
            '>=': operator.ge,
            '<=': operator.le,
            '==': operator.eq,
            '!=': operator.ne
        }

        self.__violations_registry = {}

    @property
    def get_violations(self) -> dict:
        """
        Get the dictionary containing all violations if the evaluation method has been called.
        :return: A dict containing all violations.
        """
        return self.__violations_registry

    @property
    def get_constraint_kb(self) -> ConstraintKnowledgeBase:
        """
        Get the Constraint Knowledge Base object.
        :return: The Constraint Knowledge Base instance of this matching tool.
        """
        return self.__c_kb

    @property
    def get_event_kg(self) -> EventKnowledgeGraph:
        """
        Get the Event Knowledge Graph object.
        :return: The Event Knowledge Graph instance of this matching tool.
        """
        return self.__e_kg

    def perform_evaluation(self) -> None:
        """
        Performs the Matching and Evaluation process based on the Event Knowledge Graph and Constraint Knowledge Base.
        """

        # Iterate over recorded traces
        for trace_id, trace_relationships in self.get_event_kg.get_relationships['directly follows'].items():
            # Iterate over event relationships
            for rel_id, rel_value in trace_relationships.items():
                node_subject_label = self.get_event_kg.get_nodes[trace_id][rel_value['subject']]['label']
                node_object_label = self.get_event_kg.get_nodes[trace_id][rel_value['object']]['label']

                # Iterate over all constraints
                for c_id, c_val in self.get_constraint_kb.get_kb.items():
                    # First activity of the constraint
                    constraint_subject_label = c_val['subject']
                    # Second activity of the constraint
                    constraint_object_label = c_val['object']

                    # Check if First Activity of Constraint matches First EKG Node Activity
                    if self.eval_similarity(constraint_subject_label, node_subject_label):
                        # Check if Second Activity of Constraint matches Second EKG Node Activity
                        if self.eval_similarity(constraint_object_label, node_object_label):
                            # A match has been found! Evaluate whether conditions hold

                            # Constraint Condition map
                            conditions = c_val['condition']

                            # Check if there is only one condition
                            if len(conditions) == 1:
                                node_att = self.get_event_kg.get_nodes[trace_id][rel_value['object']]['attributes']
                                if not self.eval_concat_rule_concat_value(conditions, node_att):
                                    self.register_violation(trace_id, rel_value['object'], conditions, node_att)
                            else:
                                # For more than 1 condition, the progressive validation aspect needs to be taken care of
                                progressive_validation_dict = {}

                                # The remaining conditions attributed to the current event
                                curr_condition_dict = {}

                                # Attribute key and value from the as-is event
                                event_attributes = self.get_event_kg.get_nodes[trace_id][rel_value['subject']][
                                    'attributes']

                                # If event only has 1 attribute
                                if len(event_attributes) == 1:
                                    (att_name, att_value), = event_attributes.items()
                                    for condition_key, condition_value in conditions.items():
                                        if not self.eval_similarity(att_name, condition_value['name']):
                                            progressive_validation_dict[condition_key] = condition_value
                                        else:
                                            curr_condition_dict[condition_key] = condition_value
                                else:
                                    # In case the vent has more than 1 attribute
                                    progressive_validation_dict = dict(conditions)
                                    for att_name in event_attributes.keys():
                                        for condition_key, condition_value in conditions.items():
                                            if (self.eval_similarity(att_name, condition_value['name'])
                                                    and condition_key in progressive_validation_dict):
                                                del progressive_validation_dict[condition_key]
                                                curr_condition_dict[condition_key] = condition_value

                                if self.eval_progressive_validation(trace_id, rel_value['subject'],
                                                                    progressive_validation_dict):
                                    if not self.eval_concat_rule_concat_value(curr_condition_dict, event_attributes):
                                        self.register_violation(trace_id, rel_value['object'], curr_condition_dict,
                                                                event_attributes)

    def eval_similarity(self, f_string: str, s_string: str) -> bool:
        """
        The actual NLP-based matching logic implementation.
        :param f_string: The first string to be compared.
        :param s_string: The second string to be compared.
        :return: A boolean verdict based on the cosine similarity and established threshold.
        """
        # Check if the evaluation is cached
        if f_string in self.similarity_cache and s_string in self.similarity_cache[f_string]:
            return self.similarity_cache[f_string][s_string]
        elif f_string.lower() == s_string.lower():
            # If not cached, check if strings are equal
            return True
        else:
            # Not cached and not equals:

            # Encode both strings
            enc_f_string = self.encode_text(f_string.replace('_', ' '))
            enc_s_string = self.encode_text(s_string.replace('_', ' '))

            # Check for possible numbers in strings
            f_string_num = re.findall(r'\d+', f_string)
            s_string_num = re.findall(r'\d+', s_string)

            if f_string_num and s_string_num:
                # Convert to string and measure absolute difference
                if abs(int(f_string_num[0]) - int(s_string_num[0])) > 0:
                    # If there's a numerical difference, apply penalty and return similarity
                    c_similarity = self.calc_cosine_similarity(enc_f_string, enc_s_string) - self.num_penalty

                    # Cache new comparison
                    verdict = c_similarity > self.threshold
                    self.add_to_cache(f_string, s_string, verdict)
                    return verdict

            # If there is no numerical difference, simply check for the threshold and cache result
            verdict = self.calc_cosine_similarity(enc_f_string, enc_s_string) > self.threshold
            self.add_to_cache(f_string, s_string, verdict)
            return verdict

    def eval_rule_value(self, ex_rule: str, ex_value, got_value) -> bool:
        """
        Evaluates a given value based on the expected condition value and rule.
        :param ex_rule: Condition rule.
        :param ex_value: Condition value.
        :param got_value: The received value to be compared.
        :return: boolean verdict whether the received value adheres to the expected rule and value.
        """
        # Parse the rule as defined in the operators map from the constructor with the help of operator module
        comp_function = self.operators[ex_rule]
        return comp_function(float(got_value), float(ex_value))

    def add_to_cache(self, f_string: str, s_string: str, verdict: bool) -> None:
        """
        Adds a new entry to the cache of this MatchingEvaluationTool.
        :param f_string: The key string.
        :param s_string: The value string.
        :param verdict: The verdict of the similarity evaluation between the two strings.
        """
        if f_string not in self.similarity_cache:
            self.similarity_cache[f_string] = {s_string: verdict}
        else:
            self.similarity_cache[f_string][s_string] = verdict

    def eval_concat_rule_concat_value(self, expectancy_dict: dict, got_value: dict) -> bool:
        """
        Evaluates the concatenated rules based on the concatenated values.
        :param expectancy_dict: The dictionary containing the Constraint expectancies.
        :param got_value: The dictionary containing the as-is values.
        :return: A boolean verdict whether all the as-is values adhere to all the expectancies of the constraint dict.
        """
        for condition in expectancy_dict.values():
            if any(isinstance(value, dict) for value in condition.values()):
                continue
            for node_att_key, node_att_val in got_value.items():
                if self.eval_similarity(node_att_key, condition['name']):
                    if not self.eval_rule_value(condition['rule'], condition['value'], node_att_val):
                        return False
        return True

    def eval_progressive_validation(self, trace_id: int, event_id: int, conditions: dict) -> bool:
        nodes_iterator = iter(self.get_event_kg.get_nodes[trace_id].items())
        curr_event_id = -1
        temp_cond = dict(conditions)
        while curr_event_id != event_id:
            # Get next node and process relevant data
            node_id, node_value = next(nodes_iterator)
            curr_event_id = node_id
            # Check the event attribute value
            for att_key, att_value in node_value['attributes'].items():
                # Iterate over all remaining progressive conditions to still be validated
                for cond_key, cond_value in conditions.items():
                    # If one of the progressive condition is present in this event, evaluate the as-is and to-be values
                    if self.eval_similarity(att_key, cond_value['name']):
                        if (self.eval_rule_value(cond_value['rule'], cond_value['value'], att_value)
                                and cond_key in temp_cond):
                            del temp_cond[cond_key]

                # Check if conditions map is empty, meaning that all conditions were met
                # = confirmed progressive validation
                if not temp_cond:
                    return True
        return False

    def encode_text(self, text: str) -> Tensor:
        """
        Preprocess a text and encode it using BERT's tokenizer and model.
        :param text: The text to encode.
        :returns: Torch's tensor of the encoding.
        """

        encoded_dict = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,  # Add '[CLS]' (start) and '[SEP]' (end) of sentence
            max_length=64,  # (64 was chosen here as sentence strings are all small)
            padding=True,  # All encoded texts are padded to the same length (consistent input size for BERT)
            return_attention_mask=True,  # Instructs the tokenizer to generate attention masks
            return_tensors='pt',  # Output as PyTorch tensors (required for input to BERT's model)
        )

        # Extract input (token) ids and attention masks from encoded dictionary and pass to BERT model
        input_ids = encoded_dict['input_ids']
        attention_mask = encoded_dict['attention_mask']
        outputs = self.model(input_ids, attention_mask=attention_mask)

        # (Tensor object type) Extract the last hidden state and return the mean of the embeddings (Tensor object type)
        return outputs.last_hidden_state.squeeze(0).mean(dim=0)

    @staticmethod
    def calc_cosine_similarity(subject_text: Tensor, object_text: Tensor) -> float:
        """
        Helper function to calculate cosine similarity
        :param subject_text: The sentence to be teste for similarity.
        :param object_text: The Gold-Standard sentence.
        :return: Float type similarity between [-1, 1], no further roundings.
        """
        return nn.functional.cosine_similarity(subject_text, object_text, dim=0).item()

    def register_violation(self, trace_id, event_id, conditions, attributes) -> None:
        self.get_violations[trace_id] = {
            'message': f"From trace id {trace_id} -> The Process {event_id} "
                       f"failed at least one of the conditions. \n"
                       f"Expected conditions entailed: '{conditions}'.\n"
                       f"The attribute '{attributes}' was the cause of it.",
            'failedConditions': conditions,
            'cause': attributes,
        }

    def output_to_json(self):
        with open('violations_receipt.json', 'w') as file:
            json.dump(self.get_violations, file, indent=4)

