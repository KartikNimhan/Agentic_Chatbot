from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
import os
from datetime import datetime
 

class AINewsNode:
    def __init__(self,llm):
        self.tavily=TavilyClient()
        self.llm=llm
        self.state={}
    
    def fetch_news(self, state:dict)->dict:

        frequency=state['messages'][0].content.lower()
        self.state['frequency']=frequency
        time_range_map={'daily':'d','weekly':'w','monthly':'m','year':'y'}
        days_map={'daily':1,'weekly':7,'monthly':30,'year':366}

        response=self.tavily.search(
            query="Top Artificial Intelligence(AI) technology news India and Globally",
            topic="news",
            time_range=time_range_map[frequency],
            include_answer="advanced",
            max_results=15,
            days=days_map[frequency],
        )

        state['news_data']=response.get('results',[])
        self.state['news_data']=state['news_data']
        return self.state
    
    def summarize_news(self,state:dict)->dict:
        news_items=self.state['news_data']

        prompt_template=ChatPromptTemplate.from_messages([
            ("system","""Summarize AI news articles into markdown format. For each item include:
                - Date in **YYYY-MM-DD** format in IST timezone
                - Concise 1–2 sentence summary from the latest news
                - Sort news by date (latest first)
                - Source URL included as a markdown link
                Use format strictly:

                ### [Date]
                - [Summary](URL)
                """),
                ("user","Articles:\n{articles}")

        ])
        articles_str="\n\n".join([
            f"Content:{item.get('content', '')}\nURL: {item.get('url', '')}\nDate: {item.get('published_date', '')}"
            for item in news_items
        ])

        response=self.llm.invoke(prompt_template.format(articles=articles_str))

        state["summary"]=response.content 
        self.state['summary']=state['summary']
        return self.state
    
    # def save_result(self,state):
    #     frequency=self.state['frequency']
    #     summary=self.state['summary']
    #     filename=f"./AINews/{frequency}_summary.md"
    #     with open(filename,'w') as f:
    #         f.write(f"# {frequency.capitalize()} AI News Summary\n\n")
    #         f.write(summary)
    #     self.state['filename']=filename
    #     return self.state
   

    def save_result(self, state):
        frequency = self.state['frequency']
        summary = self.state['summary']
        filename = f"./AINews/{frequency}_summary.md"

        # Ensure AINews folder exists
        os.makedirs("./AINews", exist_ok=True)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"## {frequency.capitalize()} AI News Summary ({datetime.now().strftime('%b %d, %Y')})\n\n")
            f.write(summary)

        self.state['filename'] = filename
        return self.state


