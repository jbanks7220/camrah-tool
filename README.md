# Camrah v3.2

**Camrah** is a modern Python-based OSINT visualization tool that scans publicly indexed IP cameras by country and displays them on an interactive world map with real-time logging.

Built with a focus on **clean UI**, **correct data isolation**, and **stable multi-threaded scanning**, Camrah demonstrates practical skills in Python GUI development, web scraping, concurrency, and geolocation visualization.

---

## ✨ Features

- 🌍 **Country-Based Camera Discovery**
  - Scans multiple countries via publicly indexed sources
  - Supports 19+ countries out of the box

- 🗺️ **Interactive Dark-Themed Map**
  - Live camera markers with click-to-open streams
  - Fallback positioning when precise geolocation is unavailable

- ⚡ **Multi-Threaded & Responsive**
  - Non-blocking scans
  - Per-scan isolation to prevent data bleed between countries

- 🧠 **Accurate Scan Management**
  - Each scan uses a unique ID
  - Old results are ignored automatically when switching countries

- 🖥️ **Modern Tkinter UI**
  - Dashboard-style layout
  - Activity log and results panel
  - Consistent dark OSINT-style theme

- 📜 **Real-Time Activity Logging**
  - Scan progress
  - Geo lookups
  - Error handling

---

## 🎥Video Demo

https://github.com/user-attachments/assets/dfb28f5d-91b7-4437-8e17-7495aafe6d01

---

## 🚀 Getting Started

### Requirements

- **Python 3.9+** recommended

## Clone the Repository

```bash
git clone https://github.com/jbanks7220/camrah-tool.git
cd camrah-tool
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python camrah.py
```
## 📦 Dependencies

requests — HTTP requests and scraping

fake-useragent — randomized User-Agent headers

tkintermapview — interactive map rendering

tkinter — GUI framework (bundled with Python on most systems)

## 🌐 Supported Countries

Camrah currently supports scanning the following regions:

US, JP, IT, DE, RU, AT, FR, CZ, KR, RO, CH, NO, TW, CA, NL, PL, ES, GB, SE

(Additional countries can be added easily.)

## 🧩 How It Works (High-Level)

User selects a country

Camrah scans indexed public pages for camera URLs

Each camera IP is geolocated using a public API

Results are displayed in:

a list view

an interactive map

Clicking a camera opens the stream in the default browser

All scans are threaded and isolated, ensuring UI responsiveness and data accuracy.

## ⚠️ Disclaimer

This project is intended for educational and research purposes only.

Camrah only accesses publicly indexed resources

No authentication is bypassed

No credentials are collected

The author does not endorse or support misuse of this tool

Users are responsible for complying with all applicable laws and regulations in their jurisdiction.

## 🛠️ Skills Demonstrated

Python GUI development (Tkinter / ttk)

Threading & concurrency

Web scraping & HTTP handling

OSINT-style data visualization

Geolocation APIs

UI/UX layout design

Defensive state management

## 📌 Roadmap 

Marker clustering

Scan cancellation

Multi-country batch scanning

Executable packaging (PyInstaller)

Exportable results

👤 Author

Jamir Banks
Python Developer | OSINT & Visualization Projects
GitHub: https://github.com/jbanks7220
