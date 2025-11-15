class Milestone:
    def __init__(self, milestone_id=None, phase="FYDP1", milestone_title="", expected_output="", actual_output="", submission_date="", comments=""):
        self.milestone_id = milestone_id
        self.phase = phase
        self.milestone_title = milestone_title
        self.expected_output = expected_output
        self.actual_output = actual_output
        self.submission_date = submission_date
        self.comments = comments
    
    def to_tuple(self):
        return (self.phase, self.milestone_title, self.expected_output, self.actual_output, self.submission_date, self.comments)
    
    def to_tuple_with_id(self):
        return (self.phase, self.milestone_title, self.expected_output, self.actual_output, self.submission_date, self.comments, self.milestone_id)
    
    @staticmethod
    def from_tuple(data):
        if data:
            return Milestone(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
        return None
