"""
Download course updates and prepare notebook copies
"""

from pathlib import Path
import subprocess
import sys

repository_directory = Path(__file__).resolve().parent
preparation_script    = repository_directory / "scripts" / "prepare_work.py"

print("Checking the course repository...")

try:
    status = subprocess.run(["git", "-C", str(repository_directory), "status", "--porcelain", "--untracked-files=no"], capture_output = True, text = True)
except FileNotFoundError:
    raise SystemExit("Git is not installed or is not available from this terminal.")

if status.returncode != 0:
    message = status.stderr.strip() or "Git could not read the course repository."
    raise SystemExit(message)

if status.stdout.strip():
    print()
    print("The update was stopped because a clean course file has been changed:")
    print(status.stdout.rstrip())
    print()
    print("Your notebook work should be in student_work, not in notebooks.")
    print("Move any important work to student_work and ask for help before trying the update again.")
    raise SystemExit(1)

print("Downloading the latest course material...")

update = subprocess.run(["git", "-C", str(repository_directory), "pull", "--ff-only"])

if update.returncode != 0:
    raise SystemExit("The course update failed. Your existing work was not changed.")

print()
print("Preparing editable notebook copies...")

preparation = subprocess.run([sys.executable, str(preparation_script)], cwd = repository_directory)

raise SystemExit(preparation.returncode)
