# System aukcji internetowych REST API

Projekt wykonany na przedmiot Tworzenie usług sieciowych REST.

## Opis projektu

Aplikacja umożliwia obsługę prostego systemu aukcyjnego. Użytkownik może dodawać konto, wystawiać aukcje, przeglądać aukcje oraz składać oferty w licytacji.

System został wykonany w Python FastAPI i korzysta z bazy danych SQLite.

## Technologie

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Swagger / OpenAPI
- HTML + CSS

## Funkcjonalności

- dodawanie użytkowników
- edycja użytkowników
- usuwanie użytkowników
- pobieranie użytkowników
- dodawanie aukcji
- edycja aukcji
- usuwanie aukcji
- pobieranie aukcji
- filtrowanie aukcji po kategorii
- składanie ofert
- historia ofert dla aukcji
- walidacja danych
- obsługa błędów HTTP

## Endpointy

### Users

- POST /users
- GET /users
- GET /users/{id}
- PUT /users/{id}
- DELETE /users/{id}

### Auctions

- POST /auctions
- GET /auctions
- GET /auctions/{id}
- PUT /auctions/{id}
- DELETE /auctions/{id}

### Bids

- POST /auctions/{id}/bids
- GET /auctions/{id}/bids

## Uruchomienie projektu

1. Utworzenie środowiska:

```bash
python3 -m venv venv
source venv/bin/activate