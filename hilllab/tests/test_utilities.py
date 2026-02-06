# Christopher Esther, Hill Lab, 11/6/2025
import pytest

# Test path selection
from ..utilities import print_dict_table

def test_print_dict_table(capsys):
    test_dict = {
        'key1': 'value',
        'key2': 42,
        'key3': [1, 2, 3, 4, 5],
        'key4': {
            'k': 1,
            'k2': 'v2',
            'k3': [1, 2, 3],
            'k4': {'k': 1, 'k2': 'v2'}
        }
    }

    print_dict_table(test_dict, title='test')

    captured = capsys.readouterr()
    assert 'key1' in captured.out
    assert 'value' in captured.out
    assert 'test' in captured.out
