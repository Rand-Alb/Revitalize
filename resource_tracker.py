import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict

DATA_FILE = "clinics_data.json"

def load_data() -> Dict[str, Dict[str, int]]:
    # Load clinic data from the JSON file.
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {DATA_FILE} is corrupted. Starting with empty database.")
            return {}
    return {}

def save_data(data: Dict[str, Dict[str, int]]):
    # Save clinic data to the JSON file.
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

class ResourceTrackerMenu:
    tree: ttk.Treeview
    clinic_var: tk.StringVar
    clinic_entry: ttk.Entry
    item_var: tk.StringVar
    item_entry: ttk.Entry
    qty_var: tk.StringVar
    qty_entry: ttk.Entry

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Clinic Resource Tracker")
        self.root.geometry("650x450")
        self.root.minsize(850, 450)
        
        # Load data
        self.data = load_data()
        
        # Styling
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        style.configure("Treeview", font=('Helvetica', 10), rowheight=25)
        
        self.setup_ui()
        self.refresh_inventory()
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_lbl = ttk.Label(main_frame, text="Clinic Resource Tracker", font=('Helvetica', 16, 'bold'))
        title_lbl.pack(anchor=tk.W, pady=(0, 15))

        # Inventory Table Frame
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        columns = ("Clinic", "Item", "Quantity", "Status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("Clinic", text="Clinic")
        self.tree.heading("Item", text="Item")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Status", text="Status")
        
        self.tree.column("Clinic", width=150)
        self.tree.column("Item", width=150)
        self.tree.column("Quantity", width=100, anchor=tk.CENTER)
        self.tree.column("Status", width=150, anchor=tk.W)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Controls Frame (Bottom)
        control_frame = ttk.LabelFrame(main_frame, text="Manage Inventory", padding=10)
        control_frame.pack(fill=tk.X)
        
        # Grid layout for inputs
        ttk.Label(control_frame, text="Clinic:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.clinic_var = tk.StringVar()
        self.clinic_entry = ttk.Entry(control_frame, textvariable=self.clinic_var, width=15)
        self.clinic_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(control_frame, text="Item:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.item_var = tk.StringVar()
        self.item_entry = ttk.Entry(control_frame, textvariable=self.item_var, width=15)
        self.item_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(control_frame, text="Qty:").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.qty_var = tk.StringVar()
        self.qty_entry = ttk.Entry(control_frame, textvariable=self.qty_var, width=8)
        self.qty_entry.grid(row=0, column=5, padx=5, pady=5)
        
        # Buttons
        ttk.Button(control_frame, text="Add Stock", command=self.add_stock).grid(row=0, column=6, padx=(15, 5), pady=5)
        ttk.Button(control_frame, text="Log Usage", command=self.log_usage).grid(row=0, column=7, padx=5, pady=5)
        
        # Bind table selection to auto-fill inputs
        self.tree.bind("<<TreeviewSelect>>", self.on_item_select)
        
    def refresh_inventory(self):
        # Clear current table
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Populate table
        for clinic, inventory in self.data.items():
            for item, quantity in inventory.items():
                status = "⚠️ LOW STOCK" if quantity < 10 else "OK"
                tag = "low" if quantity < 10 else "normal"
                self.tree.insert("", tk.END, values=(clinic, item, quantity, status), tags=(tag,))
                
        # Tag styling for highlighting low stock rows
        self.tree.tag_configure("low", foreground="#d9534f", font=('Helvetica', 10, 'bold'))
        self.tree.tag_configure("normal", foreground="#333333")
        
    def on_item_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.clinic_var.set(values[0])
            self.item_var.set(values[1])
            self.qty_var.set("") # Require user to specify quantity manually
            
    def get_input(self) -> tuple[str, str, int] | None:
        clinic = self.clinic_var.get().strip()
        item = self.item_var.get().strip()
        qty_str = self.qty_var.get().strip()
        
        if not clinic or not item or not qty_str:
            messagebox.showerror("Error", "Please fill in Clinic, Item, and Quantity.")
            return None
            
        try:
            qty = int(qty_str)
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive number.")
            return None
            
        return clinic, item, qty
        
    def add_stock(self):
        inputs = self.get_input()
        if not inputs: return
        clinic, item, qty = inputs
            
        if clinic not in self.data:
            self.data[clinic] = {}
            
        if item in self.data[clinic]:
            self.data[clinic][item] += qty
        else:
            self.data[clinic][item] = qty
            
        save_data(self.data)
        self.refresh_inventory()
        messagebox.showinfo("Success", f"✅ Added {qty} {item}(s) to {clinic}.")
        self.qty_var.set("")
        
    def log_usage(self):
        inputs = self.get_input()
        if not inputs: return
        clinic, item, qty = inputs
            
        if clinic not in self.data or item not in self.data[clinic]:
            messagebox.showerror("Error", f"❌ '{item}' not found in {clinic}.")
            return
            
        if self.data[clinic][item] < qty:
            messagebox.showerror("Error", f"❌ Not enough '{item}' in stock.\nCurrent stock: {self.data[clinic][item]}")
            return
            
        self.data[clinic][item] -= qty
        save_data(self.data)
        self.refresh_inventory()
        
        if self.data[clinic][item] < 10:
            messagebox.showwarning("Low Inventory Alert", f"⚠️ Low inventory for '{item}' in {clinic}!\nCurrent stock: {self.data[clinic][item]}")
        else:
            messagebox.showinfo("Success", f"✅ Logged {qty} '{item}' used in {clinic}.")
            
        self.qty_var.set("")

def main():
    root = tk.Tk()
    app = ResourceTrackerMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()
