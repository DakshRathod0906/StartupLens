from typing import List, Tuple
from ..graph.dag import DAG
from ..graph.validation import GraphValidator
from ..models import TaskTemplate
from recommendations.models import Recommendation

class DependencyGraphService:
    @staticmethod
    def build_and_validate(prototypes: List[Tuple[Recommendation, TaskTemplate]]) -> DAG:
        """
        Takes prototypes, extracts the templates, builds the DAG, and validates it.
        Raises CircularDependencyError if cycles are present.
        """
        templates = [t for r, t in prototypes]
        
        # Build DAG
        dag = DAG(templates)
        
        # Validate (throws on error)
        GraphValidator.validate(dag)
        
        return dag
