from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database import get_db
from app.models import User, Auction, Bid

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def frontend_home(db: Session = Depends(get_db)):
    auctions = db.query(Auction).all()

    rows = ""

    for auction in auctions:
        rows += f"""
        <tr>
            <td>{auction.id}</td>
            <td>{auction.title}</td>
            <td>{auction.category}</td>
            <td>{auction.starting_price}</td>
            <td>{auction.current_highest_bid}</td>
            <td>{auction.end_date.strftime('%Y-%m-%d %H:%M')}</td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>System Aukcyjny</title>
        <style>
            body {{ font-family: Arial; margin: 40px; background: #f7f7f7; }}
            h1, h2 {{ color: #222; }}
            table {{ width: 100%; border-collapse: collapse; background: white; }}
            th, td {{ border: 1px solid #ccc; padding: 10px; text-align: left; }}
            input, textarea {{ width: 100%; padding: 8px; margin: 5px 0; }}
            button {{ padding: 10px 15px; background: #222; color: white; border: none; cursor: pointer; }}
            .box {{ background: white; padding: 20px; margin-bottom: 25px; border: 1px solid #ddd; }}
            a {{ color: #222; }}
        </style>
    </head>
    <body>
        <h1>System aukcji internetowych</h1>

        <p>
            <a href="/docs">Swagger / OpenAPI</a>
        </p>

        <div class="box">
            <h2>Dodaj użytkownika</h2>
            <form method="post" action="/frontend/users">
                <input name="username" placeholder="Nazwa użytkownika" required>
                <input name="email" placeholder="Email" required>
                <button type="submit">Dodaj użytkownika</button>
            </form>
        </div>

        <div class="box">
            <h2>Dodaj aukcję</h2>
            <form method="post" action="/frontend/auctions">
                <input name="title" placeholder="Nazwa przedmiotu" required>
                <textarea name="description" placeholder="Opis" required></textarea>
                <input name="category" placeholder="Kategoria" required>
                <input name="starting_price" type="number" step="0.01" placeholder="Cena wywoławcza" required>
                <input name="owner_id" type="number" placeholder="ID właściciela" required>
                <button type="submit">Dodaj aukcję</button>
            </form>
        </div>

        <div class="box">
            <h2>Złóż ofertę</h2>
            <form method="post" action="/frontend/bids">
                <input name="auction_id" type="number" placeholder="ID aukcji" required>
                <input name="user_id" type="number" placeholder="ID użytkownika" required>
                <input name="amount" type="number" step="0.01" placeholder="Kwota oferty" required>
                <button type="submit">Złóż ofertę</button>
            </form>
        </div>

        <div class="box">
            <h2>Lista aukcji</h2>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Nazwa</th>
                    <th>Kategoria</th>
                    <th>Cena startowa</th>
                    <th>Najwyższa oferta</th>
                    <th>Koniec aukcji</th>
                </tr>
                {rows}
            </table>
        </div>
    </body>
    </html>
    """


@router.post("/frontend/users")
def frontend_add_user(
    username: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(username=username, email=email)

    db.add(user)
    db.commit()

    return RedirectResponse("/", status_code=303)


@router.post("/frontend/auctions")
def frontend_add_auction(
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    starting_price: float = Form(...),
    owner_id: int = Form(...),
    db: Session = Depends(get_db)
):
    owner = db.query(User).filter(User.id == owner_id).first()

    if owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")

    auction = Auction(
        title=title,
        description=description,
        category=category,
        starting_price=starting_price,
        current_highest_bid=starting_price,
        end_date=datetime.utcnow() + timedelta(days=7),
        owner_id=owner_id
    )

    db.add(auction)
    db.commit()

    return RedirectResponse("/", status_code=303)


@router.post("/frontend/bids")
def frontend_add_bid(
    auction_id: int = Form(...),
    user_id: int = Form(...),
    amount: float = Form(...),
    db: Session = Depends(get_db)
):
    auction = db.query(Auction).filter(Auction.id == auction_id).first()
    user = db.query(User).filter(User.id == user_id).first()

    if auction is None:
        raise HTTPException(status_code=404, detail="Auction not found")

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if datetime.utcnow() > auction.end_date:
        raise HTTPException(status_code=400, detail="Auction has ended")

    if amount <= auction.current_highest_bid:
        raise HTTPException(
            status_code=400,
            detail="Bid must be higher than current highest bid"
        )

    bid = Bid(
        auction_id=auction_id,
        user_id=user_id,
        amount=amount
    )

    auction.current_highest_bid = amount

    db.add(bid)
    db.commit()

    return RedirectResponse("/", status_code=303)