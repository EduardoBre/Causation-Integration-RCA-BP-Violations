from unittest import TestCase

from processing.constraint_kb.c_populator import ConstraintPopulator
from processing.knowledge_graph.ekg_populator import EventKnowledgeGraphPopulator
from processing.nlp_cond_evaluator.matching_evaluation_tool import MatchingEvaluationTool


class TestMatchingEvaluationTool(TestCase):

    def test_perform_evaluation(self):
        ckb = ConstraintPopulator('coffee_roasting.txt')
        ckb.parse_constraint_list()

        ekg = EventKnowledgeGraphPopulator('coffee_data_categorical.xlsx', 0, 1, 3, 4, 5)

        tool = MatchingEvaluationTool(ckb.get_kb, ekg.get_event_kg)

        tool.perform_evaluation()
        tool.output_to_json()
