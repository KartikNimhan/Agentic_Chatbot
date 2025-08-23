import streamlit as st
from langchain_core.messages import HumanMessage


class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message

        # ✅ fixed typo: "Basic Cahtbot" → "Basic Chatbot"
        if usecase == "Basic Chatbot":
            try:
                # ✅ pass correct input type (list of HumanMessage)
                for event in graph.stream({"messages": [user_message]}):
                    print(event.values())
                    for value in event.values():
                        print(value["messages"])

                        # show user message
                        with st.chat_message("user"):
                            st.write(user_message)

                        # ✅ fixed: messages is a list of strings, not .content
                        with st.chat_message("assistant"):
                            last_msg = value["messages"][-1]
                            if hasattr(last_msg, "content"):
                                st.write(last_msg.content)
                            else:
                                st.write(str(last_msg))
            except Exception as e:
                st.error(f"Error while displaying result: {e}")


