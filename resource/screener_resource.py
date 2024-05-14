from fastapi import FastAPI
from models.screener_request import ScreenerRequest
from models.criteria_factory import CriteriaFactory
import uvicorn
from service import screener_service


app = FastAPI()

@app.post("/run-screener/")
async def run_screener(request: ScreenerRequest):
    # Convert request criteria to internal criterion instances
    criteria_list = [CriteriaFactory.create(crit.type, **crit.dict()) for crit in request.criteria]

    print(criteria_list)
    # Replace with the logic to apply these criteria
    # results = apply_criteria_logic(criteria_list)
    res = screener_service.run('D', criteria_list)
    return {"results": res}


if __name__ == "__main__":
    uvicorn.run("resource.screener_resource:app", host="127.0.0.1", port=8000, reload=True)