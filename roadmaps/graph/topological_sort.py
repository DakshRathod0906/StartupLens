from typing import List, Dict
from collections import deque
from .dag import DAG, Node

class TopologicalSorter:
    @staticmethod
    def sort(dag: DAG) -> List[Node]:
        """
        Performs Kahn's algorithm for topological sorting.
        Returns nodes in execution order (dependencies first).
        """
        in_degree: Dict[int, int] = {}
        for node in dag.get_nodes():
            in_degree[node.template.id] = len(node.dependencies)
            
        queue = deque()
        for node_id, count in in_degree.items():
            if count == 0:
                queue.append(dag.nodes[node_id])
                
        sorted_nodes = []
        
        while queue:
            # For stable tie-breaking, we could sort the queue by priority here, 
            # but the SchedulingService will handle priority ordering within levels.
            # Here we just want a valid topological sort.
            
            node = queue.popleft()
            sorted_nodes.append(node)
            
            for dependent in node.dependents:
                in_degree[dependent.template.id] -= 1
                if in_degree[dependent.template.id] == 0:
                    queue.append(dependent)
                    
        return sorted_nodes
