
import json
from justnotiondb.notion import NotionClient, DB
import pytest
from requests_mock import Mocker

@pytest.fixture
def db_results():
    return {
        "results": [{
            'properties': {
                'date': {'date': {'start': '2022-01-01', 'end': None, 'time_zone': None}, 'id': '1', 'type': 'date'},
                'checkbox': {'checkbox': True, 'id': '2', 'type': 'checkbox'},
            }
        }]
    }

def test_notion_client_check_success():
    with Mocker() as mock:
        mock.get('https://api.notion.com/v1/users', status_code=200)
        assert NotionClient(secret='fake_secret').check() is True

def test_notion_client_check_failure():
    assert NotionClient(secret='fake_secret').check() is False

def test_notion_client_check_failure_error():
    client = NotionClient(secret='fake_secret')
    client.check()
    assert client.error is not None

def test_db_fetch(db_results):
    with Mocker() as mock1:
        mock1.get('https://api.notion.com/v1/users', status_code=200)
        client = NotionClient(secret='fake_secret')
        with Mocker() as mock2:
            mock2.post(
                'https://api.notion.com/v1/databases/fake_db_id/query',
                status_code=200,
                json=db_results
            )
            db = DB(client=client, id='fake_db_id')
            assert db.fetch() == [db_results]

def test_db_get(db_results):
    expected_result = [{
        'date': '2022-01-01',
        'checkbox': True
    }]
    with Mocker() as mock1:
        mock1.get('https://api.notion.com/v1/users', status_code=200)
        client = NotionClient(secret='fake_secret')
        with Mocker() as mock2:
            mock2.post(
                'https://api.notion.com/v1/databases/fake_db_id/query',
                status_code=200,
                json=db_results
            )
            db = DB(client=client, id='fake_db_id')
            assert db.get() == expected_result

def test_db_write_csv(tmp_path):
    content = [{'Name': 'Test Page', 'Status': 'In Progress'}]
    csv_path = tmp_path / "output.csv"
    DB.write_csv(content, path=str(csv_path))
    with open(csv_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        assert lines[0].strip() == 'Name,Status'
        assert lines[1].strip() == 'Test Page,In Progress'

def test_db_write_json(tmp_path):
    content = [{'Name': 'Test Page', 'Status': 'In Progress'}]
    json_path = tmp_path / "output.json"
    DB.write_json(content, path=str(json_path))
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert data == content
