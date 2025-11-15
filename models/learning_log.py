class LearningLog:
    def __init__(self, log_id=None, date="", what_i_learned="", source="", tags="", relevance_to_project=""):
        self.log_id = log_id
        self.date = date
        self.what_i_learned = what_i_learned
        self.source = source
        self.tags = tags
        self.relevance_to_project = relevance_to_project
    
    def to_tuple(self):
        return (self.date, self.what_i_learned, self.source, self.tags, self.relevance_to_project)
    
    def to_tuple_with_id(self):
        return (self.date, self.what_i_learned, self.source, self.tags, self.relevance_to_project, self.log_id)
    
    @staticmethod
    def from_tuple(data):
        if data:
            return LearningLog(data[0], data[1], data[2], data[3], data[4], data[5])
        return None
