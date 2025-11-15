import tkinter as tk
from tkinter import ttk
from database import Database
from controllers.task_controller import TaskController
from controllers.learning_log_controller import LearningLogController
from controllers.milestone_controller import MilestoneController
from controllers.report_controller import ReportController
from controllers.document_controller import DocumentController
from controllers.supervisor_note_controller import SupervisorNoteController
from controllers.reference_controller import ReferenceController
from views.dashboard_view import DashboardView
from views.task_view import TaskView
from views.learning_log_view import LearningLogView
from views.milestone_view import MilestoneView
from views.report_view import ReportView
from views.document_view import DocumentView
from views.supervisor_note_view import SupervisorNoteView
from views.reference_view import ReferenceView

class FYDPTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FYDP Progress Tracker")
        self.root.geometry("1200x750")
        self.root.configure(bg='#f0f0f0')
        
        self.db = Database()
        
        self.task_controller = TaskController(self.db)
        self.learning_log_controller = LearningLogController(self.db)
        self.milestone_controller = MilestoneController(self.db)
        self.report_controller = ReportController(self.db)
        self.document_controller = DocumentController(self.db)
        self.supervisor_note_controller = SupervisorNoteController(self.db)
        self.reference_controller = ReferenceController(self.db)
        
        self.current_view = None
        
        self.create_ui()
        
        self.show_dashboard()
    
    def create_ui(self):
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True)
        
        sidebar = tk.Frame(main_container, bg='#2c3e50', width=200)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)
        
        header = tk.Label(sidebar, text="FYDP Tracker", font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white', pady=20)
        header.pack()
        
        menu_items = [
            ("Dashboard", self.show_dashboard),
            ("Tasks", self.show_tasks),
            ("Learning Log", self.show_learning_log),
            ("Milestones", self.show_milestones),
            ("Reports", self.show_reports),
            ("Documents", self.show_documents),
            ("Supervisor Notes", self.show_supervisor_notes),
            ("Research References", self.show_references)
        ]
        
        for item_text, command in menu_items:
            btn = tk.Button(sidebar, text=item_text, command=command, bg='#34495e', fg='white', 
                          font=('Arial', 11), bd=0, padx=20, pady=12, anchor='w', 
                          activebackground='#1abc9c', activeforeground='white', cursor='hand2')
            btn.pack(fill='x', pady=2, padx=10)
            btn.bind('<Enter>', lambda e, b=btn: b.configure(bg='#1abc9c'))
            btn.bind('<Leave>', lambda e, b=btn: b.configure(bg='#34495e'))
        
        self.content_frame = tk.Frame(main_container, bg='#f0f0f0')
        self.content_frame.pack(side='right', fill='both', expand=True)
    
    def clear_content(self):
        if self.current_view:
            self.current_view.destroy()
            self.current_view = None
    
    def show_dashboard(self):
        self.clear_content()
        self.current_view = DashboardView(self.content_frame, self.task_controller)
        self.current_view.pack(fill='both', expand=True)
    
    def show_tasks(self):
        self.clear_content()
        self.current_view = TaskView(self.content_frame, self.task_controller)
        self.current_view.pack(fill='both', expand=True)
    
    def show_learning_log(self):
        self.clear_content()
        self.current_view = LearningLogView(self.content_frame, self.learning_log_controller)
        self.current_view.pack(fill='both', expand=True)
    
    def show_milestones(self):
        self.clear_content()
        self.current_view = MilestoneView(self.content_frame, self.milestone_controller)
        self.current_view.pack(fill='both', expand=True)
    
    def show_reports(self):
        self.clear_content()
        self.current_view = ReportView(self.content_frame, self.report_controller)
        self.current_view.pack(fill='both', expand=True)
    
    def show_documents(self):
        self.clear_content()
        self.current_view = DocumentView(self.content_frame, self.document_controller)
        self.current_view.pack(fill='both', expand=True)
    
    def show_supervisor_notes(self):
        self.clear_content()
        self.current_view = SupervisorNoteView(self.content_frame, self.supervisor_note_controller)
        self.current_view.pack(fill='both', expand=True)
    
    def show_references(self):
        self.clear_content()
        self.current_view = ReferenceView(self.content_frame, self.reference_controller)
        self.current_view.pack(fill='both', expand=True)
    
    def on_closing(self):
        self.db.close()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = FYDPTrackerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
