from dependency_injector.wiring import inject

from ..schemas.agentic_runner_dto import AgenticRunnerDTO
from ..services.base_service import BaseService
from ..services.agentic_test_manager import AgenticTestManager
from ..services.utils.exceptions_handler import exception_handler
from ..types.types import AgenticCollectionType


class AgenticService(BaseService):
    @inject
    def __init__(self, agentic_test_manager: AgenticTestManager) -> None:
        self.agentic_test_manager = agentic_test_manager

    @exception_handler
    async def execute_cookbook(self, cookbook_executor_data: AgenticRunnerDTO) -> str:
        id = await self.agentic_test_manager.schedule_test_task(
            cookbook_executor_data, AgenticCollectionType.COOKBOOK
        )
        return id

    @exception_handler
    async def execute_recipe(self, recipe_executor_data: AgenticRunnerDTO):
        id = await self.agentic_test_manager.schedule_test_task(
            recipe_executor_data, AgenticCollectionType.RECIPE
        )
        return id

    @exception_handler
    async def cancel_executor(self, executor_id: str) -> None:
        await self.agentic_test_manager.cancel_task(executor_id)
