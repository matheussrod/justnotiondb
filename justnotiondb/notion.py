
import csv
import json
from justnotiondb.processors import processors
import requests
from typing import Any, Optional, Self

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

    def fetch(
        self: Self, 
        filter: Optional[dict[str, Any]]=None,
        sort: Optional[list[dict[str, str]]]=None,
        pagination: bool = True
    ) -> list[dict]:
        """
        Queries the database and fetches the results as a JSON object.

        Parameters
        ----------
        filter : dict, optional
            A filter to be applied to the query. Default is None.
            You can find more information here: https://developers.notion.com/reference/post-database-query-filter

        sort : list, optional
            A list of sorting options to be applied to the query. Default is None.
            You can find more information here: https://developers.notion.com/reference/post-database-query-sort

        pagination : bool
            If `True`, when the database has more than 100 records, paging will be used to retrieve all records.
            If `False`, only the first 100 records will be retrieved.
        
        Returns
        -------
        list[dict]
            A list of dictionaries, each representing a page in the database.
        """
        url = f"{self.client.url}/databases/{self.id}/query"

        data: dict[str, Any] = {}
        if filter is not None:
            data['filter'] = filter
        if sort is not None:
            data['sorts'] = sort

        has_more = True
        raw_data = []
        while has_more:
            response = requests.post(
                url, 
                headers=self.client.headers,
                json=data
            )
            response.raise_for_status()
            response_json = response.json()

            has_more = response_json.get('has_more')
            data['start_cursor'] = response_json.get('next_cursor')
            raw_data.append(response_json)
            
            if not pagination:
                break
        return raw_data

    def get(
        self: Self, 
        filter: Optional[dict[str, Any]]=None,
        sort: Optional[list[dict[str, str]]]=None,
        pagination: bool = True
    ) -> list[dict]:
        """
        Queries the database and fetches the results as a list of dictionaries.

        Parameters
        ----------
        filter : dict, optional
            A filter to be applied to the query. Default is None.
            You can find more information here: https://developers.notion.com/reference/post-database-query-filter

        sort : list, optional
            A list of sorting options to be applied to the query. Default is None.
            You can find more information here: https://developers.notion.com/reference/post-database-query-sort

        pagination : bool
            If `True`, when the database has more than 100 records, paging will be used to retrieve all records.
            If `False`, only the first 100 records will be retrieved.

        Returns
        -------
        list[dict]
            A list of dictionaries, each representing a page in the database.
            Each dictionary contains the page's properties, processed according to their type.
            See the `processors` module for more information.
        """
        db = self.fetch(
            filter=filter,
            sort=sort,
            pagination=pagination
        )
        content = []
        for cur in db:
            results = cur['results']
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
