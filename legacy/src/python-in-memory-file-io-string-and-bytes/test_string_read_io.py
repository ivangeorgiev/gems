import io

def test_read_from_string():
    with io.StringIO("Line1\nLine2\n") as f:
        lines = f.readlines()
        assert lines == ['Line1\n', 'Line2\n']

def test_read_from_bytes():
    with io.BytesIO(b'some bytes here') as f:
        actual = f.read()
        assert b'some bytes here', actual


def test_write_to_string():
    with io.StringIO() as output:
        output.write('Little acucaracha\n')
        output.write('is hungry\n')
        result = output.getvalue()
    assert 'Little acucaracha\nis hungry\n' == result

