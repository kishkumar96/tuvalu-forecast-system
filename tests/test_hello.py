pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py

tests/test_hello.py
def test_hello():
    assert 1 + 1 == 2