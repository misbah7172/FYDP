import csv

class MilestoneController:
    def __init__(self, db):
        self.db = db
    
    def add_milestone(self, phase, milestone_title, expected_output, actual_output, submission_date, comments):
        if not milestone_title:
            return False, "Milestone title is required"
        query = "INSERT INTO milestones (phase, milestone_title, expected_output, actual_output, submission_date, comments) VALUES (?, ?, ?, ?, ?, ?)"
        success = self.db.execute_query(query, (phase, milestone_title, expected_output, actual_output, submission_date, comments))
        return success, "Milestone added successfully" if success else "Failed to add milestone"
    
    def get_all_milestones(self):
        query = "SELECT * FROM milestones ORDER BY submission_date"
        return self.db.fetch_all(query)
    
    def get_milestone_by_id(self, milestone_id):
        query = "SELECT * FROM milestones WHERE milestone_id = ?"
        return self.db.fetch_one(query, (milestone_id,))
    
    def update_milestone(self, milestone_id, phase, milestone_title, expected_output, actual_output, submission_date, comments):
        if not milestone_title:
            return False, "Milestone title is required"
        query = "UPDATE milestones SET phase=?, milestone_title=?, expected_output=?, actual_output=?, submission_date=?, comments=? WHERE milestone_id=?"
        success = self.db.execute_query(query, (phase, milestone_title, expected_output, actual_output, submission_date, comments, milestone_id))
        return success, "Milestone updated successfully" if success else "Failed to update milestone"
    
    def delete_milestone(self, milestone_id):
        query = "DELETE FROM milestones WHERE milestone_id = ?"
        success = self.db.execute_query(query, (milestone_id,))
        return success, "Milestone deleted successfully" if success else "Failed to delete milestone"
    
    def search_milestones(self, search_term):
        query = "SELECT * FROM milestones WHERE milestone_title LIKE ? OR expected_output LIKE ? ORDER BY submission_date"
        return self.db.fetch_all(query, (f'%{search_term}%', f'%{search_term}%'))
    
    def get_milestones_by_phase(self, phase):
        query = "SELECT * FROM milestones WHERE phase = ? ORDER BY submission_date"
        return self.db.fetch_all(query, (phase,))
    
    def export_to_csv(self, filename):
        milestones = self.get_all_milestones()
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'Phase', 'Title', 'Expected Output', 'Actual Output', 'Submission Date', 'Comments'])
                for milestone in milestones:
                    formatted_milestone = [
                        milestone[0],
                        milestone[1] if milestone[1] else '',
                        milestone[2] if milestone[2] else '',
                        milestone[3] if milestone[3] else '',
                        milestone[4] if milestone[4] else '',
                        f"'{milestone[5]}" if milestone[5] else '',
                        milestone[6] if milestone[6] else ''
                    ]
                    writer.writerow(formatted_milestone)
            return True, "Exported successfully"
        except Exception as e:
            return False, f"Export failed: {str(e)}"
