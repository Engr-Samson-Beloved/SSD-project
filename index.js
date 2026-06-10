// SSD Architecture Data and Interactive Simulation Logic

// Technical specification metadata for components
const componentData = {
    connector: {
        title: "M.2 PCIe 4.0 Interface Connector",
        badge: "Host Connection",
        description: "The physical and logical interface connecting the SSD directly to the motherboard. It utilizes the M.2 (2280 form factor) standard, utilizing four high-speed PCIe 4.0 lanes and the NVMe 2.0 command protocol to minimize communication latency.",
        specs: [
            ["Form Factor", "M.2 2280 (Single-sided)"],
            ["Bus Interface", "PCI Express Gen 4.0 ×4 Lanes"],
            ["Protocol", "NVMe 2.0 (Non-Volatile Memory Express)"],
            ["Bandwidth Capability", "Up to 8,000 MB/s (Theoretical)"],
            ["Connector Pins", "75 Pin Edge Key (M-Key configuration)"],
            ["Active Power Rails", "3.3V Host Power Delivery"]
        ],
        flow: "All data reads and writes start here. Reads flow from the controller back to the connector to reach the computer's CPU. Writes flow from the connector pins directly to the controller for buffering and block allocation."
    },
    controller: {
        title: "SSD Controller Chipset",
        badge: "Processing Core",
        description: "The central brain of the solid-state drive. Running custom embedded firmware, the controller handles the Flash Translation Layer (FTL), performs Garbage Collection, manages Wear Leveling algorithms to extend drive lifespan, and executes error detection and correction routines (ECC).",
        specs: [
            ["Architecture", "ARM Cortex-R8 Triple-Core Processor"],
            ["Manufacturing Node", "12nm FinFET Lithography"],
            ["Flash Channels", "8 Independent Channels (ONFI 5.0 at 2400MT/s)"],
            ["Error Correction", "LDPC (Low-Density Parity-Check) Engine v3.0"],
            ["Encryption Support", "TCG Opal 2.0, AES-256 Hardware Encrypted"],
            ["Command Queues", "64k Host Queues with up to 64k commands each"]
        ],
        flow: "The operational hub. It intercepts PCIe writes, caches indexing data in the DRAM Cache, calculates parity bits for error correction, and routes block writes along its 8 channels to the NAND flash dies. During reads, it checks data integrity via ECC before sending it back."
    },
    dram: {
        title: "LPDDR4 DRAM Cache Memory",
        badge: "High-Speed Cache",
        description: "A fast, volatile storage memory that stores the FTL (Flash Translation Layer) map table. By keeping the mapping table (which translates host-provided logical addresses to real physical cell locations on the NAND chips) in RAM, the drive avoids accessing NAND flash just to look up data locations, speeding up access times.",
        specs: [
            ["Memory Standard", "LPDDR4 SDRAM (Low Power DDR4)"],
            ["Capacity", "1 GB (1,024 Megabytes)"],
            ["Clock Frequency", "2133 MHz (DDR-4266)"],
            ["Data Access Latency", "< 10 Nanoseconds (Very high performance)"],
            ["Interface Bandwidth", "32-bit Dedicated Controller Bus"],
            ["Power Consumption", "1.1V Ultra-low active power"]
        ],
        flow: "Acts as a helper. It stores the FTL translation index. During write surges, it buffers small chunks of sequential data before they are flushed in bulk to the slower NAND arrays."
    },
    nand: {
        title: "3D TLC NAND Flash Memory Chip",
        badge: "Non-Volatile Storage",
        description: "The physical storage medium of the SSD. The drive features 8 individual dies grouped into a NAND array. This architecture uses 3D TLC (Triple-Level Cell) stacking, layering memory cells vertically to maximize capacity, stability, and speed without expanding physical chip size.",
        specs: [
            ["Die Capacity", "128 GB per die (1,024 Gbit)"],
            ["Cell Technology", "3D TLC (3 bits stored per charge cell)"],
            ["Layer Structure", "176-Layer Stacked Gate Architecture"],
            ["Page Size / Block Size", "16 KB Page / 12-16 MB Erase Block size"],
            ["Write Durability", "600 TBW (Total Bytes Written) rating"],
            ["Program/Erase Speed", "1,800 µs Page Program / 3.5 ms Block Erase"]
        ],
        flow: "The final destination of data. High-precision programming voltages trap electrons in Charge-Trap cell matrices to hold data indefinitely without power. When requested, read voltages probe cell thresholds to report stored values."
    }
};

