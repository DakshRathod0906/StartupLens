from typing import List, Tuple, Dict
from ..graph.dag import DAG, Node
from ..graph.topological_sort import TopologicalSorter
from ..models import TaskTemplate, RoadmapTask, RoadmapPhase
from recommendations.constants import RecommendationPriority

class SchedulingService:
    @staticmethod
    def _priority_weight(priority: str) -> int:
        weights = {
            RecommendationPriority.CRITICAL: 5,
            RecommendationPriority.HIGH: 4,
            RecommendationPriority.MEDIUM: 3,
            RecommendationPriority.LOW: 2,
            RecommendationPriority.OPTIONAL: 1
        }
        return weights.get(priority, 0)
        
    @staticmethod
    def _phase_weight(phase: str) -> int:
        weights = {
            RoadmapPhase.IMMEDIATE: 1,
            RoadmapPhase.SHORT_TERM: 2,
            RoadmapPhase.MEDIUM_TERM: 3,
            RoadmapPhase.LONG_TERM: 4
        }
        return weights.get(phase, 99)

    @staticmethod
    def schedule(dag: DAG) -> List[TaskTemplate]:
        """
        Sorts nodes using Topological Sort.
        Dependencies always take precedence. Priority resolves ties within the topological layers.
        We achieve this by first doing a standard topological sort, but sorting the queue by priority.
        """
        # A simple priority-aware topological sort
        from collections import deque
        
        in_degree: Dict[int, int] = {}
        for node in dag.get_nodes():
            in_degree[node.template.id] = len(node.dependencies)
            
        # We need a stable queue that sorts by priority
        # Python's deque doesn't sort automatically. We can use a standard list and sort it each time,
        # or use a priority queue (heapq), but since the queue sizes are small, sorting a list is fine.
        queue = []
        for node_id, count in in_degree.items():
            if count == 0:
                queue.append(dag.nodes[node_id])
                
        sorted_templates = []
        
        while queue:
            # Sort queue: higher priority weight first, then phase weight (earlier phases first)
            queue.sort(
                key=lambda n: (
                    SchedulingService._priority_weight(n.template.priority if hasattr(n.template, 'priority') else n.template.default_priority),
                    -SchedulingService._phase_weight(n.template.default_phase)
                ), 
                reverse=True
            )
            
            node = queue.pop(0)
            sorted_templates.append(node.template)
            
            for dependent in node.dependents:
                in_degree[dependent.template.id] -= 1
                if in_degree[dependent.template.id] == 0:
                    queue.append(dependent)
                    
        return sorted_templates
