from pydantic import BaseModel, Field
from datetime import datetime


class UserCreate(BaseModel):
    username: str = Field(min_length=3)
    email: str = Field(min_length=5)


class UserUpdate(BaseModel):
    username: str = Field(min_length=3)
    email: str = Field(min_length=5)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class AuctionCreate(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=5)
    category: str = Field(min_length=3)
    starting_price: float = Field(gt=0)
    owner_id: int


class AuctionUpdate(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=5)
    category: str = Field(min_length=3)
    starting_price: float = Field(gt=0)


class AuctionResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    starting_price: float
    current_highest_bid: float
    start_date: datetime
    end_date: datetime
    owner_id: int

    class Config:
        from_attributes = True


class BidCreate(BaseModel):
    user_id: int
    amount: float = Field(gt=0)


class BidResponse(BaseModel):
    id: int
    auction_id: int
    user_id: int
    amount: float
    created_at: datetime

    class Config:
        from_attributes = True