import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class ReportView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#f0f0f0')
        self.selected_report_id = None
        self.create_widgets()
        self.refresh_report_list()
    
    def create_widgets(self):
        title = tk.Label(self, text="Progress Reports", font=('Arial', 18, 'bold'), bg='#f0f0f0')
        title.pack(pady=10)
        
        search_frame = tk.Frame(self, bg='#f0f0f0')
        search_frame.pack(pady=5, fill='x', padx=10)
        
        tk.Label(search_frame, text="Search:", bg='#f0f0f0').pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side='left', padx=5)
        tk.Button(search_frame, text="Search", command=self.search_reports, bg='#2196F3', fg='white').pack(side='left', padx=5)
        tk.Button(search_frame, text="Clear", command=self.refresh_report_list, bg='#9E9E9E', fg='white').pack(side='left', padx=5)
        
        tree_frame = tk.Frame(self, bg='#f0f0f0')
        tree_frame.pack(pady=10, fill='both', expand=True, padx=10)
        
        columns = ('ID', 'Date', 'Work Done', 'Time Spent')
        self.report_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        
        widths = [50, 100, 450, 100]
        for col, width in zip(columns, widths):
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.report_tree.yview)
        self.report_tree.configure(yscrollcommand=scrollbar.set)
        
        self.report_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        self.report_tree.bind('<<TreeviewSelect>>', self.on_report_select)
        
        form_frame = tk.LabelFrame(self, text="Report Details", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        form_frame.pack(pady=10, fill='x', padx=10)
        
        tk.Label(form_frame, text="Date:", bg='#f0f0f0').grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.date_entry = tk.Entry(form_frame, width=20)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        tk.Label(form_frame, text="Time Spent (hrs):", bg='#f0f0f0').grid(row=0, column=2, sticky='e', padx=5, pady=5)
        self.time_entry = tk.Entry(form_frame, width=15)
        self.time_entry.grid(row=0, column=3, padx=5, pady=5, sticky='w')
        
        tk.Label(form_frame, text="Work Done:", bg='#f0f0f0').grid(row=1, column=0, sticky='ne', padx=5, pady=5)
        self.work_text = tk.Text(form_frame, width=50, height=4)
        self.work_text.grid(row=1, column=1, padx=5, pady=5, columnspan=3, sticky='ew')
        
        tk.Label(form_frame, text="Problems Faced:", bg='#f0f0f0').grid(row=2, column=0, sticky='ne', padx=5, pady=5)
        self.problems_text = tk.Text(form_frame, width=50, height=4)
        self.problems_text.grid(row=2, column=1, padx=5, pady=5, columnspan=3, sticky='ew')
        
        tk.Label(form_frame, text="Next Action:", bg='#f0f0f0').grid(row=3, column=0, sticky='ne', padx=5, pady=5)
        self.next_text = tk.Text(form_frame, width=50, height=3)
        self.next_text.grid(row=3, column=1, padx=5, pady=5, columnspan=3, sticky='ew')
        
        button_frame = tk.Frame(self, bg='#f0f0f0')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Add Report", command=self.add_report, bg='#4CAF50', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(button_frame, text="Update Report", command=self.update_report, bg='#2196F3', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(button_frame, text="Delete Report", command=self.delete_report, bg='#f44336', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(button_frame, text="Clear Form", command=self.clear_form, bg='#9E9E9E', fg='white', width=12).pack(side='left', padx=5)
    
    def refresh_report_list(self):
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        
        reports = self.controller.get_all_reports()
        for report in reports:
            work_preview = report[2][:50] + '...' if report[2] and len(report[2]) > 50 else (report[2] or '')
            self.report_tree.insert('', 'end', values=(report[0], report[1], work_preview, report[5]))
    
    def search_reports(self):
        search_term = self.search_var.get()
        if not search_term:
            self.refresh_report_list()
            return
        
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        
        reports = self.controller.search_reports(search_term)
        for report in reports:
            work_preview = report[2][:50] + '...' if report[2] and len(report[2]) > 50 else (report[2] or '')
            self.report_tree.insert('', 'end', values=(report[0], report[1], work_preview, report[5]))
    
    def on_report_select(self, event):
        selection = self.report_tree.selection()
        if selection:
            item = self.report_tree.item(selection[0])
            report_id = item['values'][0]
            report = self.controller.get_report_by_id(report_id)
            
            if report:
                self.selected_report_id = report[0]
                self.date_entry.delete(0, tk.END)
                self.date_entry.insert(0, report[1])
                
                self.work_text.delete('1.0', tk.END)
                self.work_text.insert('1.0', report[2] or '')
                
                self.problems_text.delete('1.0', tk.END)
                self.problems_text.insert('1.0', report[3] or '')
                
                self.next_text.delete('1.0', tk.END)
                self.next_text.insert('1.0', report[4] or '')
                
                self.time_entry.delete(0, tk.END)
                self.time_entry.insert(0, str(report[5]) if report[5] else '')
    
    def add_report(self):
        date = self.date_entry.get().strip()
        work = self.work_text.get('1.0', tk.END).strip()
        problems = self.problems_text.get('1.0', tk.END).strip()
        next_action = self.next_text.get('1.0', tk.END).strip()
        time_spent = self.time_entry.get().strip()
        
        success, message = self.controller.add_report(date, work, problems, next_action, time_spent)
        
        if success:
            messagebox.showinfo("Success", message)
            self.refresh_report_list()
            self.clear_form()
        else:
            messagebox.showerror("Error", message)
    
    def update_report(self):
        if not self.selected_report_id:
            messagebox.showwarning("Warning", "Please select a report to update")
            return
        
        date = self.date_entry.get().strip()
        work = self.work_text.get('1.0', tk.END).strip()
        problems = self.problems_text.get('1.0', tk.END).strip()
        next_action = self.next_text.get('1.0', tk.END).strip()
        time_spent = self.time_entry.get().strip()
        
        success, message = self.controller.update_report(self.selected_report_id, date, work, problems, next_action, time_spent)
        
        if success:
            messagebox.showinfo("Success", message)
            self.refresh_report_list()
            self.clear_form()
        else:
            messagebox.showerror("Error", message)
    
    def delete_report(self):
        if not self.selected_report_id:
            messagebox.showwarning("Warning", "Please select a report to delete")
            return
        
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this report?")
        if confirm:
            success, message = self.controller.delete_report(self.selected_report_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_report_list()
                self.clear_form()
            else:
                messagebox.showerror("Error", message)
    
    def clear_form(self):
        self.selected_report_id = None
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.work_text.delete('1.0', tk.END)
        self.problems_text.delete('1.0', tk.END)
        self.next_text.delete('1.0', tk.END)
        self.time_entry.delete(0, tk.END)
