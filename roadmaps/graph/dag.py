from typing import List, Dict, Set
from dataclasses import dataclass
from ..models import TaskTemplate

@dataclass
class Node:
    template: TaskTemplate
    dependencies: List['Node']
    dependents: List['Node']
    
    def __hash__(self):
        return hash(self.template.id)
        
    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.template.id == other.template.id

class DAG:
    def __init__(self, templates: List[TaskTemplate]):
        self.nodes: Dict[int, Node] = {}
        self._build_graph(templates)

    def _build_graph(self, templates: List[TaskTemplate]):
        # Initialize nodes
        for t in templates:
            self.nodes[t.id] = Node(template=t, dependencies=[], dependents=[])
            
        # Build edges based on depends_on
        # template.depends_on means this template depends on those other templates to be finished first.
        # So dependency -> dependent
        for t in templates:
            node = self.nodes[t.id]
            for dep_t in t.depends_on.all():
                if dep_t.id in self.nodes:
                    dep_node = self.nodes[dep_t.id]
                    node.dependencies.append(dep_node)
                    dep_node.dependents.append(node)

    def get_nodes(self) -> List[Node]:
        return list(self.nodes.values())