// DOM Elements
const svg = document.getElementById("ssd-svg");
const boardStatus = document.getElementById("board-status");
const simButtons = document.querySelectorAll(".sim-btn");
const diagIndicator = document.getElementById("diag-active-indicator");
const metricSpeed = document.getElementById("metric-speed");
const metricIops = document.getElementById("metric-iops");
const metricEcc = document.getElementById("metric-ecc");
const dramFillBar = document.getElementById("dram-buffer-fill");

const detailsCard = document.getElementById("details-card");
const detailsTitle = document.getElementById("details-title");
const detailsBadge = document.getElementById("details-badge");
const detailsPlaceholder = document.getElementById("details-placeholder");
const detailsContent = document.getElementById("details-content-container");
const detailsDescription = document.getElementById("details-description");
const detailsSpecsTable = document.getElementById("details-specs");
const detailsFlow = document.getElementById("details-flow");

// App State variables
let currentMode = "idle";
let activeInterval = null;
let selectedComponent = null;

// Initial setup
document.addEventListener("DOMContentLoaded", () => {
    setupInteraction();
    startModeSimulation(currentMode);
});

// Setup click and hover events for SVG nodes
function setupInteraction() {
    const components = document.querySelectorAll(".interactive-component");
    
    components.forEach(comp => {
        comp.addEventListener("click", (e) => {
            // Remove previous selected highlight
            components.forEach(c => c.classList.remove("selected"));
            
            // Add selected highlight to current target
            const target = e.currentTarget;
            target.classList.add("selected");
            
            // Show details
            const componentType = target.getAttribute("data-component");
            const chipId = target.getAttribute("data-chip-id");
            showComponentDetails(componentType, chipId);
            
            selectedComponent = target;
        });
    });
}

// Update Details Panel
function showComponentDetails(type, chipId) {
    const data = componentData[type];
    if (!data) return;

    detailsPlaceholder.classList.add("hidden");
    detailsContent.classList.remove("hidden");

    // Populate info
    let titleText = data.title;
    if (type === "nand" && chipId) {
        titleText = `NAND Flash Chip (Die #${chipId.padStart(2, '0')})`;
    }
    
    detailsTitle.textContent = titleText;
    detailsBadge.textContent = data.badge;
    detailsDescription.textContent = data.description;
    detailsFlow.textContent = data.flow;

    // Clear previous specs
    detailsSpecsTable.innerHTML = "";
    
    // Add specs to table
    data.specs.forEach(spec => {
        const row = document.createElement("tr");
        
        const nameCell = document.createElement("td");
        nameCell.textContent = spec[0];
        row.appendChild(nameCell);
        
        const valCell = document.createElement("td");
        valCell.textContent = spec[1];
        row.appendChild(valCell);
        
        detailsSpecsTable.appendChild(row);
    });

    // Custom row for NAND if selected
    if (type === "nand" && chipId) {
        const row = document.createElement("tr");
        const nameCell = document.createElement("td");
        nameCell.textContent = "Assigned Channel";
        row.appendChild(nameCell);
        
        const valCell = document.createElement("td");
        valCell.textContent = `Channel #${Math.ceil(chipId / 2)} (Die Select ${chipId % 2 === 0 ? 'CE1' : 'CE0'})`;
        row.appendChild(valCell);
        
        detailsSpecsTable.appendChild(row);
    }
}

// Mode Button Event Listeners
simButtons.forEach(btn => {
    btn.addEventListener("click", () => {
        simButtons.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        
        const mode = btn.getAttribute("data-mode");
        startModeSimulation(mode);
    });
});

