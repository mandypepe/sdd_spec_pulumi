"""Entry wrapper so Pulumi will execute `main.py` when running in this directory.

Pulumi's Python runtime will look for a runnable module; executing main.py
explicitly with runpy makes `pulumi up` behave the same as running
`python main.py` in an IDE.
"""
import runpy

# Execute main.py as a script so top-level Pulumi exports and resource
# definitions are evaluated when Pulumi runs the program.
runpy.run_path("main.py", run_name="__main__")

