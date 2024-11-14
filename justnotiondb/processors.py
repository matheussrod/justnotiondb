
from typing import Callable

def process_date(property: dict) -> str | None:
    """
    Processes a date property from a Notion database entry.

    Parameters
    ----------
    property : dict
        A dictionary containing a 'date' field with
        'start' and optionally 'end' keys.

    Returns
    -------
    str
        A formatted string representing the date range if both
        start and end dates are present, otherwise just the start date.
    """
    value: dict = property['date']
    if value is None:
        return None
    start = value['start']
    end = value['end']
    result = f'{start} -> {end}' if end else start
    return result

def process_list(property: dict, field: str, subfield: str) -> str | None:
    value: list[dict] = property[field]
    results = [x[subfield] for x in value]
    if len(results):
        result = results if len(results) > 1 else results[0]
        if isinstance(result, list):
            return '||'.join(result)
        if isinstance(result, str):
            return result
        return None
    else:
        return None

def process_title(property: dict) -> str | None:
    """
    Processes a title property from a Notion database entry.

    Parameters
    ----------
    property : dict
        A dictionary containing a 'title' field, which is a list of text objects.

    Returns
    -------
    list[str]
        A list of plain text strings from the title field.
    """
    return process_list(property, 'title', 'plain_text')

def process_checkbox(property: dict) -> bool:
    """
    Processes a checkbox property from a Notion database entry.

    Parameters
    ----------
    property : dict
        A dictionary containing a 'checkbox' field with a boolean value.

    Returns
    -------
    bool
        The boolean value of the checkbox field.
    """
    return property['checkbox']

def process_rich_text(property: dict) -> str | None:
    """
    Processes a rich text property from a Notion database entry.

    Parameters
    ----------
    property : dict
        A dictionary containing a 'rich_text' field, which is a list of text objects.

    Returns
    -------
    list[str]
        A list of plain text strings from the rich text field.
    """
    return process_list(property, 'rich_text', 'plain_text')

def process_number(property: dict) -> int | None:
    """
    Processes a number property from a Notion database entry.

    Parameters
    ----------
    property : dict
        A dictionary containing a 'number' field with an integer value.

    Returns
    -------
    int
        The integer value of the number field.
    """
    return property['number']

def process_select(property: dict) -> str | None:
    """
    Processes a select property from a Notion database entry.

    Parameters
    ----------
    property : dict
        A dictionary containing a 'select' field with a dictionary value.

    Returns
    -------
    str
        The name of the selected option.
    """
    value: dict = property['select']
    if value is None:
        return None
    return value['name']

def process_multi_select(property: dict) -> str | None:
    """
    Processes a multi-select property from a Notion database entry.

    Parameters
    ----------
    property : dict
        A dictionary containing a 'multi_select' field, which is a list of option objects.

    Returns
    -------
    list[str]
        A list of names of the selected options.
    """
    return process_list(property, 'multi_select', 'name')

def process_status(property: dict) -> str | None:
    """
    Processes a status property from a Notion database entry.

    Parameters
    ----------
    property : dict
        A dictionary containing a 'status' field with a dictionary value.

    Returns
    -------
    str
        The name of the status.
    """
    value: dict = property['status']
    if value is None:
        return None
    return value['name']

def process_people(property: dict) -> str | None:
    """
    Processes a people property from a Notion database entry.

    Parameters
    ----------
    property : dict
        A dictionary containing a 'people' field, which is a list of people objects.

    Returns
    -------
    list[str]
        A list of names of the people.
    """
    return process_list(property, 'people', 'name')

def process_files(property: dict) -> str | None:
    """
    Processes a files property from a Notion database entry.

    Parameters
    ----------
    property : dict
        A dictionary containing a 'files' field, which is a list of file objects.

    Returns
    -------
    list[str]
        A list of URLs of the files.
    """
    return process_list(property, 'files', 'file')

def process_url(property: dict) -> str | None:
    """
    Processes a url property from a Notion database entry.

    Parameters
    ----------
    property : dict
        A dictionary containing a 'url' field with a string value.

    Returns
    -------
    str
        The string value of the url field.
    """
    return property['url']

