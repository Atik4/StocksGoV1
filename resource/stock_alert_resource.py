import uvicorn
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List
from models.stock_alert import StockAlert
from service.alert_service import update_stock_alert

app = FastAPI()

@app.post("/add-stock-alert/", status_code=status.HTTP_201_CREATED)
async def add_stock_alert(stock_alert: StockAlert):
    # Process the stock_alert here, e.g., save to database or perform some logic
    print(f"Received stock alert for symbol: {stock_alert.symbol}")
    # Assuming a function that saves or processes the alert
    update_stock_alert(stock_alert)
    return {"message": "Stock alert added successfully!"}


if __name__ == "__main__":
    uvicorn.run("resource.stock_alert_resource:app", host="127.0.0.1", port=8000, reload=True)