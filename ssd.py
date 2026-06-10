import os
import random
import tkinter as tk
from tkinter import font as tkfont

# ═══════════════════════════════════════════════════════════════════════════
# DESIGN SYSTEM CONSTANTS (Futuristic Cyberpunk / Dark Mode PCB)
# ═══════════════════════════════════════════════════════════════════════════
COLOR_BG_DARKEST = "#050811"  # Main window background
COLOR_BG_DARKER  = "#0a0f1d"  # Frames background
COLOR_BG_CARD    = "#0f172a"  # Component panels background
COLOR_BORDER     = "#1e293b"  # Sub-borders

COLOR_PCB_GREEN  = "#0b1510"  # Main PCB Board Fill
COLOR_PCB_BORDER = "#143622"  # PCB Outline Border
COLOR_GRID_LINE  = "#0d1f14"  # Background trace grids

# Component Accents
COLOR_CONTROLLER = "#378ADD"  # Electric Blue
COLOR_NAND       = "#1D9E75"  # Teal/Jade Green
COLOR_DRAM       = "#BA7517"  # Amber/Bronze
COLOR_CONNECTOR  = "#dca020"  # Gold

# Data Flow Speeds
SPEED_READ  = 7400
SPEED_WRITE = 6700

# ═══════════════════════════════════════════════════════════════════════════
# METADATA FOR INTERACTIVE DETAILS CARD
# ═══════════════════════════════════════════════════════════════════════════
COMPONENT_DATA = {
    "connector": {
        "title": "M.2 PCIe 4.0 Interface Connector",
        "badge": "Host Physical Interface",
        "desc": "The primary interface connecting the SSD directly to the motherboard. It utilizes the M.2 (2280 form factor) standard, providing 4 high-speed PCIe Gen 4 lanes and the NVMe 2.0 command protocol to minimize communication latency.",
        "specs": [
            ("Form Factor", "M.2 2280 (Single-sided)"),
            ("Bus Interface", "PCI Express Gen 4.0 ×4 Lanes"),
            ("Protocol", "NVMe 2.0 (Non-Volatile)"),
            ("Bandwidth", "Up to 8,000 MB/s (Theoretical)"),
            ("Interface Pins", "75 Gold Edge Contacts (M-Key)")
        ],
        "flow": "Serves as the entry and exit point for host commands. Write commands flow inward from the computer CPU; read operations push requested blocks outward to the host system."
    },
    "controller": {
        "title": "SSD Controller Processors",
        "badge": "Processing & Core Engine",
        "desc": "The brain of the SSD. It manages the Flash Translation Layer (FTL), translates host-level logical requests to raw physical cells, executes Garbage Collection, maps blocks for Wear Leveling, and corrects raw read errors using an advanced LDPC ECC core.",
        "specs": [
            ("Architecture", "ARM Cortex-R8 Multi-Core"),
            ("Node Size", "12nm FinFET Technology"),
            ("Flash Channels", "8 Channels (ONFI 5.0 at 2400MT/s)"),
            ("ECC Engine", "LDPC (Low-Density Parity-Check) v3.0"),
            ("Encryption", "AES-256 Bit Hardware Cryptography")
        ],
        "flow": "Intercepts write tasks, caches mapping updates in the DRAM cache, splits payloads into 8 channels, and programs NAND sectors. During reads, it verifies cell integrity via LDPC before returning data."
    },
    "dram": {
        "title": "LPDDR4 DRAM Cache Memory",
        "badge": "High-Speed Volatile Cache",
        "desc": "Ultra-fast memory storing the dynamic Flash Translation Layer (FTL) lookup table. Rather than reading slower NAND pages just to locate file addresses, the Controller reads/writes FTL index locations instantly in DRAM, maximizing throughput.",
        "specs": [
            ("Standard", "LPDDR4 SDRAM (Low Power DDR4)"),
            ("Capacity", "1 GB (1,024 Megabytes)"),
            ("Frequency", "2133 MHz (Effective 4266 MT/s)"),
            ("Latency", "< 10 Nanoseconds (Extremely Fast)"),
            ("Bus Width", "32-Bit Dedicated Memory Interface")
        ],
        "flow": "Buffers temporary sequential writes before flashing them to NAND. Holds the live FTL tables to quicken address lookups during execution."
    },
    "nand": {
        "title": "3D TLC NAND Flash Memory Array",
        "badge": "Non-Volatile Storage",
        "desc": "High-density persistent memory dies. This SSD integrates 8 stacked 3D TLC (Triple-Level Cell) chips, achieving 1TB capacity. Vertical cell stacking allows high storage densities and fast parallel channel speeds.",
        "specs": [
            ("Total Size", "1 TB (8 × 128 GB Dies)"),
            ("Cell Type", "3D TLC (3 Bits program state per cell)"),
            ("Vertical Layers", "176-Layer Stacked Architecture"),
            ("Durability", "600 TBW (Total Bytes Written) Lifetime"),
            ("Block Size", "16 KB Page / 16 MB Erase Block")
        ],
        "flow": "The final resting place of files. Electrostatic charge trap cells hold electrons long-term. Read voltages sense the threshold of these blocks, and write operations program them."
    }
}

