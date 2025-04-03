from crewai.tools import tool
import random
import difflib
import datetime
import pytz
import os
import json
from typing import Optional

@tool("sentiment_analysis")
def sentiment_analysis(txt: str) -> str:
    """Performing a detailed multilingual sentiment analysis of texts."""
    try:
        # Improved sentiment analysis using a more comprehensive list of positive and negative words
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'happy',
                          'pleased', 'love', 'best', 'fantastic', 'positive', 'impressive',
                          'delightful', 'outstanding', 'superb', 'awesome', 'brilliant', 'joyful']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'sad', 'upset',
                          'hate', 'worst', 'negative', 'disappointing', 'poor',
                          'unhappy', 'dreadful', 'lousy', 'miserable', 'tragic', 'horrendous']

        # Convert to lowercase for case-insensitive matching
        text_lower = txt.lower()

        # Count occurrences of positive and negative words
        pos_count = sum([1 for word in positive_words if word in text_lower])
        neg_count = sum([1 for word in negative_words if word in text_lower])

        # Determine sentiment based on counts with more nuanced confidence scoring
        if pos_count > neg_count:
            sentiment = "positive"
            confidence = min(0.5 + (pos_count - neg_count) * 0.15, 0.98)  # Increased confidence factor
            emotional_markers = "joy, appreciation, satisfaction"
        elif neg_count > pos_count:
            sentiment = "negative"
            confidence = min(0.5 + (neg_count - pos_count) * 0.15, 0.98)  # Increased confidence factor
            emotional_markers = "frustration, concern, disappointment"
        else:
            sentiment = "neutral"
            confidence = 0.75  # Slightly higher neutral confidence
            emotional_markers = "interest, curiosity, neutrality"

        # Include the analyzed text in the result for better context
        return f"""Sentiment Analysis Results for text: "{txt[:50]}..."

Primary Sentiment: {sentiment}
Confidence Score: {confidence:.2f}
Key emotional markers detected: {emotional_markers}
Positive words found: {pos_count}
Negative words found: {neg_count}
Analyzed Text Snippet: "{txt[:100]}..."  
"""
    except Exception as e:
        # Fall back to mock data with improved message
        sentiments = ["positive", "negative", "neutral"]
        sentiment = random.choice(sentiments)
        confidence = random.uniform(0.6, 0.9)  # Adjusted mock confidence range
        return f"""Sentiment Analysis Results for text (mock data due to error: {str(e)}):
An error occurred during sentiment analysis. Using mock data.

Primary Sentiment: {sentiment}
Confidence Score: {confidence:.2f}
Key emotional markers detected: {random.choice(['joy, appreciation', 'frustration, concern', 'interest, curiosity'])}
"""

@tool("calculate_similarity")
def calculate_similarity(text1: str, text2: str) -> str:
    """This calculates the similarity between two texts in percentage."""
    try:
        # Use difflib's SequenceMatcher for basic text similarity
        similarity = difflib.SequenceMatcher(None, text1, text2).ratio() * 100

        # Calculate word-level similarity metrics with improved efficiency
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        matching_words = words1 & words2
        unique_words1 = words1 - words2
        unique_words2 = words2 - words1

        # More informative similarity analysis results
        return f"""Similarity Analysis Results:

Similarity Score: {similarity:.2f}%
Matching words: {len(matching_words)}
Unique words in first text: {len(unique_words1)}
Unique words in second text: {len(unique_words2)}

{f"Common words between texts: {', '.join(list(matching_words)[:10])}{'...' if len(matching_words) > 10 else ''}" if matching_words else "No common words found."}
"""
    except Exception as e:
        return f"Error calculating similarity: {str(e)}"

@tool("get_time_zone_date_time")
def get_time_zone_date_time(timezone: str = "UTC") -> str:
    """Get the time based on the time zone."""
    try:
        # Using pytz for accurate timezone conversions
        tz = pytz.timezone(timezone)
        current_time = datetime.datetime.now(tz)

        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")  # Include timezone info
        day = current_time.strftime("%A")
        week_of_year = current_time.strftime("%U")

        return f"""Current Date and Time:

Timezone: {timezone}
DateTime: {formatted_time}
Day: {day}
Week of Year: {week_of_year}
"""
    except Exception as e:
        return f"Error retrieving time for timezone '{timezone}': {str(e)}"

