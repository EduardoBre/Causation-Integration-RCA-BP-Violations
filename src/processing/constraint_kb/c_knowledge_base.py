import json
import re


class ConstraintKnowledgeBase:
    """
    This class defines and initializes a constraint Knowledge Base.
    """

    def __init__(self):
        self.__kb = {}

    @property
    def get_kb(self) -> dict:
        return self.__kb

    def add_constraint(self, id: int,
                       f_activity: str,
                       s_activity: str,
                       rel: str,
                       conditions: str,
                       comment: str) -> None:
        """
        Adds a constraint to the Knowledge Base.
        :param id: The id of the constraint.
        :param f_activity: The first activity of the constraint.
        :param s_activity: The second activity of the constraint.
        :param rel: The relationship between the first and second activity.
        :param conditions: The condition of the constraint.
        :param comment: The provided comment above the constraint.
        """
        self.get_kb[id] = {
            'subject': f_activity,
            'object': s_activity,
            'relationship': rel,
            'condition': self.add_conditions(conditions),
            'comment': comment
        }

    def add_conditions(self, condition: str) -> dict:
        """
        Adds all the conditions in the right dictionary format.
        :param condition: The complete condition string to be processed.
        :return: A dictionary containing the constraint conditions in right format.
        """

        # track condition information
        counter = 1
        res = {}

        conditions = [condition]
        if 'AND' in condition:
            conditions = [part.strip() for part in condition.split('AND')]

        for item in conditions:
            if 'OR' in condition:
                cond_dict = {}
                counter_or = 1
                curr = [part.strip() for part in item.split('OR')]
                for cond in curr:
                    if self.eval_ope_count(item):
                        conc_cond = self.parse_concatenated_conditions(cond)
                        cond_dict[counter_or] = conc_cond[0]
                        counter_or += 1
                        cond_dict[counter_or] = conc_cond[1]
                    else:
                        cond_dict[counter_or] = self.parse_conditions(cond)
                    counter_or += 1
                res[counter] = cond_dict
            else:
                if self.eval_ope_count(item):
                    conc_cond = self.parse_concatenated_conditions(item)
                    res[counter] = conc_cond[0]
                    counter += 1
                    res[counter] = conc_cond[1]
                else:
                    res[counter] = self.parse_conditions(item)
            counter += 1

        return res

    @staticmethod
    def parse_conditions(condition: str) -> dict:
        """
        Parses a Condition to extract the important components into a formatted dictionary.
        :param condition: The single condition to be process.
        :return: The dictionary containing a whole condition.
        """

        cond_parts = re.split(r"(<=|>=|<|>|==|!=|=)", condition)
        feature, rule, value = cond_parts
        return {
            'name': feature.strip(),
            'rule': rule.strip(),
            'value': value.strip()
        }

    @staticmethod
    def parse_concatenated_conditions(condition: str) -> tuple[dict, dict]:
        """
        Parses a Concatenated Condition to extract the important components into a formatted dictionary.
        :param condition: The concatenated condition to be process.
        :return: Tuple of two dictionaries each containing a whole condition.
        """

        cond_parts = re.split(r"(<=|>=|<|>)", condition)
        f_value, f_rule, feature, s_rule, s_value = cond_parts
        opposite_rules = {
            '<=': '>=',
            '>=': '<=',
            '>': '<',
            '<': '>'
        }
        return ({
                    'name': feature.strip(),
                    'rule': opposite_rules[f_rule.strip()],
                    'value': f_value.strip()
                }, {
                    'name': feature.strip(),
                    'rule': s_rule.strip(),
                    'value': s_value.strip()
                })

    @staticmethod
    def eval_ope_count(condition: str):
        operators = ['<=', '>=', '<', '>']
        return sum(condition.count(op) for op in operators) > 2

    def print_kb_as_dict(self) -> None:
        print(self.__kb)

    def print_kb_as_json(self, indent: int = 4) -> None:
        print(json.dumps(self.__kb, indent=indent))

    def output_kb_as_json(self, name: str, path: str = '', indent: int = 4) -> None:
        if path:
            if path.endswith('/'):
                f_path = f"{path}{name}.json"
            else:
                f_path = f"{path}/{name}.json"
        else:
            f_path = f"{name}.json"
        with open(f_path, 'w') as file:
            file.write(json.dumps(self.__kb, indent=indent))
