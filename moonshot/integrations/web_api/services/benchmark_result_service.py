from .... import api as moonshot_api
from ..services.base_service import BaseService
from ..services.utils.exceptions_handler import exception_handler
from ..types.types import BenchmarkResult


class BenchmarkResultService(BaseService):
    
    def _filter_results_by_processing_module(self, results: list[dict], processing_module: str = None) -> list[dict]:
        """Filter results by result processing module if specified."""
        if processing_module is None:
            return results
            
        return [
            result for result in results 
            if result.get("metadata", {}).get("result_processing_module") == processing_module
        ]
    
    @exception_handler
    def get_all_results(self, filter_by_processing_module: str = None) -> list[BenchmarkResult]:
        results = moonshot_api.api_get_all_result()
        filtered_results = self._filter_results_by_processing_module(results, filter_by_processing_module)
        return [BenchmarkResult(**result) for result in filtered_results]

    @exception_handler
    def get_all_result_name(self, filter_by_processing_module: str = None) -> list[str] | None:
        results = moonshot_api.api_get_all_result()
        filtered_results = self._filter_results_by_processing_module(results, filter_by_processing_module)
        
        result_ids = []
        for result in filtered_results:
            result_id = result.get("metadata", {}).get("id")
            if result_id:
                result_ids.append(result_id)
        return result_ids

    @exception_handler
    def get_result_by_id(self, result_id: str, validate_processing_module: str = None) -> BenchmarkResult:
        result = moonshot_api.api_read_result(result_id)
        
        # Optionally validate the result is of the expected processing module type
        if validate_processing_module:
            result_processing_module = result.get("metadata", {}).get("result_processing_module")
            if result_processing_module != validate_processing_module:
                raise ValueError(f"Result {result_id} is not a {validate_processing_module} result")
                
        return BenchmarkResult(**result)

    @exception_handler
    def delete_result(self, result_id: str, validate_processing_module: str = None) -> None:
        # Optionally validate before deletion
        if validate_processing_module:
            result = moonshot_api.api_read_result(result_id)
            result_processing_module = result.get("metadata", {}).get("result_processing_module")
            if result_processing_module != validate_processing_module:
                raise ValueError(f"Result {result_id} is not a {validate_processing_module} result")
                
        moonshot_api.api_delete_result(result_id)
