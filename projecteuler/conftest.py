import pytest
import subprocess
import os


def pytest_sessionstart(session):
    pe_dir = os.path.dirname(__file__)
    os.chdir(pe_dir)
    res = subprocess.run("mkdir -p build && cd build && cmake .. && make", shell=True)
    if res.returncode != 0:
        pytest.fail("C/C++ build failed")
