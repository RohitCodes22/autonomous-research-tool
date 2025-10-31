import web_search
import llm_client

class ResearchAgent:
    available_tools = {
        "web_search": web_search.web_search,
        "llm_client": llm_client.ask_gpt
    }
    def __init__(self):
        self.context = []

    def update_context(self, role, content):
        self.context.append({"role": role, "content": content})
    def research (self, query):
        self.context = []
        self.update_context("user", f"The question: {query}")
        print("Starting the research process. Please hold...")
        
        planning_prompt = f"""
        You are an autonomous research agent. Your goal is to fully answer the user's query: "{query}".
        
        First, you must create a detailed, step-by-step plan. The first step of the plan MUST involve using the 'web_search' tool.
        
        Current context/history: {self.context}

        Format your output as follows:
        PLAN: [Your detailed, multi-step plan]
        SEARCH_QUERY: [The specific query to be passed to the web_search tool for step 1]

        """
        response = llm_client.ask_gpt(planning_prompt)
        self.update_context("assistant", response)
        print("Planning phase has been completed. Proceeding to execute the plan...")

        try:
            plan = response.split("PLAN:")[1].split("SEARCH_QUERY:")[0].strip()
            search_query = response.split("SEARCH_QUERY:")[1].strip()
        except IndexError:
            plan = "Search and summarize."
            search_query = query

        print(f"\nExecuting Step 1: Performing web search with query: '{search_query}'")
        results = web_search.web_search(search_query)
        print("Web search completed. Updating context with search results...")

        formattedResults = []
        links = []
        for i, result in enumerate(results.get("organic_results", [])):
            title = result.get("title", "No Title")
            snippet = result.get("snippet", "No Snippet")
            link = result.get("link", "No Link")
            formattedResults.append(f"Result {i+1}:\nTitle: {title}\nSnippet: {snippet}\nLink: {link}\n")
            links.append(link)

        context = "\n".join(formattedResults)
        self.update_context("tool", f"Web search results for query '{search_query}':\n{context}")
        print("Context updated with web search results. Now synthesizing the final answer")

        synthesis_prompt = f"""
        Based on the full conversation context below, your final step is to create and generate a **5-paragraph essay** that fully addresses the user's original query.

        The essay MUST follow this structure exactly:
        1. Introduction (1 paragraph)
        2. Body Paragraph 1 (1 paragraph, utilizing the sources)
        3. Body Paragraph 2 (1 paragraph, utilizing the sources)
        4. Body Paragraph 3 (1 paragraph, utilizing the sources)
        5. Conclusion (1 paragraph)

        Crucially, ensure the entire 5-paragraph essay is completed before proceeding to the citations.

        FULL CONTEXT:
        {self.context}

        Provide the final answer below (the complete essay and sources):
        """
        final_response = llm_client.ask_gpt(synthesis_prompt)
        citations = "\n\n=== Sources ===\n" + "\n".join([f"{i+1}. {link}" for i, link in enumerate(links)])
        final_answer = final_response + citations
        self.update_context("system", "Final Answer has been generated")

        return final_answer