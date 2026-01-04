"""
Setup SQLite database with employee data
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "employees.db"

if DB_PATH.exists():
    DB_PATH.unlink()
    print(f"Removed existing database: {DB_PATH}")

conn = sqlite3.connect(str(DB_PATH))
cur = conn.cursor()

print(f"Creating database: {DB_PATH}")

cur.execute("""
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    department TEXT NOT NULL,
    position TEXT NOT NULL,
    salary REAL NOT NULL CHECK (salary >= 0),
    hire_date TEXT NOT NULL DEFAULT (date('now')),
    manager_id INTEGER,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (manager_id) REFERENCES employees(id) ON DELETE SET NULL
)
""")

print("✓ Created employees table")

# Insert CEO and top-level executives (no managers)
cur.executemany("""
INSERT INTO employees (first_name, last_name, email, phone, department, position, salary, hire_date, manager_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", [
    ('Sarah', 'Johnson', 'sarah.johnson@company.com', '555-0101', 'Executive', 'Chief Executive Officer', 250000.00, '2018-01-15', None),
    ('Michael', 'Chen', 'michael.chen@company.com', '555-0102', 'Technology', 'Chief Technology Officer', 220000.00, '2018-03-20', None),
    ('Jennifer', 'Martinez', 'jennifer.martinez@company.com', '555-0103', 'Finance', 'Chief Financial Officer', 215000.00, '2018-02-10', None),
    ('David', 'Williams', 'david.williams@company.com', '555-0104', 'Operations', 'Chief Operations Officer', 210000.00, '2018-04-05', None),
])

print("✓ Inserted executives")

# Insert Engineering Department
cur.executemany("""
INSERT INTO employees (first_name, last_name, email, phone, department, position, salary, hire_date, manager_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", [
    ('Emily', 'Brown', 'emily.brown@company.com', '555-0201', 'Engineering', 'VP of Engineering', 180000.00, '2019-01-10', 2),
    ('James', 'Davis', 'james.davis@company.com', '555-0202', 'Engineering', 'Engineering Manager', 150000.00, '2019-06-15', 5),
    ('Lisa', 'Garcia', 'lisa.garcia@company.com', '555-0203', 'Engineering', 'Engineering Manager', 148000.00, '2019-08-20', 5),
    ('Robert', 'Miller', 'robert.miller@company.com', '555-0301', 'Engineering', 'Senior Software Engineer', 135000.00, '2020-02-01', 6),
    ('Amanda', 'Wilson', 'amanda.wilson@company.com', '555-0302', 'Engineering', 'Senior Software Engineer', 132000.00, '2020-03-15', 6),
    ('Christopher', 'Moore', 'christopher.moore@company.com', '555-0303', 'Engineering', 'Software Engineer', 110000.00, '2021-01-20', 6),
    ('Jessica', 'Taylor', 'jessica.taylor@company.com', '555-0304', 'Engineering', 'Software Engineer', 108000.00, '2021-04-10', 7),
    ('Daniel', 'Anderson', 'daniel.anderson@company.com', '555-0305', 'Engineering', 'Software Engineer', 105000.00, '2021-06-01', 7),
    ('Michelle', 'Thomas', 'michelle.thomas@company.com', '555-0306', 'Engineering', 'Junior Software Engineer', 85000.00, '2022-09-15', 7),
    ('Kevin', 'Jackson', 'kevin.jackson@company.com', '555-0307', 'Engineering', 'Junior Software Engineer', 82000.00, '2023-01-10', 6),
])

print("✓ Inserted Engineering department")

# Insert Product Department
cur.executemany("""
INSERT INTO employees (first_name, last_name, email, phone, department, position, salary, hire_date, manager_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", [
    ('Rachel', 'White', 'rachel.white@company.com', '555-0401', 'Product', 'VP of Product', 175000.00, '2019-05-01', 2),
    ('Brian', 'Harris', 'brian.harris@company.com', '555-0402', 'Product', 'Senior Product Manager', 140000.00, '2020-07-15', 15),
    ('Nicole', 'Martin', 'nicole.martin@company.com', '555-0403', 'Product', 'Product Manager', 120000.00, '2021-02-20', 15),
    ('Steven', 'Thompson', 'steven.thompson@company.com', '555-0404', 'Product', 'Product Manager', 118000.00, '2021-08-10', 15),
    ('Laura', 'Garcia', 'laura.garcia@company.com', '555-0405', 'Product', 'Associate Product Manager', 95000.00, '2022-11-01', 16),
])

print("✓ Inserted Product department")

