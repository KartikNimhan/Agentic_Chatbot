# from langgraph.graph import StateGraph
# from src.langgraphagenticai.state.state import State
# from langgraph.graph import START,END
# from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode

# class GraphBuilder:
#     def __init__(self,model):
#         self.llm =model
#         self.graph_builder=StateGraph(State)

#     def basic_chatbot_build_graph(self):
#         self.basic_chatbot_node=BasicChatbotNode(self.llm)
#         self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
#         self.graph_builder.add_edge(START,"chatbot")
#         self.graph_builder.add_edge("chatbot",END)

#     def setup_graph(self,usecase:str):
#         if usecase=="Basic Chatbot":
#             self.basic_chatbot_build_graph()
#         return self.graph_builder.compile()

from langgraph.graph import StateGraph, START, END
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode

class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)

    def basic_chatbot_build_graph(self):
        chatbot_node = BasicChatbotNode(self.llm)
        self.graph_builder.add_node("chatbot", chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def setup_graph(self, usecase: str):
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        return self.graph_builder.compile()

