import os 
import asyncio
from mcp.client.streamable_http import streamablehttp_client
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_export_api_key
from typing import Any
from mcp import ClientSession
from mcp.types import CreateMessageRequestParams, CreateMessageResult, ErrorData, TextContent
from mcp.shared.context import RequestContext

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
set_tracing_export_api_key(OPENAI_API_KEY)
from dotenv import load_dotenv
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client
)

async def mock_sampler(context:RequestContext["ClientSession", Any], params:CreateMessageRequestParams)->CreateMessageResult|ErrorData:
    model_llm_response =(
        f"In a world of shimmering code, a brave little function set out to find the legendary Golden Bug. "
        f"It traversed treacherous loops and navigated complex conditionals. "
        f"Finally, it found not a bug, but a feature, more valuable than any treasure."
    )
    return CreateMessageResult(
        role="assistant",
        content=TextContent(text=model_llm_response, type="text"),
        model="openai/gpt-4o-mini",
    )
async def real_sampler(context: RequestContext["ClientSession", Any], params: CreateMessageRequestParams) -> CreateMessageResult | ErrorData:

   agent = Agent(
        name="Assistant",
        instructions="You are a helpful Assistant",
        model=model,
   )
   result = await Runner.run(agent, params.messages[0].content.text)
   response_text = result.final_output
   return CreateMessageResult(
        role="assistant",
        content=TextContent(text=response_text, type="text"),
        model=model.model
    )


async def main():
    async with streamablehttp_client("http://localhost:8000/mcp") as (read_stream, write_stream, session_id):
        async with ClientSession(read_stream=read_stream, write_stream=write_stream, sampling_callback=real_sampler) as session:
            await session.initialize()
            tool_result = await session.call_tool("create_story",arguments={"topic":"a function's adventure"})
            if tool_result:
                    print(f"'{tool_result.content[0].text}'")
            else:
                    print("No content received from server.")



asyncio.run(main())
