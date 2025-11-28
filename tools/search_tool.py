from langchain.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()

if __name__ == "__main__":
    
    query = "Ankara hava durumu nedir ?"
    
    result = search.run(query)
    
    print(f"Search results for '{query}':\n{result}")
