# Vehicle API Service

## Description
This is a simple web service for managing vehicle data. It provides CRUD-style API access to a database of vehicles. Each vehicle is uniquely identified by its VIN (Vehicle Identification Number) and includes attributes such as manufacturer, model year, description, and more.

The service is implemented in Django using Django REST Framework (DRF) and supports the following operations:
- Listing all vehicles (GET)
- Creating a new vehicle (POST)
- Retrieving a specific vehicle by VIN (GET)
- Updating an existing vehicle (PUT)
- Deleting a vehicle (DELETE)

## Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- SQLite (default) or PostgreSQL (optional)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kimberlyyliuu/apollo-superday.git
   cd apollo_project
   cd vehicle_app 
    ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
    ```
4. Database Setup
```
python manage.py makemigrations
python manage.py migrate
```

5. Run the development server 
```bash
python manage.py runserver
```
If "Error: That port is already in use"
Run:
```
sudo lsof -t -i tcp:8000 | xargs kill -9
```

Then run:
```
 python manage.py runserver
```

## Running Tests: 
Run unit tests to ensure all functionality works as expected:
```
python manage.py test vehicle_app.tests
```
