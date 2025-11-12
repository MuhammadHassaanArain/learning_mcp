import asyncio
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def progress_handler(progress: float, total: float | None, message: str | None):
    if total:
        percentage = (progress / total) * 100
        progress_bar = "█" * int(percentage // 5) + "░" * (20 - int(percentage // 5))
        print(f"    📊 [{progress_bar}] {percentage:.1f}% - {message or 'Working...'}")
    else:
        print(f"    📊 Progress: {progress} - {message or 'Working...'}")

async def main():
    async with streamablehttp_client("http://localhost:8000/mcp") as (read_stream, write_stream, session_id):
        async with ClientSession(read_stream, write_stream) as session:
            print("✅ Connected to MCP server!")
            init_result = await session.initialize()
            print(f"🔧 Server capabilities: {init_result.capabilities}")

            tools_result = await session.list_tools()
            print(f"🛠️ Available tools: {[tool.name for tool in tools_result.tools]}")
            scenarios = [
                {
                    "name": "📁 File Download",
                    "tool": "download_file",
                    "args": {"filename": "dataset.zip", "size_mb": 2}
                },
                {
                    "name": "🔄 Data Processing", 
                    "tool": "process_data",
                    "args": {"records": 20}
                }
            ]
            for scenario in scenarios:
                print(f"\n{scenario['name']}")
                print("-" * 40)
                try:
                    result = await session.call_tool(scenario['tool'],scenario['args'], progress_callback=progress_handler)
                    if result.content:
                        for content in result.content:
                            print(f"✅ Result: {content}")
                    else:
                        print("No Output")

                except Exception as e:
                    print(f"❌ Error calling tool: {e}")
            



asyncio.run(main())




