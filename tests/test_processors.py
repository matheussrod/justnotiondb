
from justnotiondb.processors import process_date, process_list

def test_date_with_start_and_end():
    property = {'date': {'start': '1900-01-01', 'end': '1900-01-01'}}
    expected_result = '1900-01-01 -> 1900-01-01'
    assert process_date(property) == expected_result

def test_date_with_only_start():
    property = {'date': {'start': '1900-01-01', 'end': None}}
    expected_result = '1900-01-01'
    assert process_date(property) == expected_result

def test_date_none():
    property = {'date': None}
    expected_result = None
    assert process_date(property) == expected_result

def test_process_list_single_item():
    property = {'title': [{'plain_text': 'Item 1'}]}
    assert process_list(property, 'title', 'plain_text') == 'Item 1'

def test_process_list_multiple_items():
    property = {'title': [{'plain_text': 'Item 1'}, {'plain_text': 'Item 2'}]}
    assert process_list(property, 'title', 'plain_text') == 'Item 1||Item 2'
