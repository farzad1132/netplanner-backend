"""
    This schema contains sharing schemas
"""

from pydantic import BaseModel


class ShareRecord(BaseModel):
    """
        This schema represents a share record
    """

    user_id: str
    username: str