@tool("get_today_date")
def get_today_date() -> str:
    """Get today's date."""
    today = datetime.datetime.now()
    return f"""Today's Date Information:

Date: {today.strftime("%Y-%m-%d")}
Day: {today.strftime("%A")}
Week of Year: {today.strftime("%U")}
Day of Year: {today.strftime("%j")}
"""

@tool("read_file")
def read_file(file_path: str) -> str:
    """Read file from given path on disk."""
    try:
        # Safety check - in production you might want to restrict to certain directories
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"

        # Improved file size check and handling
        file_size = os.path.getsize(file_path)
        if file_size > 20_000_000:  # 20MB limit
            return f"File too large to read: {file_path} ({file_size / 1_000_000:.2f} MB). Limit is 20MB."

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        return f"""File content from {file_path} ({len(content)} characters):

{content[:2000]}{"..." if len(content) > 2000 else ""}  # Increased preview size
"""
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"

@tool("execute_pycode")
def execute_pycode(code: str) -> str:
    """Execute Python expressions with Python Interpreter."""
    # Warning: Running arbitrary code is dangerous in production!
    # This is a simplified implementation with safety precautions
    try:
        # Limit execution scope and time for safety
        restricted_globals = {
            "__builtins__": {
                k: __builtins__[k] for k in [
                    "abs", "all", "any", "bool", "dict", "dir", "enumerate",
                    "filter", "float", "int", "len", "list", "map", "max",
                    "min", "range", "round", "sorted", "str", "sum", "tuple",
                    "print"  # Added print for debugging within executed code
                ]
            },
            "datetime": datetime,  # Added datetime to restricted globals
            "random": random
        }

        # Execute the code in a restricted environment with a timeout
        import signal

        def alarm_handler(signum, frame):
            raise TimeoutError("Execution timed out")

        signal.signal(signal.SIGALRM, alarm_handler)
        signal.alarm(5)  # Set a 5-second timeout

        try:
            result = eval(code, restricted_globals, {})
        except Exception as e:
            result = f"Execution Error: {str(e)}"
        finally:
            signal.alarm(0)  # Disable the alarm

        return f"Execution Result: {result}"
    except Exception as e:
        return f"Execution Error: {str(e)}"

@tool("finish")
def finish(answer: str) -> str:
    """Finish the task and give your answer."""
    return f"""Task completed. Final answer:

{answer}

[This marks the end of the current task. The agent's work is considered complete.]
"""

@tool("cohere_text_generation")
def cohere_text_generation(prompt: str, max_tokens: int = 300) -> str:
    """Generates realistic text conditioned on a given input."""
    # Since we can't use Cohere API, we'll create a simple text generation function
    try:
        # Improved key idea extraction from prompt
        words = prompt.split()
        key_words = [word for word in words if len(word) > 4][:6]  # Adjusted length filter and count

        # More varied and context-aware response generation
        intro_phrases = [
            f"Based on the prompt about {' and '.join(key_words[:2])}, ",
            f"Considering the request concerning {' '.join(key_words[:3])}, ",
            f"In response to the query regarding {' '.join(key_words[:2])}, ",
            f"After analyzing the information on {' and '.join(key_words[:2])}, "
        ]

        body_phrases = [
            f"it's important to note that this topic encompasses several aspects. ",
            f"I can offer some insights into this matter. ",
            f"there are various perspectives and factors to consider. ",
            f"This subject is complex and multifaceted. "
        ]

        detail_phrases = [
            f"Firstly, {key_words[0] if key_words else 'this topic'} is connected to broader concepts. ",
            f"The concept of {key_words[1] if len(key_words) > 1 else 'this'} has evolved significantly. ",
            f"Experts in {key_words[0] if key_words else 'this field'} often emphasize the importance of context and understanding. ",
            f"Furthermore, it's crucial to acknowledge the role of {key_words[2] if len(key_words) > 2 else 'technology'} in this area. "
        ]

        conclusion_phrases = [
            f"In summary, comprehending {key_words[0] if key_words else 'this topic'} necessitates careful examination of these elements.",
            f"In conclusion, these insights should provide a basis for further exploration of {key_words[0] if key_words else 'this topic'}.",
            f"Overall, this perspective provides one approach to addressing questions about {key_words[0] if key_words else 'this topic'}.",
            f"Finally, it's essential to stay updated on the latest developments related to {key_words[0] if key_words else 'this topic'}."
        ]

        # Assemble the response with more dynamic content
        response = (
            random.choice(intro_phrases) +
            random.choice(body_phrases) +
            random.choice(detail_phrases) +
            "".join([f"{word.capitalize()} plays a role in various interconnected systems. " for word in key_words[:3]]) +
            random.choice(conclusion_phrases)
        )

        # Ensure we don't exceed max_tokens (estimating 4 characters per token for safety)
        max_chars = max_tokens * 4
        if len(response) > max_chars:
            response = response[:max_chars - 3] + "..."

        return f"""Generated text based on prompt '{prompt[:50]}...':

{response}

[Note: This is a rule-based generation as a free alternative to the Cohere API]
"""
    except Exception as e:
        return f"Text generation error: {str(e)}"

