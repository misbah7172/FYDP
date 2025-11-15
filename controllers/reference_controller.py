class ReferenceController:
    def __init__(self, db):
        self.db = db
    
    def add_reference(self, link, title, summary, relevance):
        if not title:
            return False, "Title is required"
        query = 'INSERT INTO "references" (link, title, summary, relevance) VALUES (?, ?, ?, ?)'
        success = self.db.execute_query(query, (link, title, summary, relevance))
        return success, "Reference added successfully" if success else "Failed to add reference"
    
    def get_all_references(self):
        query = 'SELECT * FROM "references"'
        return self.db.fetch_all(query)
    
    def get_reference_by_id(self, ref_id):
        query = 'SELECT * FROM "references" WHERE ref_id = ?'
        return self.db.fetch_one(query, (ref_id,))
    
    def update_reference(self, ref_id, link, title, summary, relevance):
        if not title:
            return False, "Title is required"
        query = 'UPDATE "references" SET link=?, title=?, summary=?, relevance=? WHERE ref_id=?'
        success = self.db.execute_query(query, (link, title, summary, relevance, ref_id))
        return success, "Reference updated successfully" if success else "Failed to update reference"
    
    def delete_reference(self, ref_id):
        query = 'DELETE FROM "references" WHERE ref_id = ?'
        success = self.db.execute_query(query, (ref_id,))
        return success, "Reference deleted successfully" if success else "Failed to delete reference"
    
    def search_references(self, search_term):
        query = 'SELECT * FROM "references" WHERE title LIKE ? OR summary LIKE ? OR relevance LIKE ?'
        return self.db.fetch_all(query, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
