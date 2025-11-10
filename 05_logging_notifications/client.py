# Client.py:

from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
import asyncio
from mcp.types import LoggingMessageNotificationParams


async def log_handler(params:LoggingMessageNotificationParams):
    
    emoji_map = {
        "debug": "🔍",
        "info": "📰",
        "warning": "⚠️",
        "error": "❌",
    }
    emoji = emoji_map.get(params.level.lower(), "📝")
    logger_info = f" [{params.logger}]" if params.logger else ""
    print(f"    {emoji} [{params.level.upper()}]{logger_info} {params.data}")


async def main():

    try:
        async with streamablehttp_client("http://localhost:8000/mcp") as (read_stream, write_stream, session_id):
            async with ClientSession(read_stream,write_stream,logging_callback=log_handler) as session:
                await session.initialize()
                print("\nSCENARIO 1: Successful processing")
                result = await session.call_tool("Process_item", {"item": "item-123", "should_fail": False})
                if result.content:
                    print(f"✅ Result: {result.content[0].text}")

                await asyncio.sleep(1)

                print("\nSCENARIO 2: Processing with failure")
                
                result = await session.call_tool("Process_item", {"item": "item-456", "should_fail": True})
                if result.content:
                    print(f"✅ Result: {result.content[0].text}")

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("💡 Make sure the server is running.")

asyncio.run(main())