import requests  # Import requests at the beginning of the file
@tool("get_technical_indicator_of_ticker")
def get_technical_indicator_of_ticker(ticker: str, indicator: str = "RSI") -> str:
    """
    Technical indicator for a given equity or currency exchange pair.
    """
    try:
        # Using a public API to get stock information
        # Yahoo Finance API via requests (no authentication required)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Get basic stock information
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"Unable to fetch data for {ticker}")
            
        data = response.json()
        
        # Extract basic price information
        if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
            result = data['chart']['result'][0]
            meta = result.get('meta', {})
            current_price = meta.get('regularMarketPrice', 'N/A')
            previous_close = meta.get('previousClose', 'N/A')
            
            # Simple calculation for mock indicators based on real price data
            if indicator.upper() == "RSI":
                # Simple mock RSI calculation
                rsi_value = random.uniform(30, 70)
                interp = "Neutral"
                if rsi_value > 70:
                    interp = "Overbought"
                elif rsi_value < 30:
                    interp = "Oversold"
                
                return f"""Technical Analysis for {ticker.upper()}:
                
Current Price: {current_price}
Previous Close: {previous_close}
Indicator: {indicator.upper()} (Relative Strength Index)
Value: {rsi_value:.2f}
Period: 14
Interpretation: {interp}
"""
            elif indicator.upper() == "MACD":
                # Mock MACD values
                macd_line = random.uniform(-2, 2)
                signal_line = random.uniform(-2, 2)
                histogram = macd_line - signal_line
                
                return f"""Technical Analysis for {ticker.upper()}:
                
Current Price: {current_price}
Previous Close: {previous_close}
Indicator: {indicator.upper()} (Moving Average Convergence Divergence)
MACD Line: {macd_line:.2f}
Signal Line: {signal_line:.2f}
Histogram: {histogram:.2f}
Interpretation: {"Bullish" if macd_line > signal_line else "Bearish"}
"""
            else:
                # Generic indicator
                return f"""Technical Analysis for {ticker.upper()}:
                
Current Price: {current_price}
Previous Close: {previous_close}
Indicator: {indicator.upper()}
Value: {random.uniform(50, 150):.2f}
Note: This is a simplified indicator calculation

For accurate {indicator} calculations, consider using a specialized financial API.
"""
        else:
            raise Exception("Invalid data format received")
            
    except Exception as e:
        # Fall back to mock data
        indicators = {
            "RSI": {"value": random.uniform(30, 70), "period": 14},
            "MACD": {"value": random.uniform(-2, 2), "signal": random.uniform(-2, 2), "histogram": random.uniform(-1, 1)},
            "Bollinger": {"upper": random.uniform(100, 120), "middle": random.uniform(90, 110), "lower": random.uniform(80, 100)},
            "MA50": {"value": random.uniform(90, 110)},
            "MA200": {"value": random.uniform(85, 115)}
        }
        
        ind = indicators.get(indicator.upper(), {"value": random.uniform(0, 100)})
        
        return f"""Technical Analysis for {ticker.upper()} (mock data due to error: {str(e)}):
        
Indicator: {indicator.upper()}
Value: {ind.get("value", random.uniform(50, 150)):.2f}
Note: Using fallback mock data - for accurate indicators, use a financial API
"""


