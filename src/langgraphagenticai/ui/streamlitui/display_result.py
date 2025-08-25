import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from src.langgraphagenticai.tools.search_tool import get_tools
from langchain_core.messages import HumanMessage
''

class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message

        print("User message:", user_message)

        if usecase == "Basic Chatbot":
            # for event in graph.stream({'messages': ("user", user_message)}):
            for event in graph.stream({"messages": [HumanMessage(content=user_message)]}):
                for value in event.values():
                    print(value['messages'])
                    with st.chat_message("user"):
                        st.write(user_message)
                    with st.chat_message("assistant"):
                        st.write(value["messages"].content)

        elif usecase == "Chatbot With Web":
            # Fetch tools from the graph or fallback
            tools = getattr(graph, "tools", None)
            if tools is None or tools == []:
                tools = get_tools()  # fallback to get tools

            # Prepare state and invoke the graph with tools
            # initial_state = {"messages": [user_message]}
            # res = graph.invoke(initial_state, tools=tools)
            initial_state = {"messages": [HumanMessage(content=user_message)]}
            res = graph.invoke(initial_state)   # removed tools=tools

            # Display messages in Streamlit chat
            for message in res['messages']:
                if isinstance(message, HumanMessage):
                    with st.chat_message("user"):
                        st.write(message.content)
                elif isinstance(message, ToolMessage):
                    with st.chat_message("ai"):
                        st.write("Tool Call Start")
                        st.write(message.content)
                        st.write("Tool Call End")
                elif isinstance(message, AIMessage) and message.content:
                    with st.chat_message("assistant"):
                        st.write(message.content)
        
        elif usecase=="AI News":
            frequency=self.user_message
            with st.spinner("Fetching and summarizing news..."):
                # result=graph.invoke({"messages":frequency})
                result = graph.invoke({"messages": [HumanMessage(content=frequency.lower())]})
                try:
                    AI_NEWS_PATH=f"./AINews/{frequency.lower()}_summary.md"
                    with open(AI_NEWS_PATH,"r") as file:
                        markdown_content=file.read()

                        st.markdown(markdown_content,unsafe_allow_html=True)
                except FileNotFoundError:
                    st.error(f"News Not Generated or File not found{AI_NEWS_PATH}")
                except Exception as e:
                    st.error(f"An error occured:{str(e)}")

