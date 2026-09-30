from pydantic import BaseModel,HttpUrl

class UrlCreate(BaseModel):
    original_url:HttpUrl


class URLResponse(BaseModel):
    original_url: str
    short_code: str

    model_config = {
        "from_attributes": True
    }