from pydantic import BaseModel,Field

class preResponce(BaseModel):
    Predicted_demand :float = Field(...,description="Predicted demand value.")
    R2_Score :float = Field(...,description="R2 score of model")
    RMSE :float = Field(...,description="rmse of model")