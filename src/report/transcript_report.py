from core.report import Report
class TranscriptReport(Report):
    def __init__(self,student):
        super().__init__(f"Transcript - {student.name}")
        self