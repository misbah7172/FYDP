class Report:
    def __init__(self, report_id=None, date="", work_done="", problems_faced="", next_action="", time_spent=0.0):
        self.report_id = report_id
        self.date = date
        self.work_done = work_done
        self.problems_faced = problems_faced
        self.next_action = next_action
        self.time_spent = time_spent
    
    def to_tuple(self):
        return (self.date, self.work_done, self.problems_faced, self.next_action, self.time_spent)
    
    def to_tuple_with_id(self):
        return (self.date, self.work_done, self.problems_faced, self.next_action, self.time_spent, self.report_id)
    
    @staticmethod
    def from_tuple(data):
        if data:
            return Report(data[0], data[1], data[2], data[3], data[4], data[5])
        return None
