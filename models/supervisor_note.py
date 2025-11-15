class SupervisorNote:
    def __init__(self, note_id=None, date="", meeting_notes="", assigned_tasks=""):
        self.note_id = note_id
        self.date = date
        self.meeting_notes = meeting_notes
        self.assigned_tasks = assigned_tasks
    
    def to_tuple(self):
        return (self.date, self.meeting_notes, self.assigned_tasks)
    
    def to_tuple_with_id(self):
        return (self.date, self.meeting_notes, self.assigned_tasks, self.note_id)
    
    @staticmethod
    def from_tuple(data):
        if data:
            return SupervisorNote(data[0], data[1], data[2], data[3])
        return None
