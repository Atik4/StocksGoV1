from dao import stock_alert_dao


# TODO: Add alert for stock for a user ->
#  input : username, stock name/symbol and list of criteria

def update_stock_alert(stock_alert):
    symbol = stock_alert.symbol
    new_alert = stock_alert.alerts[0]
    existing_stock_alert = stock_alert_dao.get_alerts_for_symbol(symbol)
    alert_exists = False
    if existing_stock_alert is not None:
        existing_alert_list = existing_stock_alert.alerts
        for alert in existing_alert_list:
            if are_criteria_lists_equal(alert.criteria_list, new_alert.criteria_list):
                alert_exists = True
                alert.users.append(new_alert.users[0])
                break
        if not alert_exists:
            existing_alert_list.append(new_alert)

        stock_alert_dao.create_new_stock_alert(existing_stock_alert)
    else:
        stock_alert_dao.create_new_stock_alert(stock_alert)


def are_criteria_lists_equal(criteria_list1, criteria_list2):
    if len(criteria_list1) != len(criteria_list2):
        return False

    # Sort lists based on a consistent attribute or representation
    sorted_criteria1 = sorted(criteria_list1, key=lambda x: x.json())
    sorted_criteria2 = sorted(criteria_list2, key=lambda x: x.json())

    # Compare sorted lists element by element
    for crit1, crit2 in zip(sorted_criteria1, sorted_criteria2):
        if crit1 != crit2:
            return False

    return True
