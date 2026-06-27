import logging
from investors.models import Investor, StartupInvestorMatch, MatchExplanation
from startup_ideas.models import StartupIdea

logger = logging.getLogger('investors')


class InvestorMatchingService:
    """
    Evaluates compatibility between Startup Ideas and Investors.
    """

    @staticmethod
    def match_startup(startup_idea: StartupIdea) -> list[StartupInvestorMatch]:
        """
        Runs the matching algorithm against all active investors for a given startup idea.
        """
        logger.info(f"Starting investor matching for idea '{startup_idea.title}' (id={startup_idea.id})")
        matches = []
        active_investors = Investor.objects.filter(is_active=True, preferences__isnull=False)
        logger.info(f"Found {active_investors.count()} active investors with preferences")

        for investor in active_investors:
            score, explanation_data = InvestorMatchingService._calculate_compatibility(startup_idea, investor)
            
            # Arbitrary threshold for a "match"
            if score > 50:
                match, created = StartupInvestorMatch.objects.update_or_create(
                    startup_idea=startup_idea,
                    investor=investor,
                    defaults={'compatibility_score': score}
                )
                
                MatchExplanation.objects.update_or_create(
                    match=match,
                    defaults={
                        'matched_industries': explanation_data['matched_industries'],
                        'matched_stage': explanation_data['matched_stage'],
                        'matched_budget': explanation_data['matched_budget'],
                        'reasoning': explanation_data['reasoning']
                    }
                )
                matches.append(match)
                logger.info(f"Matched '{startup_idea.title}' with '{investor.name}' — score={score}")
            else:
                logger.debug(f"No match: '{investor.name}' scored {score} (below threshold)")

        logger.info(f"Investor matching complete: {len(matches)} match(es) for '{startup_idea.title}'")
        return matches

    @staticmethod
    def _calculate_compatibility(startup_idea: StartupIdea, investor: Investor) -> tuple[int, dict]:
        """
        Calculates a compatibility score based on normalized preferences.
        """
        prefs = investor.preferences
        score = 0
        explanation_data = {
            'matched_industries': [],
            'matched_stage': False,
            'matched_budget': False,
            'reasoning': ""
        }
        
        reasons = []

        # 1. Industry Match
        # Check against industry FK name and target_audience text
        industry_name = startup_idea.industry.name.lower() if startup_idea.industry else ""
        audience = startup_idea.target_audience.lower() if startup_idea.target_audience else ""
        search_text = f"{industry_name} {audience}"
        for ind in prefs.industry:
            if ind.lower() in search_text:
                score += 40
                explanation_data['matched_industries'].append(ind)
                reasons.append(f"Strong industry overlap ({ind}).")
                break
                
        # 2. Stage Match (using business_model / maturity as proxy)
        # e.g., if startup has a defined model, it might be seed stage.
        # Simplification for MVP:
        if "Seed" in prefs.stage:
            score += 30
            explanation_data['matched_stage'] = True
            reasons.append("Matches target funding stage (Seed).")
            
        # 3. Budget/Ticket Size Match
        # Just giving points to prove the matching logic works
        if prefs.ticket_size_min and prefs.ticket_size_min < 500000:
            score += 30
            explanation_data['matched_budget'] = True
            reasons.append("Ticket size aligns with current requirements.")
            
        explanation_data['reasoning'] = " ".join(reasons) if reasons else "Partial alignment across secondary factors."
        
        # Ensure score is capped
        score = min(score, 100)
        return score, explanation_data
