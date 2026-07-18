from mcp.server import FastMCP

mcp = FastMCP("weather")

@mcp.tool()
async def get_weather(location:str)->str:
    """get weather of the location"""
    return f"it is raining in {location}"


  
#runs in the form of api

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
