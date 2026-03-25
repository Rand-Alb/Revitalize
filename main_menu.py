"""
-------------------------------------------
[main_menu.py]
-------------------------------------------
Author: Dorian Le
Updated: 2026-03-25
Desc: This module implements the main menu
of the clinic management system. It can access
both the patient records and resource tracker.
-------------------------------------------
"""
# Imports
import tkinter as tk
from triage import TriageGUI
from patient_tracker import PatientGUI
from resource_tracker import ResourceTrackerMenu

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Menu")
        self.root.geometry("500x300")
        self.root.minsize(500, 300)

        # Title
        tk.Label(root, text="Revitalize - Clinic Management System", font=('Helvetica', 24, 'bold')).pack(pady=20)

        # Buttons
        tk.Button(root, text="Triage System", command=self.open_triage_menu, width=20).pack(pady=10)
        tk.Button(root, text="Patient Records", command=self.open_patient_records, width=20).pack(pady=10)
        tk.Button(root, text="Clinic Resource Tracker", command=self.open_resource_tracker, width=20).pack(pady=10)
        tk.Button(root, text="Exit", command=root.quit, width=20).pack(pady=10)

    def open_triage_menu(self):
        triage_window = tk.Toplevel(self.root)
        TriageGUI(triage_window)

    def open_patient_records(self):
        patient_window = tk.Toplevel(self.root)
        PatientGUI(patient_window)

    def open_resource_tracker(self):
        tracker_window = tk.Toplevel(self.root)
        ResourceTrackerMenu(tracker_window)

if __name__ == "__main__":
    root = tk.Tk()
    MainMenu(root)
    root.mainloop()