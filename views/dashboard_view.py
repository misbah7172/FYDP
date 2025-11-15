import tkinter as tk
from tkinter import ttk
from datetime import datetime

class DashboardView(tk.Frame):
    def __init__(self, parent, task_controller):
        super().__init__(parent)
        self.task_controller = task_controller
        self.configure(bg='#f0f0f0')
        self.create_widgets()
    
    def create_widgets(self):
        title = tk.Label(self, text="FYDP Progress Dashboard", font=('Arial', 20, 'bold'), bg='#f0f0f0')
        title.pack(pady=20)
        
        stats_frame = tk.Frame(self, bg='#f0f0f0')
        stats_frame.pack(pady=10, fill='x', padx=20)
        
        self.total_label = tk.Label(stats_frame, text="Total Tasks: 0", font=('Arial', 12), bg='#f0f0f0')
        self.total_label.grid(row=0, column=0, padx=20, pady=5, sticky='w')
        
        self.completed_label = tk.Label(stats_frame, text="Completed: 0", font=('Arial', 12), bg='#f0f0f0')
        self.completed_label.grid(row=0, column=1, padx=20, pady=5, sticky='w')
        
        self.pending_label = tk.Label(stats_frame, text="Pending: 0", font=('Arial', 12), bg='#f0f0f0')
        self.pending_label.grid(row=1, column=0, padx=20, pady=5, sticky='w')
        
        self.progress_label = tk.Label(stats_frame, text="Progress: 0%", font=('Arial', 12), bg='#f0f0f0')
        self.progress_label.grid(row=1, column=1, padx=20, pady=5, sticky='w')
        
        progress_frame = tk.Frame(self, bg='#f0f0f0')
        progress_frame.pack(pady=10, fill='x', padx=20)
        
        tk.Label(progress_frame, text="Overall Progress:", font=('Arial', 12), bg='#f0f0f0').pack(anchor='w')
        self.progress_bar = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress_bar.pack(pady=5, fill='x')
        
        deadlines_frame = tk.LabelFrame(self, text="Upcoming Deadlines", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        deadlines_frame.pack(pady=20, fill='both', expand=True, padx=20)
        
        columns = ('Title', 'Deadline', 'Status', 'Phase')
        self.deadlines_tree = ttk.Treeview(deadlines_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.deadlines_tree.heading(col, text=col)
            self.deadlines_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(deadlines_frame, orient='vertical', command=self.deadlines_tree.yview)
        self.deadlines_tree.configure(yscrollcommand=scrollbar.set)
        
        self.deadlines_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        refresh_btn = tk.Button(self, text="Refresh Dashboard", command=self.refresh_dashboard, 
                               bg='#4CAF50', fg='white', font=('Arial', 10), padx=20, pady=5)
        refresh_btn.pack(pady=10)
        
        self.refresh_dashboard()
    
    def refresh_dashboard(self):
        stats = self.task_controller.get_task_stats()
        
        self.total_label.config(text=f"Total Tasks: {stats['total']}")
        self.completed_label.config(text=f"Completed: {stats['completed']}")
        self.pending_label.config(text=f"Pending: {stats['pending']}")
        
        progress = int((stats['completed'] / stats['total'] * 100) if stats['total'] > 0 else 0)
        self.progress_label.config(text=f"Progress: {progress}%")
        self.progress_bar['value'] = progress
        
        for item in self.deadlines_tree.get_children():
            self.deadlines_tree.delete(item)
        
        upcoming = self.task_controller.get_upcoming_deadlines(10)
        for task in upcoming:
            self.deadlines_tree.insert('', 'end', values=(task[1], task[4], task[5], task[6]))
