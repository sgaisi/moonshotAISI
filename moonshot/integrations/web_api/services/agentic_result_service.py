from .... import api as moonshot_api
from ..services.base_service import BaseService
from ..services.utils.exceptions_handler import exception_handler
from ..types.types import BenchmarkResult


class AgenticResultService(BaseService):
    def _is_agentic_result(self, result: dict) -> bool:
        """Check if a result is an agentic result based on its metadata."""
        metadata = result.get("metadata", {})
        return metadata.get("result_processing_module") == "agentic-result"

    @exception_handler
    def get_all_results(self) -> list[BenchmarkResult]:
        all_results = moonshot_api.api_get_all_result()
        # Filter only agentic results
        agentic_results = [result for result in all_results if self._is_agentic_result(result)]
        return [BenchmarkResult(**result) for result in agentic_results]

    @exception_handler
    def get_all_result_name(self) -> list[str] | None:
        all_results = moonshot_api.api_get_all_result()
        # Filter only agentic results and extract their IDs
        agentic_result_ids = []
        for result in all_results:
            if self._is_agentic_result(result):
                result_id = result.get("metadata", {}).get("id")
                if result_id:
                    agentic_result_ids.append(result_id)
        return agentic_result_ids

    @exception_handler
    def get_result_by_id(self, result_id: str) -> BenchmarkResult:
        result = moonshot_api.api_read_result(result_id)
        # Verify this is actually an agentic result
        if not self._is_agentic_result(result):
            raise ValueError(f"Result {result_id} is not an agentic result")
        return BenchmarkResult(**result)

    @exception_handler
    def delete_result(self, result_id: str) -> None:
        result = moonshot_api.api_read_result(result_id)
        # Verify this is actually an agentic result before deletion
        if not self._is_agentic_result(result):
            raise ValueError(f"Result {result_id} is not an agentic result")
        moonshot_api.api_delete_result(result_id)
