"""Copy course notebooks, tools, and data to the local student workspace."""

from pathlib import Path
import importlib.util
import shutil
import subprocess
import sys


repository_directory = Path(__file__).resolve().parent.parent
source_directory     = repository_directory / "notebooks"
tools_directory      = source_directory / "course_tools"
data_directory       = repository_directory / "data"
work_directory       = repository_directory / "student_work"

course_packages = [
    ("dipole",  "git+https://github.com/klaundal/dipole.git"),
    ("polplot", "git+https://github.com/klaundal/polplot.git"),
]

print("Checking course Python packages...")

for module_name, package_location in course_packages:
    if importlib.util.find_spec(module_name) is not None:
        print(f"  {module_name} is already installed.")
        continue

    print(f"  Installing {module_name}...")
    installation = subprocess.run([sys.executable, "-m", "pip", "install", package_location])

    if installation.returncode != 0:
        raise SystemExit(f"The installation of {module_name} failed. The course files were updated, but this Python environment is not ready.")

print()

if not source_directory.is_dir():
    raise SystemExit(f"The notebook directory does not exist: {source_directory}")

source_notebooks = sorted(
    path for path in source_directory.rglob("*.ipynb")
    if ".ipynb_checkpoints" not in path.parts
)
source_tools = sorted(tools_directory.rglob("*.py"))
source_data  = sorted(
    path for path in data_directory.rglob("*")
    if path.is_file() and path.name != ".DS_Store"
)

if not source_notebooks:
    raise SystemExit(f"No notebooks were found in: {source_directory}")

work_directory.mkdir(parents=True, exist_ok=True)

copied_notebooks   = []
existing_notebooks = []
updated_tools      = []
updated_data       = []

for source_notebook in source_notebooks:
    relative_path        = source_notebook.relative_to(source_directory)
    destination_notebook = work_directory / relative_path

    if destination_notebook.exists():
        existing_notebooks.append(relative_path)
        continue

    destination_notebook.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_notebook, destination_notebook)
    copied_notebooks.append(relative_path)

for source_tool in source_tools:
    relative_path    = source_tool.relative_to(source_directory)
    destination_tool = work_directory / relative_path

    destination_tool.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_tool, destination_tool)
    updated_tools.append(relative_path)

for source_data_file in source_data:
    relative_path         = source_data_file.relative_to(data_directory)
    destination_data_file = work_directory / "data" / relative_path

    destination_data_file.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_data_file, destination_data_file)
    updated_data.append(relative_path)

if copied_notebooks:
    print("Copied new notebooks to student_work:")
    for notebook in copied_notebooks:
        print(f"  {notebook}")
else:
    print("No new notebooks needed to be copied.")

if existing_notebooks:
    print(f"Kept {len(existing_notebooks)} existing notebook(s) unchanged.")

if updated_tools:
    print("Updated course tools:")
    for tool in updated_tools:
        print(f"  {tool}")

if updated_data:
    print("Updated course data:")
    for data_file in updated_data:
        print(f"  data/{data_file}")

print()
print("Work only in student_work, and remember to back up that directory.")
