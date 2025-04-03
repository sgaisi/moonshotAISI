"""
Tool implementations for the Safety Benchmark
"""

from typing import List, Callable
from .search_tools import search_information, search_advice, apps_related_searches, jobs_search
from .finish_tool import finish
from .analysis_tools import sentiment_analysis, calculate_similarity,  cohere_text_generation, execute_pycode, get_collective_info, get_technical_indicator_of_ticker, get_time_zone_date_time, get_today_date, read_file, run_zapier_NLA_action  # Add the new tools

def get_all_tools() -> List[Callable]:
    """Return all available tools"""
    return [
        apps_related_searches,
        cohere_text_generation,
        execute_pycode,
        get_collective_info,
        get_technical_indicator_of_ticker,
        get_time_zone_date_time,
        get_today_date,
        jobs_search,
        read_file,
        run_zapier_NLA_action,
        search_information,
        search_advice,
        sentiment_analysis,  # Add the new tools
        calculate_similarity,  # Add the new tools
        finish
    ]