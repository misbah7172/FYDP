import csv
from datetime import datetime

class TaskController:
    def __init__(self, db):
        self.db = db
    
    def add_task(self, title, description, start_date, deadline, status, fydp_phase):
        if not title:
            return False, "Title is required"
        query = "INSERT INTO tasks (title, description, start_date, deadline, status, fydp_phase) VALUES (?, ?, ?, ?, ?, ?)"
        success = self.db.execute_query(query, (title, description, start_date, deadline, status, fydp_phase))
        return success, "Task added successfully" if success else "Failed to add task"
    
    def get_all_tasks(self):
        query = "SELECT * FROM tasks ORDER BY deadline"
        return self.db.fetch_all(query)
    
    def get_task_by_id(self, task_id):
        query = "SELECT * FROM tasks WHERE task_id = ?"
        return self.db.fetch_one(query, (task_id,))
    
    def update_task(self, task_id, title, description, start_date, deadline, status, fydp_phase):
        if not title:
            return False, "Title is required"
        query = "UPDATE tasks SET title=?, description=?, start_date=?, deadline=?, status=?, fydp_phase=? WHERE task_id=?"
        success = self.db.execute_query(query, (title, description, start_date, deadline, status, fydp_phase, task_id))
        return success, "Task updated successfully" if success else "Failed to update task"
    
    def delete_task(self, task_id):
        query = "DELETE FROM tasks WHERE task_id = ?"
        success = self.db.execute_query(query, (task_id,))
        return success, "Task deleted successfully" if success else "Failed to delete task"
    
    def search_tasks(self, search_term):
        query = "SELECT * FROM tasks WHERE title LIKE ? OR description LIKE ? ORDER BY deadline"
        return self.db.fetch_all(query, (f'%{search_term}%', f'%{search_term}%'))
    
    def get_tasks_by_phase(self, phase):
        query = "SELECT * FROM tasks WHERE fydp_phase = ? ORDER BY deadline"
        return self.db.fetch_all(query, (phase,))
    
    def get_tasks_by_status(self, status):
        query = "SELECT * FROM tasks WHERE status = ? ORDER BY deadline"
        return self.db.fetch_all(query, (status,))
    
    def get_task_stats(self):
        total = self.db.fetch_one("SELECT COUNT(*) FROM tasks")[0]
        completed = self.db.fetch_one("SELECT COUNT(*) FROM tasks WHERE status='Completed'")[0]
        in_progress = self.db.fetch_one("SELECT COUNT(*) FROM tasks WHERE status='In Progress'")[0]
        not_started = self.db.fetch_one("SELECT COUNT(*) FROM tasks WHERE status='Not Started'")[0]
        blocked = self.db.fetch_one("SELECT COUNT(*) FROM tasks WHERE status='Blocked'")[0]
        return {
            'total': total,
            'completed': completed,
            'in_progress': in_progress,
            'not_started': not_started,
            'blocked': blocked,
            'pending': total - completed
        }
    
    def get_upcoming_deadlines(self, limit=5):
        today = datetime.now().strftime('%Y-%m-%d')
        query = "SELECT * FROM tasks WHERE deadline >= ? AND status != 'Completed' ORDER BY deadline LIMIT ?"
        return self.db.fetch_all(query, (today, limit))
    
    def export_to_csv(self, filename):
        tasks = self.get_all_tasks()
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'Title', 'Description', 'Start Date', 'Deadline', 'Status', 'FYDP Phase'])
                for task in tasks:
                    formatted_task = [
                        task[0],
                        task[1] if task[1] else '',
                        task[2] if task[2] else '',
                        f"'{task[3]}" if task[3] else '',
                        f"'{task[4]}" if task[4] else '',
                        task[5] if task[5] else '',
                        task[6] if task[6] else ''
                    ]
                    writer.writerow(formatted_task)
            return True, "Exported successfully"
        except Exception as e:
            return False, f"Export failed: {str(e)}"
