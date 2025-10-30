import web_search
import llm_client

class ResearchAgent:
    def __init__(self):
        pass

    def research (self, query):
        print(f"The user has asked about: {query}")
        plan = [
            "Perform a web search to gather information.",
            "Summarize the findings using the LLM."
        ]

        print (f"Plan: {plan}")
        search_results = web_search.web_search(query)
        text_block = ""
        for result in search_results.get("organic_results", []):
            title = result.get("title", "No Title")
            snippet = result.get("snippet", "No Snippet")
            link = result.get("link", "No Link")
            text_block += f"Title: {title}\nSnippet: {snippet}\nLink: {link}\n\n"

        prompt = f"""
        You are a research assistant. Based on the following search results, provide a concise summary of the information related to the query: "{query}": 
        {text_block}

        Please write a clear and factual summary that answers the user's question.
        """
        summary = llm_client.ask_gpt(prompt) + "\n\nSources:\n"
        for result in search_results.get("organic_results", []):
            link = result.get("link", "No Link")
            summary += f"- {link}\n"  
      
        return summary
    