# ═══════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS FOR RENDERING BEAUTIFUL VECTOR SHAPES
# ═══════════════════════════════════════════════════════════════════════════
def draw_rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    """Draws a pixel-perfect rounded rectangle on the Tkinter canvas."""
    fill = kwargs.get("fill", "")
    outline = kwargs.get("outline", "")
    width = kwargs.get("width", 1)
    tags = kwargs.get("tags", ())
    
    # Render filled shapes if color is specified
    f_items = []
    if fill:
        a1 = canvas.create_arc(x1, y1, x1+2*r, y1+2*r, start=90, extent=90, fill=fill, outline="", style="pieslice", tags=tags)
        a2 = canvas.create_arc(x2-2*r, y1, x2, y1+2*r, start=0, extent=90, fill=fill, outline="", style="pieslice", tags=tags)
        a3 = canvas.create_arc(x2-2*r, y2-2*r, x2, y2, start=270, extent=90, fill=fill, outline="", style="pieslice", tags=tags)
        a4 = canvas.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90, fill=fill, outline="", style="pieslice", tags=tags)
        r1 = canvas.create_rectangle(x1+r, y1, x2-r, y2, fill=fill, outline="", tags=tags)
        r2 = canvas.create_rectangle(x1, y1+r, x2, y2-r, fill=fill, outline="", tags=tags)
        f_items.extend([a1, a2, a3, a4, r1, r2])
        
    # Render outline paths
    ol_items = []
    if outline:
        l1 = canvas.create_line(x1+r, y1, x2-r, y1, fill=outline, width=width, tags=tags)
        l2 = canvas.create_line(x2, y1+r, x2, y2-r, fill=outline, width=width, tags=tags)
        l3 = canvas.create_line(x2-r, y2, x1+r, y2, fill=outline, width=width, tags=tags)
        l4 = canvas.create_line(x1, y2-r, x1, y1+r, fill=outline, width=width, tags=tags)
        
        a1_o = canvas.create_arc(x1, y1, x1+2*r, y1+2*r, start=90, extent=90, outline=outline, width=width, style="arc", tags=tags)
        a2_o = canvas.create_arc(x2-2*r, y1, x2, y1+2*r, start=0, extent=90, outline=outline, width=width, style="arc", tags=tags)
        a3_o = canvas.create_arc(x2-2*r, y2-2*r, x2, y2, start=270, extent=90, outline=outline, width=width, style="arc", tags=tags)
        a4_o = canvas.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90, outline=outline, width=width, style="arc", tags=tags)
        ol_items.extend([l1, l2, l3, l4, a1_o, a2_o, a3_o, a4_o])
        
    return f_items + ol_items


def get_path_point(path, t):
    """Linearly interpolates points along a multiline coordinate array."""
    if t <= 0: return path[0]
    if t >= 1: return path[-1]
    
    n_segs = len(path) - 1
    seg_idx = int(t * n_segs)
    if seg_idx >= n_segs:
        seg_idx = n_segs - 1
        
    seg_t = (t * n_segs) - seg_idx
    p0 = path[seg_idx]
    p1 = path[seg_idx+1]
    
    x = p0[0] + (p1[0] - p0[0]) * seg_t
    y = p0[1] + (p1[1] - p0[1]) * seg_t
    return x, y

