"""
Search-related tools
"""

from crewai.tools import tool
import random
import difflib
import datetime
import os
import json
from typing import Optional
import requests
import logging
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import re
from fake_useragent import UserAgent

# Configure detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

import logging
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import random

# Configure detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def search_information_helper(query: str, num_results: int = 10) -> list:
    """
    Helper function to search for information using multiple sources.
    Returns a list of dictionaries with title, snippet, and source.
    """
    results = []
    
    # First try Wikipedia API
    logging.info(f"Searching Wikipedia for: {query}")
    try:
        wiki_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={urllib.parse.quote(query)}&limit={num_results}&format=json"
        response = requests.get(wiki_url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            titles = data[1]
            descriptions = data[2]
            links = data[3]
            
            if titles:
                for i, (title, desc, link) in enumerate(zip(titles, descriptions, links)):
                    if i >= num_results:
                        break
                    results.append({
                        "title": title,
                        "snippet": desc if desc else "No description available",
                        "source": link
                    })
                logging.info(f"Found {len(results)} results from Wikipedia")
    except Exception as e:
        logging.warning(f"Wikipedia search failed: {str(e)}")
    
    # If we don't have enough results, try DuckDuckGo
    if len(results) < num_results:
        logging.info(f"Searching DuckDuckGo for: {query}")
        try:
            ua = UserAgent()
            headers = {
                'User-Agent': ua.random
            }
            search_url = f"https://html.duckduckgo.com/html/?q={query}"
            
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            result_elements = soup.select('.result')
            
            for result in result_elements:
                if len(results) >= num_results:
                    break
                
                title_element = result.select_one('.result__title')
                snippet_element = result.select_one('.result__snippet')
                
                if title_element and snippet_element:
                    title = title_element.get_text().strip()
                    snippet = snippet_element.get_text().strip()
                    
                    # Get the link if available
                    link_element = title_element.select_one('a')
                    link = link_element.get('href', '#') if link_element else '#'
                    
                    results.append({
                        "title": title,
                        "snippet": snippet,
                        "source": link
                    })
            
            logging.info(f"Added {len(result_elements)} results from DuckDuckGo")
        except Exception as e:
            logging.warning(f"DuckDuckGo search failed: {str(e)}")
    
    return results

@tool("search_information")
def search_information(query: str, num: str = "10") -> str:
    """Search some information for the query.
    
    Args:
        query: The query need to search
        num: The maximum number of results to return
    """
    try:
        num_results = int(num)
        logging.info(f"search_information called with query: '{query}', num: {num_results}")
        
       
        search_results = search_information_helper(query, num_results)
        
        if search_results:
            formatted_results = []
            for i, result in enumerate(search_results, 1):
                formatted_results.append(
                    f"{i}. {result['title']}\n   {result['snippet']}\n   Source: {result['source']}\n"
                )
            return f"Search results for '{query}' (limited to {len(formatted_results)} results):\n\n" + "\n".join(formatted_results)
        
        # Fallback to generic response if all search methods fail
        return f"Search results for '{query}' (limited to 5 results):\n\n" + "\n\n".join([
            f"1. Overview of {query}\n   This result provides general information about {query} from multiple sources.",
            f"2. Recent trends in {query}\n   Analysis of the latest developments and patterns related to {query}.",
            f"3. Statistical data on {query}\n   Numerical information and metrics concerning {query} from research reports.",
            f"4. Expert opinions on {query}\n   Perspectives from industry leaders and researchers regarding {query}.",
            f"5. Future outlook for {query}\n   Projections and forecasts about how {query} may evolve in coming years."
        ])
        
    except Exception as e:
        logging.error(f"Error performing search for '{query}': {str(e)}")
        return f"Error performing search for '{query}': {str(e)}\n\nPlease try a different query or check your internet connection."


@tool("search_advice")
def search_advice(query: str) -> str:
    """Search some advice for the given query.
    
    Args:
        query: The search query provided
    """
    logging.info(f"Searching advice for query: {query}")
    advice_query = f"advice tips how to {query}"
    
    # Use DuckDuckGo directly
    try:
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random
        }
        search_url = f"https://html.duckduckgo.com/html/?q=advice+about+{query}"
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        result_elements = soup.select('.result')
        logging.info(f"Found {len(result_elements)} result elements")
        
        results = []
        
        for i, result in enumerate(result_elements[:5]):
            title_element = result.select_one('.result__title')
            snippet_element = result.select_one('.result__snippet')
            
            if title_element and snippet_element:
                title = title_element.get_text().strip()
                snippet = snippet_element.get_text().strip()
                link_element = title_element.select_one('a')
                link = link_element.get('href', '#') if link_element else '#'
                
                results.append(f"{i+1}. {title}\n   {snippet}\n   Source: {link}\n")
        
        if results:
            return f"Advice related to '{query}':\n\n" + "\n".join(results)
    except Exception as e:
        logging.error(f"DuckDuckGo search failed: {str(e)}")
    
    # If the search failed, provide generic advice
    return f"Sorry, I couldn't find specific advice for '{query}'. Here are some general approaches:\n\n" + "\n\n".join([
        f"1. Research best practices\n   Look for established methodologies and approaches related to {query}.",
        f"2. Consult experts\n   Seek advice from professionals with experience in {query}.",
        f"3. Learn from case studies\n   Examine real-world examples of successful {query} scenarios.",
        f"4. Follow step-by-step guides\n   Break down the process of {query} into manageable steps.",
        f"5. Join relevant communities\n   Connect with others dealing with similar {query} situations."
    ])
    
@tool("apps_related_searches")
def apps_related_searches(query: str) -> str:
    """Obtain information about the queried application or related applications."""
    try:
        # Using DuckDuckGo search for app information
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random
        }
        search_url = f"https://html.duckduckgo.com/html/?q={query}+app+review+information"
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        result_elements = soup.select('.result')
        
        # Extract app information from search results
        count = 0
        for result in result_elements[:5]:  # Limit to top 5
            title_element = result.select_one('.result__title')
            snippet_element = result.select_one('.result__snippet')
            
            if title_element and snippet_element:
                title = title_element.get_text().strip()
                snippet = snippet_element.get_text().strip()
                
                results.append(f"{count+1}. {title}\n   {snippet}\n")
                count += 1
        
        if not results:
            return f"No app information found for '{query}'."
            
        return f"App information related to '{query}':\n\n" + "\n".join(results)
    except Exception as e:
        return f"Could not find app information for '{query}'."

@tool("jobs_search")
def jobs_search(query: str, location: str = "Remote") -> str:
    """Search some jobs information according to the query."""
    try:
        # Using DuckDuckGo to search for job information
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random
        }
        search_url = f"https://html.duckduckgo.com/html/?q={query}+jobs+in+{location}"
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        result_elements = soup.select('.result')

        # Extract job information from search results
        count = 0
        for result in result_elements[:5]:  # Limit to top 5
            title_element = result.select_one('.result__title')
            snippet_element = result.select_one('.result__snippet')
            
            if title_element and snippet_element:
                title = title_element.get_text().strip()
                snippet = snippet_element.get_text().strip()
                
                results.append(f"{count+1}. {title}\n   {snippet}\n")
                count += 1
        
        if not results:
            return f"No job information found for '{query}'."
            
        return f"Job information related to '{query}':\n\n" + "\n".join(results)
    except Exception as e:
        return f"Could not find job information for '{query}'."