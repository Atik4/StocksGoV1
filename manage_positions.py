from fyers_api import fyersModel
from main import login, app_id

fyers = fyersModel.FyersModel(is_async=False, client_id=app_id, token=login(),
                              log_path="/Users/atik.agarwal/Projects/personal/trading/logs/")


def get_funds():
    try:
        response = fyers.funds()
        return response['fund_limit']
    except Exception as e:
        print(e)

def exit_position(id):
    data = {
        # "id": "NSE:NIFTY2390719600CE-INTRADAY"
        "id": id
    }
    response = fyers.exit_positions(data=data)
    # # # response = fyers.positions()
    print(response)


def exit_all_positions():
    print(fyers.positions())
    response = fyers.exit_positions(data={})
    print(response)


def get_current_positions():
    try:
        response = fyers.positions()
        return response
    except Exception as e:
        print(e)
    # print(response)


def get_position_details_for_symbol(symbol):
    all_positions = fyers.positions()["netPositions"]
    position_details = []
    for position in all_positions:
        if symbol in position["symbol"]:
            position_details.append(position)

    return position_details

positions = get_current_positions()
total_pl = 0
if positions is not None:
    current_positions = positions['netPositions']
    for position in positions['netPositions']:
        total_pl += position['pl']
    print(current_positions)
    print(f"total pl = {total_pl}")


# for position in current_positions:
#     # print(position)
#     if "NIFTY" in position["symbol"] and str(19600) in position["symbol"]:
#         print(position)

# exit_all_positions()

# print(get_funds())