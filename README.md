# Vendor Management System
This project is a Vendor Management System developed using Django REST Framework.

# Setup Instructions
Follow these steps to set up the project locally:
Clone the repository to your local machine:
git clone <repository_url>
vendor-management-system-django 
This system will handle vendor profiles, track purchase orders, and calculate vendor performance metrics

# Prerequisites
Python (version 3.10.8)
Django (version 4.2.7)
Installation

# 1. Clone the repository:
command prompt:
git clone https://github.com/ManjulaJatavath/Vendor-Management-system.git
cd project-directory vendor_management_system-

# 2.Create a virtual environment:
python -m venv venv
source venv/bin/activate # For Linux/Mac
venv\Scripts\activate # For Windows

# 3.Install dependencies:
pip install -r requirements.txt

# 4.Database setup:
python manage.py makemigrations
python manage.py migrate

# Usage:

# 1.Start the server:
python manage.py runserver

# 2.Access API endpoints:

Rigister API: api/register/

Vendor API: api/vendors/

Purchase Order API:  api/purchase-orders/

Vendors Performance API: api/vendors_performance

# 3.After creating user to access token:
I used Postman to test API

'api-token-auth/ ' # provide username and password in json eg. { "username":"superuser","password":"password" }

once Token is created or received, provide it to HEADER 

with key as Authorization (eg. key : Authorization) and value as Token <token_id>

# 4.API Endpoints:
Vendor API
● POST /api/vendors/: Create a new vendor.

● GET /api/vendors/: List all vendors.

● GET /api/vendors/{vendor_id}/: Retrieve a specific vendor's details.

● PUT /api/vendors/{vendor_id}/: Update a vendor's details.

● DELETE /api/vendors/{vendor_id}/: Delete a vendor

● Vendor Performance Endpoint (GET /api/vendors/performance/{vendor_id})

# 5.Purchase Order API:
● POST /api/purchase_orders/: Create a purchase order.

● GET /api/purchase_orders/: List all purchase orders with an option to filter by vendor.

● GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.

● PUT /api/purchase_orders/{po_id}/: Update a purchase order.

● DELETE /api/purchase_orders/{po_id}/: Delete a purchase order

# 6.Vendor Performance API:
● GET /api/vendors_performance/{vendor_id}/: Retrieve a vendor's performance metric

# 7.Historical Performance API:
GET /vendor/historical_performance: List historical performance for all vendors.

GET /vendor/historical_performance/{id}/: Retrieve historical performance for a specific vendor.

# 8.Update Acknowledgment Endpoint:
● While not explicitly detailed in the previous sections, consider an endpoint like
POST /api/acknowledge_purchase_oder/ for vendors to acknowledge POs.

● This endpoint will update acknowledgment_date and trigger the recalculation of average_response_time

# 9.Running Tests:
Run the test suite:
python manage.py test
