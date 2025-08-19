from enum import Enum
from moonshot.src.utils.log import configure_logger

logger = configure_logger(__name__)

class RunnerType(Enum):
    BENCHMARK = "benchmark"
    REDTEAM = "redteam"
    AGENTIC = "agentic"

    # Helper function in case we need more complex handling in the future
    def to_module_name(self):
        return self.value

    @staticmethod
    def from_str(inp: str):
        try:
            runner_enum = RunnerType(inp)
        except Exception as e:
            logger.error(f"Unable to deserialize provided runner [{inp}] to a valid RunnerType.")
            raise KeyError("Invalid Runner string specified.")
        logger.debug(f"Deserialized RunnerType string {inp} into {runner_enum}")
        return runner_enum
    
    @staticmethod
    def get_values():
        return [e.value for e in RunnerType]