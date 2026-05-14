# Revitalize — Clinic Management System

A Python desktop application that consolidates three core clinic workflows — patient triage, patient records, and supply tracking — into a single, multi-window interface. Built during **Golden Hacks 2026** at Wilfrid Laurier University.

> **Tech:** Python · Tkinter · JSON
> **Built:** March 2026 (Golden Hacks Hackathon)

---

## About

Clinics typically juggle several disconnected tools to manage patients and supplies. Revitalize brings these workflows together so a clinician can keep all three views open simultaneously and switch between them without losing context. Patient and inventory data are persisted to local JSON files, removing the need for a database service and keeping the app fully self-contained.

## Features

- **Triage System** — Add patients to a priority queue based on severity level, ensuring the most urgent cases are seen first.
- **Patient Records** — Create, view, update, and persist patient information across sessions, with input/output tied to each patient record.
- **Clinic Resource Tracker** — Track supplies across clinics, log inventory additions and usage, and receive alerts when stock runs low.
- **Multi-Window Interface** — Open Triage, Patient Records, and Resource Tracker side-by-side as separate `Toplevel` windows for simultaneous access to all three core functions.
- **JSON Persistence** — Patient and clinic data are saved to `patients.json` and `clinics_data.json` so state survives between runs.

## Tech Stack

| Layer | Technology |
| --- | --- |
| Language | Python 3 |
| GUI | Tkinter (standard library) |
| Data Storage | JSON (file-based) |
| Architecture | Modular — one file per feature, shared launcher |

## Project Structure

```
Revitalize/
├── main_menu.py          # Application entry point and main menu
├── triage.py             # Triage GUI + priority queue interface
├── priority_queue.py     # Priority queue data structure for triage
├── patient_menu.py       # Patient records menu and navigation
├── patient_new.py        # Form for adding new patients
├── patient_records.py    # Patient record viewing and editing
├── resource_tracker.py   # Clinic supply tracking GUI
├── patients.json         # Persisted patient data
└── clinics_data.json     # Persisted clinic/supply data
```

The main menu opens with four options:

1. **Triage System** — manage the patient priority queue
2. **Patient Records** — view, add, and update patient information
3. **Clinic Resource Tracker** — track and log inventory across clinics
4. **Exit** — close the application

All three feature windows can be opened at the same time.

## Authors

Built by a three-person team at Golden Hacks 2026:

- [Ali Al-Khazraji](https://github.com/AliAl-Khazraji)
- [Rand Albaroudi] (https://github.com/Rand-Alb)
- [Dorian Le](https://github.com/DorianLe)
