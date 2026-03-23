import patient_records
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog

class PatientGUI:
    def __init__(self, root):
        self.db = patient_records.PatientDatabase()
        self.db.load_from_file()
        self.root = root
        self.root.title("Patient Records Management System")

        # Listbox for patients
        self.patient_list = tk.Listbox(root, width=50, height=10)
        self.patient_list.pack(pady=10)

        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack()

        tk.Button(button_frame, text="Add Patient", command=self.add_patient).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Remove Patient", command=self.remove_patient).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="View Patient Info", command=self.view_patient).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Add Medical Record", command=self.add_record).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="View Medical Records", command=self.view_records).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Exit", command=root.quit).grid(row=2, column=1, padx=5, pady=5)

        self.update_patient_list()

    def update_patient_list(self):
        self.patient_list.delete(0, tk.END)
        for pid in self.db.patients:
            self.patient_list.insert(tk.END, pid)

    def get_selected_patient_id(self):
        selection = self.patient_list.curselection()
        if selection:
            return self.patient_list.get(selection[0])
        else:
            messagebox.showwarning("Selection", "Please select a patient.")
            return None

    def add_patient(self):
        patient_id = simpledialog.askstring("Add Patient", "Patient ID:")
        if not patient_id: return
        name = simpledialog.askstring("Add Patient", "Name:")
        if not name: return
        dob_str = simpledialog.askstring("Add Patient", "Date of Birth (YYYY-MM-DD):")
        try:
            dob = datetime.strptime(dob_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
            return
        contact = simpledialog.askstring("Add Patient", "Contact Number:")
        email = simpledialog.askstring("Add Patient", "Email:")
        patient = patient_records.Patient(patient_id, name, dob, contact, email)
        self.db.add_patient(patient)
        self.db.save_to_file()
        self.update_patient_list()
        messagebox.showinfo("Success", "Patient added successfully.")

    def view_patient(self):
        patient_id = self.get_selected_patient_id()
        if not patient_id: return
        patient = self.db.get_patient(patient_id)
        if patient:
            info = f"ID: {patient.patient_id}\nName: {patient.name}\nDOB: {patient.date_of_birth.strftime('%Y-%m-%d')}\nContact: {patient.contact_number}\nEmail: {patient.email}"
            messagebox.showinfo("Patient Info", info)
        else:
            messagebox.showerror("Error", "Patient not found.")

    def add_record(self):
        patient_id = self.get_selected_patient_id()
        if not patient_id: return
        patient = self.db.get_patient(patient_id)
        if not patient:
            messagebox.showerror("Error", "Patient not found.")
            return
        diagnosis = simpledialog.askstring("Add Record", "Diagnosis:")
        treatment = simpledialog.askstring("Add Record", "Treatment:")
        notes = simpledialog.askstring("Add Record", "Notes:")
        patient.add_record(diagnosis, treatment, notes or "")
        self.db.save_to_file()
        messagebox.showinfo("Success", "Record added.")

    def view_records(self):
        patient_id = self.get_selected_patient_id()
        if not patient_id: return
        patient = self.db.get_patient(patient_id)
        if not patient:
            messagebox.showerror("Error", "Patient not found.")
            return
        records = patient.get_records()
        if not records:
            messagebox.showinfo("Records", "No records found.")
            return
        info = ""
        for record in records:
            info += f"Date: {record.date.strftime('%Y-%m-%d %H:%M:%S')}\nDiagnosis: {record.diagnosis}\nTreatment: {record.treatment}\nNotes: {record.notes}\n---\n"
        messagebox.showinfo("Medical Records", info)

    def remove_patient(self):
        patient_id = self.get_selected_patient_id()
        if not patient_id: return
        self.db.remove_patient(patient_id)
        self.db.save_to_file()
        self.update_patient_list()
        messagebox.showinfo("Success", "Patient removed.")

if __name__ == "__main__":
    root = tk.Tk()
    gui = PatientGUI(root)
    root.mainloop()