class Document:
    def __init__(self, doc_id=None, doc_name="", version="", updated_date="", file_path="", submission_status=""):
        self.doc_id = doc_id
        self.doc_name = doc_name
        self.version = version
        self.updated_date = updated_date
        self.file_path = file_path
        self.submission_status = submission_status
    
    def to_tuple(self):
        return (self.doc_name, self.version, self.updated_date, self.file_path, self.submission_status)
    
    def to_tuple_with_id(self):
        return (self.doc_name, self.version, self.updated_date, self.file_path, self.submission_status, self.doc_id)
    
    @staticmethod
    def from_tuple(data):
        if data:
            return Document(data[0], data[1], data[2], data[3], data[4], data[5])
        return None
