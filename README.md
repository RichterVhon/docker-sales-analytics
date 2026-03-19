# 📊 Sales Analytics Dashboard (Dockerized)

**Developer:** R.V. Dela Cruz  
**Tech Stack:** Python 3.11, Pandas, Seaborn, Docker, WSL2

## 🚀 Project Overview
This is a containerized data science pipeline that processes sales datasets to generate 5 key business insights. It uses Docker to ensure that dependencies (like `matplotlib` and `gcc`) are handled automatically, regardless of the host OS.

---

## 🛠️ Setup & Installation

### 1. Prerequisites
* **Docker Desktop** installed and running.
* **Hardware Virtualization** (SVM/VT-x) enabled in BIOS.

### 2. Clone the Repository
Open your terminal and run:
`git clone https://github.com/RichterVhon/docker-sales-analytics.git`
`cd docker-sales-analytics`

### 3. Build the Image
This command creates the isolated Linux environment.
`docker build -t sales-analytics .`

---

## 📈 How to Run & View Results

To run the analysis and see the generated graphs on your Windows machine, use the following command (optimized for Git Bash):

**Command:**
`MSYS_NO_PATHCONV=1 docker run --rm -v "/$(pwd)/output:/app/output" sales-analytics`

### 📂 Output Location
After the container finishes, check the following folder on your computer:
* **`/output/graphs_YYYYMMDD_HHMMSS/`**: Contains 5 high-resolution PNG charts.
* **`/logs/`**: Contains execution logs for debugging.

---

## 🧪 Included Visualizations
1. **Regional Revenue Battle**: Sales vs. Volume by territory.
2. **Category Profitability Matrix**: Heatmap of return rates and AOV.
3. **Channel Efficiency**: Comparison of Retail vs. Online performance.
4. **Customer Lifetime Value**: VIP vs. Regular segment analysis.
5. **Payment Method Strategy**: Market share and risk assessment.

---

## 🔧 Troubleshooting
* **Virtualization Error:** Ensure "SVM Mode" is Enabled in your BIOS (Advanced > CPU Configuration).
* **Path Errors (Windows):** If using Git Bash, ensure you use the `MSYS_NO_PATHCONV=1` prefix.