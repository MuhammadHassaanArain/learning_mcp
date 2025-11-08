import json
import asyncio
from typing import Optional
from mcp import ClientSession
from contextlib import AsyncExitStack
from mcp.client.streamable_http import streamablehttp_client
from mcp.types import( ListToolsResult, CallToolResult, ListResourcesResult, 
ListResourceTemplatesResult, ReadResourceResult, ListPromptsResult,  GetPromptResult)

class MCPClient:
    def __init__(self, server_url):
        self._server_url : str = server_url
        self._session: Optional[ClientSession] = None
        self._exit_stack:AsyncExitStack= AsyncExitStack()

    async def connection(self):
        _read, _write, _ = await self._exit_stack.enter_async_context(
            streamablehttp_client(self._server_url)
        )
        self._session = await self._exit_stack.enter_async_context(
            ClientSession(_read,_write)
        )
        await self._session.initialize()
        return self._session
    
    async def Cleanup(self):
        await self._exit_stack.aclose()

    async def __aenter__(self):
        await self.connection()
        return self
    
    async def __aexit__(self,*args):
        await self.Cleanup()
        self._session = None

    # Tools
    async def tool_list(self)-> ListToolsResult:
        assert self._session, "Session Not Found"
        res = await self._session.list_tools()
        return res.tools
    
    async def tool_call(self, tool_name:str, arguments:dict[str,any])->CallToolResult:
        assert self._session, "Session Not Found"
        res = await self._session.call_tool(name=tool_name, arguments=arguments)
        return res.content[0].text
    
    # Resources
    async def list_resource(self)-> ListResourcesResult:
        assert self._session, "Session Not Found"
        res = await self._session.list_resources()
        return res.resources
    async def list_template_res(self)-> ListResourceTemplatesResult:
        assert self._session, "Session Not Found"
        res = await self._session.list_resource_templates()
        return res.resourceTemplates
    async def get_resource(self, uri:str)-> ReadResourceResult:
        assert self._session, "Session Not Found"
        res = await self._session.read_resource(uri)
        return res
    # Prompts
    async def list_prompt(self)-> ListPromptsResult:
        assert self._session, "Session Not Found"
        res = await self._session.list_prompts()
        return res
    async def get_prompt(self, prompt_name:str)-> GetPromptResult:
        assert self._session, "Session Not Found"
        res = await self._session.get_prompt(name=prompt_name)
        return res
    

async def main():
    async with MCPClient("http://localhost:8000/mcp") as client:
        print("-"*100)

        tool_list = await client.tool_list()
        for tools in tool_list:
            print("TOOLS LIST: ",tools.name)

        tool_call = await client.tool_call(tool_name="Read_Docs",arguments={"docs_id":"spec.txt"})
        print("TOOLS CALL : ",tool_call)

        tool_call = await client.tool_call(tool_name="Edit_Doc",arguments={"doc_id":"deposition.md","new_doc":"THIS IS UPDATED DOC"})
        print("TOOLS CALL : ",tool_call)

        print("-"*100)

        list_res = await client.list_resource()
        print("LIST RESOURCES : ", list_res[0].name)

        list_tem_res = await client.list_template_res()
        print("LIST TEMPLATE RESOURCES : ", list_tem_res[0].name)

        read_res = await client.get_resource(uri="docs://documents")
        print("READ RESOURCES : ", read_res.contents[0].text)

        Spec_docs_list = json.loads(read_res.contents[0].text)
        read_spec_res = await client.get_resource(uri=f"docs://documents/{Spec_docs_list[2]}")
        print("READ SPEC RESOURCES : ", read_spec_res.contents[0].text)

        print("-"*100)

        list_prompt = await client.list_prompt()
        for prompt in list_prompt.prompts:
            print("LIST PROMPT : ", prompt.name)

        get_first_prompt = await client.get_prompt(prompt_name="Convert_to_markdown")
        print("GET PROMPT : ", get_first_prompt.messages[0].content.text)

        get_second_prompt = await client.get_prompt(prompt_name="Summarizer")
        print("GET PROMPT : ", get_second_prompt.messages[0].content.text)
        
        print("-"*100)

asyncio.run(main())