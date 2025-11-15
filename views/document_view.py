import tkinter as tk
from tkinter import ttk, messagebox

class DocumentView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#f0f0f0')
        self.selected_doc_id = None
        self.create_widgets()
        self.refresh_document_list()
    
    def create_widgets(self):
        title = tk.Label(self, text="Document Manager", font=('Arial', 18, 'bold'), bg='#f0f0f0')
        title.pack(pady=10)
        
        search_frame = tk.Frame(self, bg='#f0f0f0')
        search_frame.pack(pady=5, fill='x', padx=10)
        
        tk.Label(search_frame, text="Search:", bg='#f0f0f0').pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side='left', padx=5)
        tk.Button(search_frame, text="Search", command=self.search_documents, bg='#2196F3', fg='white').pack(side='left', padx=5)
        tk.Button(search_frame, text="Clear", command=self.refresh_document_list, bg='#9E9E9E', fg='white').pack(side='left', padx=5)
        
        tree_frame = tk.Frame(self, bg='#f0f0f0')
        tree_frame.pack(pady=10, fill='both', expand=True, padx=10)
        
        columns = ('ID', 'Document Name', 'Version', 'Updated Date', 'Status')
        self.doc_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
        
        widths = [50, 250, 100, 120, 150]
        for col, width in zip(columns, widths):
            self.doc_tree.heading(col, text=col)
            self.doc_tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.doc_tree.yview)
        self.doc_tree.configure(yscrollcommand=scrollbar.set)
        
        self.doc_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        self.doc_tree.bind('<<TreeviewSelect>>', self.on_document_select)
        
        form_frame = tk.LabelFrame(self, text="Document Details", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        form_frame.pack(pady=10, fill='x', padx=10)
        
        tk.Label(form_frame, text="Document Name:", bg='#f0f0f0').grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.name_entry = tk.Entry(form_frame, width=40)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=3, sticky='ew')
        
        tk.Label(form_frame, text="Version:", bg='#f0f0f0').grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.version_entry = tk.Entry(form_frame, width=15)
        self.version_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        tk.Label(form_frame, text="Updated Date:", bg='#f0f0f0').grid(row=1, column=2, sticky='e', padx=5, pady=5)
        self.date_entry = tk.Entry(form_frame, width=15)
        self.date_entry.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        
        tk.Label(form_frame, text="File Path:", bg='#f0f0f0').grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.path_entry = tk.Entry(form_frame, width=40)
        self.path_entry.grid(row=2, column=1, padx=5, pady=5, columnspan=3, sticky='ew')
        
        tk.Label(form_frame, text="Submission Status:", bg='#f0f0f0').grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.status_entry = tk.Entry(form_frame, width=40)
        self.status_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=3, sticky='ew')
        
        button_frame = tk.Frame(self, bg='#f0f0f0')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Add Document", command=self.add_document, bg='#4CAF50', fg='white', width=14).pack(side='left', padx=5)
        tk.Button(button_frame, text="Update Document", command=self.update_document, bg='#2196F3', fg='white', width=14).pack(side='left', padx=5)
        tk.Button(button_frame, text="Delete Document", command=self.delete_document, bg='#f44336', fg='white', width=14).pack(side='left', padx=5)
        tk.Button(button_frame, text="Clear Form", command=self.clear_form, bg='#9E9E9E', fg='white', width=14).pack(side='left', padx=5)
    
    def refresh_document_list(self):
        for item in self.doc_tree.get_children():
            self.doc_tree.delete(item)
        
        documents = self.controller.get_all_documents()
        for doc in documents:
            self.doc_tree.insert('', 'end', values=(doc[0], doc[1], doc[2], doc[3], doc[5]))
    
    def search_documents(self):
        search_term = self.search_var.get()
        if not search_term:
            self.refresh_document_list()
            return
        
        for item in self.doc_tree.get_children():
            self.doc_tree.delete(item)
        
        documents = self.controller.search_documents(search_term)
        for doc in documents:
            self.doc_tree.insert('', 'end', values=(doc[0], doc[1], doc[2], doc[3], doc[5]))
    
    def on_document_select(self, event):
        selection = self.doc_tree.selection()
        if selection:
            item = self.doc_tree.item(selection[0])
            doc_id = item['values'][0]
            doc = self.controller.get_document_by_id(doc_id)
            
            if doc:
                self.selected_doc_id = doc[0]
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, doc[1])
                
                self.version_entry.delete(0, tk.END)
                self.version_entry.insert(0, doc[2] or '')
                
                self.date_entry.delete(0, tk.END)
                self.date_entry.insert(0, doc[3] or '')
                
                self.path_entry.delete(0, tk.END)
                self.path_entry.insert(0, doc[4] or '')
                
                self.status_entry.delete(0, tk.END)
                self.status_entry.insert(0, doc[5] or '')
    
    def add_document(self):
        name = self.name_entry.get().strip()
        version = self.version_entry.get().strip()
        date = self.date_entry.get().strip()
        path = self.path_entry.get().strip()
        status = self.status_entry.get().strip()
        
        success, message = self.controller.add_document(name, version, date, path, status)
        
        if success:
            messagebox.showinfo("Success", message)
            self.refresh_document_list()
            self.clear_form()
        else:
            messagebox.showerror("Error", message)
    
    def update_document(self):
        if not self.selected_doc_id:
            messagebox.showwarning("Warning", "Please select a document to update")
            return
        
        name = self.name_entry.get().strip()
        version = self.version_entry.get().strip()
        date = self.date_entry.get().strip()
        path = self.path_entry.get().strip()
        status = self.status_entry.get().strip()
        
        success, message = self.controller.update_document(self.selected_doc_id, name, version, date, path, status)
        
        if success:
            messagebox.showinfo("Success", message)
            self.refresh_document_list()
            self.clear_form()
        else:
            messagebox.showerror("Error", message)
    
    def delete_document(self):
        if not self.selected_doc_id:
            messagebox.showwarning("Warning", "Please select a document to delete")
            return
        
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this document?")
        if confirm:
            success, message = self.controller.delete_document(self.selected_doc_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_document_list()
                self.clear_form()
            else:
                messagebox.showerror("Error", message)
    
    def clear_form(self):
        self.selected_doc_id = None
        self.name_entry.delete(0, tk.END)
        self.version_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.path_entry.delete(0, tk.END)
        self.status_entry.delete(0, tk.END)