def process_email(property: dict) -> str | None:
    """
    Processes an email property from a Notion database entry.

    Parameters
    ----------
    property : dict
        A dictionary containing a 'email' field with a string value.

    Returns
    -------
    str
        The string value of the email field.
    """
    return property['email']

def process_phone_number(property: dict) -> str | None:
    """
    Processes a phone number property from a Notion database entry.

    Parameters
    ----------
    property : dict
        A dictionary containing a 'phone_number' field with a string value.

    Returns
    -------
    str
        The string value of the phone number field.
    """
    return property['phone_number']

def process_formula(property: dict) -> str | None:
    """
    Processes a formula property from a Notion database entry.

    Parameters
    ----------
    property : dict
        A dictionary containing a 'formula' field with a dictionary value.

    Returns
    -------
    str
        The string value of the formula field.
    """
    value: dict = property['formula']
    result = value[value['type']]
    return result

def process_relation(property: dict) -> str | None:
    """
    Processes a relation property from a Notion database entry.

    Parameters
    ----------
    property : dict
        A dictionary containing a 'relation' field, which is a list of relation objects.

    Returns
    -------
    list[str]
        A list of IDs of the related pages.
    """
    return process_list(property, 'relation', 'id')

def process_rollup(property: dict) -> str | None:
    value: dict = property['rollup']
    value_type = value['type']
    if value_type == 'array':
        results = []
        for x in value[value_type]:
            results.append(str(processors[x['type']](x)))
        return '||'.join(results)
    else:
        return str(value[value_type])

def process_created_time(property: dict) -> str | None:
    """
    Processes a created time property from a Notion database entry.

    Parameters
    ----------
    property : dict
        A dictionary containing a 'created_time' field with a string value.

    Returns
    -------
    str
        The string value of the created time field.
    """
    return property['created_time']

def process_created_by(property: dict) -> str | None:
    """
    Processes a created by property from a Notion database entry.

    Parameters
    ----------
    property : dict
        A dictionary containing a 'created_by' field with a dictionary value.

    Returns
    -------
    str
        The string value of the created by field.
    """
    return property['created_by']['id']

def process_last_edited_time(property: dict) -> str | None:
    """
    Processes a last edited time property from a Notion database entry.

    Parameters
    ----------
    property : dict
        A dictionary containing a 'last_edited_time' field with a string value.

    Returns
    -------
    str
        The string value of the last edited time field.
    """
    return property['last_edited_time']

def process_last_edited_by(property: dict) -> str | None:
    """
    Processes a last edited by property from a Notion database entry.

    Parameters
    ----------
    property : dict
        A dictionary containing a 'last_edited_by' field with a dictionary value.

    Returns
    -------
    str
        The string value of the last edited by field.
    """
    return property['last_edited_by']['name']

def process_button(property: dict) -> None:
    """
    Processes a button property from a Notion database entry.

    Parameters
    ----------
    property : dict
        A dictionary containing a 'button' field with a dictionary value.

    Returns
    -------
    None
        The button property has no value to process, so this function simply returns None.
    """
    return None

def process_unique_id(property: dict) -> str | None:
    """
    Processes a unique id property from a Notion database entry.

    Parameters
    ----------
    property : dict
        A dictionary containing a 'unique_id' field with a string value.

    Returns
    -------
    str
        The string value of the unique id field.
    """
    return property['unique_id']['number']

processors: dict[str, Callable] = {
    'date': process_date,
    'title': process_title,
    'checkbox': process_checkbox,
    'rich_text': process_rich_text,
    'number': process_number,
    'select': process_select,
    'multi_select': process_multi_select,
    'status': process_status,
    'people': process_people,
    'files': process_files,
    'url': process_url,
    'email': process_email,
    'phone_number': process_phone_number,
    'formula': process_formula,
    'relation': process_relation,
    'rollup': process_rollup,
    'button': process_button,
    'created_time': process_created_time,
    'created_by': process_created_by,
    'last_edited_time': process_last_edited_time,
    'last_edited_by': process_last_edited_by,
    'unique_id': process_unique_id
}
