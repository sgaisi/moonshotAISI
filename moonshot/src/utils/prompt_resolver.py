"""
Utility module for resolving system prompts based on priority hierarchy.
"""

from typing import Optional

from moonshot.src.cookbooks.cookbook import Cookbook
from moonshot.src.datasets.dataset import Dataset
from moonshot.src.recipes.recipe import Recipe
from moonshot.src.utils.log import configure_logger

# Create a logger for this module
logger = configure_logger(__name__)


class PromptResolver:
    """
    Utility class for resolving system prompts using priority hierarchy:
    1. Dataset-level (highest priority)
    2. Recipe-level
    3. Cookbook-level
    4. CLI arguments
    5. Default values (lowest priority)
    """

    @staticmethod
    def resolve_system_prompt_for_recipe(
        recipe_id: str,
        dataset_id: str,
        cookbook_id: Optional[str] = None,
        cli_system_prompt: str = ""
    ) -> str:
        """
        Resolve system prompt for a specific recipe and dataset combination.

        Args:
            recipe_id (str): The ID of the recipe
            dataset_id (str): The ID of the dataset
            cookbook_id (Optional[str]): The ID of the cookbook (if applicable)
            cli_system_prompt (str): System prompt from CLI arguments

        Returns:
            str: The resolved system prompt
        """
        try:
            # Load the components
            dataset = Dataset.read(dataset_id)
            recipe = Recipe.read(recipe_id)
            cookbook = None
            if cookbook_id:
                cookbook = Cookbook.read(cookbook_id)

            # Resolve system prompt: Dataset > Recipe > Cookbook > CLI > Default("")
            system_prompt = (
                dataset.system_prompt or
                recipe.system_prompt or
                (cookbook.system_prompt if cookbook else "") or
                cli_system_prompt or
                ""
            )

            logger.debug(f"Resolved system prompt for recipe={recipe_id}, dataset={dataset_id}: "
                        f"system_prompt={'<set>' if system_prompt else '<empty>'}")

            return system_prompt

        except Exception as e:
            logger.error(f"Failed to resolve system prompt for recipe={recipe_id}, dataset={dataset_id}: {str(e)}")
            # Return defaults on error
            return cli_system_prompt or ""

    @staticmethod
    def resolve_system_prompt_for_cookbook(
        cookbook_id: str,
        recipe_id: str,
        dataset_id: str,
        cli_system_prompt: str = ""
    ) -> str:
        """
        Resolve system prompt for a cookbook-based execution.

        Args:
            cookbook_id (str): The ID of the cookbook
            recipe_id (str): The ID of the recipe
            dataset_id (str): The ID of the dataset
            cli_system_prompt (str): System prompt from CLI arguments

        Returns:
            str: The resolved system prompt
        """
        return PromptResolver.resolve_system_prompt_for_recipe(
            recipe_id=recipe_id,
            dataset_id=dataset_id,
            cookbook_id=cookbook_id,
            cli_system_prompt=cli_system_prompt
        )
