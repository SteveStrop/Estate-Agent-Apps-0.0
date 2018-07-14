from pathlib import Path

from PyGrab import rename_file

test_rename_file_case = Path('C:/Test Folder/test.jpg')


def test_rename_file_rename_0():
    p = rename_file(test_rename_file_case, 0, 0)
    assert p.name == test_rename_file_case.name


def test_rename_file_rename_1():
    p = rename_file(test_rename_file_case, 1, 0)
    assert p.name == '01' + test_rename_file_case.suffix


def test_rename_file_rename_2():
    p = rename_file(test_rename_file_case, 2, 0)
    assert p.name == '001' + test_rename_file_case.suffix


def test_rename_file_rename_3():
    p = rename_file(test_rename_file_case, 3, 0)
    assert p.name == '00' + test_rename_file_case.suffix


def test_rename_file_rename_4():
    p = rename_file(test_rename_file_case, 4, 0)
    assert p.name == '000' + test_rename_file_case.suffix
