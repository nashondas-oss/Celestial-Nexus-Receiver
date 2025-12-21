# user_state.py

from datetime import datetime
from typing import List, Optional

class UserState:
    def __init__(self, user_id: str, state: str, last_updated: Optional[datetime] = None):
        self.user_id = user_id
        self.state = state
        self.last_updated = last_updated or datetime.utcnow()

    def update_state(self, new_state: str):
        self.state = new_state
        self.last_updated = datetime.utcnow()

class AssessmentResult:
    def __init__(self, assessment_id: str, user_id: str, score: float, max_score: float):
        self.assessment_id = assessment_id
        self.user_id = user_id
        self.score = score
        self.max_score = max_score

    def percentage(self) -> float:
        return (self.score / self.max_score) * 100

class AssessmentHistory:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.assessments: List[AssessmentResult] = []

    def add_assessment(self, assessment: AssessmentResult):
        self.assessments.append(assessment)

    def get_latest_assessment(self) -> Optional[AssessmentResult]:
        return self.assessments[-1] if self.assessments else None