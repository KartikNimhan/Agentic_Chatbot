# from src.langgraphagenticai.state.state import State

# class BasicChatbotNode:
#     def __init__(self,model):
#         self.llm=model

#     def process(self,state:State)->dict:
#         return {"messages":self.llm.invoke(state['message'])}


# from src.langgraphagenticai.state.state import State
# from langchain_core.messages import AIMessage, HumanMessage


# class BasicChatbotNode:
#     """
#     Basic Chatbot logic implementation
#     """
#     def __init__(self, model):
#         self.llm = model

#     def process(self, state: State) -> dict:
#         try:
#             user_message = state["messages"][-1]  # last HumanMessage
#             print("🟢 User message:", user_message)

#             # ✅ Convert HumanMessage → string before invoking LLM
#             if isinstance(user_message, HumanMessage):
#                 query = user_message.content
#             else:
#                 query = str(user_message)

#             response = self.llm.invoke(query)
#             print("🟢 Raw model response:", response)

#             if hasattr(response, "content"):
#                 response_text = response.content
#             else:
#                 response_text = str(response)

#             # ✅ return AIMessage back into graph
#             return {"messages": [AIMessage(content=response_text)]}

#         except Exception as e:
#             print("❌ ERROR in BasicChatbotNode:", str(e))
#             raise e
import re
from src.langgraphagenticai.state.state import State
from langchain_core.messages import AIMessage, HumanMessage


class BasicChatbotNode:
    def __init__(self, model):
        self.llm = model

    def process(self, state: State) -> dict:
        try:
            user_message = state["messages"][-1]
            if isinstance(user_message, HumanMessage):
                query = user_message.content
            else:
                query = str(user_message)

            response = self.llm.invoke(query)

            # Extract response text
            if hasattr(response, "content"):
                response_text = response.content
            else:
                response_text = str(response)

            # ✅ Remove <think>...</think> block if present
            cleaned_text = re.sub(r"<think>.*?</think>", "", response_text, flags=re.DOTALL).strip()

            return {"messages": [AIMessage(content=cleaned_text)]}

        except Exception as e:
            print("❌ ERROR in BasicChatbotNode:", str(e))
            raise e
