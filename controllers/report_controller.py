class ReportController:
    def __init__(self, db):
        self.db = db
    
    def add_report(self, date, work_done, problems_faced, next_action, time_spent):
        if not date:
            return False, "Date is required"
        try:
            time_spent_float = float(time_spent) if time_spent else 0.0
        except ValueError:
            return False, "Invalid time spent value"
        
        query = "INSERT INTO reports (date, work_done, problems_faced, next_action, time_spent) VALUES (?, ?, ?, ?, ?)"
        success = self.db.execute_query(query, (date, work_done, problems_faced, next_action, time_spent_float))
        return success, "Report added successfully" if success else "Failed to add report"
    
    def get_all_reports(self):
        query = "SELECT * FROM reports ORDER BY date DESC"
        return self.db.fetch_all(query)
    
    def get_report_by_id(self, report_id):
        query = "SELECT * FROM reports WHERE report_id = ?"
        return self.db.fetch_one(query, (report_id,))
    
    def update_report(self, report_id, date, work_done, problems_faced, next_action, time_spent):
        if not date:
            return False, "Date is required"
        try:
            time_spent_float = float(time_spent) if time_spent else 0.0
        except ValueError:
            return False, "Invalid time spent value"
        
        query = "UPDATE reports SET date=?, work_done=?, problems_faced=?, next_action=?, time_spent=? WHERE report_id=?"
        success = self.db.execute_query(query, (date, work_done, problems_faced, next_action, time_spent_float, report_id))
        return success, "Report updated successfully" if success else "Failed to update report"
    
    def delete_report(self, report_id):
        query = "DELETE FROM reports WHERE report_id = ?"
        success = self.db.execute_query(query, (report_id,))
        return success, "Report deleted successfully" if success else "Failed to delete report"
    
    def search_reports(self, search_term):
        query = "SELECT * FROM reports WHERE work_done LIKE ? OR problems_faced LIKE ? ORDER BY date DESC"
        return self.db.fetch_all(query, (f'%{search_term}%', f'%{search_term}%'))
