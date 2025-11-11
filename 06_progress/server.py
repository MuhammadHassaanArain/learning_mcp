from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.server import Context
import asyncio
import logging
mcp = FastMCP(name="progress_in_mcp", stateless_http=True)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@mcp.tool()
async def download_file(filename:str,size_mb:int, ctx:Context)-> str:
    await ctx.info(f"Starting Download of {filename} ({size_mb} MB)")
    total_chunk = size_mb * 10
    for chunk in range(total_chunk + 1):
        progress = chunk
        percentage  = (chunk/total_chunk) * 100

        await ctx.report_progress(
            progress=progress,
            total=total_chunk,
            message=f"Downloading {filename}... {percentage:.1f}%"
        )
        await asyncio.sleep(0.1)
    await ctx.info(f"Download completed: {filename}")
    return f"Successfully downloaded {filename} ({size_mb}MB)"

@mcp.tool()
async def process_data(records:int, ctx:Context)-> str:
    await ctx.info(f"Starting to process {records} records")
    
    for i in range(records + 1):
        # Report progress with descriptive messages
        if i == 0:
            message = "Initializing data processor..."
        elif i < records // 4:
            message = "Loading and validating records..."
        elif i < records // 2:
            message = "Applying transformations..."
        elif i < records * 3 // 4:
            message = "Running calculations..."
        else:
            message = "Finalizing results..."
            
        await ctx.report_progress(
            progress=i,
            total=records,
            message=message
        )
        await asyncio.sleep(0.05)
    await ctx.info(f"Processing completed: {records} records")
    return f"Successfully processed {records} records"


mcp_app = mcp.streamable_http_app()