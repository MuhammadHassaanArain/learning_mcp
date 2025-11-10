from mcp.server.fastmcp import FastMCP, Context
from mcp.types import SamplingMessage, TextContent
mcp = FastMCP(name="mcp-Smapling", stateless_http=False)

@mcp.tool()
async def create_story(ctx:Context, topic:str)-> str:

    result = await ctx.session.create_message(
        messages=[
            SamplingMessage(
                role="user",
                content=TextContent(type="text", text=f"Write a very short, three-sentence story about: {topic}")
            )
        ],
        max_tokens=100,
    )
    if result.content.type == "text":
        return result.content.text
    return str(result.content)

mcp_app = mcp.streamable_http_app()