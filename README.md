BloodBridge — A Blood Donation Platform

BloodBridge is a web-based platform built to connect blood donors, recipients, and hospitals efficiently. It aims to streamline the donation process, manage requests, and reduce the gap between supply and demand of blood.

Features
- User roles: Donor, Recipient, Hospital, Admin
- Donor registration with blood type, contact, location
- Request creation by recipients/hospitals for specific blood types
- Matching and notification system to pair donors with requests
- Status tracking of donation requests (pending, accepted, fulfilled)
- Basic dashboard for monitoring available requests and donors

Installation & Setup

1. Clone the repository:
git clone https://github.com/Sana874/BloodBridge---A-Blood-Donation-Platform.git
cd BloodBridge---A-Blood-Donation-Platform

2. Create a virtual environment and install dependencies:

python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt


3. Configure database (e.g. SQLite, MySQL) and set connection in config file.

4. Run migrations or set up schema.

5. Start the server (Flask / Django / whatever stack used):
python app/main.py             # or the entrypoint for your web app

Usage
- Register as Donor / Recipient / Hospital
- Create and manage donation requests
- Match donors to requests automatically or manually
- Track status of donation requests
- Dashboard to view donors, requests, and system statistics

Future Enhancements
- Add geolocation / mapping features for donor proximity
- Notify donor via SMS / email alerts

Add blood inventory management & blood bank integration

Real-time analytics of demand vs supply
