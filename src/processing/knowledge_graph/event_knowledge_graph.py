from processing.knowledge_graph.knowledge_graph import AbstractKnowledgeGraph, KGType, NodeType, Relationships


class EventKnowledgeGraph(AbstractKnowledgeGraph):
    """
    Event Knowledge Graph contains a compact amount of data which reduces the amount of redundancy.
    At current version, this Event Knowledge Graph only stores 'directly follows' relationships.
    """

    def __init__(self):
        super().__init__(kg_name='Event Knowledge Graph',
                         kg_type=KGType.EVENT_KG,
                         kg_node_type=NodeType.EVENT)

    def add_node(self,
                 trace_id: int,
                 activity_name: str,
                 attributes: dict,
                 node_id: int) -> int:
        """
        Add an event to the nodes of this Event Knowledge Graph.
        :param trace_id: The ID of the trace of this event.
        :param activity_name: The name of the activity in the event.
        :param attributes: The attributes of the event.
        :param node_id: The unique event id.
        :return: the id of the added event.
        """
        # Handle duplicated events
        if trace_id in self.get_nodes and node_id in self.get_nodes[trace_id]:
            raise KeyError('An event already exists under the provided id for this trace.')

        # If this trace has not been recorded yet
        if trace_id not in self.get_nodes:
            self.get_nodes[trace_id] = {}

        # Temp dict to store ordered event key events
        temp = {}
        # Save new node in ordered manner
        if self.get_nodes[trace_id]:
            for key in sorted(self.get_nodes[trace_id].keys()):
                if key < node_id:
                    temp[key] = self.get_nodes[trace_id][key]
                elif key == node_id:
                    continue
                else:
                    if node_id not in temp:
                        temp[node_id] = {
                            'label': activity_name,
                            'attributes': attributes,
                            'relationships': []
                        }
                    temp[key] = self.get_nodes[trace_id][key]
        if node_id not in temp:
            temp[node_id] = self.get_nodes[trace_id][node_id] = {
                'label': activity_name,
                'attributes': attributes,
                'relationships': []
            }

        # update nodes under trace with ordered keys
        self.get_nodes[trace_id] = temp

        # Update stats
        self.inc_node_count()
        return node_id

    def add_rel(self,
                trace_id: int,
                subject_id: int,
                rel_type: Relationships,
                object_id: int):
        """
        Add a relationship to the nodes of this Event Knowledge Graph.
        :param trace_id: The ID of the trace of this relationship.
        :param subject_id: The id of the leading activity.
        :param rel_type: The type of relationship of the two activities.
        :param object_id: The id of the object activity.
        :return: The id of the added relationship.
        """

        # If trace_id entry already exists:
        if trace_id in self.get_relationships[rel_type.value]:
            rel_id = len(self.get_relationships[rel_type.value][trace_id]) + 1
            # Add new relationship to existing trace id key
            self.get_relationships[rel_type.value][trace_id][rel_id] = {
                'subject': subject_id,
                'object': object_id
            }
        else:
            # Add new trace id key with first relationship
            rel_id = 1
            self.get_relationships[rel_type.value][trace_id] = {
                rel_id: {
                    'subject': subject_id,
                    'object': object_id
                }
            }

        # Record relationship on nodes
        self.get_nodes[trace_id][subject_id]['relationships'].append(rel_id)
        self.get_nodes[trace_id][object_id]['relationships'].append(rel_id)

        # Update stats
        self.inc_rel_count()
        return rel_id

    def rm_node(self, trace_id: int, node_id: int) -> dict:
        """
        Remove a node from this Event Knowledge Graph.
        :param node_id: The id of the node to be removed.
        :return: A dictionary of the deleted node.
        """
        # Handle input errors
        if not trace_id or not node_id:
            raise TypeError('Expected to receive an int value id.')
        elif trace_id not in self.get_nodes:
            raise KeyError('No events have been recorded for this trace.')
        elif node_id not in self.get_nodes[trace_id]:
            raise KeyError('No events under the provided event id.')
        # Update stats
        self.dec_node_count()

        # Remove recorded relationships as well
        for rel in self.get_nodes[trace_id][node_id]['relationships']:
            if len(self.get_relationships['directly follows'][trace_id]) == 1:
                del self.get_relationships['directly follows'][trace_id]
            else:
                del self.get_relationships['directly follows'][trace_id][rel]

        res = self.get_nodes[trace_id].pop(node_id)
        if len(self.get_nodes[trace_id]) == 0:
            del self.get_nodes[trace_id]
        return res

    def rm_rel(self, trace_id: int, rel_id: int) -> dict:
        """
        Remove a relationship from this Event Knowledge Graph.
        :param trace_id: The trace containing relationship.
        :param rel_id: The id of the relationship to be removed.
        :return: A dictionary of the deleted relationship.
        """
        # Handle input errors
        if not rel_id:
            raise TypeError('Expected to receive an int value id.')
        elif trace_id not in self.get_relationships['directly follows']:
            raise KeyError('No relationships under provided trace id.')
        elif rel_id not in self.get_relationships['directly follows'][trace_id]:
            raise KeyError('No records under provided relationship id.')
        # Update stats
        self.dec_rel_count()
        return self.get_relationships['directly follows'][trace_id].pop(rel_id)
