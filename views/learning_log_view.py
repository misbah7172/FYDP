import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

class LearningLogView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#f0f0f0')
        self.selected_log_id = None
        self.create_widgets()
        self.refresh_log_list()
    
    def create_widgets(self):
        title = tk.Label(self, text="Learning Log", font=('Arial', 18, 'bold'), bg='#f0f0f0')
        title.pack(pady=10)
        
        search_frame = tk.Frame(self, bg='#f0f0f0')
        search_frame.pack(pady=5, fill='x', padx=10)
        
        tk.Label(search_frame, text="Search:", bg='#f0f0f0').pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side='left', padx=5)
        tk.Button(search_frame, text="Search", command=self.search_logs, bg='#2196F3', fg='white').pack(side='left', padx=5)
        tk.Button(search_frame, text="Clear", command=self.refresh_log_list, bg='#9E9E9E', fg='white').pack(side='left', padx=5)
        tk.Button(search_frame, text="Export CSV", command=self.export_csv, bg='#FF9800', fg='white').pack(side='left', padx=5)
        
        tree_frame = tk.Frame(self, bg='#f0f0f0')
        tree_frame.pack(pady=10, fill='both', expand=True, padx=10)
        
        columns = ('ID', 'Date', 'What I Learned', 'Source', 'Tags')
        self.log_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        
        widths = [50, 100, 300, 150, 150]
        for col, width in zip(columns, widths):
            self.log_tree.heading(col, text=col)
            self.log_tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.log_tree.yview)
        self.log_tree.configure(yscrollcommand=scrollbar.set)
        
        self.log_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        self.log_tree.bind('<<TreeviewSelect>>', self.on_log_select)
        
        form_frame = tk.LabelFrame(self, text="Log Details", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        form_frame.pack(pady=10, fill='x', padx=10)
        
        tk.Label(form_frame, text="Date:", bg='#f0f0f0').grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.date_entry = tk.Entry(form_frame, width=20)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        tk.Label(form_frame, text="What I Learned:", bg='#f0f0f0').grid(row=1, column=0, sticky='ne', padx=5, pady=5)
        self.learned_text = tk.Text(form_frame, width=50, height=4)
        self.learned_text.grid(row=1, column=1, padx=5, pady=5, columnspan=3, sticky='ew')
        
        tk.Label(form_frame, text="Source:", bg='#f0f0f0').grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.source_entry = tk.Entry(form_frame, width=50)
        self.source_entry.grid(row=2, column=1, padx=5, pady=5, columnspan=3, sticky='ew')
        
        tk.Label(form_frame, text="Tags:", bg='#f0f0f0').grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.tags_entry = tk.Entry(form_frame, width=50)
        self.tags_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=3, sticky='ew')
        
        tk.Label(form_frame, text="Relevance:", bg='#f0f0f0').grid(row=4, column=0, sticky='ne', padx=5, pady=5)
        self.relevance_text = tk.Text(form_frame, width=50, height=3)
        self.relevance_text.grid(row=4, column=1, padx=5, pady=5, columnspan=3, sticky='ew')
        
        button_frame = tk.Frame(self, bg='#f0f0f0')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Add Log", command=self.add_log, bg='#4CAF50', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(button_frame, text="Update Log", command=self.update_log, bg='#2196F3', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(button_frame, text="Delete Log", command=self.delete_log, bg='#f44336', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(button_frame, text="Clear Form", command=self.clear_form, bg='#9E9E9E', fg='white', width=12).pack(side='left', padx=5)
    
    def refresh_log_list(self):
        for item in self.log_tree.get_children():
            self.log_tree.delete(item)
        
        logs = self.controller.get_all_logs()
        for log in logs:
            self.log_tree.insert('', 'end', values=(log[0], log[1], log[2][:50] + '...' if len(log[2]) > 50 else log[2], log[3], log[4]))
    
    def search_logs(self):
        search_term = self.search_var.get()
        if not search_term:
            self.refresh_log_list()
            return
        
        for item in self.log_tree.get_children():
            self.log_tree.delete(item)
        
        logs = self.controller.search_logs(search_term)
        for log in logs:
            self.log_tree.insert('', 'end', values=(log[0], log[1], log[2][:50] + '...' if len(log[2]) > 50 else log[2], log[3], log[4]))
    
    def on_log_select(self, event):
        selection = self.log_tree.selection()
        if selection:
            item = self.log_tree.item(selection[0])
            log_id = item['values'][0]
            log = self.controller.get_log_by_id(log_id)
            
            if log:
                self.selected_log_id = log[0]
                self.date_entry.delete(0, tk.END)
                self.date_entry.insert(0, log[1])
                
                self.learned_text.delete('1.0', tk.END)
                self.learned_text.insert('1.0', log[2] or '')
                
                self.source_entry.delete(0, tk.END)
                self.source_entry.insert(0, log[3] or '')
                
                self.tags_entry.delete(0, tk.END)
                self.tags_entry.insert(0, log[4] or '')
                
                self.relevance_text.delete('1.0', tk.END)
                self.relevance_text.insert('1.0', log[5] or '')
    
    def add_log(self):
        date = self.date_entry.get().strip()
        learned = self.learned_text.get('1.0', tk.END).strip()
        source = self.source_entry.get().strip()
        tags = self.tags_entry.get().strip()
        relevance = self.relevance_text.get('1.0', tk.END).strip()
        
        success, message = self.controller.add_log(date, learned, source, tags, relevance)
        
        if success:
            messagebox.showinfo("Success", message)
            self.refresh_log_list()
            self.clear_form()
        else:
            messagebox.showerror("Error", message)
    
    def update_log(self):
        if not self.selected_log_id:
            messagebox.showwarning("Warning", "Please select a log to update")
            return
        
        date = self.date_entry.get().strip()
        learned = self.learned_text.get('1.0', tk.END).strip()
        source = self.source_entry.get().strip()
        tags = self.tags_entry.get().strip()
        relevance = self.relevance_text.get('1.0', tk.END).strip()
        
        success, message = self.controller.update_log(self.selected_log_id, date, learned, source, tags, relevance)
        
        if success:
            messagebox.showinfo("Success", message)
            self.refresh_log_list()
            self.clear_form()
        else:
            messagebox.showerror("Error", message)
    
    def delete_log(self):
        if not self.selected_log_id:
            messagebox.showwarning("Warning", "Please select a log to delete")
            return
        
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this log?")
        if confirm:
            success, message = self.controller.delete_log(self.selected_log_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_log_list()
                self.clear_form()
            else:
                messagebox.showerror("Error", message)
    
    def clear_form(self):
        self.selected_log_id = None
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.learned_text.delete('1.0', tk.END)
        self.source_entry.delete(0, tk.END)
        self.tags_entry.delete(0, tk.END)
        self.relevance_text.delete('1.0', tk.END)
    
    def export_csv(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            success, message = self.controller.export_to_csv(filename)
            if success:
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)
