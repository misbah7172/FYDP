class Task:
    def __init__(self, task_id=None, title="", description="", start_date="", deadline="", status="Not Started", fydp_phase="FYDP1"):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.start_date = start_date
        self.deadline = deadline
        self.status = status
        self.fydp_phase = fydp_phase
    
    def to_tuple(self):
        return (self.title, self.description, self.start_date, self.deadline, self.status, self.fydp_phase)
    
    def to_tuple_with_id(self):
        return (self.title, self.description, self.start_date, self.deadline, self.status, self.fydp_phase, self.task_id)
    
    @staticmethod
    def from_tuple(data):
        if data:
            return Task(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
        return None
