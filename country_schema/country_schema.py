from pydantic import BaseModel, Field,  ConfigDict






  

class Country(BaseModel):
    country_name: str
    # allows pydantic to read data from sqlalchemy models and convert them to pydantic models
    model_config = ConfigDict(from_attributes=True)

class CountryCreate(Country):
    pass


class CountryRead(Country):
    country_id: int
    country_name: str



class CountrySubscriptionsRead(BaseModel):

    subscriptions: dict
