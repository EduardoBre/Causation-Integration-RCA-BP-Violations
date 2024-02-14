from datetime import datetime
from enum import Enum
from uuid import UUID
from abc import ABC, abstractmethod
import uuid

import numpy as np

from processing.knowledge_graph.kg_enums import KGType, Relationships, NodeType
import json
import os


class AbstractKnowledgeGraph(ABC):
    """
    Skeleton for a generic knowledge graph.
    :param kg_name: Name of the knowledge graph.
    :param kg_type: Type of the knowledge graph.
    :param kg_node_type: Type of the nodes of the knowledge graph.
    """

    def __init__(self,
                 kg_name: str = 'Abstract Knowledge Graph',
                 kg_type: KGType = KGType.GENERIC,
                 kg_node_type: NodeType = NodeType.GENERIC):
        self.__kg_name = kg_name
        self.__kg_type = kg_type
        self.__kg_node_type = kg_node_type
        self.__kg_id = uuid.uuid4()
        # Instance variables to store JSON data and create base structure:
        self.__kg_info_json = {}  # Dynamic Information about the KG
        self.__kg_node_json = {}  # Node information
        self.__kg_rel_json = {'directly follows': {}}  # Nodes relationships information
        self.init_info_sec()

    def init_info_sec(self) -> None:
        """
        Initializes the JSON structure of the KG info section.
        :return: None.
        """
        self.__kg_info_json['name'] = self.__kg_name
        self.__kg_info_json['type'] = self.__kg_type
        self.__kg_info_json['stats'] = {'node_type': self.__kg_node_type,
                                        'nodes': 0,
                                        'relationships': 0
                                        }

    def create_kg(self) -> dict:
        """
        Generates the KG with the stored data.
        :return: dictionary containing the KG structured information.
        """
        return {'id': self.__kg_id,
                'info': self.__kg_info_json,
                'nodes': self.__kg_node_json,
                'relationships': self.__kg_rel_json,
                }

    @abstractmethod
    def add_node(self,
                 trace_id: int,
                 activity_name: str,
                 attributes: dict,
                 node_id):
        """
        Adds a node to the KG.
        :param trace_id: The ID of the trace of this node.
        :param activity_name: Name of the node.
        :param attributes: Attributes of the node.
        :param node_id: The id of the node be added.
        """
        pass

    @abstractmethod
    def add_rel(self,
                trace_id: int,
                subject_id: int,
                rel_type: Relationships,
                object_id: int) -> int:
        """
        Adds a relationship to the KG
        :param trace_id: The ID of the trace of this relationship.
        :param subject_id: The ID the source of the relationship.
        :param rel_type: Type of the relationship.
        :param object_id: The ID of the object of the relationship.
        :return: ID of the added relationship.
        """
        pass

    @abstractmethod
    def rm_node(self, trace_id: int, node_id) -> dict:
        """
        Removes a node to the KG.
        :param node_id: ID of the node.
        :return: Dictionary of the deleted node, None if no node under the provided id could be found.
        """
        pass

    @abstractmethod
    def rm_rel(self, trace_id: int, rel_id: int) -> dict:
        """
        Adds a node to the KG.
        :param trace_id: The trace of the relationship.
        :param rel_id: ID of the relationship.
        :return: Dictionary of the deleted relationship, None if no node under the provided id could be found.
        """
        pass

    def inc_node_count(self) -> None:
        self.__kg_info_json['stats']['nodes'] += 1

    def dec_node_count(self) -> None:
        self.__kg_info_json['stats']['nodes'] -= 1

    def inc_rel_count(self) -> None:
        self.__kg_info_json['stats']['relationships'] += 1

    def dec_rel_count(self) -> None:
        self.__kg_info_json['stats']['relationships'] -= 1

    @property
    def get_relationships(self) -> dict[str, dict]:
        return self.__kg_rel_json

    @property
    def get_nodes(self) -> dict:
        return self.__kg_node_json

    @property
    def get_kg_info(self) -> dict:
        return self.__kg_info_json

    @property
    def get_kg_name(self) -> str:
        return self.__kg_name

    @property
    def get_kg_type(self) -> KGType:
        return self.__kg_type

    @property
    def get_kg_node_type(self) -> NodeType:
        return self.__kg_node_type

    @property
    def get_kg_id(self) -> UUID:
        return self.__kg_id

    def export_kg(self, path: str = 'output', file_name: str = 'kg.json', indentation: int = None) -> None:
        """
        Exports knowledge stored in the object as a .json file.
        :param file_name: Name of the output file.
        :param path: Path to the file.
        :param indentation: The desired indentation of the JSON dump.
        :return: None.
        """
        with open(os.path.normpath(path + '/' + file_name), 'w') as file:
            json.dump(self.create_kg(), file, cls=KGEnumEncoder, indent=indentation)

    def print_kg_dict(self):
        print(self.create_kg())

    def __str__(self):
        """
        Stringifies the KG.
        :return: formated stringified JSON of the KG.
        """
        return json.dumps(self.create_kg(), cls=KGEnumEncoder)


class KGEnumEncoder(json.JSONEncoder):
    """
    Encoder to stringify Enums.
    """

    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        elif isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super().default(obj)
