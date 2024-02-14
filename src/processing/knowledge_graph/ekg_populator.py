import numpy as np
import pandas as pd

from processing.knowledge_graph.event_knowledge_graph import EventKnowledgeGraph
from processing.knowledge_graph.kg_enums import Relationships


class EventKnowledgeGraphPopulator:

    def __init__(self, path: str,
                 trace_column: int,
                 id_column: int,
                 label_column: int,
                 att_key_column: int,
                 att_val_column: int):
        """
        A Populator instance that populates an Event Knowledge Graph.
        :param path: The path of the dataset to be used for the population.
        :param trace_column: Integer of the column containing trace ids.
        :param id_column: Integer of the column containing event ids.
        :param label_column: Integer of the column containing event labels.
        :param att_key_column: Integer of the column containing event attribute keys.
        :param att_val_column: Integer of the column containing event attribute values.
        """
        self.__event_kg = EventKnowledgeGraph()
        self.__df = pd.read_excel(path)
        self.populate_ekg(trace_column, id_column, label_column, att_key_column, att_val_column)

    @property
    def get_df(self) -> pd.DataFrame:
        """
        Getter for this Populator's Dataframe.
        :return: Populator's Dataframe.
        """
        return self.__df

    @property
    def get_event_kg(self) -> EventKnowledgeGraph:
        """
        Getter for this Populator's Event Knowledge Graph.
        :return: Populator's Knowledge Graph.
        """
        return self.__event_kg

    def populate_ekg(self,
                     trace_column: int,
                     id_column: int,
                     label_column: int,
                     att_key_column: int,
                     att_val_column: int) -> None:
        """
        Method to instruct the Populator to use the dataset to populate the internal Event Knowledge Graph.
        :param trace_column: Number of the column containing trace ids.
        :param id_column: Number of the column containing event ids.
        :param label_column: Number of the column containing event labels.
        :param att_key_column: Number of the column containing event attribute keys.
        :param att_val_column: Number of the column containing event attribute values.
        """

        previous_id = -1
        previous_trace = -1
        for row_index in range(len(self.get_df)):
            # Get event data and add node
            trace_id = self.get_df.iloc[row_index, trace_column]
            event_id = self.get_df.iloc[row_index, id_column]
            if isinstance(event_id, np.integer):
                event_id = int(event_id)
            if isinstance(trace_id, np.integer):
                trace_id = int(trace_id)
            label = self.get_df.iloc[row_index, label_column]
            att = self.parse_attribute(self.get_df.iloc[row_index, att_key_column],
                                       self.get_df.iloc[row_index, att_val_column])

            # Add the node
            if trace_id not in self.get_event_kg.get_nodes or event_id not in self.get_event_kg.get_nodes[trace_id]:
                self.get_event_kg.add_node(trace_id, label, att, event_id)

            # If event is directly followed, then add the relationship
            if trace_id == previous_trace:
                # Check for repetitive labels
                if (trace_id in self.get_event_kg.get_nodes and
                        self.get_event_kg.get_nodes[trace_id][previous_id]['label'] == label):
                    curr_idx = row_index + 1
                    while self.get_df.iloc[curr_idx, label_column] == label:
                        curr_idx += 1
                    curr_id = int(self.get_df.iloc[curr_idx, id_column])
                    curr_trace_id = int(self.get_df.iloc[curr_idx, trace_column])
                    if curr_trace_id == trace_id:
                        if curr_id not in self.get_event_kg.get_nodes[trace_id]:
                            self.get_event_kg.add_node(curr_trace_id,
                                                       self.get_df.iloc[curr_idx, label_column],
                                                       self.parse_attribute(self.get_df.iloc[curr_idx, att_key_column],
                                                                            self.get_df.iloc[curr_idx, att_val_column]),
                                                       curr_id)
                        self.get_event_kg.add_rel(trace_id, previous_id, Relationships.DIRECTLY_FOLLOWS, curr_id)
                else:
                    self.get_event_kg.add_rel(trace_id, previous_id, Relationships.DIRECTLY_FOLLOWS, event_id)

            # Record last event and trace id
            previous_trace = trace_id
            previous_id = event_id

    @staticmethod
    def parse_attribute(key, value) -> dict:
        """
        Helper function key values of attributes.
        :param key: Dataframe entry from key cell.
        :param value: Dataframe entry from value cell.
        :return: Dictionary containing the key/values in right format.
        """
        res = {}

        # If value is an integer/float, simply parse it and return
        if isinstance(value, (int, float)):
            return {
                key: value
            }
        else:
            # In case it's not an integer/float, handle multiplicity of attributes
            key = str(key)
            value = str(value)
            attribute_keys = [keys.strip() for keys in value.split(',')] if ',' in key else [key]
            attribute_vals = [val.strip() for val in value.split(',')] if ',' in value else [value]

            # Handle not putting comma or uneven number of key/value
            if len(attribute_keys) != len(attribute_vals):
                raise ValueError("The number of attribute keys does not match the number of attribute values.")

            # Add key, value pairs to attribute dict
            for key, value in zip(attribute_keys, attribute_vals):
                res[key] = value

            return res

    def output_populated_ekg(self, path: str = 'output', file_name: str = '', indentation: int = None) -> None:
        """
        Outputs the populated Event Knowledge Graph in JSON format.
        :param path: The path for the JSON output file.
        :param file_name: Name of the output file.
        :param indentation: The desired indentation for the JSON file.
        """
        self.get_event_kg.export_kg(path=path, file_name=file_name, indentation=indentation)
