from pydantic import BaseModel, Field
from typing_extensions import TypedDict,List
from langgraph.graph.message import add_messages
from typing import Annotated
from langchain_core.messages import BaseMessage



# class State(TypedDict):
#     message:Annotated[List,add_messages]

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

