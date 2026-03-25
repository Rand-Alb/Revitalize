import tkinter as tk
from patient_menu import PatientGUI
from resource_tracker import ResourceTrackerMenu

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Menu")
        self.root.geometry("400x300")
        self.root.minsize(400, 300)

        # Title
        tk.Label(root, text="Revitalize - Clinic Management System", font=('Helvetica', 16, 'bold')).pack(pady=20)

        # Buttons
        tk.Button(root, text="Patient Records", command=self.open_patient_records, width=20).pack(pady=10)
        tk.Button(root, text="Clinic Resource Tracker", command=self.open_resource_tracker, width=20).pack(pady=10)
        tk.Button(root, text="Exit", command=root.quit, width=20).pack(pady=10)

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