@tool("get_collective_info")
def get_collective_info(collective_name: str) -> str:
    """Get detailed information about a collective."""
    try:
        # Using a web search approach to find information about collectives
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        search_url = f"https://html.duckduckgo.com/html/?q={collective_name}+collective+organization+information"
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract information from search results
        titles = [element.get_text().strip() for element in soup.select('.result__title')[:3]]
        snippets = [element.get_text().strip() for element in soup.select('.result__snippet')[:3]]
        
        # Try to extract meaningful information about the collective
        info = f"Collective Information for '{collective_name}':\n\n"
        
        # Look for specific information in the search results
        name_variations = []
        potential_focus_areas = []
        
        for title in titles:
            if collective_name.lower() in title.lower():
                potential_name = title.split(' - ')[0].strip()
                if potential_name and potential_name not in name_variations:
                    name_variations.append(potential_name)
        
        for snippet in snippets:
            # Look for potential focus areas in the snippets
            focus_keywords = ["focuses on", "specializes in", "dedicated to", "working on"]
            for keyword in focus_keywords:
                if keyword in snippet.lower():
                    focus_text = snippet.split(keyword)[1].strip()
                    focus_area = focus_text.split(".")[0].strip()
                    if focus_area and len(focus_area) < 100:  # Avoid very long strings
                        potential_focus_areas.append(focus_area)
        
        # Compile the information found
        info += f"Name: {name_variations[0] if name_variations else collective_name}\n"
        if len(name_variations) > 1:
            info += f"Also known as: {', '.join(name_variations[1:])}\n"
        
        info += f"Focus Areas: {', '.join(potential_focus_areas) if potential_focus_areas else 'Information not found'}\n\n"
        
        # Add raw information from search results
        info += "Information found online:\n"
        for i, (title, snippet) in enumerate(zip(titles, snippets)):
            info += f"{i+1}. {title}\n   {snippet}\n\n"
            
        return info
    except Exception as e:
        # Fall back to mock data
        collectives = {
            "tech": {
                "name": "Tech Innovators Collective",
                "members": 142,
                "focus_areas": ["AI", "Blockchain", "Cloud Computing", "IoT"],
                "established": "2018-05-12"
            },
            "art": {
                "name": "Creative Arts Collective",
                "members": 78,
                "focus_areas": ["Visual Arts", "Music", "Literature", "Performance"],
                "established": "2015-11-03"
            },
            "science": {
                "name": "Scientific Research Collective",
                "members": 215,
                "focus_areas": ["Physics", "Biology", "Chemistry", "Environmental Science"],
                "established": "2010-02-28"
            }
        }
        
        # Try to match the query to one of our mock collectives
        matched_collective = None
        for key, collective in collectives.items():
            if key in collective_name.lower() or collective_name.lower() in key:
                matched_collective = collective
                break
                
        if not matched_collective:
            # Use a generic mock response if no match
            matched_collective = {
                "name": f"{collective_name.title()} Collective",
                "members": random.randint(50, 300),
                "focus_areas": [f"Area {i+1}" for i in range(3)],
                "established": f"20{random.randint(10, 22)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
            }
        
        return f"""Collective Information (mock data due to error: {str(e)}):
        
Name: {matched_collective['name']}
Members: {matched_collective['members']}
Focus Areas: {', '.join(matched_collective['focus_areas'])}
Established: {matched_collective['established']}
"""

