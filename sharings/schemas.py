from pydantic import BaseModel

class ShareRecord(BaseModel):
    user_id: str
    username: str
