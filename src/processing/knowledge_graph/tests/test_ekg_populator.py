from unittest import TestCase
from unittest.mock import patch
import uuid

from processing.knowledge_graph.ekg_populator import EventKnowledgeGraphPopulator


class TestConstraintKnowledgeBasePopulation(TestCase):

    @patch('knowledge_graph.uuid.uuid4')
    def test_populates_ds1(self, mock_uuid4):
        # Mock uuid to return a specific UUID
        mock_uuid = uuid.UUID('15ff57e6-4e3d-4bc3-869a-738ba23dd32a')
        mock_uuid4.return_value = mock_uuid

        populator = EventKnowledgeGraphPopulator('coffee_data_categorical.xlsx', 0, 1, 3, 4, 5)
        populator.output_populated_ekg(file_name='coffee.json')

    @patch('knowledge_graph.uuid.uuid4')
    def test_populates_ds2(self, mock_uuid4):
        # Mock uuid to return a specific UUID
        mock_uuid = uuid.UUID('15ff57e6-4e3d-4bc3-869a-738ba23dd32a')
        mock_uuid4.return_value = mock_uuid

        populator = EventKnowledgeGraphPopulator('smart_meter_3-5_logs.xlsx', 0, 1, 3, 4, 5)
        populator.output_populated_ekg(file_name='smart_meter.json')
