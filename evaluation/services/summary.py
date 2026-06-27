class SummaryService:
    @staticmethod
    def generate_summary(readiness_level, strengths, risks):
        if readiness_level == "INVESTMENT_READY":
            base = "Startup demonstrates strong fundamentals and is ready for investment or major scaling."
        elif readiness_level == "PROMISING":
            base = "Startup shows significant potential but requires focused execution on critical tasks."
        elif readiness_level == "EARLY_STAGE":
            base = "Startup is in early stages of validation. Significant foundational work remains."
        else:
            base = "Startup is not currently ready for external evaluation and must resolve fundamental risks."
            
        strength_text = f" Key strengths include {len(strengths)} major areas." if strengths else ""
        risk_text = f" However, {len(risks)} critical risk factors must be addressed." if risks else ""
        
        return f"{base}{strength_text}{risk_text}"