"""
unit test pour la fonction raise_app()
"""
import raise_app


def test_raise_app(mocker):
    getpid = mocker.patch('os.getpid')
    sp_call = mocker.patch('subprocess.call', create=True)
    plat_sys = mocker.patch('platform.system')

    # sous macOS, on doit
    plat_sys.return_value = 'Darwin'
    raise_app.raise_app()
    assert getpid.call_count == 1
    assert sp_call.call_count == 1
    assert plat_sys.call_count == 1

    # sinon, on ne fait rien
    plat_sys.return_value = 'other'
    raise_app.raise_app()
    assert getpid.call_count == 1
    assert sp_call.call_count == 1
    assert plat_sys.call_count == 2
