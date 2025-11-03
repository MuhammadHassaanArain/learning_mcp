from mcp.server.fastmcp import FastMCP
from docs import doc

mcp = FastMCP("Prompt-Learning-Server", stateless_http=True)

@mcp.tool(name="Testing-Tool")
async def testing_tool():
    return "This Tool is for Testing Purpose!"

@mcp.resource(uri="docs://documents")
async def testing_resource():
    return list(doc.keys())

@mcp.prompt(name="Testing-Prompt")
async def testing_prompt():
    return "This Prompt is for Testing Purpose!"

mcp_app = mcp.streamable_http_app()