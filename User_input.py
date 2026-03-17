from pydantic import BaseModel, Field, computed_field
from typing import Annotated
from datetime import datetime
from geopy.geocoders import Nominatim
import pickle

with open('schema/kmeans.pkl','rb') as f:
    helper_model = pickle.load(f)

geolocator = Nominatim(user_agent="app")

def get_cluster(place):
    location = geolocator.geocode(place)
    if location is None:
        return None
    lat = location.latitude
    lon = location.longitude
    cluster = helper_model.predict([[lat, lon]])
    return cluster[0]

class UserInput(BaseModel):

    year: Annotated[int, Field(..., description="Enter year")]
    month: Annotated[int, Field(..., description="Enter month (1-12)")]
    day: Annotated[int, Field(..., description="Enter day (1-31)")]
    hour: Annotated[int,Field(...,description="Enter hour in 0 to 23")]
    location: Annotated[str, Field(..., description="Enter pickup location")]

    @computed_field
    @property
    def date(self) -> datetime:
        return datetime(self.year, self.month, self.day)

    @computed_field
    @property
    def day_of_week(self) -> int:
        return self.date.weekday()

    @computed_field
    @property
    def is_weekend(self) -> int:
        return 1 if self.day_of_week >= 5 else 0
    
    @computed_field
    @property
    def cluster(self) -> int:
        clusterid = get_cluster(self.location)
        if clusterid is None:
            raise ValueError("Invalid location")
        return clusterid
