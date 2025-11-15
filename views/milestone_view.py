import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

class MilestoneView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#f0f0f0')
        self.selected_milestone_id = None
        self.create_widgets()
        self.refresh_milestone_list()
    
    def create_widgets(self):
        title = tk.Label(self, text="Milestone Tracker", font=('Arial', 18, 'bold'), bg='#f0f0f0')
        title.pack(pady=10)
        
        search_frame = tk.Frame(self, bg='#f0f0f0')
        search_frame.pack(pady=5, fill='x', padx=10)
        
        tk.Label(search_frame, text="Search:", bg='#f0f0f0').pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side='left', padx=5)
        tk.Button(search_frame, text="Search", command=self.search_milestones, bg='#2196F3', fg='white').pack(side='left', padx=5)
        tk.Button(search_frame, text="Clear", command=self.refresh_milestone_list, bg='#9E9E9E', fg='white').pack(side='left', padx=5)
        tk.Button(search_frame, text="Export CSV", command=self.export_csv, bg='#FF9800', fg='white').pack(side='left', padx=5)
        
        tk.Label(search_frame, text="Filter Phase:", bg='#f0f0f0').pack(side='left', padx=10)
        self.phase_filter = ttk.Combobox(search_frame, values=['All', 'FYDP1', 'FYDP2', 'FYDP3'], width=10)
        self.phase_filter.set('All')
        self.phase_filter.pack(side='left', padx=5)
        self.phase_filter.bind('<<ComboboxSelected>>', lambda e: self.filter_milestones())
        
        tree_frame = tk.Frame(self, bg='#f0f0f0')
        tree_frame.pack(pady=10, fill='both', expand=True, padx=10)
        
        columns = ('ID', 'Phase', 'Title', 'Submission Date')
        self.milestone_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        
        widths = [50, 80, 350, 120]
        for col, width in zip(columns, widths):
            self.milestone_tree.heading(col, text=col)
            self.milestone_tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.milestone_tree.yview)
        self.milestone_tree.configure(yscrollcommand=scrollbar.set)
        
        self.milestone_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        self.milestone_tree.bind('<<TreeviewSelect>>', self.on_milestone_select)
        
        form_frame = tk.LabelFrame(self, text="Milestone Details", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        form_frame.pack(pady=10, fill='x', padx=10)
        
        tk.Label(form_frame, text="Phase:", bg='#f0f0f0').grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.phase_combo = ttk.Combobox(form_frame, values=['FYDP1', 'FYDP2', 'FYDP3'], width=17)
        self.phase_combo.set('FYDP1')
        self.phase_combo.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        tk.Label(form_frame, text="Title:", bg='#f0f0f0').grid(row=0, column=2, sticky='e', padx=5, pady=5)
        self.title_entry = tk.Entry(form_frame, width=30)
        self.title_entry.grid(row=0, column=3, padx=5, pady=5, sticky='ew')
        
        tk.Label(form_frame, text="Expected Output:", bg='#f0f0f0').grid(row=1, column=0, sticky='ne', padx=5, pady=5)
        self.expected_text = tk.Text(form_frame, width=50, height=3)
        self.expected_text.grid(row=1, column=1, padx=5, pady=5, columnspan=3, sticky='ew')
        
        tk.Label(form_frame, text="Actual Output:", bg='#f0f0f0').grid(row=2, column=0, sticky='ne', padx=5, pady=5)
        self.actual_text = tk.Text(form_frame, width=50, height=3)
        self.actual_text.grid(row=2, column=1, padx=5, pady=5, columnspan=3, sticky='ew')
        
        tk.Label(form_frame, text="Submission Date:", bg='#f0f0f0').grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.submission_entry = tk.Entry(form_frame, width=20)
        self.submission_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        
        tk.Label(form_frame, text="Comments:", bg='#f0f0f0').grid(row=4, column=0, sticky='ne', padx=5, pady=5)
        self.comments_text = tk.Text(form_frame, width=50, height=3)
        self.comments_text.grid(row=4, column=1, padx=5, pady=5, columnspan=3, sticky='ew')
        
        button_frame = tk.Frame(self, bg='#f0f0f0')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Add Milestone", command=self.add_milestone, bg='#4CAF50', fg='white', width=14).pack(side='left', padx=5)
        tk.Button(button_frame, text="Update Milestone", command=self.update_milestone, bg='#2196F3', fg='white', width=14).pack(side='left', padx=5)
        tk.Button(button_frame, text="Delete Milestone", command=self.delete_milestone, bg='#f44336', fg='white', width=14).pack(side='left', padx=5)
        tk.Button(button_frame, text="Clear Form", command=self.clear_form, bg='#9E9E9E', fg='white', width=14).pack(side='left', padx=5)
    
    def refresh_milestone_list(self):
        for item in self.milestone_tree.get_children():
            self.milestone_tree.delete(item)
        
        milestones = self.controller.get_all_milestones()
        for milestone in milestones:
            self.milestone_tree.insert('', 'end', values=(milestone[0], milestone[1], milestone[2], milestone[5]))
    
    def search_milestones(self):
        search_term = self.search_var.get()
        if not search_term:
            self.refresh_milestone_list()
            return
        
        for item in self.milestone_tree.get_children():
            self.milestone_tree.delete(item)
        
        milestones = self.controller.search_milestones(search_term)
        for milestone in milestones:
            self.milestone_tree.insert('', 'end', values=(milestone[0], milestone[1], milestone[2], milestone[5]))
    
    def filter_milestones(self):
        phase = self.phase_filter.get()
        
        for item in self.milestone_tree.get_children():
            self.milestone_tree.delete(item)
        
        if phase == 'All':
            milestones = self.controller.get_all_milestones()
        else:
            milestones = self.controller.get_milestones_by_phase(phase)
        
        for milestone in milestones:
            self.milestone_tree.insert('', 'end', values=(milestone[0], milestone[1], milestone[2], milestone[5]))
    
    def on_milestone_select(self, event):
        selection = self.milestone_tree.selection()
        if selection:
            item = self.milestone_tree.item(selection[0])
            milestone_id = item['values'][0]
            milestone = self.controller.get_milestone_by_id(milestone_id)
            
            if milestone:
                self.selected_milestone_id = milestone[0]
                self.phase_combo.set(milestone[1])
                
                self.title_entry.delete(0, tk.END)
                self.title_entry.insert(0, milestone[2])
                
                self.expected_text.delete('1.0', tk.END)
                self.expected_text.insert('1.0', milestone[3] or '')
                
                self.actual_text.delete('1.0', tk.END)
                self.actual_text.insert('1.0', milestone[4] or '')
                
                self.submission_entry.delete(0, tk.END)
                self.submission_entry.insert(0, milestone[5] or '')
                
                self.comments_text.delete('1.0', tk.END)
                self.comments_text.insert('1.0', milestone[6] or '')
    
    def add_milestone(self):
        phase = self.phase_combo.get()
        title = self.title_entry.get().strip()
        expected = self.expected_text.get('1.0', tk.END).strip()
        actual = self.actual_text.get('1.0', tk.END).strip()
        submission = self.submission_entry.get().strip()
        comments = self.comments_text.get('1.0', tk.END).strip()
        
        success, message = self.controller.add_milestone(phase, title, expected, actual, submission, comments)
        
        if success:
            messagebox.showinfo("Success", message)
            self.refresh_milestone_list()
            self.clear_form()
        else:
            messagebox.showerror("Error", message)
    
    def update_milestone(self):
        if not self.selected_milestone_id:
            messagebox.showwarning("Warning", "Please select a milestone to update")
            return
        
        phase = self.phase_combo.get()
        title = self.title_entry.get().strip()
        expected = self.expected_text.get('1.0', tk.END).strip()
        actual = self.actual_text.get('1.0', tk.END).strip()
        submission = self.submission_entry.get().strip()
        comments = self.comments_text.get('1.0', tk.END).strip()
        
        success, message = self.controller.update_milestone(self.selected_milestone_id, phase, title, expected, actual, submission, comments)
        
        if success:
            messagebox.showinfo("Success", message)
            self.refresh_milestone_list()
            self.clear_form()
        else:
            messagebox.showerror("Error", message)
    
    def delete_milestone(self):
        if not self.selected_milestone_id:
            messagebox.showwarning("Warning", "Please select a milestone to delete")
            return
        
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this milestone?")
        if confirm:
            success, message = self.controller.delete_milestone(self.selected_milestone_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_milestone_list()
                self.clear_form()
            else:
                messagebox.showerror("Error", message)
    
    def clear_form(self):
        self.selected_milestone_id = None
        self.phase_combo.set('FYDP1')
        self.title_entry.delete(0, tk.END)
        self.expected_text.delete('1.0', tk.END)
        self.actual_text.delete('1.0', tk.END)
        self.submission_entry.delete(0, tk.END)
        self.comments_text.delete('1.0', tk.END)
    
    def export_csv(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            success, message = self.controller.export_to_csv(filename)
            if success:
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)
