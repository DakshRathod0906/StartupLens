from typing import Set, List
from .dag import DAG, Node
from ..exceptions import CircularDependencyError

class GraphValidator:
    @staticmethod
    def validate(dag: DAG):
        """
        Validates the DAG for cycles using DFS.
        Raises CircularDependencyError if a cycle is detected.
        """
        visited: Set[int] = set()
        rec_stack: Set[int] = set()
        
        def dfs(node: Node) -> bool:
            visited.add(node.template.id)
            rec_stack.add(node.template.id)
            
            for dependent in node.dependents:
                if dependent.template.id not in visited:
                    if dfs(dependent):
                        return True
                elif dependent.template.id in rec_stack:
                    return True
                    
            rec_stack.remove(node.template.id)
            return False

        for node in dag.get_nodes():
            if node.template.id not in visited:
                if dfs(node):
                    raise CircularDependencyError("Cycle detected in dependency graph.")
