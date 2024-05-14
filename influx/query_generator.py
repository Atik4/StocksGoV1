def generate_influx_query(symbols, range_from, range_to, table_name):
    """
    Generate an InfluxDB SQL query for a list of symbols and a specified date range.

    :param symbols: List of symbol strings.
    :param range_from: Start date in "YYYY-MM-DD" format.
    :param range_to: End date in "YYYY-MM-DD" format.
    :return: A string containing the SQL query.
    """
    symbol_filters = " OR ".join([f'"symbol" = \'{symbol}\'' for symbol in symbols])
    query = (
        f"SELECT * FROM \"{table_name}\" "
        f"WHERE ({symbol_filters}) AND time >= '{range_from}T00:00:00Z' AND time <= '{range_to}T23:59:59Z' "
        f"ORDER BY \"symbol\", time ASC"
    )
    return query

# Example usage
# symbols = ['ITC', 'TCS', 'RELIANCE']
# range_from = '2024-01-10'
# range_to = '2024-02-29'
# query = generate_influx_query(symbols, range_from, range_to)
# print(query)
