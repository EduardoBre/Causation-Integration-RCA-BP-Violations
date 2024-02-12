import re

from processing.constraint_kb.c_knowledge_base import ConstraintKnowledgeBase


class ConstraintPopulator:
    """
    Populator of the Constraint Knowledge Base.
    """

    def __init__(self, path: str):
        """
        Creates a Constraint Knowledge Base and populates it.
        :param path: Path of the file to use for population.
        """
        self.__kb = ConstraintKnowledgeBase()
        self.__path = path
        self.parse_constraint_list()

    @property
    def get_kb(self) -> ConstraintKnowledgeBase:
        """
        Returns the Constraint Knowledge Base object.
        :return:
        """
        return self.__kb

    @property
    def get_path(self) -> str:
        return self.__path

    def parse_constraint_list(self) -> None:
        c_comment = ''
        with open(self.get_path, 'r') as file:
            for line in file:
                # Check for new constraint group comment
                if line.startswith("##"):
                    # If line contains comment, save it to store for constraints
                    c_comment = line[2:].strip()
                elif line.startswith('c'):
                    id = re.search('c(\d+)', line).group(1)
                    c_patterns = '\{([^}]+)\}'
                    c_components = re.findall(c_patterns, line)
                    self.get_kb.add_constraint(id, *c_components, c_comment)