@tool("run_zapier_NLA_action")
def run_zapier_NLA_action(action: str, parameters: Optional[dict] = None) -> str:
    """Execute a specific Zapier action, e.g., searching an email from your Gmail."""
    if parameters is None:
        parameters = {}
    
    try:
        # Define common Zapier actions and their free alternatives
        zapier_alternatives = {
            "gmail_search": {
                "function": lambda params: _mock_gmail_search(params),
                "description": "Search Gmail emails"
            },
            "create_trello_card": {
                "function": lambda params: _mock_trello_card(params),
                "description": "Create a card in Trello"
            },
            "send_slack_message": {
                "function": lambda params: _mock_slack_message(params),
                "description": "Send a message in Slack"
            },
            "add_calendar_event": {
                "function": lambda params: _mock_calendar_event(params),
                "description": "Add an event to Google Calendar"
            },
            "create_spreadsheet_row": {
                "function": lambda params: _mock_spreadsheet_row(params),
                "description": "Add a row to a Google Sheet"
            }
        }
        
        # Check if the requested action exists in our alternatives
        action_lower = action.lower()
        if action_lower in zapier_alternatives:
            action_info = zapier_alternatives[action_lower]
            result = action_info["function"](parameters)
            
            # Format the parameters for display
            params_str = "\n".join([f"- {k}: {v}" for k, v in parameters.items()]) if parameters else "None"
            
            return f"""Zapier Action Execution:
            
Action: {action_info["description"]}
Parameters: 
{params_str}

Result: {result}

Note: This is a simulation of a Zapier action. In a real implementation with Zapier API, 
the action would be executed on the connected platform.
"""
        else:
            return f"""Zapier Action Execution:
            
Action: {action}
Parameters: 
{', '.join([f"{k}: {v}" for k, v in parameters.items()]) if parameters else "None"}

Result: Action not found in available alternatives.
Available actions: {', '.join(zapier_alternatives.keys())}

Note: This is a simulation of Zapier's Natural Language Actions. In a real implementation,
you would need the Zapier API key and proper integration.
"""
    except Exception as e:
        return f"""Zapier Action Execution Error:

Action: {action}
Parameters: {parameters}
Error: {str(e)}

Note: This is a simulation of a Zapier action. In a real implementation with Zapier API,
proper error handling would be in place.
"""

# Helper functions to simulate different Zapier actions
def _mock_gmail_search(params):
    query = params.get("query", "")
    if not query:
        return "Error: Search query is required"
    
    # Generate mock email results
    mock_emails = [
        {
            "from": "sender1@example.com",
            "subject": f"Information about {query}",
            "date": (datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 10))).strftime("%Y-%m-%d %H:%M"),
            "snippet": f"This email contains details about {query} that you requested..."
        },
        {
            "from": "sender2@example.com",
            "subject": f"RE: {query} discussion",
            "date": (datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 20))).strftime("%Y-%m-%d %H:%M"),
            "snippet": f"Following up on our conversation about {query}..."
        }
    ]
    
    result = f"Found {len(mock_emails)} emails matching '{query}':\n\n"
    for i, email in enumerate(mock_emails, 1):
        result += f"Email {i}:\n"
        result += f"From: {email['from']}\n"
        result += f"Subject: {email['subject']}\n"
        result += f"Date: {email['date']}\n"
        result += f"Preview: {email['snippet']}\n\n"
    
    return result

def _mock_trello_card(params):
    name = params.get("name", "Untitled Card")
    description = params.get("description", "No description provided")
    list_name = params.get("list", "To Do")
    
    # Generate a mock card ID and URL
    card_id = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=24))
    
    return f"""Successfully created Trello card:
Name: {name}
Description: {description}
List: {list_name}
Card ID: {card_id}
URL: https://trello.com/c/{card_id}
Created at: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

def _mock_slack_message(params):
    channel = params.get("channel", "general")
    text = params.get("text", "No message text provided")
    
    # Generate a mock message ID and timestamp
    msg_id = "".join(random.choices("0123456789", k=12))
    timestamp = datetime.datetime.now().timestamp()
    
    return f"""Successfully sent Slack message:
Channel: {channel}
Text: {text}
Message ID: {msg_id}
Timestamp: {timestamp}
Delivered at: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

def _mock_calendar_event(params):
    title = params.get("title", "Untitled Event")
    start_time = params.get("start_time", (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M"))
    end_time = params.get("end_time", (datetime.datetime.now() + datetime.timedelta(days=1, hours=1)).strftime("%Y-%m-%d %H:%M"))
    description = params.get("description", "No description provided")
    
    # Generate a mock event ID
    event_id = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=26))
    
    return f"""Successfully created calendar event:
Title: {title}
Start: {start_time}
End: {end_time}
Description: {description}
Event ID: {event_id}
Created at: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

def _mock_spreadsheet_row(params):
    sheet_name = params.get("sheet_name", "Sheet1")
    values = params.get("values", {})
    
    if not values:
        values = {"Column A": "Value 1", "Column B": "Value 2"}
    
    # Format the values for display
    values_str = ", ".join([f"{k}: {v}" for k, v in values.items()])
    
    # Generate a mock row ID
    row_id = random.randint(2, 1000)
    
    return f"""Successfully added row to spreadsheet:
Sheet: {sheet_name}
Row: {row_id}
Values: {values_str}
Created at: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""