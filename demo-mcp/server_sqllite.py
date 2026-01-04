"""
MCP SQLite Server - A simple MCP server for querying employee data from SQLite
"""

from fastmcp import FastMCP
import sqlite3
import json
import os
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware


mcp = FastMCP("SQLite Employee Database")

async def add_cors_headers(request, call_next):
    if request.method == "OPTIONS":
        from fastapi.responses import Response
        return Response(
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Credentials": "true",
            }
        )

    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

mcp.add_middleware(add_cors_headers)


DB_PATH = Path(__file__).parent / "employees.db"


def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  
    return conn


@mcp.tool()
def list_employees(limit: int = 10, offset: int = 0) -> str:
    """List all employees with pagination"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, first_name, last_name, email, department, position, salary, hire_date
            FROM employees
            ORDER BY id
            LIMIT ? OFFSET ?
        """, (limit, offset))

        employees = [dict(row) for row in cur.fetchall()]
        cur.close()
        conn.close()

        if not employees:
            return "No employees found."

        return json.dumps(employees, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def get_employee_by_id(employee_id: int) -> str:
    """Get detailed information about a specific employee by ID"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, first_name, last_name, email, department, position,
                   salary, hire_date, manager_id, phone
            FROM employees
            WHERE id = ?
        """, (employee_id,))

        employee = cur.fetchone()
        cur.close()
        conn.close()

        if not employee:
            return f"Employee with ID {employee_id} not found."

        return json.dumps(dict(employee), indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def search_employees_by_name(name: str) -> str:
    """Search for employees by first name or last name"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        search_pattern = f"%{name}%"
        cur.execute("""
            SELECT id, first_name, last_name, email, department, position
            FROM employees
            WHERE first_name LIKE ? OR last_name LIKE ?
            ORDER BY last_name, first_name
        """, (search_pattern, search_pattern))

        employees = [dict(row) for row in cur.fetchall()]
        cur.close()
        conn.close()

        if not employees:
            return f"No employees found matching '{name}'."

        return json.dumps(employees, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def get_employees_by_department(department: str) -> str:
    """Get all employees in a specific department"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, first_name, last_name, email, position, salary, hire_date
            FROM employees
            WHERE department LIKE ?
            ORDER BY last_name, first_name
        """, (department,))

        employees = [dict(row) for row in cur.fetchall()]
        cur.close()
        conn.close()

        if not employees:
            return f"No employees found in department '{department}'."

        return json.dumps(employees, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def get_department_statistics() -> str:
    """Get statistics about employees grouped by department"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                department,
                COUNT(*) as employee_count,
                AVG(salary) as average_salary,
                MIN(salary) as min_salary,
                MAX(salary) as max_salary
            FROM employees
            GROUP BY department
            ORDER BY employee_count DESC
        """)

        stats = [dict(row) for row in cur.fetchall()]
        cur.close()
        conn.close()

        if not stats:
            return "No department statistics available."

        return json.dumps(stats, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def get_salary_range(min_salary: float, max_salary: float) -> str:
    """Get employees within a specific salary range"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, first_name, last_name, department, position, salary
            FROM employees
            WHERE salary BETWEEN ? AND ?
            ORDER BY salary DESC
        """, (min_salary, max_salary))

        employees = [dict(row) for row in cur.fetchall()]
        cur.close()
        conn.close()

        if not employees:
            return f"No employees found with salary between ${min_salary} and ${max_salary}."

        return json.dumps(employees, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def get_recent_hires(days: int = 90) -> str:
    """Get employees hired in the last N days"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, first_name, last_name, email, department, position, hire_date
            FROM employees
            WHERE hire_date >= date('now', '-' || ? || ' days')
            ORDER BY hire_date DESC
        """, (days,))

        employees = [dict(row) for row in cur.fetchall()]
        cur.close()
        conn.close()

        if not employees:
            return f"No employees hired in the last {days} days."

        return json.dumps(employees, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def get_employees_by_manager(manager_id: int) -> str:
    """Get all employees reporting to a specific manager"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, first_name, last_name, email, department, position
            FROM employees
            WHERE manager_id = ?
            ORDER BY last_name, first_name
        """, (manager_id,))

        employees = [dict(row) for row in cur.fetchall()]
        cur.close()
        conn.close()

        if not employees:
            return f"No employees found reporting to manager ID {manager_id}."

        return json.dumps(employees, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def execute_custom_query(query: str) -> str:
    """Execute a custom SQL query (SELECT only for safety)"""
    try:
        # Basic safety check - only allow SELECT queries
        if not query.strip().upper().startswith("SELECT"):
            return "Error: Only SELECT queries are allowed for safety reasons."

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(query)
        results = [dict(row) for row in cur.fetchall()]

        cur.close()
        conn.close()

        if not results:
            return "Query executed successfully but returned no results."

        return json.dumps(results, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def get_position_count() -> str:
    """Get count of employees by position"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT position, COUNT(*) as count
            FROM employees
            GROUP BY position
            ORDER BY count DESC
        """)

        positions = [dict(row) for row in cur.fetchall()]
        cur.close()
        conn.close()

        if not positions:
            return "No position data available."

        return json.dumps(positions, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="sse", port=9000)
