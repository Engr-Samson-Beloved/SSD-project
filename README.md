# Solid State Drive (SSD) Architecture Explorer

A comprehensive graphical and interactive simulation of Solid State Drive (SSD) internal components, physical PCB routing, and real-time data flow operations. This project features dual implementations: a native **Python Desktop GUI Application** and a modern **Web-based Interactive Dashboard**.

---

## 🚀 Key Features

*   **Interactive PCB Layout Vector Graphics:** Fully detailed representations of the M.2 NVMe interface connector, the multi-core ARM Controller, the low-latency LPDDR4 DRAM cache, and the 8× 3D TLC NAND Flash memory array.
*   **Animated Data Flow Visualization:** Custom particle routing that maps command flows in real-time depending on the operation mode:
    *   *Idle Mode:* Minimal trace activity.
    *   *Read Mode:* Data packets stream from NAND Flash memory dies, through the Controller, and out to the M.2 PCIe host interface.
    *   *Write Mode:* Payloads flow from the host interface, buffer in the DRAM Cache, and program parallel lines to individual NAND sectors.
    *   *Garbage Collection (GC):* Visualizes internal wear-leveling and blocks cleanup cycling inside the flash arrays.
*   **Live Performance Diagnostics:** Real-time dashboards showcasing dynamically changing read/write throughput speeds (up to 7,400 MB/s), active FTL IOPS, LDPC ECC bit-error rates, and dynamic DRAM write cache fills.
*   **Detailed Specifications Card:** Hover and click interactions that select individual chips, instantly displaying technical parameters, specifications, and their exact operational role in the drive architecture.

---

## 🛠️ Project Implementations

The project is structured to offer both desktop and web-based execution paths:

### 1. Python Desktop GUI Application (`ssd.py`)
Built entirely on top of Python's standard `tkinter` library. It requires **no external packages or installations**, rendering graphics natively and smoothly on Windows systems.

#### How to Run:
Ensure you have Python 3.x installed. Navigate to the project directory and run:
```powershell
python ssd.py
```

### 2. Web-based Interactive Dashboard (`index.html`)
An elegant web implementation utilizing responsive inline SVG elements, modern glassmorphic layouts, CSS keyframe animations for trace flows, and vanilla JavaScript for simulation states.

#### How to Run:
Simply double-click the `index.html` file to open and explore the layout in your default web browser.

---

## 📂 Repository Structure

```
SSD-project/
├── ssd.py          # Native Python Tkinter Desktop GUI Application
├── index.html      # Web Dashboard Structure & Inline SVG PCB Vector Layout
├── index.css       # Premium Styling, Glassmorphic effects, and Trace Animations
├── index.js        # Event Bindings, Specs Table, and Diagnostic Sim Loops
└── README.md       # Project Documentation
```

---

## 📖 Component Descriptions

*   **M.2 Interface Connector:** Links the host system to the drive using the M.2 2280 form factor. It provides four PCIe 4.0 lanes mapped to the NVMe 2.0 command protocol.
*   **SSD Controller Chipset:** The CPU managing FTL algorithms, wear leveling, bad block allocation, encryption, and LDPC error correction.
*   **DRAM Cache Memory:** A high-speed volatile LPDDR4 buffer storing FTL lookup indices to avoid slow NAND searches.
*   **NAND Flash Arrays:** The physical non-volatile storage blocks comprising 176-layer stacked 3D TLC cell matrices.