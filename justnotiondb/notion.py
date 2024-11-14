
import csv
import json
from justnotiondb.processors import processors
import requests
from typing import Self

class NotionClient:
    """
    A class representing a Notion API connection
    """
    url = 'https://api.notion.com/v1'
    def __init__(self: Self, secret: str) -> None:
        """
        Initializes a NotionAPI object with a secret, and sets up the
        headers for all requests. Also checks the API connection and raises
        an exception if the connection is invalid.

        Parameters
        ----------
        secret : str
            The secret for the Notion API.
        """
        self.__headers = {
            'Authorization': f'Bearer {secret}',
            'Notion-Version': '2022-06-28',
            'Content-Type': "application/json"
        }
        self.__error: None | str = None

    @property
    def headers(self: Self) -> dict:
        return self.__headers

    @property
    def error(self: Self) -> str | None:
        """
        The error message of the last failed request if any.
        
        Returns
        -------
        str | None
            The error message or None if the last request was successful.
        """
        return self.__error
    
    @error.setter
    def error(self: Self, error: str) -> None:
        self.__error = error

    def check(self: Self) -> bool:
        """
        Checks the connection to the Notion API by attempting to retrieve user information.
        
        Returns
        -------
        bool
            If the request is successful, returns True. 
            If the request fails, returns False.
        """
        try:
            response = requests.get(
                url=f'{self.url}/users',
                headers=self.headers
            )
            response.raise_for_status()
            return True
        except Exception as e:
            self.error = str(e)
            return False


class DB:
    """
    A class representing a Notion database
    """
    def __init__(self: Self, client: NotionClient, id: str) -> None:
        """
        Initializes a DB object.

        Parameters
        ----------
        client : NotionClient
            The NotionClient object to use for requests.

        id : str
            The ID of the database to query.
        """
        self.client = client
        self.id = id

    def fetch(self: Self, filter: dict) -> dict:
        """
        Queries the database and fetches the results as a JSON object.

        Parameters
        ----------
        filter : dict
            A filter to be applied to the query.
            You can find more information here: https://developers.notion.com/reference/post-database-query-filter

        Returns
        -------
        dict
            A JSON object containing the query results.
        """
        url = f"{self.client.url}/databases/{self.id}/query"
        response = requests.post(
            url, 
            headers=self.client.headers,
            data=json.dumps(filter)
        )
        response.raise_for_status()
        return response.json()

    def get(self: Self, filter: dict={}) -> list[dict]:
        """
        Queries the database and fetches the results as a list of dictionaries.

        Parameters
        ----------
        filter : dict, optional
            A filter to be applied to the query. Defaults to an empty filter.

        Returns
        -------
        list[dict]
            A list of dictionaries, each representing a page in the database.
            Each dictionary contains the page's properties, processed according to their type.
        """
        db = self.fetch(filter=filter)
        results = db['results']
        content = []
        for result in results:
            properties = result['properties']
            content.append({
                key: processors[value['type']](value)
                for key, value in properties.items()
            })
        return content

    @classmethod
    def write_csv(cls, content: list[dict], path: str, **kwargs) -> None:
        """
        Writes a list of dictionaries to a CSV file.

        Parameters
        ----------
        content : list[dict]
            A list of dictionaries, each representing a row in the CSV file
        path : str
            The path to the CSV file.
        **kwargs
            Additional keyword arguments to be passed to the CSV writer
        """
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=content[0].keys(), **kwargs)
            writer.writeheader()
            writer.writerows(content)

    @classmethod
    def write_json(cls, content: list[dict], path: str) -> None:
        """
        Writes a list of dictionaries to a JSON file.

        Parameters
        ----------
        content : list[dict]
            A list of dictionaries, each representing a row in the JSON file
        path : str
            The path to the JSON file
        """
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=4, ensure_ascii=False)
