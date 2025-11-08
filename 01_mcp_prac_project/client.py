import asyncio
from typing import Optional
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from contextlib import AsyncExitStack

class MCPClient:
    def __init__(self,server_url):
        self._server_url:str = server_url
        self._session :Optional[ClientSession] = None
        self._exit_stack:AsyncExitStack = AsyncExitStack()

    async def connection(self):
        _read,_write, _ = await self._exit_stack.enter_async_context(
            streamablehttp_client(self._server_url)
        )
        self._session = await self._exit_stack.enter_async_context(
            ClientSession(_read,_write)
        )
        await self._session.initialize()
        return self._session

    async def cleanup(self):
        await self._exit_stack.aclose()

    async def __aenter__(self):
        await self.connection()
        return self

    async def __aexit__(self, *args):
        await self.cleanup()


    # TOOLS/RESOURCS/PROMPTS

    async def tool_list(self):
        assert self._session, "Session Not Found"
        result = await self._session.list_tools()
        return result.tools
    async def tool_call(self,name:str):
        assert self._session, "Session Not Found"
        result = await self._session.call_tool(name=name)
        return result.content[0].text
    
    async def resource_list(self):
        assert self._session, "Session Not Found"
        result = await self._session.list_resources()
        return result.resources
    async def read_resource(self,uri):
        assert self._session, "Session Not Found"
        result = await self._session.read_resource(uri=uri)
        return result.contents[0].text
    
    async def prompt_list(self):
        assert self._session, "Session Not Found"
        result = await self._session.list_prompts()
        return result.prompts
    async def get_prompt(self,prompt_name:str):
        assert self._session, "Session Not Found"
        result = await self._session.get_prompt(prompt_name)
        return result.messages[0].content.text

async def main():
    async with MCPClient("http://localhost:8000/mcp") as client:
        tool_list =await client.tool_list()
        print("\n TOOL LIST : \t",tool_list)
        tool_call = await client.tool_call("Testing-Tool")
        print("TOOL CALL : \t",tool_call,"\n")

        resource_list = await client.resource_list()
        print(" RESOURCE LIST :\t",resource_list)
        read_resource = await client.read_resource(resource_list[0].uri)
        print("READ RESOURCE :\t",read_resource,"\n")

        prompt_list = await client.prompt_list()
        print(" PROMPT LIST : \t",prompt_list)
        get_prompt = await client.get_prompt(prompt_list[0].name)
        print(" GET PROMPT : \t", get_prompt,"\n")


asyncio.run(main())