# Insert Marketing Department
cur.executemany("""
INSERT INTO employees (first_name, last_name, email, phone, department, position, salary, hire_date, manager_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", [
    ('Andrew', 'Martinez', 'andrew.martinez@company.com', '555-0501', 'Marketing', 'VP of Marketing', 165000.00, '2019-03-15', 1),
    ('Karen', 'Robinson', 'karen.robinson@company.com', '555-0502', 'Marketing', 'Marketing Manager', 125000.00, '2020-05-20', 20),
    ('Joseph', 'Clark', 'joseph.clark@company.com', '555-0503', 'Marketing', 'Content Marketing Manager', 115000.00, '2020-09-10', 20),
    ('Patricia', 'Rodriguez', 'patricia.rodriguez@company.com', '555-0504', 'Marketing', 'Social Media Manager', 95000.00, '2021-11-15', 21),
    ('Timothy', 'Lewis', 'timothy.lewis@company.com', '555-0505', 'Marketing', 'Marketing Coordinator', 72000.00, '2022-06-01', 21),
    ('Sandra', 'Lee', 'sandra.lee@company.com', '555-0506', 'Marketing', 'Marketing Coordinator', 70000.00, '2023-02-15', 22),
])

print("✓ Inserted Marketing department")

# Insert Sales Department
cur.executemany("""
INSERT INTO employees (first_name, last_name, email, phone, department, position, salary, hire_date, manager_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", [
    ('Charles', 'Walker', 'charles.walker@company.com', '555-0601', 'Sales', 'VP of Sales', 170000.00, '2019-02-01', 1),
    ('Elizabeth', 'Hall', 'elizabeth.hall@company.com', '555-0602', 'Sales', 'Sales Manager', 130000.00, '2020-04-15', 26),
    ('Paul', 'Allen', 'paul.allen@company.com', '555-0603', 'Sales', 'Senior Sales Representative', 110000.00, '2020-10-20', 27),
    ('Susan', 'Young', 'susan.young@company.com', '555-0604', 'Sales', 'Sales Representative', 95000.00, '2021-05-10', 27),
    ('Gregory', 'Hernandez', 'gregory.hernandez@company.com', '555-0605', 'Sales', 'Sales Representative', 92000.00, '2021-09-01', 27),
    ('Deborah', 'King', 'deborah.king@company.com', '555-0606', 'Sales', 'Sales Representative', 90000.00, '2022-03-15', 27),
])

print("✓ Inserted Sales department")

# Insert Finance Department
cur.executemany("""
INSERT INTO employees (first_name, last_name, email, phone, department, position, salary, hire_date, manager_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", [
    ('Thomas', 'Wright', 'thomas.wright@company.com', '555-0701', 'Finance', 'Finance Manager', 145000.00, '2019-07-10', 3),
    ('Nancy', 'Lopez', 'nancy.lopez@company.com', '555-0702', 'Finance', 'Senior Accountant', 105000.00, '2020-08-15', 32),
    ('Joshua', 'Hill', 'joshua.hill@company.com', '555-0703', 'Finance', 'Accountant', 85000.00, '2021-10-20', 32),
    ('Donna', 'Scott', 'donna.scott@company.com', '555-0704', 'Finance', 'Accountant', 83000.00, '2022-01-15', 32),
    ('Ryan', 'Green', 'ryan.green@company.com', '555-0705', 'Finance', 'Financial Analyst', 88000.00, '2022-07-01', 32),
])

print("✓ Inserted Finance department")

# Insert HR Department
cur.executemany("""
INSERT INTO employees (first_name, last_name, email, phone, department, position, salary, hire_date, manager_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", [
    ('Angela', 'Adams', 'angela.adams@company.com', '555-0801', 'Human Resources', 'VP of HR', 160000.00, '2019-04-01', 1),
    ('Jason', 'Baker', 'jason.baker@company.com', '555-0802', 'Human Resources', 'HR Manager', 115000.00, '2020-06-15', 37),
    ('Betty', 'Gonzalez', 'betty.gonzalez@company.com', '555-0803', 'Human Resources', 'HR Specialist', 78000.00, '2021-03-20', 38),
    ('Edward', 'Nelson', 'edward.nelson@company.com', '555-0804', 'Human Resources', 'Recruiter', 75000.00, '2021-12-01', 38),
    ('Dorothy', 'Carter', 'dorothy.carter@company.com', '555-0805', 'Human Resources', 'HR Coordinator', 65000.00, '2022-08-15', 38),
])

print("✓ Inserted Human Resources department")

# Insert Operations Department
cur.executemany("""
INSERT INTO employees (first_name, last_name, email, phone, department, position, salary, hire_date, manager_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", [
    ('Kenneth', 'Mitchell', 'kenneth.mitchell@company.com', '555-0901', 'Operations', 'Operations Manager', 135000.00, '2019-09-01', 4),
    ('Helen', 'Perez', 'helen.perez@company.com', '555-0902', 'Operations', 'Operations Coordinator', 82000.00, '2020-11-10', 42),
    ('Gary', 'Roberts', 'gary.roberts@company.com', '555-0903', 'Operations', 'Operations Coordinator', 80000.00, '2021-07-15', 42),
    ('Carolyn', 'Turner', 'carolyn.turner@company.com', '555-0904', 'Operations', 'Operations Specialist', 75000.00, '2022-04-20', 42),
])

print("✓ Inserted Operations department")

# Insert IT Support Department
cur.executemany("""
INSERT INTO employees (first_name, last_name, email, phone, department, position, salary, hire_date, manager_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", [
    ('Frank', 'Phillips', 'frank.phillips@company.com', '555-1001', 'IT', 'IT Manager', 125000.00, '2020-01-15', 2),
    ('Sharon', 'Campbell', 'sharon.campbell@company.com', '555-1002', 'IT', 'Senior IT Support Specialist', 95000.00, '2020-12-01', 46),
    ('Larry', 'Parker', 'larry.parker@company.com', '555-1003', 'IT', 'IT Support Specialist', 72000.00, '2021-08-15', 46),
    ('Cynthia', 'Evans', 'cynthia.evans@company.com', '555-1004', 'IT', 'IT Support Specialist', 70000.00, '2022-05-10', 46),
    ('Dennis', 'Edwards', 'dennis.edwards@company.com', '555-1005', 'IT', 'Help Desk Technician', 58000.00, '2023-03-01', 47),
])

print("✓ Inserted IT department")

# Commit changes
conn.commit()

# Verify data insertion
cur.execute("SELECT COUNT(*) FROM employees")
total = cur.fetchone()[0]
print(f"\n✓ Total employees inserted: {total}")

cur.execute("SELECT department, COUNT(*) as count FROM employees GROUP BY department ORDER BY count DESC")
print("\nEmployees by department:")
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]}")

cur.close()
conn.close()

print(f"\n✓ Database setup complete: {DB_PATH}")
