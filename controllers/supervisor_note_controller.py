class SupervisorNoteController:
    def __init__(self, db):
        self.db = db
    
    def add_note(self, date, meeting_notes, assigned_tasks):
        if not date:
            return False, "Date is required"
        query = "INSERT INTO supervisor_notes (date, meeting_notes, assigned_tasks) VALUES (?, ?, ?)"
        success = self.db.execute_query(query, (date, meeting_notes, assigned_tasks))
        return success, "Supervisor note added successfully" if success else "Failed to add note"
    
    def get_all_notes(self):
        query = "SELECT * FROM supervisor_notes ORDER BY date DESC"
        return self.db.fetch_all(query)
    
    def get_note_by_id(self, note_id):
        query = "SELECT * FROM supervisor_notes WHERE note_id = ?"
        return self.db.fetch_one(query, (note_id,))
    
    def update_note(self, note_id, date, meeting_notes, assigned_tasks):
        if not date:
            return False, "Date is required"
        query = "UPDATE supervisor_notes SET date=?, meeting_notes=?, assigned_tasks=? WHERE note_id=?"
        success = self.db.execute_query(query, (date, meeting_notes, assigned_tasks, note_id))
        return success, "Supervisor note updated successfully" if success else "Failed to update note"
    
    def delete_note(self, note_id):
        query = "DELETE FROM supervisor_notes WHERE note_id = ?"
        success = self.db.execute_query(query, (note_id,))
        return success, "Supervisor note deleted successfully" if success else "Failed to delete note"
    
    def search_notes(self, search_term):
        query = "SELECT * FROM supervisor_notes WHERE meeting_notes LIKE ? OR assigned_tasks LIKE ? ORDER BY date DESC"
        return self.db.fetch_all(query, (f'%{search_term}%', f'%{search_term}%'))
