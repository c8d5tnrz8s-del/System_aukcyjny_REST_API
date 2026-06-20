from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from app.database import get_db
from app.models import User, Auction, Bid
from app.schemas import (
    UserCreate, UserUpdate, UserResponse,
    AuctionCreate, AuctionUpdate, AuctionResponse,
    BidCreate, BidResponse
)

router = APIRouter()


@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(username=user_data.username, email=user_data.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.username = user_data.username
    user.email = user_data.email
    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return None


@router.post("/auctions", response_model=AuctionResponse, status_code=201)
def create_auction(auction_data: AuctionCreate, db: Session = Depends(get_db)):
    owner = db.query(User).filter(User.id == auction_data.owner_id).first()
    if owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")

    auction = Auction(
        title=auction_data.title,
        description=auction_data.description,
        category=auction_data.category,
        starting_price=auction_data.starting_price,
        current_highest_bid=auction_data.starting_price,
        end_date=datetime.utcnow() + timedelta(days=7),
        owner_id=auction_data.owner_id
    )

    db.add(auction)
    db.commit()
    db.refresh(auction)
    return auction


@router.get("/auctions", response_model=list[AuctionResponse])
def get_auctions(
    category: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Auction)

    if category:
        query = query.filter(Auction.category == category)

    auctions = query.all()

    if status == "active":
        auctions = [a for a in auctions if datetime.utcnow() <= a.end_date]
    elif status == "ended":
        auctions = [a for a in auctions if datetime.utcnow() > a.end_date]
    elif status is not None:
        raise HTTPException(status_code=400, detail="Status must be active or ended")

    return auctions


@router.get("/auctions/{auction_id}", response_model=AuctionResponse)
def get_auction(auction_id: int, db: Session = Depends(get_db)):
    auction = db.query(Auction).filter(Auction.id == auction_id).first()
    if auction is None:
        raise HTTPException(status_code=404, detail="Auction not found")
    return auction


@router.put("/auctions/{auction_id}", response_model=AuctionResponse)
def update_auction(auction_id: int, auction_data: AuctionUpdate, db: Session = Depends(get_db)):
    auction = db.query(Auction).filter(Auction.id == auction_id).first()
    if auction is None:
        raise HTTPException(status_code=404, detail="Auction not found")

    auction.title = auction_data.title
    auction.description = auction_data.description
    auction.category = auction_data.category
    auction.starting_price = auction_data.starting_price

    db.commit()
    db.refresh(auction)
    return auction


@router.delete("/auctions/{auction_id}", status_code=204)
def delete_auction(auction_id: int, db: Session = Depends(get_db)):
    auction = db.query(Auction).filter(Auction.id == auction_id).first()
    if auction is None:
        raise HTTPException(status_code=404, detail="Auction not found")

    db.delete(auction)
    db.commit()
    return None


@router.post("/auctions/{auction_id}/bids", response_model=BidResponse, status_code=201)
def create_bid(auction_id: int, bid_data: BidCreate, db: Session = Depends(get_db)):
    auction = db.query(Auction).filter(Auction.id == auction_id).first()
    user = db.query(User).filter(User.id == bid_data.user_id).first()

    if auction is None:
        raise HTTPException(status_code=404, detail="Auction not found")
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if datetime.utcnow() > auction.end_date:
        raise HTTPException(status_code=400, detail="Auction has ended")
    if bid_data.amount <= auction.current_highest_bid:
        raise HTTPException(status_code=400, detail="Bid must be higher than current highest bid")

    bid = Bid(
        auction_id=auction_id,
        user_id=bid_data.user_id,
        amount=bid_data.amount
    )

    auction.current_highest_bid = bid_data.amount
    db.add(bid)
    db.commit()
    db.refresh(bid)
    return bid


@router.get("/auctions/{auction_id}/bids", response_model=list[BidResponse])
def get_bids_for_auction(auction_id: int, db: Session = Depends(get_db)):
    auction = db.query(Auction).filter(Auction.id == auction_id).first()
    if auction is None:
        raise HTTPException(status_code=404, detail="Auction not found")

    return db.query(Bid).filter(Bid.auction_id == auction_id).all()