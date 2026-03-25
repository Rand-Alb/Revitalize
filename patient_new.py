"""
-------------------------------------------------------
[patient_new.py]
-------------------------------------------------------
Author:  Ali Al-Khazraji
ID:      169106570
Email:   alk6570@mylaurier.ca
__updated__ = "2026-03-25"
-------------------------------------------------------
"""

class Patient:

    def __init__(self, name, severity, arrival_time):
        self.name = name
        self.severity = severity
        self.arrival_time = arrival_time

    def __lt__(self, other):
        if self.severity == other.severity:
            return self.arrival_time < other.arrival_time
        return self.severity < other.severity

    def __repr__(self):
        return f"{self.name} (Priority {self.severity})"