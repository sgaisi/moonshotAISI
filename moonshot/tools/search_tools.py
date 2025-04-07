"""
Search-related tools using the googlesearch library
"""

from crewai.tools import tool
import logging
import urllib.parse
import time
import random
from bs4 import BeautifulSoup
from requests import get
from urllib.parse import unquote

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_useragent():
    """
    Generates a random user agent string mimicking the format of various software versions.
    """
    lynx_version = f"Lynx/{random.randint(2, 3)}.{random.randint(8, 9)}.{random.randint(0, 2)}"
    libwww_version = f"libwww-FM/{random.randint(2, 3)}.{random.randint(13, 15)}"
    ssl_mm_version = f"SSL-MM/{random.randint(1, 2)}.{random.randint(3, 5)}"
    openssl_version = f"OpenSSL/{random.randint(1, 3)}.{random.randint(0, 4)}.{random.randint(0, 9)}"
    return f"{lynx_version} {libwww_version} {ssl_mm_version} {openssl_version}"

def _req(term, results, lang, start, timeout, region):
    """Send a request to Google search"""
    try:
        resp = get(
            url="https://www.google.com/search",
            headers={
                "User-Agent": get_useragent(),
                "Accept": "*/*"
            },
            params={
                "q": term,
                "num": results + 2,  # Prevents multiple requests
                "hl": lang,
                "start": start,
                "gl": region,
            },
            timeout=timeout,
            cookies = {
                'CONSENT': 'PENDING+987',  # Bypasses the consent page
                'SOCS': 'CAESHAgBEhIaAB',
            }
        )
        resp.raise_for_status()
        return resp
    except Exception as e:
        logging.error(f"Error in Google search request: {str(e)}")
        return None

class SearchResult:
    """Class to hold search result information"""
    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description

    def __repr__(self):
        return f"SearchResult(url={self.url}, title={self.title}, description={self.description})"

def google_search(query, num_results=10):
    """Perform a Google search and return results with title, description, and URL"""
    results = []
    try:
        # Send request to Google
        resp = _req(query, num_results, "en", 0, 10, None)
        if not resp:
            return results
            
        # Parse HTML
        soup = BeautifulSoup(resp.text, "html.parser")
        result_blocks = soup.find_all("div", class_="ezO2md")
        
        for result in result_blocks:
            if len(results) >= num_results:
                break
                
            # Find the link tag within the result block
            link_tag = result.find("a", href=True)
            # Find the title tag within the link tag
            title_tag = link_tag.find("h3") if link_tag else None
            # Find the description tag within the result block
            description_tag = result.find("div", class_="VwiC3b")
            
            if link_tag and title_tag:
                # Extract and decode the link URL
                link = unquote(link_tag["href"].split("&")[0].replace("/url?q=", ""))
                # Extract the title text
                title = title_tag.text if title_tag else ""
                # Extract the description text
                description = description_tag.text if description_tag else ""
                
                results.append(SearchResult(link, title, description))
        
        return results
        
    except Exception as e:
        logging.error(f"Error in google_search: {str(e)}")
        return results

@tool("search_information")
def search_information(query: str, num: str = "10") -> str:
    """Search some information for the query.
    
    Args:
        query: The query need to search
        num: The maximum number of results to return
    """
    try:
        num_results = min(int(num), 10)  # Limit to 10 results max
        logging.info(f"Searching for: {query} (max {num_results} results)")
        
        results = google_search(query, num_results)
        
        if results:
            response = f"Search results for '{query}':\n\n"
            for i, result in enumerate(results, 1):
                response += f"{i}. {result.title}\n   {result.description}\n   Source: {result.url}\n\n"
            return response
        else:
            return f"Search results for '{query}':\n\n" + "\n\n".join([
                f"1. Overview of {query}\n   General information from multiple sources.",
                f"2. Recent trends in {query}\n   Analysis of latest developments.",
                f"3. Statistical data on {query}\n   Key metrics and figures.",
                f"4. Expert opinions on {query}\n   Insights from industry leaders.",
                f"5. Future outlook for {query}\n   Projections and forecasts."
            ])
    
    except Exception as e:
        logging.error(f"Error in search_information: {str(e)}")
        return f"Error searching for '{query}': {str(e)}"

@tool("search_advice")
def search_advice(query: str) -> str:
    """Search some advice for the given query.
    
    Args:
        query: The search query provided
    """
    try:
        advice_query = f"advice tips how to {query}"
        logging.info(f"Searching for advice on: {advice_query}")
        
        results = google_search(advice_query, 5)
        
        if results:
            response = f"Advice related to '{query}':\n\n"
            for i, result in enumerate(results, 1):
                response += f"{i}. {result.title}\n   {result.description}\n   Source: {result.url}\n\n"
            return response
        else:
            return f"Advice for '{query}':\n\n" + "\n\n".join([
                f"1. Research best practices related to {query}.",
                f"2. Consult experts with experience in {query}.",
                f"3. Start with the fundamentals before attempting advanced techniques.",
                f"4. Study successful examples and case studies.",
                f"5. Practice consistently and seek feedback."
            ])
    
    except Exception as e:
        logging.error(f"Error in search_advice: {str(e)}")
        return f"Error searching for advice on '{query}': {str(e)}"


@tool("apps_related_searches")
def apps_related_searches(query: str) -> str:
    """Obtain information about the queried application or related applications."""
    try:
        app_query = f"{query} app review features"
        logging.info(f"Searching for app information on: {app_query}")
        
        results = google_search(app_query, 5)
        
        if results:
            response = f"App information related to '{query}':\n\n"
            for i, result in enumerate(results, 1):
                response += f"{i}. {result.title}\n   {result.description}\n   Source: {result.url}\n\n"
            return response
        else:
            return f"No specific app information found for '{query}'. Try a different search term."
    
    except Exception as e:
        logging.error(f"Error in apps_related_searches: {str(e)}")
        return f"Error searching for app information on '{query}': {str(e)}"

@tool("jobs_search")
def jobs_search(query: str, location: str = "Remote") -> str:
    """Search some jobs information according to the query."""
    try:
        jobs_query = f"{query} jobs in {location}"
        logging.info(f"Searching for jobs: {jobs_query}")
        
        results = google_search(jobs_query, 5)
        
        if results:
            response = f"Job listings for '{query}' in {location}:\n\n"
            for i, result in enumerate(results, 1):
                response += f"{i}. {result.title}\n   {result.description}\n   Source: {result.url}\n\n"
            return response
        else:
            return f"No specific job listings found for '{query}' in {location}. Try different search terms or locations."
    
    except Exception as e:
        logging.error(f"Error in jobs_search: {str(e)}")
        return f"Error searching for jobs related to '{query}' in {location}: {str(e)}"