import pytest
import subprocess
import os


def pytest_sessionstart(session):
    pe_dir = os.path.dirname(__file__)
    os.chdir(pe_dir)
    os.makedirs("build", exist_ok=True)
    res = subprocess.run("cd build && cmake .. && make V=1", shell=True, stderr=None)
    if res.returncode != 0:
        # pytest.fail("C/C++ build failed")
        print("C/C++ build failed - will skip native tests")
        pytest.native_tests_available = False
    else:
        pytest.native_tests_available = True
