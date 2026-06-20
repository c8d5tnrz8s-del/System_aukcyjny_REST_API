# System Aukcyjny REST API


## Opis projektu

System Aukcyjny REST API to aplikacja webowa umożliwiająca zarządzanie użytkownikami, aukcjami oraz procesem licytacji. Projekt został zrealizowany zgodnie z architekturą REST i wykorzystuje trwałe przechowywanie danych w bazie SQLite.

Aplikacja udostępnia REST API do obsługi użytkowników, aukcji oraz ofert, a także prosty frontend komunikujący się z backendem wyłącznie za pomocą zapytań HTTP.

## Główne funkcjonalności

### Zarządzanie użytkownikami

* dodawanie użytkowników,
* pobieranie danych użytkownika,
* edycja danych użytkownika,
* usuwanie użytkowników,
* pobieranie listy użytkowników.

### Zarządzanie aukcjami

* tworzenie nowych aukcji,
* edycja aukcji,
* usuwanie aukcji,
* pobieranie szczegółów aukcji,
* przeglądanie wszystkich aukcji,
* filtrowanie aukcji po kategorii,
* filtrowanie aukcji po statusie (aktywne / zakończone).

### Licytacja

* składanie ofert,
* weryfikacja poprawności ofert,
* blokowanie licytacji po zakończeniu aukcji,
* przechowywanie historii ofert.

## Technologie

* Python 3
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Swagger / OpenAPI
* HTML
* CSS
* JavaScript

## Struktura projektu

```text
System_aukcyjny_REST_API
│
├── app
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routes.py
│   └── frontend.py
│
├── main.py
├── requirements.txt
├── auction_system.db
├── README.md
└── DOKUMENTACJA.pdf
```

## Endpointy REST API

### Users

| Metoda | Endpoint    |
| ------ | ----------- |
| POST   | /users      |
| GET    | /users      |
| GET    | /users/{id} |
| PUT    | /users/{id} |
| DELETE | /users/{id} |

### Auctions

| Metoda | Endpoint       |
| ------ | -------------- |
| POST   | /auctions      |
| GET    | /auctions      |
| GET    | /auctions/{id} |
| PUT    | /auctions/{id} |
| DELETE | /auctions/{id} |

Filtrowanie:

```text
/auctions?category=Elektronika
/auctions?status=active
/auctions?status=ended
```

### Bids

| Metoda | Endpoint            |
| ------ | ------------------- |
| POST   | /auctions/{id}/bids |
| GET    | /auctions/{id}/bids |

## Dokumentacja API

Po uruchomieniu aplikacji dokumentacja Swagger dostępna jest pod adresem:

```text
http://127.0.0.1:8001/docs
```

## Uruchomienie projektu

### 1. Utworzenie środowiska wirtualnego

```bash
python3 -m venv venv
```

### 2. Aktywacja środowiska

macOS / Linux:

```bash
source venv/bin/activate
```

### 3. Instalacja zależności

```bash
python3 -m pip install -r requirements.txt
```

### 4. Uruchomienie aplikacji

```bash
python3 -m uvicorn main:app --reload --port 8001
```

### 5. Dostęp do aplikacji

Frontend:

```text
http://127.0.0.1:8001
```

Swagger:

```text
http://127.0.0.1:8001/docs
```

## Obsługa błędów

Aplikacja wykorzystuje standardowe kody HTTP:

* 200 OK
* 201 Created
* 204 No Content
* 400 Bad Request
* 404 Not Found
* 500 Internal Server Error
