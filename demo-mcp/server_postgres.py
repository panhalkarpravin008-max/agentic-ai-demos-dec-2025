from fastmcp import FastMCP
import psycopg2
from psycopg2.extras import RealDictCursor
import json
import os
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("PostgreSQL Employee Database")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "10.0.10.199"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "ChangeMe123!"),
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


@mcp.tool()
def list_employees(limit: int = 10, offset: int = 0) -> str:
    """List all employees with pagination"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
            SELECT id, first_name, last_name, email, department, position, salary, hire_date
            FROM employees
            ORDER BY id
            LIMIT %s OFFSET %s
        """, (limit, offset))

        employees = cur.fetchall()
        cur.close()
        conn.close()

        if not employees:
            return "No employees found."

        return json.dumps(employees, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"
    
if __name__ == "__main__":
    mcp.run()