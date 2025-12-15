"""
Camrah v3.2 – Modern UI (Fixed Country Scans)
Stable | Fast | Correct Country Results | Terminal Logs
"""

import tkinter as tk
from tkinter import ttk
import threading, queue, re, time, webbrowser, uuid
import requests
from fake_useragent import UserAgent
import tkintermapview

# ================= GLOBALS =================
RESULT_QUEUE = queue.Queue()
LOG_QUEUE = queue.Queue()

UA = UserAgent()

COUNTRIES = {
    "US": ("http://insecam.org/en/bycountry/US/", 37.0902, -95.7129),
    "JP": ("http://insecam.org/en/bycountry/JP/", 36.2048, 138.2529),
    "IT": ("http://insecam.org/en/bycountry/IT/", 41.8719, 12.5674),
    "DE": ("http://insecam.org/en/bycountry/DE/", 51.1657, 10.4515),
    "RU": ("http://insecam.org/en/bycountry/RU/", 61.5240, 105.3188),
    "AT": ("http://insecam.org/en/bycountry/AT/", 47.5162, 14.5501),
    "FR": ("http://insecam.org/en/bycountry/FR/", 46.2276, 2.2137),
    "CZ": ("http://insecam.org/en/bycountry/CZ/", 49.8175, 15.4730),
    "KR": ("http://insecam.org/en/bycountry/KR/", 35.9078, 127.7669),
    "RO": ("http://insecam.org/en/bycountry/RO/", 45.9432, 24.9668),
    "CH": ("http://insecam.org/en/bycountry/CH/", 46.8182, 8.2275),
    "NO": ("http://insecam.org/en/bycountry/NO/", 60.4720, 8.4689),
    "TW": ("http://insecam.org/en/bycountry/TW/", 23.6978, 120.9605),
    "CA": ("http://insecam.org/en/bycountry/CA/", 56.1304, -106.3468),
    "NL": ("http://insecam.org/en/bycountry/NL/", 52.1326, 5.2913),
    "PL": ("http://insecam.org/en/bycountry/PL/", 51.9194, 19.1451),
    "ES": ("http://insecam.org/en/bycountry/ES/", 40.4637, -3.7492),
    "GB": ("http://insecam.org/en/bycountry/GB/", 55.3781, -3.4360),
    "SE": ("http://insecam.org/en/bycountry/SE/", 60.1282, 18.6435),
}

CAM_REGEX = re.compile(r"http://\d+\.\d+\.\d+\.\d+:\d+/")

# ================= CRAWLER =================
def crawl_country(scan_id, url, pages):
    found = set()
    for p in range(1, pages + 1):
        try:
            LOG_QUEUE.put(f"[SCAN] Page {p}")
            r = requests.get(
                f"{url}?page={p}",
                headers={"User-Agent": UA.random},
                timeout=8
            )
            cams = CAM_REGEX.findall(r.text)
            if not cams:
                break
            found.update(cams)
            LOG_QUEUE.put(f"[FOUND] {len(cams)} cams")
        except:
            LOG_QUEUE.put(f"[ERROR] Page {p}")
    RESULT_QUEUE.put((scan_id, list(found)))

# ================= GEO =================
def geo_lookup(ip):
    try:
        r = requests.get(f"https://ipwho.is/{ip}", timeout=6).json()
        if r.get("success"):
            return r["latitude"], r["longitude"], r["city"], r["country"]
    except:
        pass
    return None

def geo_worker(scan_id, cam, callback, fallback_lat, fallback_lon):
    ip = cam.split("//")[1].split(":")[0]
    geo = geo_lookup(ip)

    if geo:
        lat, lon, city, country = geo
        LOG_QUEUE.put(f"[GEO] {ip} → {city}")
    else:
        lat, lon = fallback_lat, fallback_lon
        city, country = "Approximate", "Country Center"
        LOG_QUEUE.put(f"[GEO FALLBACK] {ip}")

    callback(scan_id, cam, lat, lon, city, country)

