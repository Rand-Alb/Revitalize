"""
-------------------------------------------------------
[triage.py]
-------------------------------------------------------
Author:  Ali Al-Khazraji
ID:      169106570
Email:   alk6570@mylaurier.ca
__updated__ = "2026-03-25"
-------------------------------------------------------
"""
# Imports
from patient_new import Patient
from priority_queue import Priority_Queue
import tkinter as tk
from tkinter import messagebox

class TriageGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Triage System")

        self.pq = Priority_Queue()
        self.arrival_counter = 0
        self.root.geometry("565x500")
        self.root.minsize(565, 500)
        self.root.configure(background='steelblue2')

        self.severities = {
            "Life-Threatening": 1,
            "Urgent": 2,
            "Serious": 3,
            "Non-urgent": 4,
            "Trivial": 5
        }

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(4, weight=1)

        header_label = tk.Label(root, text="Triage System", font=('Helvetica', 16, 'bold'), bg='steelblue2', fg='black')
        header_label.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        tk.Label(root, text="Patient Name").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        tk.Label(root, text="Condition").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.condition_var = tk.StringVar(root)
        self.condition_var.set("Condition")

        menu = tk.OptionMenu(root, self.condition_var, *self.severities.keys())
        menu.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        tk.Button(root, text="Add Patient", command=self.add_patient).grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        self.output = tk.Text(root, height=15)
        self.output.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)

        tk.Button(root, text="Call Next Patient", command=self.call_next).grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=(5, 10))

    def add_patient(self):
        name = self.name_entry.get()
        condition = self.condition_var.get()

        if name == "":
            messagebox.showerror("Error", "Please enter a name for the patient.")
            return

        severity = self.severities[condition]
        self.arrival_counter += 1

        patient = Patient(name, severity, self.arrival_counter)
        self.pq.insert(patient)
        self.output.insert(tk.END, f"Added: {name} ({condition}, Priority {severity})\n")
        self.name_entry.delete(0, tk.END)

    def call_next(self):
        if self.pq.is_empty():
            messagebox.showinfo("Info", "No patients waiting.")
            return

        patient = self.pq.remove()
        self.output.insert(tk.END, f"Now treating: {patient}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = TriageGUI(root)
    root.mainloop()