"""
MCP Math Server - A simple MCP server for solving math queries
"""

from fastmcp import FastMCP
import math

mcp = FastMCP("Math Calculator")


@mcp.tool()
def add(a: float, b: float) -> str:
    """Add two numbers together"""
    result = a + b
    return f"{a} + {b} = {result}"


@mcp.tool()
def subtract(a: float, b: float) -> str:
    """Subtract second number from first number"""
    result = a - b
    return f"{a} - {b} = {result}"


@mcp.tool()
def multiply(a: float, b: float) -> str:
    """Multiply two numbers"""
    result = a * b
    return f"{a} × {b} = {result}"


@mcp.tool()
def divide(a: float, b: float) -> str:
    """Divide first number by second number"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    result = a / b
    return f"{a} ÷ {b} = {result}"


@mcp.tool()
def power(base: float, exponent: float) -> str:
    """Raise a number to a power"""
    result = base ** exponent
    return f"{base}^{exponent} = {result}"


@mcp.tool()
def sqrt(number: float) -> str:
    """Calculate square root of a number"""
    if number < 0:
        raise ValueError("Cannot calculate square root of negative number")
    result = math.sqrt(number)
    return f"√{number} = {result}"


@mcp.tool()
def factorial(n: int) -> str:
    """Calculate factorial of a non-negative integer"""
    if n < 0:
        raise ValueError("Factorial is only defined for non-negative integers")
    result = math.factorial(n)
    return f"{n}! = {result}"


@mcp.tool()
def percentage(value: float, percent: float) -> str:
    """Calculate percentage of a number"""
    result = (value * percent) / 100
    return f"{percent}% of {value} = {result}"


@mcp.tool()
def average(numbers: list[float]) -> str:
    """Calculate average of a list of numbers"""
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    avg = sum(numbers) / len(numbers)
    return f"Average of {numbers} = {avg}"


@mcp.tool()
def modulo(a: float, b: float) -> str:
    """Calculate remainder of division (a mod b)"""
    if b == 0:
        raise ValueError("Cannot calculate modulo with divisor of zero")
    result = a % b
    return f"{a} mod {b} = {result}"


@mcp.tool()
def absolute(number: float) -> str:
    """Calculate absolute value of a number"""
    result = abs(number)
    return f"|{number}| = {result}"


@mcp.tool()
def round_number(number: float, decimals: int = 0) -> str:
    """Round a number to specified decimal places"""
    result = round(number, decimals)
    return f"{number} rounded to {decimals} decimals = {result}"


@mcp.tool()
def gcd(a: int, b: int) -> str:
    """Calculate greatest common divisor of two integers"""
    result = math.gcd(a, b)
    return f"GCD of {a} and {b} = {result}"


@mcp.tool()
def lcm(a: int, b: int) -> str:
    """Calculate least common multiple of two integers"""
    result = abs(a * b) // math.gcd(a, b) if a and b else 0
    return f"LCM of {a} and {b} = {result}"


@mcp.tool()
def sine(angle: float, use_degrees: bool = False) -> str:
    """Calculate sine of an angle (in radians by default, or degrees if use_degrees=True)"""
    if use_degrees:
        angle_rad = math.radians(angle)
        result = math.sin(angle_rad)
        return f"sin({angle}°) = {result}"
    else:
        result = math.sin(angle)
        return f"sin({angle}) = {result}"


@mcp.tool()
def cosine(angle: float, use_degrees: bool = False) -> str:
    """Calculate cosine of an angle (in radians by default, or degrees if use_degrees=True)"""
    if use_degrees:
        angle_rad = math.radians(angle)
        result = math.cos(angle_rad)
        return f"cos({angle}°) = {result}"
    else:
        result = math.cos(angle)
        return f"cos({angle}) = {result}"


@mcp.tool()
def tangent(angle: float, use_degrees: bool = False) -> str:
    """Calculate tangent of an angle (in radians by default, or degrees if use_degrees=True)"""
    if use_degrees:
        angle_rad = math.radians(angle)
        result = math.tan(angle_rad)
        return f"tan({angle}°) = {result}"
    else:
        result = math.tan(angle)
        return f"tan({angle}) = {result}"


@mcp.tool()
def logarithm(number: float, base: float = math.e) -> str:
    """Calculate logarithm of a number with specified base (default is natural log)"""
    if number <= 0:
        raise ValueError("Logarithm only defined for positive numbers")
    if base <= 0 or base == 1:
        raise ValueError("Base must be positive and not equal to 1")

    if base == math.e:
        result = math.log(number)
        return f"ln({number}) = {result}"
    elif base == 10:
        result = math.log10(number)
        return f"log₁₀({number}) = {result}"
    else:
        result = math.log(number, base)
        return f"log_{base}({number}) = {result}"


if __name__ == "__main__":
    mcp.run()
