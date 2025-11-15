import csv

class LearningLogController:
    def __init__(self, db):
        self.db = db
    
    def add_log(self, date, what_i_learned, source, tags, relevance_to_project):
        if not date or not what_i_learned:
            return False, "Date and learning content are required"
        query = "INSERT INTO learning_logs (date, what_i_learned, source, tags, relevance_to_project) VALUES (?, ?, ?, ?, ?)"
        success = self.db.execute_query(query, (date, what_i_learned, source, tags, relevance_to_project))
        return success, "Learning log added successfully" if success else "Failed to add log"
    
    def get_all_logs(self):
        query = "SELECT * FROM learning_logs ORDER BY date DESC"
        return self.db.fetch_all(query)
    
    def get_log_by_id(self, log_id):
        query = "SELECT * FROM learning_logs WHERE log_id = ?"
        return self.db.fetch_one(query, (log_id,))
    
    def update_log(self, log_id, date, what_i_learned, source, tags, relevance_to_project):
        if not date or not what_i_learned:
            return False, "Date and learning content are required"
        query = "UPDATE learning_logs SET date=?, what_i_learned=?, source=?, tags=?, relevance_to_project=? WHERE log_id=?"
        success = self.db.execute_query(query, (date, what_i_learned, source, tags, relevance_to_project, log_id))
        return success, "Learning log updated successfully" if success else "Failed to update log"
    
    def delete_log(self, log_id):
        query = "DELETE FROM learning_logs WHERE log_id = ?"
        success = self.db.execute_query(query, (log_id,))
        return success, "Learning log deleted successfully" if success else "Failed to delete log"
    
    def search_logs(self, search_term):
        query = "SELECT * FROM learning_logs WHERE what_i_learned LIKE ? OR tags LIKE ? ORDER BY date DESC"
        return self.db.fetch_all(query, (f'%{search_term}%', f'%{search_term}%'))
    
    def export_to_csv(self, filename):
        logs = self.get_all_logs()
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'Date', 'What I Learned', 'Source', 'Tags', 'Relevance to Project'])
                for log in logs:
                    formatted_log = [
                        log[0],
                        f"'{log[1]}" if log[1] else '',
                        log[2] if log[2] else '',
                        log[3] if log[3] else '',
                        log[4] if log[4] else '',
                        log[5] if log[5] else ''
                    ]
                    writer.writerow(formatted_log)
            return True, "Exported successfully"
        except Exception as e:
            return False, f"Export failed: {str(e)}"
