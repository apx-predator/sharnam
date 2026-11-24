Sharnam Network Automation Tool
A Model-Driven Network Automation Platform (YANG / NETCONF / FastAPI / PHP)

Sharnam is a full-stack network orchestration and provisioning demo designed to showcase modern network automation principles. Instead of relying on legacy CLI screen-scraping, it uses YANG data models over NETCONF to manage network devices programmatically, ensuring transactional integrity and structured configuration.

🚀 Core Features
Model-Driven Programmability: Utilizes Cisco IOS-XE YANG models to push configurations (VLANs, Interfaces, interfaces features, Port-Channels, etc.) via NETCONF.

Two-Phase Commit (Confirmed-Commit): Implements a safety-net mechanism using <commit><confirmed/>. If a configuration change causes a lockout or failure, it automatically rolls back unless explicitly confirmed, ensuring zero network downtime.

Drift Detection & Validation: Compares intended state (from the database) against operational state (pulled via NETCONF) to identify configuration drift.

Full-Stack Architecture: A custom web dashboard built on XAMPP (PHP/HTML/JS) communicates with a highly concurrent Python FastAPI backend via REST APIs.

🏗️ Architecture
Frontend (UI): HTML/CSS/JS dashboard to select devices and push configurations.

Middleware (PHP): Acts as the web controller, translating UI actions into REST API calls.

Backend API (FastAPI): Receives requests, queries the MySQL inventory, and orchestrates network changes.

Network Engine (Nornir & Scrapli): Uses Python threading to concurrently connect to multiple devices via NETCONF (Port 830) and push YANG-formatted XML payloads.

Database (MySQL): Stores device inventory, site details, interface records, and configuration histories.

🛠️ Technologies Used
Network Automation: Nornir, Scrapli, NETCONF, YANG (Cisco-IOS-XE models).

Backend: Python 3, FastAPI, Uvicorn, Pydantic.

Frontend/Web: PHP, HTML5, CSS3, JavaScript (AJAX/Fetch).

Database: MySQL (via XAMPP).

Security: Confirmed-commit rollback safety, strict capability checking.

💡 Why YANG & NETCONF?
Traditional CLI automation (using Netmiko/Paramiko) is prone to errors when device prompts change or when output formats vary between IOS versions. By using YANG, the tool sends structured XML data that the device natively understands. This guarantees that configurations are idempotent, transactional, and can be programmatically validated before they are committed to the running datastore.

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
