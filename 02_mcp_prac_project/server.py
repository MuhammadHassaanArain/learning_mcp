from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
mcp = FastMCP("DocumentMCP", stateless_http=True)
docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# TODO: Write a tool to read a doc
@mcp.tool(name="Read_Docs", description="Tool to read Documentation.")
async def read_doc(docs_id:str=Field(description="ID of the document to read."))->TextContent:
    if docs_id not in docs:
        return TextContent(type="text",text=f"Document '{docs_id}' not found.")
    return TextContent(type="text",text=docs[docs_id])

# TODO: Write a tool to edit a doc
@mcp.tool(name="Edit_Doc",description="This tool is to edit docs.")
async def edit_doc(doc_id:str,new_doc:str)->TextContent:
    new_doc = docs[doc_id].replace(docs[doc_id],new_doc)
    docs[doc_id] = new_doc
    return TextContent(type="text", text=new_doc)
    
# TODO: Write a resource to return all doc id's
@mcp.resource("docs://documents")
async def all_docs_id():
    return list(docs.keys())

# TODO: Write a resource to return the contents of a particular doc
@mcp.resource(uri="docs://documents/{doc_id}")
async def read_spec_res(doc_id:str):
    if doc_id not in docs:
        return f"Document '{doc_id}' not found."
    return docs[doc_id]

# TODO: Write a prompt to rewrite a doc in markdown format
@mcp.prompt(name="Convert_to_markdown", description="Prompt to convert and re-write text in markdown format.")
async def re_write_prompt()->str:
    return "Convert the text and re-write it in markdown format"

# TODO: Write a prompt to summarize a doc
@mcp.prompt(name="Summarizer",description="Prompt to summarize the document.")
async def Summarizer_prompt()-> str:
    return "You Work is to Summarize the given doc."



mcp_app = mcp.streamable_http_app()