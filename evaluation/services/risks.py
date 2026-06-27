class RiskService:
    @staticmethod
    def extract_risks(overall_assessment, recommendation_summary, roadmap):
        risks = []
        if recommendation_summary.critical_count > 0:
            risks.append({"source": "recommendations", "description": f"{recommendation_summary.critical_count} critical recommendations pending."})
            
        if hasattr(roadmap, 'progress') and roadmap.progress.blocked_tasks > 0:
            risks.append({"source": "roadmap", "description": f"{roadmap.progress.blocked_tasks} tasks blocked on execution roadmap."})
            
        if overall_assessment.overall_score < 50:
            risks.append({"source": "assessment", "description": "Overall fundamentals require significant improvement."})
            
        return risks