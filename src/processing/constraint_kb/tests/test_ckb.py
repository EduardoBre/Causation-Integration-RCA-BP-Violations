from unittest import TestCase

from processing.constraint_kb.c_populator import ConstraintPopulator


class TestConstraintKnowledgeBasePopulation(TestCase):

    @classmethod
    def setUp(cls):
        """
        Initialize a new Populator.
        """
        cls.populator = ConstraintPopulator('../input/coffee_roasting_constraints.txt')

    def test_population(self):
        self.populator.parse_constraint_list()
        self.populator.get_kb.output_kb_as_json('coffee_roasting_constraints')