# ================= GUI =================
class CamrahApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camrah v3.2")
        self.root.geometry("1500x880")
        self.root.configure(bg="#0b0b0f")

        self.markers = []
        self.current_scan_id = None

        self.setup_styles()
        self.build_ui()

        self.poll_results()
        self.poll_logs()

    # ---------- STYLES ----------
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("App.TFrame", background="#0b0b0f")
        style.configure("Header.TLabel", background="#0b0b0f", foreground="white",
                        font=("Segoe UI Semibold", 16))
        style.configure("Sub.TLabel", background="#0b0b0f", foreground="#9ca3af",
                        font=("Segoe UI", 10))

        style.configure("Accent.TButton", background="#7c3aed",
                        foreground="white", padding=(14, 6))
        style.map("Accent.TButton", background=[("active", "#6d28d9")])

    # ---------- UI ----------
    def build_ui(self):
        container = ttk.Frame(self.root, style="App.TFrame")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        self.build_header(container)
        self.build_body(container)

    def build_header(self, parent):
        header = ttk.Frame(parent, style="App.TFrame")
        header.pack(fill="x", pady=(0, 15))

        ttk.Label(header, text="Camrah v3.2", style="Header.TLabel").pack(side="left")
        ttk.Label(header, text="Live Camera Map Scanner",
                  style="Sub.TLabel").pack(side="left", padx=12)

        self.verbosity = tk.IntVar(value=30)
        ttk.Scale(header, from_=10, to=200,
                  variable=self.verbosity, length=220).pack(side="right")

    def build_body(self, parent):
        body = ttk.Frame(parent, style="App.TFrame")
        body.pack(fill="both", expand=True)

        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(1, weight=1)

        left = ttk.Frame(body, style="App.TFrame")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        right = ttk.Frame(body, style="App.TFrame")
        right.grid(row=0, column=1, sticky="nsew", padx=(12, 0))

        bottom = ttk.Frame(body, style="App.TFrame")
        bottom.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(16, 0))

        self.build_country_buttons(left)
        self.build_camera_list(left)
        self.build_terminal(right)
        self.build_map(bottom)

    def build_country_buttons(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=(0, 10))

        for i, c in enumerate(COUNTRIES):
            ttk.Button(frame, text=c, style="Accent.TButton",
                       command=lambda k=c: self.start_crawl(k)).grid(row=i // 6, column=i % 6, padx=4, pady=4)

    def build_camera_list(self, parent):
        ttk.Label(parent, text="Discovered Cameras", style="Sub.TLabel").pack(anchor="w")
        self.listbox = tk.Listbox(parent, bg="#111827", fg="#a855f7",
                                  font=("Consolas", 11), highlightthickness=0)
        self.listbox.pack(fill="both", expand=True)
        self.listbox.bind("<Double-Button-1>", self.open_feed_from_listbox)

    def build_terminal(self, parent):
        ttk.Label(parent, text="Activity Log", style="Sub.TLabel").pack(anchor="w")
        self.terminal = tk.Text(parent, bg="#020617", fg="#22c55e",
                                font=("Consolas", 10), highlightthickness=0)
        self.terminal.pack(fill="both", expand=True)

    def build_map(self, parent):
        ttk.Label(parent, text="Live Map", style="Sub.TLabel").pack(anchor="w")
        self.map_widget = tkintermapview.TkinterMapView(parent, corner_radius=12)
        self.map_widget.pack(fill="both", expand=True)
        self.map_widget.set_tile_server(
            "https://basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", max_zoom=20)
        self.map_widget.set_zoom(2)

    # ---------- LOGIC ----------
    def start_crawl(self, country):
        self.current_scan_id = uuid.uuid4().hex

        self.listbox.delete(0, tk.END)
        for m in self.markers:
            m.delete()
        self.markers.clear()

        url, lat, lon = COUNTRIES[country]

        threading.Thread(
            target=crawl_country,
            args=(self.current_scan_id, url, int(self.verbosity.get())),
            daemon=True
        ).start()

        self.fallback_lat = lat
        self.fallback_lon = lon

    def poll_results(self):
        while not RESULT_QUEUE.empty():
            scan_id, cams = RESULT_QUEUE.get()
            if scan_id != self.current_scan_id:
                continue

            for cam in cams:
                self.listbox.insert(tk.END, cam)
                threading.Thread(
                    target=geo_worker,
                    args=(scan_id, cam, self.add_camera,
                          self.fallback_lat, self.fallback_lon),
                    daemon=True
                ).start()

        self.root.after(100, self.poll_results)

    def add_camera(self, scan_id, cam, lat, lon, city, country):
        if scan_id != self.current_scan_id:
            return

        marker = self.map_widget.set_marker(
            lat, lon,
            text=f"{city}\n{cam.split('//')[1]}",
            command=lambda _=None, url=cam: webbrowser.open(url)
        )
        self.markers.append(marker)

    def poll_logs(self):
        while not LOG_QUEUE.empty():
            self.terminal.insert(tk.END, LOG_QUEUE.get() + "\n")
            self.terminal.see(tk.END)
        self.root.after(100, self.poll_logs)

    def open_feed_from_listbox(self, _):
        cam = self.listbox.get(self.listbox.curselection())
        webbrowser.open(cam)

# ================= RUN =================
if __name__ == "__main__":
    root = tk.Tk()
    app = CamrahApp(root)
    root.mainloop()
