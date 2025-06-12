import cmd2
from moonshot.api import transform_inspect_to_moonshot
import os
from rich.console import Console
from pathlib import Path
from moonshot.src.configs.env_variables import EnvironmentVars


console = Console()

def convert_inspect_result(args) -> None:
    try:
        file_path = args.input_file
        file_name = Path(file_path).stem + "_moonshot.json"

        default_dir = Path(EnvironmentVars.RESULTS[0] or EnvironmentVars.RESULTS[1])  # use env or fallback
        output_path = args.output_file or str(default_dir / file_name)

        if not os.path.exists(file_path):
            console.print(f"[red]Error: File '{file_path}' not found.[/red]")
            return

        with open(file_path, "r", encoding="utf-8") as f:
            inspect_json_str = f.read()

        moonshot_json = transform_inspect_to_moonshot(inspect_json_str)

        if moonshot_json:
            os.makedirs(default_dir, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(moonshot_json)

            console.print(f"[blue]Successfully converted and saved to:[/blue] {output_path}")
        else:
            console.print("[red]Conversion failed. No output generated.[/red]")

    except Exception as e:
        console.print(f"[convert_inspect_result]: [red]{e}[/red]")

def convert_inspect_result_args(parser):
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to Inspect JSON file",
    )
    parser.add_argument(
        "-o",
        "--output_file",
        type=str,
        help="Optional path for output Moonshot JSON file",
        default=None,
    )
