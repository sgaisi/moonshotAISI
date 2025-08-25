import asyncio
import uuid
from typing import Any

from dependency_injector.wiring import inject

from moonshot.src.runners.runner import Runner

from ..schemas.agentic_runner_dto import AgenticRunnerDTO
from ..services.base_service import BaseService
from ..services.benchmark_test_state import BenchmarkTestState
from ..services.runner_service import RunnerService
from ..status_updater.interface.benchmark_progress_callback import (
    InterfaceBenchmarkProgressCallback,
)
from ..types.types import AgenticCollectionType, TestRunProgress


class AgenticTestManager(BaseService):
    @inject
    def __init__(
        self,
        benchmark_test_state: BenchmarkTestState,
        progress_status_updater: InterfaceBenchmarkProgressCallback,
        runner_service: RunnerService,
    ) -> None:
        self.benchmark_test_state = benchmark_test_state
        self.progress_status_updater = progress_status_updater
        self.runner_service = runner_service
        super().__init__()

    def generate_unique_task_id(self) -> str:
        unique_id = str(uuid.uuid4())
        return f"agentic_task_{unique_id}"

    def add_task(
        self, executor_id: str, task: asyncio.Task[Any], moonshot_runner: Runner
    ) -> None:
        self.benchmark_test_state.add_task(executor_id, task, moonshot_runner)

    def remove_task(self, executor_id: str) -> None:
        self.benchmark_test_state.remove_task(executor_id)

    async def cancel_task(self, executor_id: str) -> None:
        await self.benchmark_test_state.cancel_task(executor_id)

    def update_progress_status(self, updates: TestRunProgress):
        self.benchmark_test_state.update_progress_status(updates)

    def on_task_completed(self, task: asyncio.Task[Any]) -> None:
        self.logger.debug(f"Agentic task {task.get_name()} has completed")

    async def run_test(
        self,
        agentic_input_data: AgenticRunnerDTO,
        agentic_type: AgenticCollectionType,
        moonshot_runner: Runner,
    ) -> None:
        try:
            if agentic_type == AgenticCollectionType.COOKBOOK:
                async_run = moonshot_runner.run_cookbooks(
                    cookbooks=agentic_input_data.inputs,
                    prompt_selection_percentage=agentic_input_data.prompt_selection_percentage,
                    random_seed=agentic_input_data.random_seed,
                    system_prompt=agentic_input_data.system_prompt,
                    runner_processing_module=agentic_input_data.runner_processing_module,
                    result_processing_module="agentic-result",  # Use agentic result processor
                )
            else:
                async_run = moonshot_runner.run_recipes(
                    recipes=agentic_input_data.inputs,
                    prompt_selection_percentage=agentic_input_data.prompt_selection_percentage,
                    random_seed=agentic_input_data.random_seed,
                    system_prompt=agentic_input_data.system_prompt,
                    runner_processing_module=agentic_input_data.runner_processing_module,
                    result_processing_module="agentic-result",  # Use agentic result processor
                )
        except Exception as e:
            self.logger.error(f"Failed to execute agentic test - {e}")
            raise Exception(f"Unexpected error in agentic core library - {e}")

        await async_run
        await async_run.close()

    async def schedule_test_task(
        self, input_data: AgenticRunnerDTO, agentic_type: AgenticCollectionType
    ) -> str:
        task_id = self.generate_unique_task_id()
        runner = self.runner_service.create_runner(
            input_data.run_name,
            input_data.endpoints,
            input_data.description,
            self.progress_status_updater.on_progress_update,
        )
        agentic_coroutine = self.run_test(input_data, agentic_type, runner)

        task = asyncio.create_task(agentic_coroutine, name=task_id)

        def on_executor_completion(task: asyncio.Task[Any]):
            if task.exception():
                self.logger.error(
                    f"Agentic executor {task.get_name()} has failed - {task.exception()}"
                )
            else:
                self.logger.debug(f"Agentic executor {task.get_name()} has completed")

        task.add_done_callback(on_executor_completion)

        self.add_task(runner.id, task, runner)
        return runner.id
