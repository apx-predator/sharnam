# Sharnam Network Automation Tool

A full-stack networking automation demo built to provision and manage network devices. 

## Architecture
- **Frontend:** HTML/CSS/JS
- **Middleware / Web Server:** PHP (XAMPP)
- **Backend API:** Python (FastAPI)
- **Database:** MySQL
- **Networking:** Python (Nornir / Scrapli / Netmiko via NETCONF/SSH)

## How it works
1. The user interacts with the HTML frontend.
2. PHP scripts handle web requests and communicate with the Python FastAPI backend.
3. FastAPI orchestrates network configurations (VLANs, Interfaces, BGP) and pushes them to devices.
4. Configuration states and device inventory are stored in MySQL.

## Local Setup Instructions
Since this project was built on XAMPP, follow these steps to run it locally:

1. **Clone the repo into your XAMPP htdocs:**
   `git clone https://github.com/joseph9999-tech/sharnam.git`
2. **Database:**
   - Open phpMyAdmin.
   - Create a database named `sharnam_db`.
   - Import the `database.sql` file (included in this repo).
3. **Python Backend:**
   - Navigate to the API folder.
   - Create a virtual environment: `python -m venv venv`
   - Activate it and install dependencies: `pip install -r requirements.txt`
   - Start the server: `uvicorn main:app --reload`
4. **Frontend:**
   - Ensure Apache and MySQL are running in XAMPP.
   - Visit `http://localhost/sharnam/index.php`