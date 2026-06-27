class StrengthService:
    @staticmethod
    def extract_strengths(overall_assessment, recommendation_summary):
        strengths = []
        # Extract from top assessment categories
        # Placeholder for real logic
        strengths.append({"source": "assessment", "description": "Strong market potential identified."})
        if recommendation_summary.completed_count > 0:
            strengths.append({"source": "recommendations", "description": f"{recommendation_summary.completed_count} critical recommendations already completed."})
        
        return strengths