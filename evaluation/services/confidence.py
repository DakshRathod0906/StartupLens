from decimal import Decimal

class ConfidenceService:
    @staticmethod
    def calculate_confidence(overall_assessment, recommendation_summary, roadmap):
        # Research Coverage = 30%
        # Assessment Completeness = 30%
        # Recommendation Coverage = 20%
        # Roadmap Coverage = 20%
        
        # Simplified for now. Should calculate based on number of insights/findings etc.
        research_coverage = 80.0
        assessment_completeness = 90.0
        recommendation_coverage = 85.0
        roadmap_coverage = 75.0
        
        confidence = (
            (research_coverage * 0.3) +
            (assessment_completeness * 0.3) +
            (recommendation_coverage * 0.2) +
            (roadmap_coverage * 0.2)
        )
        
        return Decimal(str(round(confidence, 2)))