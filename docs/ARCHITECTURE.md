# Sunsoft Backup Agent
## Architecture Documentation

Version: 1.0

---

# Overview

Sunsoft Backup Agent είναι μία εφαρμογή backup και diagnostics για εγκαταστάσεις Sunsoft.

Στόχος του έργου είναι:

- Backup βάσεων δεδομένων
- Backup αρχείων ρυθμίσεων
- Backup Registry
- Backup ProgramData
- Backup εκτυπωτών
- Backup Windows Services
- Δημιουργία Manifest
- Έλεγχος ακεραιότητας (Integrity Verification)
- Restore
- Cloud Backup
- Scheduled Backup

---

# Architecture Principles

Το project ακολουθεί τις παρακάτω αρχές:

- Single Responsibility Principle
- Separation of Concerns
- Composition over Inheritance
- Small reusable modules
- Result-based error handling
- No business logic inside UI

---

# Folder Structure

```
core/

backup/
backup_targets/
collectors/
common/
compression/
controllers/
database/
destination/
discovery/
engine/
health/
manifest/
pipeline/
planner/
policy/
providers/
restore/
scheduler/
services/
system/
windows/
```

---

# Folder Responsibilities

## backup/

Business logic που αφορά το backup.

## backup_targets/

Υλοποιήσεις των επιμέρους στόχων backup (SQL, Registry, ProgramData κ.λπ.).

## collectors/

Συλλογή πληροφοριών από το λειτουργικό σύστημα.

## common/

Κοινές βοηθητικές κλάσεις (Result, Validators, Status κ.ά.).

## compression/

Δημιουργία και διαχείριση συμπιεσμένων αρχείων.

## controllers/

Σύνδεση UI με το business logic.

## database/

Λειτουργίες σχετικές με βάσεις δεδομένων.

## destination/

Διαχείριση προορισμών αποθήκευσης backup.

## discovery/

Ανακάλυψη στοιχείων συστήματος.

## engine/

Κεντρικός μηχανισμός εκτέλεσης.

## health/

Έλεγχοι υγείας και προαπαιτούμενων.

## manifest/

Δημιουργία και ανάγνωση metadata backup.

## pipeline/

Ορισμός και εκτέλεση της ροής backup.

## planner/

Σχεδιασμός εργασιών backup.

## policy/

Κανόνες και πολιτικές backup.

## providers/

Τοπικοί και cloud providers.

## restore/

Λειτουργίες επαναφοράς backup.

## scheduler/

Προγραμματισμένες εργασίες.

## services/

Background υπηρεσίες.

## system/

Πληροφορίες λειτουργικού συστήματος.

## windows/

Windows-specific wrappers και API integrations.

---

# Development Rules

1. Κάθε νέο feature τοποθετείται στον κατάλληλο φάκελο.
2. Αποφεύγουμε duplicate modules.
3. Οι αλλαγές συνοδεύονται από ενημέρωση τεκμηρίωσης όταν επηρεάζουν την αρχιτεκτονική.
4. Ο κώδικας πρέπει να παραμένει απλός, επεκτάσιμος και εύκολα ελέγξιμος.

---

# Status

Architecture Version: 1.0

Status: Active Development