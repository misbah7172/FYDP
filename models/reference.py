class Reference:
    def __init__(self, ref_id=None, link="", title="", summary="", relevance=""):
        self.ref_id = ref_id
        self.link = link
        self.title = title
        self.summary = summary
        self.relevance = relevance
    
    def to_tuple(self):
        return (self.link, self.title, self.summary, self.relevance)
    
    def to_tuple_with_id(self):
        return (self.link, self.title, self.summary, self.relevance, self.ref_id)
    
    @staticmethod
    def from_tuple(data):
        if data:
            return Reference(data[0], data[1], data[2], data[3], data[4])
        return None
