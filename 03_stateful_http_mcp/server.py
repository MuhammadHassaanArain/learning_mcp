from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="Stateful_http_lifecycle", stateless_http=False)

# Some Tools
@mcp.tool(name="get_forecast")
async def get_forecast(city:str)->str:
    return f"The Weather in {city} will be cloudy today! ☁"

@mcp.tool(name="Server_status")
async def server_status()-> str:
    return """Server Status: Running 🏃‍♂️"""


mcp_app = mcp.streamable_http_app()