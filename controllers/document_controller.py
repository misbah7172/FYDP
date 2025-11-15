class DocumentController:
    def __init__(self, db):
        self.db = db
    
    def add_document(self, doc_name, version, updated_date, file_path, submission_status):
        if not doc_name:
            return False, "Document name is required"
        query = "INSERT INTO documents (doc_name, version, updated_date, file_path, submission_status) VALUES (?, ?, ?, ?, ?)"
        success = self.db.execute_query(query, (doc_name, version, updated_date, file_path, submission_status))
        return success, "Document added successfully" if success else "Failed to add document"
    
    def get_all_documents(self):
        query = "SELECT * FROM documents ORDER BY updated_date DESC"
        return self.db.fetch_all(query)
    
    def get_document_by_id(self, doc_id):
        query = "SELECT * FROM documents WHERE doc_id = ?"
        return self.db.fetch_one(query, (doc_id,))
    
    def update_document(self, doc_id, doc_name, version, updated_date, file_path, submission_status):
        if not doc_name:
            return False, "Document name is required"
        query = "UPDATE documents SET doc_name=?, version=?, updated_date=?, file_path=?, submission_status=? WHERE doc_id=?"
        success = self.db.execute_query(query, (doc_name, version, updated_date, file_path, submission_status, doc_id))
        return success, "Document updated successfully" if success else "Failed to update document"
    
    def delete_document(self, doc_id):
        query = "DELETE FROM documents WHERE doc_id = ?"
        success = self.db.execute_query(query, (doc_id,))
        return success, "Document deleted successfully" if success else "Failed to delete document"
    
    def search_documents(self, search_term):
        query = "SELECT * FROM documents WHERE doc_name LIKE ? ORDER BY updated_date DESC"
        return self.db.fetch_all(query, (f'%{search_term}%',))
