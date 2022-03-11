"""GraphQL related filter plugins."""


def build_graphql_filter_string(filter: dict) -> str:
    """Takes a dictionary and builds a graphql filter

    Args:
        filter (dict): Key/Value pairs to build filter from

    Returns:
        str: Proper graphQL filter
    """
    base_filter = "({0})"
    loop_filters = []
    for key, value in filter.items():
        temp_string = f"{key}: "
        value_string = f"{value}"

        # GraphQL variables do not need quotes
        if isinstance(value, str) and not key.startswith("$"):
            value_string = "'" + value_string + "'"

        loop_filters.append(temp_string + value_string)

    return base_filter.format(", ".join(loop_filters))


def convert_to_graphql_string(query: dict, start=0) -> str:
    """Provide a dictionary to convert to a graphQL string.

    Args:
        query (dict): A dictionary mapping to the graphQL call to be made.

    Returns:
        str: GraphQL query string
    """
    graphql_string = f""""""
    for k, v in query.items():
        loop_string = "{}".format(" " * (start * 2))
        loop_filter = None
        if not v:
            loop_string += f"{k}\n"
        elif isinstance(v, dict):
            if v.get("filters"):
                loop_filter = build_graphql_filter_string(v.pop("filters"))
            # Increment start for recursion
            start += 1
            loop_string += "{0} {1}\n".format(k, loop_filter + " {" if loop_filter else " {")
            loop_string += convert_to_graphql_string(v, start)
            # Decrement start to continue at the same level we were at prior to recursion
            start -= 1
            loop_string += "{0}{1}\n".format(" " * (start * 2), "}")
        else:
            loop_string += '{0} {1}\n'.format(k, "{")
            # We want to keep the doubling spaces, but add 2 more
            loop_string += "{0}".format(" " * (start * 2 + 2))
            loop_string += f"{v}\n"
            loop_string += "{0}{1}\n".format(" " * (start * 2), "}")
            # loop_string += "}\n"
        graphql_string += loop_string

    return graphql_string.replace("'", '"')


class FilterModule:
    """Return graphQL filters."""

    def filters(self):
        """Map filter functions to filter names."""
        return {
            "graphql_string": convert_to_graphql_string,
        }
