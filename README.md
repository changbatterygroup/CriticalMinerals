Here's a clean, professional `README.md` file for your Critical Minerals Project:

---

# ⚒️ Critical Minerals Demand & Supply Simulation

This project simulates the **total demand and supply of critical minerals** over time based on cathode chemistries used in battery manufacturing. It includes a dashboard for visualizing trends and a series of Jupyter notebooks for analytical exploration.

## 📌 Objective

The goal is to model mineral demand associated with different **cathode chemistries**—such as **NMC811**, **LFP**, and **NMC532**—from **2010 to 2025**, using estimated production capacity data.

The simulation uses key input parameters including:

* **Cathode capacity** (in GWh)
* **Porosity**
* **Thickness**
* **Particle radius**

From these, a Pybamm model computes the **average cell voltage**, which is then used to estimate the **mass of materials required**—effectively modeling critical mineral demand for each cathode type over time.

---

## 📊 Dashboard

The interactive dashboard is built using **Dash** and is located in the `src/` directory. It is hosted on **Render** and provides:

* Time-series demand visualization
* Mineral breakdown across cathode types
* Comparative trends between demand and known supply

> 🔗 https://changlab-critical-minerals.onrender.com/

---

## 📁 Project Structure

```
├── src/                 # Dash app source code
├──     requirements.txt        # Python dependencies
├──     ...      
├── README.md            # Project description and setup
└── ...                  # Additional analysis files
```

---

## 🗂️ Data Sources (On Onedrive)

* **Capacity.xlsx**: Includes estimated GWh capacities per year (2010–2025), broken down by cathode type.
* **SPGlobal_MetalsAndMiningProperties-Combined-Dec-2024.xlsx**: Extracted from **S\&P Global** (2010–2025), detailing the supply potential of key critical minerals.


The dashboard uses parquet copies for privacy and serializability. Any changes to the data
means these would also need to be recreated. These files are found in `./src/assets`

---

## 🛠️ Setup Instructions

### Requirements

* Python
* Jupyter Notebook
* Dash


First clone this repository.



### Install Dependencies

Make sure you are in the `src` directory. Then run

```bash
pip install -r requirements.txt
```

### Running the Dashboard

To test the app locally using development mode, run

```bash
cd src
python app.py
```

### Simulate on a local production server

You can also simulate the production environment to test if everything is working before deployment. To do so,
run the command

```bash
gunicorn app:server
```


---

## 📓 Notebooks

Located in the `notebooks/` directory, these provide detailed:

* Simulation logic and assumptions
* Sensitivity analysis of parameters
* Mineral mass estimations across chemistries


----
## 🤝 Contributing
Contributions, issue reports, or suggestions are welcome. 
After cloning the repository, any changes committed within the
`src` folder will automatically trigger a re-deploy on the server.
---

## 📄 License

MIT License. See [LICENSE](LICENSE) for more information.

---


