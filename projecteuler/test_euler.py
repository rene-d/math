"""
unit test pour les solutions aux problèmes de Project Euler
"""

import pytest
import importlib.util
import subprocess
import glob
import hashlib

SOLUTIONS = {
    # solution_start
    1: 'c0b20f4665d0388d564f0b6ecf3edc9f9480cb15fff87198b95701d9f5fe1f7b',
    2: '1f5882e19314ac13acca52ad5503184b3cb1fd8dbeea82e0979d799af2361704',
    3: '5c09f0554518a413e58e6bc5964ba90655713483d0b2bbc94572ad6b0b4dda28',
    4: 'aa74f52b4c428d89606b411bc165eb81a6266821ecc9b4f30cdb70c5c930f4d9',
    5: '1ba90ab11bfb2d2400545337212b0de2a5c7f399215175ade6396e91388912b1',
    6: '537942be3eb323c507623a6a73fa87bf5aeb97b7c7422993a82aa7c15f6d9cd6',
    7: 'ecbe74e25cfa4763dbc304ccac2ffb9912e9625cd9993a84bd0dd6d7dc0ca021',
    8: 'b9fb30b6553415e9150051ce5710a93d0f55b22557c0068d8e16619a388f145a',
    9: 'd912d9d473ef86f12da1fb2011c5c0c155bd3a0ebdb4bbd7ea275cecdcb63731',
    10: 'bed2d160e02f0540f19a64ca738aacb79cfcd08ba7e2421567b16cb6e7e3e90e',
    11: '9ded5bc849d33e477aa9c944138d34f0aacc485a372e84464e8a572712a5b7da',
    12: '3e7be445b6c19e6db58c2482005c1f78cb74011a4279249ca632011a9f1b61a2',
    13: '3cb265a96c5645a9ad11d47551f015c25f3f99792c951617656d84626fbc4868',
    14: '78a262dd40eba0f7195686ec7f3891a39437523456f8d16fa9065a34409eeac6',
    15: '7b8f812ca89e311e1b16b903de76fa7b0800a939b3028d9dc4d35f6fa4050281',
    16: 'a6f988d30328bd706c66f8ac0d92aac21dd732149cdd69cb31f459dca20c5abe',
    17: '1a455b216c6e916943acf3fa4c7e57a7a5cac66d97cc51befca810c223ef9c23',
    18: 'fde3f2e7127f6810eb4160bf7bb0563240d78c9d75a9a590b6d6244748a7f4ff',
    19: '284de502c9847342318c17d474733ef468fbdbe252cddf6e4b4be0676706d9d0',
    20: 'c86a2932e1c79343a3c16fb218b9944791aaeedd3e30c87d1c7f505c0e588f7c',
    21: 'e8c6ef4a1736a245b5682e0262c5c43862cfb233ca5e286be2f5bb4d8a974ecf',
    22: '85148c096c25e3ed3da55c7e9c89448018b0f5f53ad8d042129c33d9beac6736',
    23: '42e2552a2f589e021824339e2508629ffa00b3489ea467f47e77a1ea97e735c9',
    24: '4677b3d9daa3b30a9665e4558f826e04f7833dda886b8ef24f7176519a0db537',
    25: '7d398da8791745001b3d1c41030676d1c036687eb1ab32e0b5a1832e7579c073',
    26: 'fbe10beedf9d29cf53137ba38859ffd1dbe7642cedb7ef0a102a3ab109b47842',
    27: 'e4110e0852a2f70703f0081fc91c4a20f595919a038729cb37c564d68b875c6f',
    28: '261171a770d594f6a7fc76c1a839eda7f6dd4e9495e00e75048578fc86d8adf0',
    29: 'a207c35d8417aeed4c9e78bcf83f936cd8191c702893be62aa690ce16bc909ca',
    30: '46e68e4199ab0a663ab306651528b06756556c9f0d8b819095af45e036dfbe6b',
    31: '8de34b4ba97b184c7a2096b9266776175242b87d67bc8d77d7289be6f70cd105',
    32: '0d246750daa7f1b367a21f55da454ddc8f62e0a95d163062e9b9273320d5130f',
    33: 'ad57366865126e55649ecb23ae1d48887544976efea46a48eb5d85a6eeb4d306',
    34: '728b8d7d6d5d34cad9cbb7c3ea15f807ae57144594b1740b3c73b82314ccd1ed',
    35: '02d20bbd7e394ad5999a4cebabac9619732c343a4cac99470c03e23ba2bdc2bc',
    36: '9480c0160719234b57defc0681c0949a175ffb3ff4a3bf5e8163ac843f383f35',
    37: 'e9800abda89919edac504e90dac91f95e0778e3ba0f21a0bac4e77a84766eaaf',
    38: 'b2004522103364a6e842b9d042c0707d79af68dec7810078729d061fb7948912',
    39: 'fd0f7e53c5b02b688a57ee37f3d52065cb168a7b9fd5a3abd93d37e1559fbd30',
    40: 'd29d53701d3c859e29e1b90028eec1ca8e2f29439198b6e036c60951fb458aa1',
    41: 'bf05020e70de94e26dba112bb6fb7b0755db5ca88c7225e99187c5a08c8a0428',
    42: '79d6eaa2676189eb927f2e16a70091474078e2117c3fc607d35cdc6b591ef355',
    43: '6512f20c244844b6130204379601855098826afa1b55ff91c293c853ddf67db5',
    44: '97e2524fd3796e83b06c0f89fdcb16e4c544e76e9c0496f57ac84834869f4cc3',
    45: '8b0300d71656b9cf0716318be9453c99a13bb8644d227fd683d06124e6a28b35',
    46: '8485ee802cc628b8cbd82476133d11b57af87e00711516a703525a9af0193b12',
    47: 'c7274da71333bd93201fa1e05b1ed54e0074d83f259bd7148c70ddc43082bde1',
    48: '743d17cbff06ab458b99ecbb32e1d6bb9a7ff2ac804118f7743177dd969cfc61',
    49: '47c6094ff1ff6e37788def89190c8256619ef1511681c503fea02c171569d16e',
    50: '6ee74ef623df9fb69facd30b91ed78fe70370462bb267097f0dfeef9d9b057bb',
    51: 'd17cec28356b4f9a7f1ec0f20cca4c89e270aeb0e75d70d485b05bb1f28e9f6d',
    52: 'ebd72b510911af3e254a030cd891cb804e1902189eee7a0f6199472eb5e4dba2',
    53: '9705cc6128a60cc22581217b715750a6053b2ddda67cc3af7e14803b27cf0c1f',
    55: '9f484139a27415ae2e8612bf6c65a8101a18eb5e9b7809e74ca63a45a65f17f4',
    56: '3658d7fa3c43456f3c9c87db0490e872039516e6375336254560167cc3db2ea2',
    57: '620c9c332101a5bae955c66ae72268fbcd3972766179522c8deede6a249addb7',
    58: '196f327021627b6a48db9c6e0a3388d110909d4bb957eb3fbc90ff1ecbda42cb',
    59: '30f8673eb8490e9b2c07ee2f4de3fcad91b9fd8dd96511b60a9833d2fb884cd6',
    60: 'ad7c26db722221bfb1bf7e3c36b501bedf8be857b1cfa8664fccb074b54354f9',
    61: '94e4fb283c1abcccae4b8b28e39a294a323cdc9732c3d3ce1133c518d0a286f6',
    62: 'd25a595036aa8722157aca38f90084acb369b00df1070f49e203d5a3b7a0736d',
    63: '0e17daca5f3e175f448bacace3bc0da47d0655a74c8dd0dc497a3afbdad95f1f',
    64: '6d62aa4b52071e39f064a930d190b85ab327eb1a5045a8050ac538666ee765ca',
    65: '1c6c0bb2c7ecdc3be8e134f79b9de45155258c1f554ae7542dce48f5cc8d63f0',
    66: '316c0f93c7fe125865d85d6e7e7a31b79e9a46c414c45078b732080fa22ef2a3',
    67: '53f66b6783cb7552d83015df01b0d5229569fce1dd7d1856335c7244b9a3ded6',
    70: '08c6a7c8c06a01d2b17993ada398084b0707652bcfbd580f9173bcddf120ac2c',
    76: '81c54809c3bdfc23f844fde21ae645525817b6e1bee1525270f49282888a5546',
    80: '58bfe3a44f8ae452aaa6ef6267bafc3e841cfe7f9672bdfeb841d2e3a62c1587',
    81: '04bad90d08bdf11010267ec9d1c9bbb49a813194dace245868ea8140aec9a1f7',
    82: '52c42c55daea3131d5357498b8a0ddcf99d1babd16f6ccaee67cb3d0a665b772',
    92: '538cd20a275b610698691d714b2adf4e4c321915def05667f4d25d97413ec076',
    97: 'f0e2911e303617c9648692ee8056beeb045d89e469315716abed47cd94a3cd56',
    104: '87dfcf5471e77980d098ff445701dbada0f6f7bac2fa5e43fa7685ec435040e1',
    601: '571c5ade4cd89b460b7d2568a44d1efb05e2927ec840d8ecf149dc9e0ff09734',
    607: '2d9b6a1b4810a39471e5dae85eadf595fc108097eeda746c8925a7be057464de',
    613: 'afe8c7002c5e15859be829b4b69f0da00c1298971d5afa469b050016fc021978',
    621: '458ca388a6b74c57ae13d1233984d5b66abb1f18dbfa12aa14ba868a9b5a708d',
    # solution_end
}


def is_solution(output, numero):
    result = output.split('\n', 1)[0]
    return hashlib.sha256(result.encode()).hexdigest() == SOLUTIONS[numero]


def test_c(numero_c):
    """
    lance la résolution d'un problème compilé et teste la sortie
    """

    numero_c = int(numero_c)
    if not pytest.native_tests_available:
        pytest.skip("native tests are unavailable")
    if numero_c not in SOLUTIONS:
        pytest.fail("solution {} is not known".format(numero_c))
    res = subprocess.run("build/p%03d" % numero_c, stdout=subprocess.PIPE)
    assert res.returncode == 0
    assert is_solution(res.stdout.decode("utf-8"), numero_c)


def test_py(numero_py, capsys):
    """
    lance un test Python et teste la sortie
    """

    numero_py = int(numero_py)
    if numero_py not in SOLUTIONS:
        pytest.fail("solution {} is not known".format(numero_py))

    if numero_py in [60]:
        pytest.skip("test {} is known for being too long".format(numero_py))

    spec = importlib.util.find_spec("p%03d" % (numero_py))
    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)
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
