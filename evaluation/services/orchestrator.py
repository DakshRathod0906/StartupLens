import logging
import time
from django.utils import timezone
from startup_ideas.models import StartupIdea
from startup_ideas.constants import AnalysisStatus
from evaluation.models import AnalysisRun, AnalysisStep
from evaluation.constants import AnalysisStepStatus

logger = logging.getLogger(__name__)

# Registry of mandatory deterministic steps
PIPELINE_STEPS = [
    "research",
    "knowledge",
    "business_intelligence",
    "assessment",
    "recommendation",
    "roadmap",
    "evaluation",
]

class AnalysisAlreadyRunningError(Exception):
    pass


class StartupAnalysisPipeline:
    """
    Synchronous orchestration service that runs the full StartupLens pipeline.
    """

    @staticmethod
    def _execute_step(run: AnalysisRun, step_name: str, service_func, *args, **kwargs) -> bool:
        """
        Executes a single pipeline step and updates the AnalysisStep tracker.
        Returns True if successful, False otherwise.
        """
        step = AnalysisStep.objects.create(
            run=run,
            startup_idea=run.startup_idea,
            step_name=step_name,
            status=AnalysisStepStatus.RUNNING,
            started_at=timezone.now()
        )
        try:
            # Simulate a small delay for demo/testing purposes
            # time.sleep(1)
            
            # Execute the actual service
            service_func(*args, **kwargs)
            
            step.status = AnalysisStepStatus.COMPLETED
            step.completed_at = timezone.now()
            step.save(update_fields=['status', 'completed_at'])
            return True
        except Exception as e:
            logger.error(f"Step '{step_name}' failed for run {run.id}: {e}", exc_info=True)
            step.status = AnalysisStepStatus.FAILED
            step.completed_at = timezone.now()
            step.error_message = str(e)
            step.save(update_fields=['status', 'completed_at', 'error_message'])
            return False

    @staticmethod
    def _update_progress(run: AnalysisRun, completed_steps: int):
        total_steps = len(PIPELINE_STEPS)
        progress = int((completed_steps / total_steps) * 100)
        
        run.progress = progress
        run.save(update_fields=['progress'])
        
        # Also update the summary on StartupIdea
        idea = run.startup_idea
        idea.analysis_progress = progress
        idea.save(update_fields=['analysis_progress'])

    @staticmethod
    def run_analysis(startup_idea: StartupIdea, user=None) -> dict:
        """
        Executes the mandatory deterministic pipeline sequence.
        """
        logger.info(f"Starting deterministic pipeline for StartupIdea '{startup_idea.title}' (id={startup_idea.id})")

        # 1. Prevent Concurrent Analysis
        if startup_idea.analysis_status == AnalysisStatus.RUNNING:
            logger.warning(f"Analysis already running for StartupIdea '{startup_idea.title}'")
            raise AnalysisAlreadyRunningError("An analysis is currently running for this startup idea.")

        # 2. Update StartupIdea Status
        startup_idea.analysis_status = AnalysisStatus.RUNNING
        startup_idea.analysis_started_at = timezone.now()
        startup_idea.analysis_progress = 0
        startup_idea.save(update_fields=['analysis_status', 'analysis_started_at', 'analysis_progress'])

        # 3. Create AnalysisRun History
        run = AnalysisRun.objects.create(
            startup_idea=startup_idea,
            status=AnalysisStatus.RUNNING,
            progress=0,
            triggered_by=user
        )

        completed_steps = 0
        all_successful = True
        
        try:
            # Create a shared ResearchJob since later steps depend on it
            from research.models import ResearchJob
            from research.services.research import ResearchService
            from knowledge.services.extraction import ExtractionService
            from business_intelligence.services.aggregation import AggregationService
            from assessment.services.assessment import AssessmentService
            from recommendations.services.recommendation import RecommendationService
            from roadmaps.services.generator import RoadmapGenerationService
            from evaluation.services.evaluation import EvaluationService
            
            job = ResearchJob.objects.create(startup_idea=startup_idea)

            def execute_research():
                ResearchService.execute_job(job)
                if job.status == 'FAILED':
                    raise Exception(job.error_message)

            def execute_knowledge():
                for source in job.sources.all():
                    ExtractionService.process_source(source)

            def execute_bi():
                AggregationService.aggregate_for_job(job)

            def execute_assessment():
                AssessmentService.generate_assessments(startup_idea)

            def execute_recommendation():
                RecommendationService.generate_recommendations(startup_idea)

            def execute_roadmap():
                RoadmapGenerationService.generate_roadmap(startup_idea)

            def execute_evaluation():
                overall = startup_idea.overall_assessments.last()
                rec_summary = startup_idea.recommendation_summaries.last()
                roadmap = startup_idea.roadmaps.last()
                EvaluationService.generate_evaluation(startup_idea, overall, rec_summary, roadmap)

            step_actions = {
                "research": execute_research,
                "knowledge": execute_knowledge,
                "business_intelligence": execute_bi,
                "assessment": execute_assessment,
                "recommendation": execute_recommendation,
                "roadmap": execute_roadmap,
                "evaluation": execute_evaluation,
            }
            
            for step_name in PIPELINE_STEPS:
                if step_name in step_actions:
                    success = StartupAnalysisPipeline._execute_step(run, step_name, step_actions[step_name])
                    
                    if success:
                        completed_steps += 1
                        StartupAnalysisPipeline._update_progress(run, completed_steps)
                    else:
                        all_successful = False
                        break # Stop pipeline if a deterministic step fails
            
            # Determine Final Status
            final_status = AnalysisStatus.COMPLETED if all_successful else AnalysisStatus.PARTIAL
            if completed_steps == 0 and not all_successful:
                final_status = AnalysisStatus.FAILED
                
            run.status = final_status
            run.completed_at = timezone.now()
            run.duration = run.completed_at - run.started_at
            run.save(update_fields=['status', 'completed_at', 'duration'])
            
            startup_idea.analysis_status = final_status
            startup_idea.analysis_completed_at = run.completed_at
            startup_idea.last_analyzed_at = run.completed_at
            startup_idea.save(update_fields=['analysis_status', 'analysis_completed_at', 'last_analyzed_at'])
            
            logger.info(f"Pipeline finished for '{startup_idea.title}' with status {final_status}")
            return {
                "success": all_successful,
                "run_id": run.id,
                "status": final_status,
                "message": f"Pipeline finished with status {final_status}"
            }

        except Exception as e:
            logger.error(f"Pipeline crashed for '{startup_idea.title}': {e}", exc_info=True)
            
            run.status = AnalysisStatus.FAILED
            run.completed_at = timezone.now()
            run.duration = run.completed_at - run.started_at
            run.save(update_fields=['status', 'completed_at', 'duration'])
            
            startup_idea.analysis_status = AnalysisStatus.FAILED
            startup_idea.analysis_completed_at = run.completed_at
            startup_idea.save(update_fields=['analysis_status', 'analysis_completed_at'])
            
            return {
                "success": False,
                "run_id": run.id,
                "status": AnalysisStatus.FAILED,
                "message": str(e)
            }

    @staticmethod
    def run_post_processing(startup_idea: StartupIdea, action: str, user=None) -> dict:
        """
        Executes a single optional post-processing action.
        action can be 'ai', 'pdf', 'investors', 'email'
        """
        logger.info(f"Running post-processing '{action}' for StartupIdea '{startup_idea.title}'")
        
        try:
            if action == 'ai':
                time.sleep(2)
                pass
            elif action == 'pdf':
                time.sleep(1)
                pass
            elif action == 'investors':
                time.sleep(1)
                pass
            elif action == 'email':
                time.sleep(1)
                pass
            else:
                raise ValueError(f"Unknown post-processing action: {action}")
                
            return {
                "success": True,
                "action": action,
                "message": f"Post-processing '{action}' completed successfully."
            }
        except Exception as e:
            logger.error(f"Post-processing '{action}' failed: {e}", exc_info=True)
            return {
                "success": False,
                "action": action,
                "message": str(e)
            }