# ═══════════════════════════════════════════════════════════════════════════
# MAIN INTERACTIVE WINDOW APPLICATION
# ═══════════════════════════════════════════════════════════════════════════
class SSDExplorerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SSD Solid State Drive - Interactive Architecture & Data Flow")
        self.geometry("1280x760")
        self.configure(bg=COLOR_BG_DARKEST)
        
        # Keep window size static for predictable coordinate mappings
        self.resizable(False, False)
        
        # Load custom fonts
        self.font_title = tkfont.Font(family="Helvetica", size=14, weight="bold")
        self.font_subtitle = tkfont.Font(family="Helvetica", size=11, weight="bold")
        self.font_body = tkfont.Font(family="Helvetica", size=10)
        self.font_mono = tkfont.Font(family="Consolas", size=10)
        self.font_metric = tkfont.Font(family="Consolas", size=18, weight="bold")
        
        # Application State
        self.active_mode = "idle"
        self.selected_component = None
        self.dram_buffer_percent = 5.0
        self.packets = []
        self.packet_spawn_counter = 0
        
        # Initialize UI Grid layouts
        self.setup_ui_layout()
        self.setup_pcb_diagram()
        self.setup_paths()
        
        # Select connector initially to avoid empty state
        self.select_component("connector")
        
        # Start core GUI rendering & animation tick loop
        self.animation_loop()

    # ═══════════════════════════════════════════════════════════════════════
    # SETUP LAYOUT CONTAINERS
    # ═══════════════════════════════════════════════════════════════════════
    def setup_ui_layout(self):
        # 1. Main Header
        header_frame = tk.Frame(self, bg=COLOR_BG_DARKER, height=60, bd=0, highlightthickness=1, highlightbackground=COLOR_BORDER)
        header_frame.pack(side="top", fill="x", padx=15, pady=(15, 0))
        header_frame.pack_propagate(False)
        
        lbl_logo = tk.Label(header_frame, text="⚡ SSD ARCHITECTURE EXPLORER", font=self.font_title, fg="#ffffff", bg=COLOR_BG_DARKER)
        lbl_logo.pack(side="left", padx=15)
        
        badge_frame = tk.Frame(header_frame, bg="#1e293b", padx=8, pady=3)
        badge_frame.pack(side="right", padx=15)
        lbl_badge = tk.Label(badge_frame, text="M.2 NVMe PCIe Gen 4x4", font=self.font_mono, fg="#38bdf8", bg="#1e293b")
        lbl_badge.pack()

        # 2. Main Workspace Body
        self.body_frame = tk.Frame(self, bg=COLOR_BG_DARKEST)
        self.body_frame.pack(side="bottom", fill="both", expand=True, padx=15, pady=15)

        # Left Column: Canvas PCB Drawing View
        self.left_column = tk.Frame(self.body_frame, bg=COLOR_BG_DARKEST)
        self.left_column.pack(side="left", fill="both", expand=True)
        
        # Right Column: Side Controller & Specs Drawer
        self.right_column = tk.Frame(self.body_frame, bg=COLOR_BG_DARKEST, width=380)
        self.right_column.pack(side="right", fill="both", expand=False, padx=(15, 0))
        self.right_column.pack_propagate(False)

        self.setup_right_sidebar()

    # ═══════════════════════════════════════════════════════════════════════
    # SETUP THE INTERACTIVE SIDEBAR & DIAGNOSTICS
    # ═══════════════════════════════════════════════════════════════════════
    def setup_right_sidebar(self):
        # A. Mode Simulator Controller Card
        ctrl_card = tk.Frame(self.right_column, bg=COLOR_BG_DARKER, bd=0, highlightthickness=1, highlightbackground=COLOR_BORDER)
        ctrl_card.pack(fill="x", pady=(0, 10))
        
        tk.Label(ctrl_card, text="Operation Mode Simulator", font=self.font_subtitle, fg="#ffffff", bg=COLOR_BG_DARKER, anchor="w").pack(fill="x", padx=15, pady=(12, 8))
        
        btn_frame = tk.Frame(ctrl_card, bg=COLOR_BG_DARKER)
        btn_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.buttons = {}
        modes = [
            ("idle", "Idle Mode", "#64748b"),
            ("read", "Read Mode", "#3b82f6"),
            ("write", "Write Mode", "#f97316"),
            ("maintenance", "Garbage Col.", "#10b981")
        ]
        
        for i, (mode_id, label, color) in enumerate(modes):
            r = i // 2
            c = i % 2
            btn = tk.Button(
                btn_frame, text=label, font=self.font_body, fg="#94a3b8", bg="#1e293b",
                activebackground="#334155", activeforeground="#ffffff", relief="flat", bd=0,
                command=lambda m=mode_id: self.change_mode(m)
            )
            btn.grid(row=r, column=c, sticky="nsew", padx=4, pady=4)
            btn_frame.grid_columnconfigure(c, weight=1)
            self.buttons[mode_id] = (btn, color)
            
        self.update_button_states()

        # B. Diagnostics Dashboard Card
        diag_card = tk.Frame(self.right_column, bg=COLOR_BG_DARKER, bd=0, highlightthickness=1, highlightbackground=COLOR_BORDER)
        diag_card.pack(fill="x", pady=5)
        
        tk.Label(diag_card, text="Diagnostic Dashboard", font=self.font_subtitle, fg="#ffffff", bg=COLOR_BG_DARKER, anchor="w").pack(fill="x", padx=15, pady=(12, 5))
        
        self.lbl_status = tk.Label(diag_card, text="SYSTEM NOMINAL", font=self.font_mono, fg="#10b981", bg=COLOR_BG_DARKER, anchor="w")
        self.lbl_status.pack(fill="x", padx=15, pady=(0, 8))
        
        metrics_frame = tk.Frame(diag_card, bg=COLOR_BG_DARKER)
        metrics_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Grid metrics: Speed / IOPS
        m1 = tk.Frame(metrics_frame, bg="#0d1527", bd=0, highlightthickness=1, highlightbackground=COLOR_BORDER, padx=10, pady=8)
        m1.grid(row=0, column=0, sticky="nsew", padx=(0, 4))
        tk.Label(m1, text="TRANSFER SPEED", font=self.font_mono, fg="#94a3b8", bg="#0d1527", anchor="w").pack(fill="x")
        self.lbl_metric_speed = tk.Label(m1, text="0 MB/s", font=self.font_metric, fg="#ffffff", bg="#0d1527", anchor="w")
        self.lbl_metric_speed.pack(fill="x")
        
        m2 = tk.Frame(metrics_frame, bg="#0d1527", bd=0, highlightthickness=1, highlightbackground=COLOR_BORDER, padx=10, pady=8)
        m2.grid(row=0, column=1, sticky="nsew", padx=(4, 0))
        tk.Label(m2, text="FTL OPERATION", font=self.font_mono, fg="#94a3b8", bg="#0d1527", anchor="w").pack(fill="x")
        self.lbl_metric_iops = tk.Label(m2, text="0 IOPS", font=self.font_metric, fg="#ffffff", bg="#0d1527", anchor="w")
        self.lbl_metric_iops.pack(fill="x")
        
        metrics_frame.grid_columnconfigure(0, weight=1)
        metrics_frame.grid_columnconfigure(1, weight=1)
        
        # ECC Status
        ecc_frame = tk.Frame(diag_card, bg=COLOR_BG_DARKER)
        ecc_frame.pack(fill="x", padx=15, pady=(0, 5))
        tk.Label(ecc_frame, text="ECC Engine Correction Level:", font=self.font_body, fg="#94a3b8", bg=COLOR_BG_DARKER).pack(side="left")
        self.lbl_ecc = tk.Label(ecc_frame, text="BER < 10⁻¹⁰", font=self.font_mono, fg="#10b981", bg=COLOR_BG_DARKER)
        self.lbl_ecc.pack(side="right")
        
        # DRAM Buffer Bar
        db_frame = tk.Frame(diag_card, bg=COLOR_BG_DARKER)
        db_frame.pack(fill="x", padx=15, pady=(0, 15))
        tk.Label(db_frame, text="DRAM Write Cache Buffer Capacity:", font=self.font_body, fg="#94a3b8", bg=COLOR_BG_DARKER, anchor="w").pack(fill="x", pady=(5, 3))
        
        self.dram_bar_canvas = tk.Canvas(db_frame, height=14, bg="#1e293b", bd=0, highlightthickness=0)
        self.dram_bar_canvas.pack(fill="x")
        self.dram_bar_fill = self.dram_bar_canvas.create_rectangle(0, 0, 0, 14, fill="#fb923c", outline="")

        # C. Interactive Explanatory Details Card
        self.details_card = tk.Frame(self.right_column, bg=COLOR_BG_DARKER, bd=0, highlightthickness=1, highlightbackground=COLOR_BORDER)
        self.details_card.pack(fill="both", expand=True, pady=(5, 0))
        
        # Headers inside card
        det_header = tk.Frame(self.details_card, bg=COLOR_BG_DARKER)
        det_header.pack(fill="x", padx=15, pady=(12, 5))
        
        self.lbl_det_title = tk.Label(det_header, text="Select Component", font=self.font_subtitle, fg="#ffffff", bg=COLOR_BG_DARKER, anchor="w")
        self.lbl_det_title.pack(side="left")
        
        self.lbl_det_badge = tk.Label(det_header, text="Overview", font=self.font_mono, fg="#94a3b8", bg="#1e293b", padx=6, pady=2)
        self.lbl_det_badge.pack(side="right")
        
        # Inner scroll/details body
        self.det_body = tk.Frame(self.details_card, bg=COLOR_BG_DARKER)
        self.det_body.pack(fill="both", expand=True, padx=15, pady=(5, 12))
        
        self.lbl_det_desc = tk.Label(self.det_body, text="", font=self.font_body, fg="#94a3b8", bg=COLOR_BG_DARKER, wraplength=330, justify="left", anchor="w")
        self.lbl_det_desc.pack(fill="x", pady=(0, 8))
        
        # Specifications Table representation
        tk.Label(self.det_body, text="TECHNICAL SPECIFICATIONS", font=self.font_mono, fg="#38bdf8", bg=COLOR_BG_DARKER, anchor="w").pack(fill="x", pady=(5, 2))
        
        self.specs_table = tk.Frame(self.det_body, bg=COLOR_BG_DARKER)
        self.specs_table.pack(fill="x", pady=2)
        
        # Role in data flow explanation
        tk.Label(self.det_body, text="ROLE IN DATA FLOW", font=self.font_mono, fg="#38bdf8", bg=COLOR_BG_DARKER, anchor="w").pack(fill="x", pady=(10, 2))
        self.lbl_det_flow = tk.Label(self.det_body, text="", font=self.font_body, fg="#94a3b8", bg=COLOR_BG_DARKER, wraplength=330, justify="left", anchor="w")
        self.lbl_det_flow.pack(fill="x")

    # ═══════════════════════════════════════════════════════════════════════
    # SETUP THE PCB DIAGRAM CANVAS
    # ═══════════════════════════════════════════════════════════════════════
    def setup_pcb_diagram(self):
        # 1. Main Canvas Area
        canvas_border = tk.Frame(self.left_column, bg=COLOR_BG_DARKER, bd=0, highlightthickness=1, highlightbackground=COLOR_BORDER)
        canvas_border.pack(fill="both", expand=True)
        
        self.canvas = tk.Canvas(canvas_border, bg=COLOR_BG_DARKEST, bd=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 2. PCB Base Board
        draw_rounded_rect(self.canvas, 20, 20, 830, 530, 20, fill=COLOR_PCB_GREEN, outline=COLOR_PCB_BORDER, width=3)
        
        # Decorative grids & lines
        for y in range(80, 500, 60):
            self.canvas.create_line(20, y, 830, y, fill=COLOR_GRID_LINE, width=1, dash=(8, 8))
        for x in range(120, 800, 100):
            self.canvas.create_line(x, 20, x, 530, fill=COLOR_GRID_LINE, width=1, dash=(8, 8))
            
        # Background routing tracks
        tracks = [
            (90, 275, 160, 275),
            (250, 150, 250, 100, 400, 100),
            (340, 275, 370, 215, 400, 215),
            (340, 275, 370, 300, 400, 300),
            (340, 275, 370, 385, 400, 385),
            (340, 275, 370, 470, 400, 470),
            (340, 275, 360, 150, 550, 150, 550, 215, 570, 215),
            (340, 275, 360, 150, 550, 150, 550, 300, 570, 300),
            (340, 275, 360, 520, 550, 520, 550, 385, 570, 385),
            (340, 275, 360, 520, 550, 520, 550, 470, 570, 470)
        ]
        for trk in tracks:
            self.canvas.create_line(*trk, fill="#132718", width=2, capstyle="round")

        # 3. INTERACTIVE CHIP ELEMENTS

        # A. Connector Chip
        draw_rounded_rect(self.canvas, 30, 180, 90, 370, 10, fill="#78500c", outline=COLOR_CONNECTOR, width=2, tags=("connector",))
        # Draw Gold Teeth
        for ty in range(195, 360, 14):
            self.canvas.create_rectangle(32, ty, 48, ty+8, fill="#ffd040", outline="#b88810", tags=("connector",))
        self.canvas.create_text(70, 275, text="M.2 KEY", fill="#ffffff", font=self.font_mono, angle=90, tags=("connector",))
        self.canvas.create_text(60, 160, text="M.2 PCIe Gen4", fill=COLOR_CONNECTOR, font=self.font_mono, tags=("connector",))

        # B. Controller Chip
        draw_rounded_rect(self.canvas, 160, 150, 340, 400, 15, fill="#0c447c", outline=COLOR_CONTROLLER, width=3, tags=("controller",))
        # Inner silicon die layout
        draw_rounded_rect(self.canvas, 180, 170, 320, 380, 10, fill="#0a3060", outline="#2266a8", tags=("controller",))
        # Corner pin dot
        self.canvas.create_oval(192, 182, 202, 192, fill=COLOR_CONTROLLER, outline="", tags=("controller",))
        # Text
        self.canvas.create_text(250, 250, text="CONTROLLER", fill="#ffffff", font=self.font_subtitle, tags=("controller",))
        self.canvas.create_text(250, 280, text="FTL Engine", fill="#7ab8f0", font=self.font_mono, tags=("controller",))
        self.canvas.create_text(250, 305, text="LDPC ECC v3.0", fill="#7ab8f0", font=self.font_mono, tags=("controller",))
        self.canvas.create_text(250, 340, text="ARM core", fill="#15e6a2", font=self.font_mono, tags=("controller",))

        # C. DRAM Cache
        draw_rounded_rect(self.canvas, 400, 50, 530, 150, 10, fill="#412402", outline=COLOR_DRAM, width=2.5, tags=("dram",))
        draw_rounded_rect(self.canvas, 415, 65, 515, 135, 6, fill="#2e1a02", outline="#7a5010", tags=("dram",))
        self.canvas.create_text(465, 90, text="DRAM", fill="#ffffff", font=self.font_subtitle, tags=("dram",))
        self.canvas.create_text(465, 115, text="1GB LPDDR4", fill="#FAC775", font=self.font_mono, tags=("dram",))

        # D. NAND Flash array (8 distinct chips: 2 columns * 4 rows)
        self.nand_chips = []
        nand_specs = [
            # Col 1
            (400, 180, 530, 250, "01"), (400, 265, 530, 335, "02"),
            (400, 350, 530, 420, "03"), (400, 435, 530, 505, "04"),
            # Col 2
            (570, 180, 700, 250, "05"), (570, 265, 700, 335, "06"),
            (570, 350, 700, 420, "07"), (570, 435, 700, 505, "08")
        ]
        
        for idx, (nx1, ny1, nx2, ny2, die_num) in enumerate(nand_specs):
            nand_tag = f"nand_{die_num}"
            draw_rounded_rect(self.canvas, nx1, ny1, nx2, ny2, 10, fill="#085041", outline=COLOR_NAND, width=2, tags=(nand_tag, "nand_group"))
            draw_rounded_rect(self.canvas, nx1+10, ny1+10, nx2-10, ny2-10, 6, fill="#043428", outline="#0F6E56", tags=(nand_tag, "nand_group"))
            self.canvas.create_text((nx1+nx2)/2, (ny1+ny2)/2 - 8, text="NAND FLASH", fill="#ffffff", font=self.font_subtitle, tags=(nand_tag, "nand_group"))
            self.canvas.create_text((nx1+nx2)/2, (ny1+ny2)/2 + 10, text=f"Die #{die_num} - 128GB", fill="#9FE1CB", font=self.font_mono, tags=(nand_tag, "nand_group"))
            self.nand_chips.append(nand_tag)

        # Header Label for NAND array
        self.canvas.create_text(550, 35, text="1TB Stacked 3D TLC NAND Array", fill="#9FE1CB", font=self.font_subtitle, anchor="center")

        # 4. BIND CLICK AND HOVER EVENTS
        self.setup_canvas_event_bindings()

    # ═══════════════════════════════════════════════════════════════════════
    # SETUP COORDINATE PATHS FOR DATA PACKET ROUTING
    # ═══════════════════════════════════════════════════════════════════════
    def setup_paths(self):
        # Coordinates mapped precisely to canvas connections
        self.paths = {
            "pcie": [(90, 275), (160, 275)],
            "dram": [(250, 250), (250, 100), (400, 100)],
            
            # Col 1 Chips
            "nand_01": [(250, 275), (340, 275), (370, 215), (400, 215)],
            "nand_02": [(250, 275), (340, 275), (370, 300), (400, 300)],
            "nand_03": [(250, 275), (340, 275), (370, 385), (400, 385)],
            "nand_04": [(250, 275), (340, 275), (370, 470), (400, 470)],
            
            # Col 2 Chips (Routing paths bypass col 1)
            "nand_05": [(250, 275), (340, 275), (360, 150), (550, 150), (550, 215), (570, 215)],
            "nand_06": [(250, 275), (340, 275), (360, 150), (550, 150), (550, 300), (570, 300)],
            "nand_07": [(250, 275), (340, 275), (360, 520), (550, 520), (550, 385), (570, 385)],
            "nand_08": [(250, 275), (340, 275), (360, 520), (550, 520), (550, 470), (570, 470)],
        }

    # ═══════════════════════════════════════════════════════════════════════
    # CANVAS EVENT BINDINGS (Clicks / Hover States)
    # ═══════════════════════════════════════════════════════════════════════
    def setup_canvas_event_bindings(self):
        # We map simple tags
        interactive_tags = ["connector", "controller", "dram"] + self.nand_chips
        
        for tag in interactive_tags:
            # Click
            self.canvas.tag_bind(tag, "<Button-1>", lambda e, t=tag: self.on_component_click(t))
            # Enter (Hover)
            self.canvas.tag_bind(tag, "<Enter>", lambda e, t=tag: self.on_component_enter(t))
            # Leave
            self.canvas.tag_bind(tag, "<Leave>", lambda e, t=tag: self.on_component_leave(t))

    def on_component_click(self, tag):
        # De-select currently selected borders visual outline
        self.clear_selection_visuals()
        
        # Find type
        comp_type = tag
        chip_id = None
        if tag.startswith("nand_"):
            comp_type = "nand"
            chip_id = tag.split("_")[1]
            
        self.selected_component = tag
        self.select_component(comp_type, chip_id)
        
        # Add a thick selection stroke outline on selected element
        self.apply_selection_visual(tag, active=True)

    def on_component_enter(self, tag):
        self.canvas.config(cursor="hand2")
        if self.selected_component != tag:
            self.apply_selection_visual(tag, active=True)

    def on_component_leave(self, tag):
        self.canvas.config(cursor="")
        if self.selected_component != tag:
            self.apply_selection_visual(tag, active=False)

    def apply_selection_visual(self, tag, active):
        # Map highlighting colors
        color_map = {
            "connector": ("#ffd700" if active else COLOR_CONNECTOR),
            "controller": ("#60a5fa" if active else COLOR_CONTROLLER),
            "dram": ("#fbbf24" if active else COLOR_DRAM),
        }
        
        color = "#5dcaa5" if active else COLOR_NAND
        if not tag.startswith("nand_"):
            color = color_map.get(tag, "#ffffff")
            
        items = self.canvas.find_withtag(tag)
        for item in items:
            itype = self.canvas.type(item)
            if itype in ("arc", "rectangle"):
                try:
                    self.canvas.itemconfigure(item, outline=color)
                except tk.TclError:
                    pass
            elif itype == "line":
                try:
                    self.canvas.itemconfigure(item, fill=color)
                except tk.TclError:
                    pass

    def clear_selection_visuals(self):
        self.restore_tag_color("connector", COLOR_CONNECTOR)
        self.restore_tag_color("controller", COLOR_CONTROLLER)
        self.restore_tag_color("dram", COLOR_DRAM)
        self.restore_tag_color("nand_group", COLOR_NAND)

    def restore_tag_color(self, tag, color):
        items = self.canvas.find_withtag(tag)
        for item in items:
            itype = self.canvas.type(item)
            if itype in ("arc", "rectangle"):
                try:
                    self.canvas.itemconfigure(item, outline=color)
                except tk.TclError:
                    pass
            elif itype == "line":
                try:
                    self.canvas.itemconfigure(item, fill=color)
                except tk.TclError:
                    pass

    # ═══════════════════════════════════════════════════════════════════════
    # SELECTION LOGIC & DETAIL CARD UPDATING
    # ═══════════════════════════════════════════════════════════════════════
    def select_component(self, comp_type, chip_id=None):
        data = COMPONENT_DATA.get(comp_type)
        if not data: return
        
        # Set Header Details
        title = data["title"]
        if comp_type == "nand" and chip_id:
            title = f"NAND Flash Die #{chip_id} (Sector {chip_id})"
            
        self.lbl_det_title.config(text=title)
        self.lbl_det_badge.config(text=data["badge"])
        self.lbl_det_desc.config(text=data["desc"])
        self.lbl_det_flow.config(text=data["flow"])
        
        # Re-build Specs Grid table
        for widget in self.specs_table.winfo_children():
            widget.destroy()
            
        for r, (name, val) in enumerate(data["specs"]):
            # Name Col
            lbl_name = tk.Label(self.specs_table, text=name, font=self.font_mono, fg="#94a3b8", bg=COLOR_BG_DARKER, anchor="w")
            lbl_name.grid(row=r, column=0, sticky="ew", pady=2, padx=(0, 10))
            
            # Val Col
            lbl_val = tk.Label(self.specs_table, text=val, font=self.font_body, fg="#ffffff", bg=COLOR_BG_DARKER, anchor="w")
            lbl_val.grid(row=r, column=1, sticky="ew", pady=2)
            
        # If it's a specific NAND, add its channel routing mapping
        if comp_type == "nand" and chip_id:
            idx = int(chip_id)
            lbl_name = tk.Label(self.specs_table, text="Routing Bus", font=self.font_mono, fg="#94a3b8", bg=COLOR_BG_DARKER, anchor="w")
            lbl_name.grid(row=5, column=0, sticky="ew", pady=2, padx=(0, 10))
            
            chan = (idx + 1) // 2
            lbl_val = tk.Label(self.specs_table, text=f"Channel {chan} (CE{idx % 2})", font=self.font_body, fg="#ffffff", bg=COLOR_BG_DARKER, anchor="w")
            lbl_val.grid(row=5, column=1, sticky="ew", pady=2)

        # Force render refresh
        self.specs_table.grid_columnconfigure(1, weight=1)

    # ═══════════════════════════════════════════════════════════════════════
    # SIMULATOR STATE CHANGER
    # ═══════════════════════════════════════════════════════════════════════
    def change_mode(self, mode):
        self.active_mode = mode
        self.update_button_states()
        
        # Clear animating packets
        for packet in self.packets:
            self.canvas.delete(packet["id"])
        self.packets.clear()

        # Specific Reset parameters
        if mode == "idle":
            self.lbl_status.config(text="SYSTEM STATUS: NOMINAL", fg="#10b981")
            self.lbl_metric_speed.config(text="0 MB/s")
            self.lbl_metric_iops.config(text="0 IOPS")
            self.lbl_ecc.config(text="BER < 10⁻¹⁰", fg="#10b981")
        elif mode == "read":
            self.lbl_status.config(text="DATA TRANSFER: READ CYCLE", fg="#3b82f6")
        elif mode == "write":
            self.lbl_status.config(text="DATA TRANSFER: WRITE CYCLE", fg="#f97316")
        elif mode == "maintenance":
            self.lbl_status.config(text="MAINTENANCE: GARBAGE COLLECTION", fg="#10b981")

    def update_button_states(self):
        for mode_id, (btn, color) in self.buttons.items():
            if mode_id == self.active_mode:
                btn.config(bg=color, fg="#ffffff", font=self.font_subtitle)
            else:
                btn.config(bg="#1e293b", fg="#94a3b8", font=self.font_body)

    # ═══════════════════════════════════════════════════════════════════════
    # PHYSICS TICK AND RENDERING CYCLE ENGINE (60 FPS approximate)
    # ═══════════════════════════════════════════════════════════════════════
    def animation_loop(self):
        # A. Trigger Packet Spawns according to mode rules
        self.packet_spawn_counter += 1
        
        if self.active_mode == "write" and self.packet_spawn_counter % 8 == 0:
            # Spawn PCIe Packet (orange)
            self.spawn_packet("pcie", COLOR_CONNECTOR, direction=1)
            # Spawn DRAM Packet (amber)
            self.spawn_packet("dram", COLOR_DRAM, direction=1)
            # Spawn NAND Packets (green)
            for chip_tag in self.nand_chips:
                self.spawn_packet(chip_tag, COLOR_NAND, direction=1)
                
        elif self.active_mode == "read" and self.packet_spawn_counter % 8 == 0:
            # Spawn PCIe Packet (orange, backward)
            self.spawn_packet("pcie", COLOR_CONNECTOR, direction=-1)
            # Spawn DRAM Packet (amber, backward)
            self.spawn_packet("dram", COLOR_DRAM, direction=-1)
            # Spawn NAND Packets (green, backward)
            for chip_tag in self.nand_chips:
                self.spawn_packet(chip_tag, COLOR_NAND, direction=-1)
                
        elif self.active_mode == "maintenance" and self.packet_spawn_counter % 12 == 0:
            # Internal copying: read from odd dies, write to even dies
            for i, chip_tag in enumerate(self.nand_chips):
                if i % 2 == 0:
                    self.spawn_packet(chip_tag, COLOR_NAND, direction=-1)  # Read out
                else:
                    self.spawn_packet(chip_tag, COLOR_NAND, direction=1)   # Write in
            self.spawn_packet("dram", COLOR_DRAM, direction=1)

        # B. Move Active Packets along Paths
        dead_packets = []
        for packet in self.packets:
            packet["progress"] += packet["speed"]
            
            if packet["progress"] >= 1.0:
                dead_packets.append(packet)
            else:
                t = packet["progress"] if packet["direction"] == 1 else (1.0 - packet["progress"])
                x, y = get_path_point(packet["path"], t)
                self.canvas.coords(packet["id"], x-4, y-4, x+4, y+4)
                
        # Cleanup completed packets
        for packet in dead_packets:
            self.canvas.delete(packet["id"])
            self.packets.remove(packet)

        # C. Update Real-time Statistics
        self.update_live_metrics()

        # D. Queue next loop frame (~30ms intervals)
        self.after(30, self.animation_loop)

    def spawn_packet(self, path_key, color, direction):
        path = self.paths.get(path_key)
        if not path: return
        
        # Draw packet dot
        p_id = self.canvas.create_oval(0, 0, 0, 0, fill=color, outline="")
        
        packet = {
            "id": p_id,
            "path": path,
            "progress": 0.0,
            "speed": 0.015 + random.random() * 0.01,  # slightly randomized velocity
            "color": color,
            "direction": direction
        }
        self.packets.append(packet)

    def update_live_metrics(self):
        # Update metrics dynamically depending on the current operation mode
        if self.active_mode == "idle":
            self.dram_buffer_percent = max(5.0, self.dram_buffer_percent - 0.5)
            
        elif self.active_mode == "read":
            speed_val = int(SPEED_READ + random.randint(-250, 250))
            iops_val = int(880000 + random.randint(-40000, 40000))
            ber = 1.2 + random.random() * 2
            
            self.lbl_metric_speed.config(text=f"{speed_val} MB/s")
            self.lbl_metric_iops.config(text=f"{iops_val:,}")
            self.lbl_ecc.config(text=f"LDPC {ber:.1f}e-6", fg="#fb923c")
            
            # Static buffer size for reads
            self.dram_buffer_percent = 25.0 + random.uniform(-1, 1)
            
        elif self.active_mode == "write":
            speed_val = int(SPEED_WRITE + random.randint(-400, 400))
            iops_val = int(680000 + random.randint(-30000, 30000))
            
            self.lbl_metric_speed.config(text=f"{speed_val} MB/s")
            self.lbl_metric_iops.config(text=f"{iops_val:,}")
            self.lbl_ecc.config(text="BER < 10⁻¹⁰", fg="#10b981")
            
            # Animate the DRAM Cache buffer filling up and flushing
            self.dram_buffer_percent += 0.8
            if self.dram_buffer_percent >= 96.0:
                self.dram_buffer_percent = 20.0
                
        elif self.active_mode == "maintenance":
            iops_val = int(140000 + random.randint(-15000, 15000))
            ber = 2.4 + random.random() * 1.5
            
            self.lbl_metric_speed.config(text="0 MB/s (Host)")
            self.lbl_metric_iops.config(text=f"{iops_val:,}")
            self.lbl_ecc.config(text=f"LDPC {ber:.1f}e-6", fg="#fb923c")
            
            # Active buffering of tables
            self.dram_buffer_percent = 45.0 + random.uniform(-3, 3)

        # Update the progress bar width
        canvas_width = self.dram_bar_canvas.winfo_width()
        if canvas_width > 1:
            target_width = int(canvas_width * (self.dram_buffer_percent / 100.0))
            self.dram_bar_canvas.coords(self.dram_bar_fill, 0, 0, target_width, 14)


# ═══════════════════════════════════════════════════════════════════════════
# APPLICATION INITIALIZATION ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = SSDExplorerApp()
    app.mainloop()