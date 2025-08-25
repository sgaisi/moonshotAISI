from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from ..container import Container
from ..schemas.agentic_runner_dto import AgenticRunnerDTO
from ..services.agentic_result_service import AgenticResultService
from ..services.agentic_service import AgenticService
from ..services.benchmark_test_state import BenchmarkTestState
from ..services.utils.exceptions_handler import ServiceException
from ..types.types import AgenticCollectionType

router = APIRouter(tags=["Agentic"])


@router.post("/api/v1/agentic")
@inject
async def agentic_executor(
    type: AgenticCollectionType,
    data: AgenticRunnerDTO,
    agentic_service: AgenticService = Depends(
        Provide[Container.agentic_service]
    ),
) -> dict:
    """
    Execute an agentic test.

    Args:
        type (AgenticCollectionType): The type of agentic test to execute.
        data (AgenticRunnerDTO): The data required to execute the agentic test.
        agentic_service (AgenticService, optional): The service that will execute the agentic test.

    Returns:
        dict: A dictionary with the 'id' key containing the ID of the created execution task.

    Raises:
        HTTPException: If the provided type is invalid (status code 400) or if the service fails to create
        and execute the agentic test (status code 500).
    """
    try:
        if type is AgenticCollectionType.COOKBOOK:
            id = await agentic_service.execute_cookbook(data)
            return {"id": id}
        elif type is AgenticCollectionType.RECIPE:
            id = await agentic_service.execute_recipe(data)
            return {"id": id}
        else:
            raise HTTPException(status_code=400, detail="Invalid query parameter: type")
    except ServiceException as e:
        raise HTTPException(
            status_code=500, detail=f"Unable to create and execute agentic test: {e}"
        )


@router.get("/api/v1/agentic/status")
@inject
def get_agentic_progress(
    benchmark_state: BenchmarkTestState = Depends(
        Provide[Container.benchmark_test_state]
    ),
):
    """
    Retrieve the progress status of all agentic tests.

    Args:
        benchmark_state (BenchmarkTestState, optional): The state service that tracks agentic test progress.

    Returns:
        The progress status of all agentic tests.

    Raises:
        HTTPException: If there is an error retrieving the progress status, with a status code indicating the
        nature of the error (404 for file not found, 400 for validation error).
    """
    try:
        all_status = benchmark_state.get_all_progress_status()
        return all_status
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to retrieve agentic progress status: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to retrieve agentic progress status: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to retrieve agentic progress status: {e.msg}"
            )


@router.post("/api/v1/agentic/cancel/{runner_id}")
@inject
async def cancel_agentic_executor(
    runner_id: str,
    agentic_service: AgenticService = Depends(
        Provide[Container.agentic_service]
    ),
):
    """
    Cancel an agentic test execution task.

    Args:
        runner_id (str): The ID of the runner executing the agentic test.
        agentic_service (AgenticService): The service that will cancel the agentic test execution.

    Returns:
        None

    Raises:
        HTTPException: If the service is unable to cancel the agentic test, with a status code
        500 indicating an internal server error.
    """
    try:
        await agentic_service.cancel_executor(runner_id)
    except ServiceException as e:
        raise HTTPException(status_code=500, detail=f"Unable to cancel agentic test: {e}")


@router.get("/api/v1/agentic/results")
@inject
async def get_all_agentic_results(
    agentic_result_service: AgenticResultService = Depends(
        Provide[Container.agentic_result_service]
    ),
) -> list[dict]:
    """
    Retrieve all agentic results.

    This endpoint retrieves a list of all agentic results from the database. Each agentic result is
    represented as a dictionary containing its associated data.

    Args:
        agentic_result_service (AgenticResultService): The service responsible for fetching agentic results.

    Returns:
        list[dict]: A list of dictionaries, each representing a single agentic result.

    Raises:
        HTTPException: Raised if the results file cannot be found (404) or if an unspecified error occurs (500).
    """
    try:
        results = agentic_result_service.get_all_results()
        return results
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to retrieve agentic results: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to retrieve agentic results: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to retrieve agentic results: {e.msg}"
            )


@router.get("/api/v1/agentic/results/name")
@inject
async def get_all_agentic_results_name(
    agentic_result_service: AgenticResultService = Depends(
        Provide[Container.agentic_result_service]
    ),
):
    """
    Get all agentic result names from the database.

    This endpoint retrieves the names of all agentic results stored in the database.

    Args:
        agentic_result_service (AgenticResultService): The service responsible for fetching
        the names of the agentic results.

    Returns:
        A list of all agentic result names.

    Raises:
        HTTPException: An error occurred while trying to find the result names file (404),
                       a validation error occurred (400), or
                       an unspecified error occurred (500).
    """
    try:
        results = agentic_result_service.get_all_result_name()
        return results
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to retrieve agentic result name: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to retrieve agentic result name: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to retrieve agentic result name: {e.msg}"
            )


@router.get("/api/v1/agentic/results/{result_id}")
@inject
async def get_one_agentic_result(
    result_id: str,
    agentic_result_service: AgenticResultService = Depends(
        Provide[Container.agentic_result_service]
    ),
):
    """
    Retrieve a single agentic result by its ID.

    This endpoint fetches the details of a specific agentic result identified by the provided result_id.

    Args:
        result_id (str): The unique identifier of the agentic result to retrieve.
        agentic_result_service (AgenticResultService): The service responsible for fetching the agentic result.

    Returns:
        dict: A dictionary containing the details of the agentic result.

    Raises:
        HTTPException: An error occurred while trying to find the results file (404) or
                       an unspecified error occurred (500).
    """
    try:
        result = agentic_result_service.get_result_by_id(result_id)
        return result
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to retrieve agentic result: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to retrieve agentic result: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to retrieve agentic result: {e.msg}"
            )


@router.delete("/api/v1/agentic/results/{result_id}")
@inject
def delete_agentic_result(
    result_id: str,
    agentic_result_service: AgenticResultService = Depends(
        Provide[Container.agentic_result_service]
    ),
) -> dict[str, str] | tuple[dict[str, str], int]:
    """
    Delete an agentic result by its ID.

    This endpoint deletes a specific agentic result identified by the provided result_id.

    Args:
        result_id (str): The unique identifier of the agentic result to delete.
        agentic_result_service (AgenticResultService): The service responsible for deleting the agentic result.

    Returns:
        dict[str, str] | tuple[dict[str, str], int]: A message indicating successful deletion,
        or an HTTPException with an appropriate status code.

    Raises:
        HTTPException: An error occurred while trying to delete the result due to the result not being found (404),
                       a validation error occurred (400), or
                       an unspecified error occurred (500).
    """
    try:
        agentic_result_service.delete_result(result_id)
        return {"message": "Agentic result deleted successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to delete agentic result: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to delete agentic result: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to delete agentic result: {e.msg}"
            )
