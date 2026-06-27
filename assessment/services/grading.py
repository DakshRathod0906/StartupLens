from decimal import Decimal

class GradeService:
    @staticmethod
    def get_grade(percentage: Decimal) -> str:
        """
        Maps a 0-100 percentage to a grade.
        90-100 -> A+
        80-89  -> A
        70-79  -> B
        60-69  -> C
        50-59  -> D
        Below 50 -> F
        """
        if percentage >= Decimal('90.0'):
            return "A+"
        elif percentage >= Decimal('80.0'):
            return "A"
        elif percentage >= Decimal('70.0'):
            return "B"
        elif percentage >= Decimal('60.0'):
            return "C"
        elif percentage >= Decimal('50.0'):
            return "D"
        else:
            return "F"
