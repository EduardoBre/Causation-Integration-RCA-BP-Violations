from unittest import TestCase
from unittest.mock import patch
import uuid

from event_knowledge_graph import EventKnowledgeGraph, Relationships


class TestConstraintKnowledgeBasePopulation(TestCase):

    @patch('knowledge_graph.uuid.uuid4')
    def test_add_nodes(self, mock_uuid4):
        # Mock uuid to return a specific UUID
        mock_uuid = uuid.UUID('15ff57e6-4e3d-4bc3-869a-738ba23dd32a')
        mock_uuid4.return_value = mock_uuid

        attr = {
            'attribute': 'value'
        }
        event_kg = EventKnowledgeGraph()
        event_kg.add_node(1, 'Subject Activity', attr, 1)
        event_kg.export_kg(indentation=4)

    @patch('knowledge_graph.uuid.uuid4')
    def test_add_rel(self, mock_uuid4):
        # Mock uuid to return a specific UUID
        mock_uuid = uuid.UUID('15ff57e6-4e3d-4bc3-869a-738ba23dd32a')
        mock_uuid4.return_value = mock_uuid

        attr = {
            'attribute': 'value'
        }
        event_kg = EventKnowledgeGraph()
        # Add 2 nodes and a relationship
        event_kg.add_node(1, 'Subject Activity', attr, 1)
        event_kg.add_node(1, 'Object Activity', attr, 2)
        event_kg.add_rel(1, 1, Relationships.DIRECTLY_FOLLOWS, 2)

        event_kg.export_kg(indentation=4)

    @patch('knowledge_graph.uuid.uuid4')
    def test_rm_node_rm_rel(self, mock_uuid4):
        # Mock uuid to return a specific UUID
        mock_uuid = uuid.UUID('15ff57e6-4e3d-4bc3-869a-738ba23dd32a')
        mock_uuid4.return_value = mock_uuid

        attr = {
            'attribute': 'value'
        }
        event_kg = EventKnowledgeGraph()
        # Add 2 nodes and a relationship
        event_kg.add_node(1, 'Subject Activity', attr, 1)
        event_kg.add_node(1, 'Object Activity', attr, 2)
        event_kg.add_rel(1, 1, Relationships.DIRECTLY_FOLLOWS, 2)
        event_kg.rm_node(1, 1)

        event_kg.export_kg(indentation=4)

    @patch('knowledge_graph.uuid.uuid4')
    def test_add_several_nodes_rels(self, mock_uuid4):
        # Mock uuid to return a specific UUID
        mock_uuid = uuid.UUID('15ff57e6-4e3d-4bc3-869a-738ba23dd32a')
        mock_uuid4.return_value = mock_uuid

        attr = {
            'attribute': 'value'
        }
        event_kg = EventKnowledgeGraph()
        # Add 2 nodes and a relationship
        event_kg.add_node(1, 'Subject Activity', attr, 1)
        event_kg.add_node(1, 'Object Activity', attr, 2)
        event_kg.add_node(1, 'Second Object Activity', attr, 3)
        event_kg.add_rel(1, 1, Relationships.DIRECTLY_FOLLOWS, 2)
        event_kg.add_rel(1, 2, Relationships.DIRECTLY_FOLLOWS, 3)

        event_kg.export_kg(indentation=4)
