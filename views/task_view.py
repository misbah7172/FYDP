import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from tkcalendar import DateEntry

class TaskView(tk.Frame):
    def __init__(self, parent, task_controller):
        super().__init__(parent)
        self.task_controller = task_controller
        self.configure(bg='#f0f0f0')
        self.selected_task_id = None
        self.create_widgets()
        self.refresh_task_list()
    
    def create_widgets(self):
        title = tk.Label(self, text="Task Management", font=('Arial', 18, 'bold'), bg='#f0f0f0')
        title.pack(pady=10)
        
        search_frame = tk.Frame(self, bg='#f0f0f0')
        search_frame.pack(pady=5, fill='x', padx=10)
        
        tk.Label(search_frame, text="Search:", bg='#f0f0f0').pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side='left', padx=5)
        
        tk.Button(search_frame, text="Search", command=self.search_tasks, bg='#2196F3', fg='white').pack(side='left', padx=5)
        tk.Button(search_frame, text="Clear", command=self.refresh_task_list, bg='#9E9E9E', fg='white').pack(side='left', padx=5)
        tk.Button(search_frame, text="Export CSV", command=self.export_csv, bg='#FF9800', fg='white').pack(side='left', padx=5)
        
        filter_frame = tk.Frame(self, bg='#f0f0f0')
        filter_frame.pack(pady=5, fill='x', padx=10)
        
        tk.Label(filter_frame, text="Filter by Status:", bg='#f0f0f0').pack(side='left', padx=5)
        self.status_filter = ttk.Combobox(filter_frame, values=['All', 'Not Started', 'In Progress', 'Completed', 'Blocked'], width=15)
        self.status_filter.set('All')
        self.status_filter.pack(side='left', padx=5)
        self.status_filter.bind('<<ComboboxSelected>>', lambda e: self.filter_tasks())
        
        tk.Label(filter_frame, text="Filter by Phase:", bg='#f0f0f0').pack(side='left', padx=5)
        self.phase_filter = ttk.Combobox(filter_frame, values=['All', 'FYDP1', 'FYDP2', 'FYDP3'], width=15)
        self.phase_filter.set('All')
        self.phase_filter.pack(side='left', padx=5)
        self.phase_filter.bind('<<ComboboxSelected>>', lambda e: self.filter_tasks())
        
        tree_frame = tk.Frame(self, bg='#f0f0f0')
        tree_frame.pack(pady=10, fill='both', expand=True, padx=10)
        
        columns = ('ID', 'Title', 'Start Date', 'Deadline', 'Status', 'Phase')
        self.task_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
        
        widths = [50, 200, 100, 100, 100, 80]
        for col, width in zip(columns, widths):
            self.task_tree.heading(col, text=col)
            self.task_tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        
        self.task_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.task_tree.bind('<<TreeviewSelect>>', self.on_task_select)
        
        form_frame = tk.LabelFrame(self, text="Task Details", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        form_frame.pack(pady=10, fill='x', padx=10)
        
        tk.Label(form_frame, text="Title:", bg='#f0f0f0').grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.title_entry = tk.Entry(form_frame, width=40)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=3, sticky='ew')
        
        tk.Label(form_frame, text="Description:", bg='#f0f0f0').grid(row=1, column=0, sticky='ne', padx=5, pady=5)
        self.desc_text = tk.Text(form_frame, width=40, height=4)
        self.desc_text.grid(row=1, column=1, padx=5, pady=5, columnspan=3, sticky='ew')
        
        tk.Label(form_frame, text="Start Date:", bg='#f0f0f0').grid(row=2, column=0, sticky='e', padx=5, pady=5)
        date_frame_start = tk.Frame(form_frame, bg='#f0f0f0')
        date_frame_start.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.start_date_entry = DateEntry(date_frame_start, width=18, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.start_date_entry.pack()
        
        tk.Label(form_frame, text="Deadline:", bg='#f0f0f0').grid(row=2, column=2, sticky='e', padx=5, pady=5)
        date_frame_deadline = tk.Frame(form_frame, bg='#f0f0f0')
        date_frame_deadline.grid(row=2, column=3, padx=5, pady=5, sticky='w')
        self.deadline_entry = DateEntry(date_frame_deadline, width=18, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.deadline_entry.pack()
        
        tk.Label(form_frame, text="Status:", bg='#f0f0f0').grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.status_combo = ttk.Combobox(form_frame, values=['Not Started', 'In Progress', 'Completed', 'Blocked'], width=17)
        self.status_combo.set('Not Started')
        self.status_combo.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        
        tk.Label(form_frame, text="Phase:", bg='#f0f0f0').grid(row=3, column=2, sticky='e', padx=5, pady=5)
        self.phase_combo = ttk.Combobox(form_frame, values=['FYDP1', 'FYDP2', 'FYDP3'], width=17)
        self.phase_combo.set('FYDP1')
        self.phase_combo.grid(row=3, column=3, padx=5, pady=5, sticky='w')
        
        button_frame = tk.Frame(self, bg='#f0f0f0')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Add Task", command=self.add_task, bg='#4CAF50', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(button_frame, text="Update Task", command=self.update_task, bg='#2196F3', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(button_frame, text="Delete Task", command=self.delete_task, bg='#f44336', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(button_frame, text="Clear Form", command=self.clear_form, bg='#9E9E9E', fg='white', width=12).pack(side='left', padx=5)
    
    def refresh_task_list(self):
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        tasks = self.task_controller.get_all_tasks()
        for task in tasks:
            self.task_tree.insert('', 'end', values=(task[0], task[1], task[3], task[4], task[5], task[6]))
    
    def search_tasks(self):
        search_term = self.search_var.get()
        if not search_term:
            self.refresh_task_list()
            return
        
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        tasks = self.task_controller.search_tasks(search_term)
        for task in tasks:
            self.task_tree.insert('', 'end', values=(task[0], task[1], task[3], task[4], task[5], task[6]))
    
    def filter_tasks(self):
        status = self.status_filter.get()
        phase = self.phase_filter.get()
        
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        if status == 'All' and phase == 'All':
            tasks = self.task_controller.get_all_tasks()
        elif status != 'All' and phase == 'All':
            tasks = self.task_controller.get_tasks_by_status(status)
        elif status == 'All' and phase != 'All':
            tasks = self.task_controller.get_tasks_by_phase(phase)
        else:
            all_tasks = self.task_controller.get_all_tasks()
            tasks = [t for t in all_tasks if t[5] == status and t[6] == phase]
        
        for task in tasks:
            self.task_tree.insert('', 'end', values=(task[0], task[1], task[3], task[4], task[5], task[6]))
    
    def on_task_select(self, event):
        selection = self.task_tree.selection()
        if selection:
            item = self.task_tree.item(selection[0])
            task_id = item['values'][0]
            task = self.task_controller.get_task_by_id(task_id)
            
            if task:
                self.selected_task_id = task[0]
                self.title_entry.delete(0, tk.END)
                self.title_entry.insert(0, task[1])
                
                self.desc_text.delete('1.0', tk.END)
                self.desc_text.insert('1.0', task[2] or '')
                
                if task[3]:
                    try:
                        self.start_date_entry.set_date(task[3])
                    except:
                        pass
                
                if task[4]:
                    try:
                        self.deadline_entry.set_date(task[4])
                    except:
                        pass
                
                self.status_combo.set(task[5])
                self.phase_combo.set(task[6])
    
    def add_task(self):
        title = self.title_entry.get().strip()
        description = self.desc_text.get('1.0', tk.END).strip()
        start_date = self.start_date_entry.get_date().strftime('%Y-%m-%d')
        deadline = self.deadline_entry.get_date().strftime('%Y-%m-%d')
        status = self.status_combo.get()
        phase = self.phase_combo.get()
        
        success, message = self.task_controller.add_task(title, description, start_date, deadline, status, phase)
        
        if success:
            messagebox.showinfo("Success", message)
            self.refresh_task_list()
            self.clear_form()
        else:
            messagebox.showerror("Error", message)
    
    def update_task(self):
        if not self.selected_task_id:
            messagebox.showwarning("Warning", "Please select a task to update")
            return
        
        title = self.title_entry.get().strip()
        description = self.desc_text.get('1.0', tk.END).strip()
        start_date = self.start_date_entry.get_date().strftime('%Y-%m-%d')
        deadline = self.deadline_entry.get_date().strftime('%Y-%m-%d')
        status = self.status_combo.get()
        phase = self.phase_combo.get()
        
        success, message = self.task_controller.update_task(self.selected_task_id, title, description, start_date, deadline, status, phase)
        
        if success:
            messagebox.showinfo("Success", message)
            self.refresh_task_list()
            self.clear_form()
        else:
            messagebox.showerror("Error", message)
    
    def delete_task(self):
        if not self.selected_task_id:
            messagebox.showwarning("Warning", "Please select a task to delete")
            return
        
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?")
        if confirm:
            success, message = self.task_controller.delete_task(self.selected_task_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_task_list()
                self.clear_form()
            else:
                messagebox.showerror("Error", message)
    
    def clear_form(self):
        self.selected_task_id = None
        self.title_entry.delete(0, tk.END)
        self.desc_text.delete('1.0', tk.END)
        self.start_date_entry.set_date(datetime.now())
        self.deadline_entry.set_date(datetime.now())
        self.status_combo.set('Not Started')
        self.phase_combo.set('FYDP1')
    
    def export_csv(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            success, message = self.task_controller.export_to_csv(filename)
            if success:
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)
