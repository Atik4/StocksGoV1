from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from couchbase.auth import PasswordAuthenticator
from models.stock_alert import StockAlert
from models.alert import Alert
from models.criteria.rsi_criteria import RSICriteria
from models.criteria.ema_criteria import EMACriteria
from models.operator import Operator
from models.user import User


cluster = Cluster('couchbase://localhost', ClusterOptions(
    PasswordAuthenticator('root', 'root1234')))
cb = cluster.bucket('stock_alerts')

collection = cb.default_collection()


def create_new_stock_alert(stock_alert):
    doc_id = stock_alert.symbol
    stock_alert_dict = stock_alert.dict()
    collection.upsert(doc_id, stock_alert_dict)
    print(f"Created new stock alert: {doc_id}")


def get_alerts_for_symbol(symbol):
    try:
        # Attempt to retrieve the document by its ID
        result = collection.get(symbol)
        stock_alert_dict = result.content_as[dict]
        stock_alert = StockAlert.parse_obj(stock_alert_dict)
        return stock_alert  # Correctly access the content as a dictionary
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# rsi_criteria = RSICriteria(period=14, threshold=70, operator=Operator(type="Above", lower_bound=70), timeframe='D')
# ema_criteria = EMACriteria(period=14, operator=Operator(type="Above", lower_bound=70), timeframe='D')
# user = User(name='Atik', mobile="871789288")
# alert = Alert(criteria_list=[rsi_criteria, ema_criteria], users=[user])
# print(alert.criteria_list)
# print(rsi_criteria.dict())
# print(alert.dict())
#
# stock_alert = StockAlert(symbol="RELIANCE", alerts=[alert])
# create_new_stock_alert(stock_alert)

# print(get_alerts_for_symbol("HDFC"))