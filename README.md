# CVE Project

This project consumes CVE (Common Vulnerabilities and Exposures) information from the NVD (National Vulnerability Database) API, stores the data in a PostgreSQL database, cleanses and transforms the data, and provides an interface to visualize and filter the CVE data. The project also includes a backend API built with Flask and a frontend built using HTML, CSS, and JavaScript.

## Features

- **API Integration**: Fetch CVE data from the NVD API.
- **Data Cleansing**: Handle and clean the data, removing duplicates and inconsistencies.
- **Database Integration**: Store CVE data in a PostgreSQL database (`cve_data`).
- **Custom API Endpoints**: Expose APIs to filter and query CVE data by various parameters:
  - CVE ID
  - CVE year
  - CVE score (CVSS)
  - Last modified in the last N days
- **Frontend Visualization**: Display the CVE data in a table format with pagination and sorting functionality.
- **Data Synchronization**: Periodically update the CVE data in the database either through full or incremental data refreshes.

## Project Structure

    ```bash
    CVE/
    │
    ├── API/
    │   ├── index.html            # Frontend template
    │   ├── app.py                # Flask application file
    │   ├── db.py                 # Database connection & query handling
    │   ├── queries.py            # SQL queries to fetch data from the API
    │   └── routes.py             # API route definitions
    │
    ├── db/
    │   └── database.py           # Database creation & management
    │
    ├── ingestion/
    │   └── fetch_Data.py         # Fetches CVE data from the NVD API
    │
    ├── transformation/
    │   └── transform_Data.py     # Cleanses and transforms CVE data
    │
    ├── .env                      # PostgreSQL DB credentials (DB_NAME, DB_USER, etc.)
    ├── requirements.txt          # Required Python libraries
    └── README.md                 # Project documentation (this file)


## Installation

### Prerequisites

- Python 3.x
- PostgreSQL
- Required libraries (listed in `requirements.txt`)

### Steps

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Sneakyfox1051/CVE.git
   cd CVE

## Output

### 1. Displaying 10 Records Per Page
The UI initially loads and displays **10 CVE records** per page.

![10 Records View](CVE_1.png)

---

### 2. Displaying 50 Records Per Page
Users can change the **"Results Per Page"** option to **50** to view more data.

![50 Records View](CVE_2.png)

---

### 3. Navigating to the Next Page
Pagination allows users to navigate through the dataset and load the **next 10 records**.

![Next Page View](CVE_3.png)

---

### 4. Viewing Details of a Specific CVE ID
Clicking on a CVE ID redirects the user to a detailed view of that specific record.

![CVE Details View](CVE_4.png)

---