// Start Real-time Metrics and Class Animations
function startModeSimulation(mode) {
    currentMode = mode;
    
    // Clear existing loop
    if (activeInterval) clearInterval(activeInterval);

    // Reset SVG class lists
    svg.classList.remove("flow-active", "mode-write", "mode-read", "mode-maintenance");

    // Set Status label
    boardStatus.textContent = `Status: ${mode.toUpperCase()}`;

    // DRAM progress control variables
    let dramPercent = 5;

    if (mode === "idle") {
        diagIndicator.textContent = "SYSTEM STATUS: NOMINAL";
        diagIndicator.className = "pulse-indicator text-green animate-pulse";
        
        metricSpeed.textContent = "0 MB/s";
        metricIops.textContent = "0 IOPS";
        metricEcc.textContent = "BER < 10⁻¹⁰";
        dramFillBar.style.width = "5%";
        
        // Disable flows
        svg.classList.remove("flow-active");
    } 
    else if (mode === "read") {
        svg.classList.add("flow-active", "mode-read");
        diagIndicator.textContent = "DATA TRANSFER: READ CYCLE";
        diagIndicator.className = "pulse-indicator text-green animate-pulse";
        
        // Loop simulation metrics
        activeInterval = setInterval(() => {
            const speed = (6800 + Math.random() * 600).toFixed(0);
            const iops = (800000 + Math.round(Math.random() * 150000)).toLocaleString();
            const eccValue = (1.2 + Math.random() * 2).toFixed(1);
            
            metricSpeed.textContent = `${speed} MB/s`;
            metricIops.textContent = `${iops} IOPS`;
            metricEcc.textContent = `LDPC ${eccValue}e-6`;
            
            // Random fluctuations in DRAM (holds cached pages)
            const dramVal = Math.round(20 + Math.random() * 10);
            dramFillBar.style.width = `${dramVal}%`;
        }, 800);
    } 
    else if (mode === "write") {
        svg.classList.add("flow-active", "mode-write");
        diagIndicator.textContent = "DATA TRANSFER: WRITE CYCLE";
        diagIndicator.className = "pulse-indicator text-green animate-pulse";
        
        // Loop simulation metrics
        activeInterval = setInterval(() => {
            const speed = (5800 + Math.random() * 800).toFixed(0);
            const iops = (600000 + Math.round(Math.random() * 120000)).toLocaleString();
            metricSpeed.textContent = `${speed} MB/s`;
            metricIops.textContent = `${iops} IOPS`;
            metricEcc.textContent = "BER < 10⁻¹⁰";
            
            // Animate buffer memory filling up and flushing
            dramPercent += 12;
            if (dramPercent > 95) {
                // Flash flush trigger
                dramPercent = 20;
                // Temporarily flash controller text status
                const ctrlText = document.getElementById("controller-activity");
                if (ctrlText) {
                    ctrlText.textContent = "FLUSHING CACHE";
                    ctrlText.style.fill = "#fb923c";
                    setTimeout(() => {
                        ctrlText.textContent = "FTL ACTIVE";
                        ctrlText.style.fill = "#15e6a2";
                    }, 600);
                }
            }
            dramFillBar.style.width = `${dramPercent}%`;
        }, 600);
    } 
    else if (mode === "maintenance") {
        svg.classList.add("flow-active", "mode-maintenance");
        diagIndicator.textContent = "MAINTENANCE: GARBAGE COLLECTION";
        diagIndicator.className = "pulse-indicator text-green animate-pulse";
        
        activeInterval = setInterval(() => {
            const speed = "0 MB/s (Host)";
            const iops = (90000 + Math.round(Math.random() * 40000)).toLocaleString();
            const eccValue = (2.5 + Math.random() * 3.5).toFixed(1);
            
            metricSpeed.textContent = speed;
            metricIops.textContent = `${iops} IOPS`;
            metricEcc.textContent = `LDPC ${eccValue}e-6`;
            
            // Maintenance keeps DRAM busy updating lookup index tables
            const dramVal = Math.round(45 + Math.random() * 15);
            dramFillBar.style.width = `${dramVal}%`;
        }, 1000);
    }
}
