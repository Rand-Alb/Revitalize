from dataclasses import dataclass
from datetime import datetime
from typing import List
import json

@dataclass
class MedicalRecord:
    date: datetime
    diagnosis: str
    treatment: str
    notes: str

@dataclass
class Patient:
    patient_id: str
    name: str
    date_of_birth: datetime
    contact_number: str
    email: str
    medical_records: List[MedicalRecord] = None
    
    def __post_init__(self):
        if self.medical_records is None:
            self.medical_records = []
    
    def add_record(self, diagnosis: str, treatment: str, notes: str = ""):
        record = MedicalRecord(
            date=datetime.now(),
            diagnosis=diagnosis,
            treatment=treatment,
            notes=notes
        )
        self.medical_records.append(record)
    
    def get_records(self) -> List[MedicalRecord]:
        return sorted(self.medical_records, key=lambda r: r.date, reverse=True)

class PatientDatabase:
    def __init__(self):
        self.patients = {}
    
    def add_patient(self, patient: Patient):
        self.patients[patient.patient_id] = patient
    
    def get_patient(self, patient_id: str) -> Patient:
        return self.patients.get(patient_id)
    
    def remove_patient(self, patient_id: str):
        if patient_id in self.patients:
            del self.patients[patient_id]
    
    def save_to_file(self, filename='patients.json'):
        data = {}
        for pid, patient in self.patients.items():
            patient_dict = {
                'patient_id': patient.patient_id,
                'name': patient.name,
                'date_of_birth': patient.date_of_birth.isoformat(),
                'contact_number': patient.contact_number,
                'email': patient.email,
                'medical_records': [
                    {
                        'date': record.date.isoformat(),
                        'diagnosis': record.diagnosis,
                        'treatment': record.treatment,
                        'notes': record.notes
                    } for record in patient.medical_records
                ]
            }
            data[pid] = patient_dict
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    
    def load_from_file(self, filename='patients.json'):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            for pid, p_dict in data.items():
                dob = datetime.fromisoformat(p_dict['date_of_birth'])
                patient = Patient(p_dict['patient_id'], p_dict['name'], dob, p_dict['contact_number'], p_dict['email'])
                for r_dict in p_dict['medical_records']:
                    date = datetime.fromisoformat(r_dict['date'])
                    record = MedicalRecord(date, r_dict['diagnosis'], r_dict['treatment'], r_dict['notes'])
                    patient.medical_records.append(record)
                self.patients[pid] = patient
        except FileNotFoundError:
            pass  # No file, start empty