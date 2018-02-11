"""
test des programmes géométrie
"""


def test_pentagone1(mocker, capsys):
    # pi = mocker.patch("math.pi")
    # pi.return_value = 3
    # sin = mocker.patch("math.sin")
    # sin.return_value = 1

    __builtins__['input'] = lambda x: "3"

    import pentagone1       # noqa

    D = 2 * 3 * 0.5877852522924731

    captured = capsys.readouterr()
    assert captured.out.endswith("Côté du pentagone :  {}\n".format(D))
