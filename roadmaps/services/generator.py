import logging
from django.db import transaction
from startup_ideas.models import StartupIdea
from ..models import Roadmap, RoadmapTask, TaskTemplate
from ..constants import RoadmapStatus
from .resolver import RecommendationResolverService
from .task_generation import TaskGenerationService
from .dependency import DependencyGraphService
from .scheduling import SchedulingService
from .summary import SummaryService

logger = logging.getLogger(__name__)

class RoadmapGenerationService:
    @staticmethod
    def generate_roadmap(idea: StartupIdea) -> Roadmap:
        try:
            # 1. Resolve Recommendations
            active_recs = RecommendationResolverService.resolve_active(idea)
            
            # Versioning for fallback or normal
            last_roadmap = Roadmap.objects.filter(startup_idea=idea).order_by('-version').first()
            next_version = 1 if not last_roadmap else last_roadmap.version + 1
            
            if not active_recs:
                logger.warning(f"No active recommendations to plan for idea {idea.id}.")
                return Roadmap.objects.create(
                    startup_idea=idea,
                    version=next_version,
                    status=RoadmapStatus.ACTIVE,
                    summary="No active recommendations available to generate tasks."
                )
                
            # 2. Task Generation (Prototypes)
            prototypes = TaskGenerationService.generate_prototypes(active_recs)
            if not prototypes:
                logger.warning(f"No active task templates found for the given recommendations for idea {idea.id}.")
                return Roadmap.objects.create(
                    startup_idea=idea,
                    version=next_version,
                    status=RoadmapStatus.ACTIVE,
                    summary="No active templates available to generate tasks."
                )
                
            with transaction.atomic():
                # 3. Supersede old roadmaps
                Roadmap.objects.filter(startup_idea=idea, status=RoadmapStatus.ACTIVE).update(status=RoadmapStatus.SUPERSEDED)
                
                # Versioning
                last_roadmap = Roadmap.objects.filter(startup_idea=idea).order_by('-version').first()
                next_version = 1 if not last_roadmap else last_roadmap.version + 1
                
                # 4. Build and Validate DAG
                dag = DependencyGraphService.build_and_validate(prototypes)
                
                # 5. Scheduling
                sorted_templates = SchedulingService.schedule(dag)
                
                # 6. Create Roadmap
                roadmap = Roadmap.objects.create(
                    startup_idea=idea,
                    version=next_version,
                    status=RoadmapStatus.ACTIVE
                )
                
                # Map templates to their corresponding recommendations
                template_to_rec = {t.id: r for r, t in prototypes}
                
                # 7. Create RoadmapTasks
                task_map = {}
                execution_order = 1
                
                # Simple scheduling assumption for now to satisfy fields
                current_day = 1
                
                for template in sorted_templates:
                    rec = template_to_rec.get(template.id)
                    
                    # Inherit priority from recommendation, fallback to template default
                    priority = rec.priority if rec else template.default_priority
                    
                    task = RoadmapTask.objects.create(
                        roadmap=roadmap,
                        recommendation=rec,
                        recommendation_title_snapshot=rec.matched_rule.title if (rec and rec.matched_rule) else "",
                        recommendation_priority_snapshot=rec.priority if rec else "",
                        task_template=template,
                        phase=template.default_phase,
                        dependency_level=0, # Simplified for now, real calculation would use DAG depth
                        execution_order=execution_order,
                        title=template.title,
                        description=template.description,
                        estimated_days=template.estimated_days,
                        scheduled_start_day=current_day,
                        scheduled_end_day=current_day + template.estimated_days - 1,
                        priority=priority
                    )
                    task_map[template.id] = task
                    execution_order += 1
                    current_day += template.estimated_days
                    
                # 8. Attach Dependencies (now that all tasks exist)
                for template in sorted_templates:
                    task = task_map[template.id]
                    for dep_template in template.depends_on.all():
                        if dep_template.id in task_map:
                            task.dependencies.add(task_map[dep_template.id])
                            
                # 9. Generate Summary
                SummaryService.generate_summary(roadmap)
                
                return roadmap
                
        except Exception as e:
            logger.error(f"Error generating roadmap for idea {idea.id}: {e}")
            raise
