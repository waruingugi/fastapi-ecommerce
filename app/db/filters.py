from fastapi_sqlalchemy_filter import Filter
from sqlalchemy.sql.selectable import Select
from sqlalchemy.orm.query import Query
from typing import Union, Dict, Any
from copy import deepcopy


def _create_filtered_query(
    query: Query, search_filter: Union[Filter, Dict[str, Any]]
) -> Query | Select:
    """
    Joins models in query (if the filter is nested) and sorts the query
    """
    if type(search_filter) is dict:
        search_filter_class = Filter(**search_filter)

        # Assign model to filter
        model = query.column_descriptions[0]["entity"]
        search_filter_class.Constants.model = model
    else:
        search_filter_class: Filter = deepcopy(search_filter)

    search_filter_dict = search_filter_class.dict(
        exclude_none=True, exclude_unset=True  # Remove fields with None values
    )

    for key, value in search_filter_dict.items():
        if (type(value) is dict) and hasattr(search_filter_class, key):
            nested_filter = getattr(search_filter_class, key)
            # Get nested model...
            if isinstance(nested_filter, Filter):
                # Then join the model to the query
                nested_model = nested_filter.Constants.model
                query = query.join(nested_model, isouter=True)

    search_query = search_filter_class.filter(query)

    return search_filter_class.sort(search_query)
