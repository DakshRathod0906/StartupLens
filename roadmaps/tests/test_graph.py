from django.test import TestCase
from recommendations.models import RecommendationRule
from roadmaps.models import TaskTemplate
from roadmaps.graph.dag import DAG
from roadmaps.graph.validation import GraphValidator
from roadmaps.graph.topological_sort import TopologicalSorter
from roadmaps.exceptions import CircularDependencyError

class GraphTests(TestCase):
    def setUp(self):
        # Create some mock rules to satisfy TaskTemplate requirements
        self.rule1 = RecommendationRule.objects.create(metric="foo", operator="EQ", priority="HIGH", rule_group="MARKET", title="m1", display_order=1)
        self.rule2 = RecommendationRule.objects.create(metric="foo", operator="EQ", priority="HIGH", rule_group="MARKET", title="m2", display_order=2)
        self.rule3 = RecommendationRule.objects.create(metric="foo", operator="EQ", priority="HIGH", rule_group="MARKET", title="m3", display_order=3)
        
        self.t1 = TaskTemplate.objects.create(recommendation_rule=self.rule1, title="Task 1", estimated_days=1)
        self.t2 = TaskTemplate.objects.create(recommendation_rule=self.rule2, title="Task 2", estimated_days=2)
        self.t3 = TaskTemplate.objects.create(recommendation_rule=self.rule3, title="Task 3", estimated_days=3)
        
    def test_dag_creation_and_topological_sort(self):
        # t3 depends on t2, t2 depends on t1
        self.t2.depends_on.add(self.t1)
        self.t3.depends_on.add(self.t2)
        
        dag = DAG([self.t1, self.t2, self.t3])
        
        # Validate should pass silently
        GraphValidator.validate(dag)
        
        # Sort
        sorted_nodes = TopologicalSorter.sort(dag)
        self.assertEqual(len(sorted_nodes), 3)
        self.assertEqual(sorted_nodes[0].template.id, self.t1.id)
        self.assertEqual(sorted_nodes[1].template.id, self.t2.id)
        self.assertEqual(sorted_nodes[2].template.id, self.t3.id)

    def test_circular_dependency_detection(self):
        # t1 -> t2 -> t3 -> t1
        self.t2.depends_on.add(self.t1)
        self.t3.depends_on.add(self.t2)
        self.t1.depends_on.add(self.t3)
        
        dag = DAG([self.t1, self.t2, self.t3])
        
        with self.assertRaises(CircularDependencyError):
            GraphValidator.validate(dag)
