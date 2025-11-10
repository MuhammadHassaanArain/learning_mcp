# Server.py:
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.server import Context
from mcp import types
import asyncio


mcp = FastMCP(name="Logging_notifications", stateless_http=True)

@mcp.tool(name="Process_item",description="processes an item and generates logs at different levels.")
async def process_item(ctx:Context, item:str, should_fail:bool= False):
    await ctx.debug(f"Starting Processing for item {item}")
    await asyncio.sleep(0.2)
    await ctx.info("Configuration Loaded Successfully.")
    await asyncio.sleep(0.2)

    if should_fail:
        await ctx.warning(f"Item: '{item}' has a validation issue. Attemptinig to proceed...")
        await asyncio.sleep(0.2)
        await ctx.error(f"Failed to process item : '{item}'. critical failure.")
        return [types.TextContent(type="text", text=f"Failed to process {item}.")]


    await ctx.info(f"Item '{item}' processed successfully.")
    return [types.TextContent(type="text", text=f"Successfully processed {item}.")]



mcp_app = mcp.streamable_http_app()