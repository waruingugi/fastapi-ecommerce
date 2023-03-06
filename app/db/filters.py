from fastapi_sqlalchemy_filter import Filter
from sqlalchemy.sql.selectable import Select
from typing import Union, Dict, Any


def _create_filtered_query(query: Select, search_filter: Union[Filter, Dict[str, Any]]):
    """
    Joins models in query (if the filter is nested) and sorts the query
    """
    if type(search_filter) is dict:
        search_filter = Filter(**search_filter)

        # Assign model to filter
        model = query.column_descriptions[0]["entity"]
        search_filter.Constants.model = model

    search_filter_dict = search_filter.dict(
        exclude_none=True, exclude_unset=True  # Remove fields with None values
    )

    for key, value in search_filter_dict.items():
        if (type(value) is dict) and hasattr(search_filter, key):
            nested_filter = getattr(search_filter, key)
            # Get nested model...
            if isinstance(nested_filter, Filter):
                # Then join the model to the query
                nested_model = nested_filter.Constants.model
                query = query.join(nested_model, isouter=True)

    query = search_filter.filter(query)
    query = search_filter.sort(query)

    return query
