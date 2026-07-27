# Sunsoft Backup Agent V2

Version: 2.0
Status: Design Phase

---

# Vision

Create a modern enterprise desktop application for backup and restore.

The application must feel comparable to professional software such as:

- Veeam
- Synology Active Backup
- JetBrains Toolbox
- Visual Studio 2022

The interface must be:

- Fast
- Clean
- Minimal
- Enterprise
- Consistent

---

# Design Principles

• One responsibility per widget

• Reusable components

• Zero duplicated UI code

• No inline magic values

• Responsive layout

• Dark theme first

• SVG icons

• Smooth animations

---

# Layout

+---------------------------------------------------------------+
| Sidebar | Header                                               |
|         |------------------------------------------------------|
|         | Summary Cards                                        |
|         |------------------------------------------------------|
|         | Progress | Actions                                   |
|         |------------------------------------------------------|
|         | Live Logs | System Information                       |
|---------------------------------------------------------------|
| Footer                                                        |
+---------------------------------------------------------------+

---

# Sidebar

Sections

Dashboard

Backup

Restore

History

Logs

Settings

About

---

# Header

Application title

Current customer

Connection status

Current backup

Settings shortcut

---

# Summary Cards

Last Backup

Files

Database

Storage

Health

---

# Progress

Circular Progress

Current Step

Speed

Elapsed Time

Remaining Time

---

# Logs

Live log viewer

Filter

Search

Copy

Export

Auto Scroll

---

# Quick Actions

Start Backup

Verify

Compress

Restore

Cloud Sync

---

# System

Windows Version

Database

Disk Space

Last Error

Provider

---

# Footer

Application Version

Copyright

Support Status

---

# Components

BaseCard

MetricCard

StatusChip

PrimaryButton

SecondaryButton

DangerButton

PageHeader

SidebarButton

ProgressWidget

LogViewer

---

# Icons

SVG only

No emojis

---

# Typography

Segoe UI

Title

Heading

Body

Small

---

# Animations

Hover

Fade

Selection

Progress

Duration:

150-200ms

---

# Backend

The V2 UI must reuse the existing backend without modification.

Workers

Services

Database

Backup logic

remain unchanged.