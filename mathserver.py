from mcp.server import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b:int)->int:
    """add two numbers"""
    return a+b


@mcp.tool()
def multiply(a: int, b:int)->int:
    """multiply two numbers"""
    return a*b   
#runs and executes commands in command prompt helps in debugging

if __name__ == "__main__":
    mcp.run(transport="stdio")
