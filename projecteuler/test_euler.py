"""
unit test pour les solutions aux problèmes de Project Euler
"""

import pytest
import importlib.util
import subprocess
import glob
import hashlib
import solutions_euler            # noqa


SLOW_TESTS = [60, 70, 84, 357]


def is_solution(output, numero):
    result = output.split('\n', 1)[0]
    return hashlib.sha256(result.encode()).hexdigest() == pytest.SOLUTIONS[numero]


def check_test(numero):
    if numero not in pytest.SOLUTIONS:
        pytest.skip("solution {} is not known".format(numero_py))
    if numero in SLOW_TESTS:
        pytest.skip("test {} is known for being too long".format(numero_py))


def test_c(numero_c):
    """
    lance la résolution d'un problème compilé et teste la sortie
    """

    if not pytest.native_tests_available:
        pytest.skip("native tests are unavailable")
    numero_c = int(numero_c)
    check_test(numero_c)
    res = subprocess.run("build/p%03d" % numero_c, stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert is_solution(res.stdout.decode("utf-8"), numero_c)


def test_py(numero_py, capsys):
    """
    lance un test Python et teste la sortie
    """

    numero_py = int(numero_py)
    check_test(numero_py)

    spec = importlib.util.find_spec("p%03d" % (numero_py))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    out = capsys.readouterr().out

    # certains programmes sont écrits avec main() ou pNNN()
    if out == "":
        main = getattr(module, "main")
        if main is not None:
            main()
        else:
            f = getattr(module, "p%03d" % (numero_py))
            if f is not None:
                f()
        out = capsys.readouterr().out

    assert is_solution(out, numero_py)


@pytest.fixture
def numero_py(request):
    return request.param


@pytest.fixture
def numero_c(request):
    return request.param


def pytest_generate_tests(metafunc):
    """
    génère les tests Python et C à partir de la présence des fichiers pNNN.py et pNNN.c[pp]
    """
    if 'numero_py' in metafunc.fixturenames:
        list_py = [i[1:4] for i in sorted(glob.iglob("p[0-9][0-9][0-9].py"))]
        metafunc.parametrize("numero_py", list_py, indirect=True)

    if 'numero_c' in metafunc.fixturenames:
        list_c = [i[1:4] for i in sorted(glob.iglob("p[0-9][0-9][0-9].c*"))]
        metafunc.parametrize("numero_c", list_c, indirect=True)
