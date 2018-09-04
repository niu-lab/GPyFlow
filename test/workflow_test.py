import os
from flow.workflow import run_workflow

if __name__ == "__main__":
    test_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "test-workflow")
    run_workflow(test_dir,
                 os.path.join(os.path.abspath(os.path.dirname(__file__)), "inputs.txt"))
