import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class SupervisorNoteView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#f0f0f0')
        self.selected_note_id = None
        self.create_widgets()
        self.refresh_note_list()
    
    def create_widgets(self):
        title = tk.Label(self, text="Supervisor Meeting Notes", font=('Arial', 18, 'bold'), bg='#f0f0f0')
        title.pack(pady=10)
        
        search_frame = tk.Frame(self, bg='#f0f0f0')
        search_frame.pack(pady=5, fill='x', padx=10)
        
        tk.Label(search_frame, text="Search:", bg='#f0f0f0').pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side='left', padx=5)
        tk.Button(search_frame, text="Search", command=self.search_notes, bg='#2196F3', fg='white').pack(side='left', padx=5)
        tk.Button(search_frame, text="Clear", command=self.refresh_note_list, bg='#9E9E9E', fg='white').pack(side='left', padx=5)
        
        tree_frame = tk.Frame(self, bg='#f0f0f0')
        tree_frame.pack(pady=10, fill='both', expand=True, padx=10)
        
        columns = ('ID', 'Date', 'Meeting Notes Preview')
        self.note_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        
        widths = [50, 120, 500]
        for col, width in zip(columns, widths):
            self.note_tree.heading(col, text=col)
            self.note_tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.note_tree.yview)
        self.note_tree.configure(yscrollcommand=scrollbar.set)
        
        self.note_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        self.note_tree.bind('<<TreeviewSelect>>', self.on_note_select)
        
        form_frame = tk.LabelFrame(self, text="Note Details", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        form_frame.pack(pady=10, fill='x', padx=10)
        
        tk.Label(form_frame, text="Date:", bg='#f0f0f0').grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.date_entry = tk.Entry(form_frame, width=20)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        tk.Label(form_frame, text="Meeting Notes:", bg='#f0f0f0').grid(row=1, column=0, sticky='ne', padx=5, pady=5)
        self.notes_text = tk.Text(form_frame, width=50, height=8)
        self.notes_text.grid(row=1, column=1, padx=5, pady=5, columnspan=3, sticky='ew')
        
        tk.Label(form_frame, text="Assigned Tasks:", bg='#f0f0f0').grid(row=2, column=0, sticky='ne', padx=5, pady=5)
        self.tasks_text = tk.Text(form_frame, width=50, height=5)
        self.tasks_text.grid(row=2, column=1, padx=5, pady=5, columnspan=3, sticky='ew')
        
        button_frame = tk.Frame(self, bg='#f0f0f0')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Add Note", command=self.add_note, bg='#4CAF50', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(button_frame, text="Update Note", command=self.update_note, bg='#2196F3', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(button_frame, text="Delete Note", command=self.delete_note, bg='#f44336', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(button_frame, text="Clear Form", command=self.clear_form, bg='#9E9E9E', fg='white', width=12).pack(side='left', padx=5)
    
    def refresh_note_list(self):
        for item in self.note_tree.get_children():
            self.note_tree.delete(item)
        
        notes = self.controller.get_all_notes()
        for note in notes:
            preview = note[2][:60] + '...' if note[2] and len(note[2]) > 60 else (note[2] or '')
            self.note_tree.insert('', 'end', values=(note[0], note[1], preview))
    
    def search_notes(self):
        search_term = self.search_var.get()
        if not search_term:
            self.refresh_note_list()
            return
        
        for item in self.note_tree.get_children():
            self.note_tree.delete(item)
        
        notes = self.controller.search_notes(search_term)
        for note in notes:
            preview = note[2][:60] + '...' if note[2] and len(note[2]) > 60 else (note[2] or '')
            self.note_tree.insert('', 'end', values=(note[0], note[1], preview))
    
    def on_note_select(self, event):
        selection = self.note_tree.selection()
        if selection:
            item = self.note_tree.item(selection[0])
            note_id = item['values'][0]
            note = self.controller.get_note_by_id(note_id)
            
            if note:
                self.selected_note_id = note[0]
                self.date_entry.delete(0, tk.END)
                self.date_entry.insert(0, note[1])
                
                self.notes_text.delete('1.0', tk.END)
                self.notes_text.insert('1.0', note[2] or '')
                
                self.tasks_text.delete('1.0', tk.END)
                self.tasks_text.insert('1.0', note[3] or '')
    
    def add_note(self):
        date = self.date_entry.get().strip()
        notes = self.notes_text.get('1.0', tk.END).strip()
        tasks = self.tasks_text.get('1.0', tk.END).strip()
        
        success, message = self.controller.add_note(date, notes, tasks)
        
        if success:
            messagebox.showinfo("Success", message)
            self.refresh_note_list()
            self.clear_form()
        else:
            messagebox.showerror("Error", message)
    
    def update_note(self):
        if not self.selected_note_id:
            messagebox.showwarning("Warning", "Please select a note to update")
            return
        
        date = self.date_entry.get().strip()
        notes = self.notes_text.get('1.0', tk.END).strip()
        tasks = self.tasks_text.get('1.0', tk.END).strip()
        
        success, message = self.controller.update_note(self.selected_note_id, date, notes, tasks)
        
        if success:
            messagebox.showinfo("Success", message)
            self.refresh_note_list()
            self.clear_form()
        else:
            messagebox.showerror("Error", message)
    
    def delete_note(self):
        if not self.selected_note_id:
            messagebox.showwarning("Warning", "Please select a note to delete")
            return
        
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this note?")
        if confirm:
            success, message = self.controller.delete_note(self.selected_note_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_note_list()
                self.clear_form()
            else:
                messagebox.showerror("Error", message)
    
    def clear_form(self):
        self.selected_note_id = None
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.notes_text.delete('1.0', tk.END)
        self.tasks_text.delete('1.0', tk.END)
