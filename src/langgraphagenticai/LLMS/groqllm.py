# import os
# import streamlit as st 
# from langchain_groq import ChatGroq

# class GroqLLM:
#     def __init__(self,user_controls_input):
#         self.user_controls_input=user_controls_input
    
#     def get_llm_model(self):
#         try:
#             groq_api_key=self.user_controls_input["GROQ_API_KEY"]
#             selected_groq_model=self.user_controls_input["selected_groq_model"]
#             if groq_api_key=="" and os.environ["GROQ_API_KEY"]=='':
#                 st.error("Please Enter the Groq API Key")
            
#             llm=ChatGroq(api_key=groq_api_key,model=selected_groq_model)
#         except Exception as e:
#             raise ValueError(f"Error occured with exception:{e}")
#         return llm 
    
import os
from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input

    def get_llm_model(self):
        try:
            groq_api_key = self.user_controls_input.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
            selected_groq_model = self.user_controls_input.get("selected_groq_model")

            if not groq_api_key:
                raise ValueError("Missing GROQ_API_KEY")

            if not selected_groq_model:
                raise ValueError("No Groq model selected")

            llm = ChatGroq(
                groq_api_key=groq_api_key,
                model=selected_groq_model,
                temperature=0.7
            )
            return llm
        except Exception as e:
            print(f"❌ ERROR in GroqLLM.get_llm_model: {str(e)}")
            return None
