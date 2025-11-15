import tkinter as tk
from tkinter import ttk, messagebox

class ReferenceView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#f0f0f0')
        self.selected_ref_id = None
        self.create_widgets()
        self.refresh_reference_list()
    
    def create_widgets(self):
        title = tk.Label(self, text="Research References", font=('Arial', 18, 'bold'), bg='#f0f0f0')
        title.pack(pady=10)
        
        search_frame = tk.Frame(self, bg='#f0f0f0')
        search_frame.pack(pady=5, fill='x', padx=10)
        
        tk.Label(search_frame, text="Search:", bg='#f0f0f0').pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side='left', padx=5)
        tk.Button(search_frame, text="Search", command=self.search_references, bg='#2196F3', fg='white').pack(side='left', padx=5)
        tk.Button(search_frame, text="Clear", command=self.refresh_reference_list, bg='#9E9E9E', fg='white').pack(side='left', padx=5)
        
        tree_frame = tk.Frame(self, bg='#f0f0f0')
        tree_frame.pack(pady=10, fill='both', expand=True, padx=10)
        
        columns = ('ID', 'Title', 'Link', 'Relevance')
        self.ref_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        
        widths = [50, 250, 250, 150]
        for col, width in zip(columns, widths):
            self.ref_tree.heading(col, text=col)
            self.ref_tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.ref_tree.yview)
        self.ref_tree.configure(yscrollcommand=scrollbar.set)
        
        self.ref_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        self.ref_tree.bind('<<TreeviewSelect>>', self.on_reference_select)
        
        form_frame = tk.LabelFrame(self, text="Reference Details", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        form_frame.pack(pady=10, fill='x', padx=10)
        
        tk.Label(form_frame, text="Title:", bg='#f0f0f0').grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.title_entry = tk.Entry(form_frame, width=50)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=3, sticky='ew')
        
        tk.Label(form_frame, text="Link/URL:", bg='#f0f0f0').grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.link_entry = tk.Entry(form_frame, width=50)
        self.link_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=3, sticky='ew')
        
        tk.Label(form_frame, text="Summary:", bg='#f0f0f0').grid(row=2, column=0, sticky='ne', padx=5, pady=5)
        self.summary_text = tk.Text(form_frame, width=50, height=5)
        self.summary_text.grid(row=2, column=1, padx=5, pady=5, columnspan=3, sticky='ew')
        
        tk.Label(form_frame, text="Relevance:", bg='#f0f0f0').grid(row=3, column=0, sticky='ne', padx=5, pady=5)
        self.relevance_text = tk.Text(form_frame, width=50, height=3)
        self.relevance_text.grid(row=3, column=1, padx=5, pady=5, columnspan=3, sticky='ew')
        
        button_frame = tk.Frame(self, bg='#f0f0f0')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Add Reference", command=self.add_reference, bg='#4CAF50', fg='white', width=14).pack(side='left', padx=5)
        tk.Button(button_frame, text="Update Reference", command=self.update_reference, bg='#2196F3', fg='white', width=14).pack(side='left', padx=5)
        tk.Button(button_frame, text="Delete Reference", command=self.delete_reference, bg='#f44336', fg='white', width=14).pack(side='left', padx=5)
        tk.Button(button_frame, text="Clear Form", command=self.clear_form, bg='#9E9E9E', fg='white', width=14).pack(side='left', padx=5)
    
    def refresh_reference_list(self):
        for item in self.ref_tree.get_children():
            self.ref_tree.delete(item)
        
        references = self.controller.get_all_references()
        for ref in references:
            link_preview = ref[1][:40] + '...' if ref[1] and len(ref[1]) > 40 else (ref[1] or '')
            self.ref_tree.insert('', 'end', values=(ref[0], ref[2], link_preview, ref[4]))
    
    def search_references(self):
        search_term = self.search_var.get()
        if not search_term:
            self.refresh_reference_list()
            return
        
        for item in self.ref_tree.get_children():
            self.ref_tree.delete(item)
        
        references = self.controller.search_references(search_term)
        for ref in references:
            link_preview = ref[1][:40] + '...' if ref[1] and len(ref[1]) > 40 else (ref[1] or '')
            self.ref_tree.insert('', 'end', values=(ref[0], ref[2], link_preview, ref[4]))
    
    def on_reference_select(self, event):
        selection = self.ref_tree.selection()
        if selection:
            item = self.ref_tree.item(selection[0])
            ref_id = item['values'][0]
            ref = self.controller.get_reference_by_id(ref_id)
            
            if ref:
                self.selected_ref_id = ref[0]
                self.link_entry.delete(0, tk.END)
                self.link_entry.insert(0, ref[1] or '')
                
                self.title_entry.delete(0, tk.END)
                self.title_entry.insert(0, ref[2])
                
                self.summary_text.delete('1.0', tk.END)
                self.summary_text.insert('1.0', ref[3] or '')
                
                self.relevance_text.delete('1.0', tk.END)
                self.relevance_text.insert('1.0', ref[4] or '')
    
    def add_reference(self):
        link = self.link_entry.get().strip()
        title = self.title_entry.get().strip()
        summary = self.summary_text.get('1.0', tk.END).strip()
        relevance = self.relevance_text.get('1.0', tk.END).strip()
        
        success, message = self.controller.add_reference(link, title, summary, relevance)
        
        if success:
            messagebox.showinfo("Success", message)
            self.refresh_reference_list()
            self.clear_form()
        else:
            messagebox.showerror("Error", message)
    
    def update_reference(self):
        if not self.selected_ref_id:
            messagebox.showwarning("Warning", "Please select a reference to update")
            return
        
        link = self.link_entry.get().strip()
        title = self.title_entry.get().strip()
        summary = self.summary_text.get('1.0', tk.END).strip()
        relevance = self.relevance_text.get('1.0', tk.END).strip()
        
        success, message = self.controller.update_reference(self.selected_ref_id, link, title, summary, relevance)
        
        if success:
            messagebox.showinfo("Success", message)
            self.refresh_reference_list()
            self.clear_form()
        else:
            messagebox.showerror("Error", message)
    
    def delete_reference(self):
        if not self.selected_ref_id:
            messagebox.showwarning("Warning", "Please select a reference to delete")
            return
        
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this reference?")
        if confirm:
            success, message = self.controller.delete_reference(self.selected_ref_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_reference_list()
                self.clear_form()
            else:
                messagebox.showerror("Error", message)
    
    def clear_form(self):
        self.selected_ref_id = None
        self.title_entry.delete(0, tk.END)
        self.link_entry.delete(0, tk.END)
        self.summary_text.delete('1.0', tk.END)
        self.relevance_text.delete('1.0', tk.END)
