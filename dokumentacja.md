# Dokumentacja techniczna projektu

## Przedmiot

**Tworzenie usług sieciowych REST**

## Tytuł projektu

**System aukcji internetowych REST API**

---

# 1. Cel projektu

Celem projektu było zaprojektowanie i implementacja aplikacji webowej opartej na architekturze REST, umożliwiającej zarządzanie użytkownikami, aukcjami oraz ofertami składanymi podczas licytacji.

System komunikuje się za pomocą REST API, wykorzystuje format JSON do wymiany danych oraz przechowuje informacje w sposób trwały w bazie danych SQLite.

Link do GitHub
https://github.com/c8d5tnrz8s-del/System_aukcyjny_REST_API
---

# 2. Zastosowane technologie

W projekcie wykorzystano następujące technologie:

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic (DTO)
* Swagger / OpenAPI
* HTML
* CSS
* JavaScript

---

# 3. Architektura systemu

Projekt został wykonany zgodnie z architekturą warstwową.

Struktura projektu:

* **main.py** – punkt startowy aplikacji
* **app/database.py** – konfiguracja bazy danych
* **app/models.py** – modele bazodanowe SQLAlchemy
* **app/schemas.py** – obiekty DTO oraz walidacja danych
* **app/routes.py** – endpointy REST API
* **app/frontend.py** – warstwa prezentacji (frontend)

Frontend komunikuje się z backendem wyłącznie poprzez REST API z wykorzystaniem funkcji `fetch()`.

---

# 4. Diagram klas

Relacje pomiędzy klasami:

* Jeden użytkownik może posiadać wiele aukcji.
* Jeden użytkownik może składać wiele ofert.
* Jedna aukcja może posiadać wiele ofert.

### Relacje

User (1) -------- (*) Auction

User (1) -------- (*) Bid

Auction (1) ----- (*) Bid

### Klasa User

Atrybuty:

* id : int
* username : string
* email : string

### Klasa Auction

Atrybuty:

* id : int
* title : string
* description : string
* category : string
* starting_price : float
* current_highest_bid : float
* start_date : datetime
* end_date : datetime
* owner_id : int

### Klasa Bid

Atrybuty:

* id : int
* auction_id : int
* user_id : int
* amount : float
* created_at : datetime

---

# 5. Opis endpointów REST API

## Użytkownicy

| Metoda | Endpoint    | Opis                                    |
| ------ | ----------- | --------------------------------------- |
| POST   | /users      | Dodanie użytkownika                     |
| GET    | /users      | Pobranie listy użytkowników             |
| GET    | /users/{id} | Pobranie użytkownika po identyfikatorze |
| PUT    | /users/{id} | Aktualizacja danych użytkownika         |
| DELETE | /users/{id} | Usunięcie użytkownika                   |

## Aukcje

| Metoda | Endpoint       | Opis                               |
| ------ | -------------- | ---------------------------------- |
| POST   | /auctions      | Dodanie aukcji                     |
| GET    | /auctions      | Pobranie listy aukcji              |
| GET    | /auctions/{id} | Pobranie aukcji po identyfikatorze |
| PUT    | /auctions/{id} | Aktualizacja aukcji                |
| DELETE | /auctions/{id} | Usunięcie aukcji                   |

Filtrowanie aukcji:

* `/auctions?category=Elektronika`
* `/auctions?status=active`
* `/auctions?status=ended`

## Licytacje

| Metoda | Endpoint            | Opis                    |
| ------ | ------------------- | ----------------------- |
| POST   | /auctions/{id}/bids | Dodanie oferty          |
| GET    | /auctions/{id}/bids | Pobranie historii ofert |

---

# 6. Obsługa błędów

System wykorzystuje standardowe kody HTTP:

| Kod | Znaczenie             |
| --- | --------------------- |
| 200 | OK                    |
| 201 | Created               |
| 204 | No Content            |
| 400 | Bad Request           |
| 404 | Not Found             |
| 500 | Internal Server Error |

Przykładowe sytuacje błędne:

* użytkownik nie istnieje – kod 404,
* aukcja nie istnieje – kod 404,
* oferta jest niższa od aktualnej najwyższej oferty – kod 400,
* próba licytacji po zakończeniu aukcji – kod 400.

---

# 7. Walidacja danych

Walidacja została zaimplementowana przy użyciu biblioteki Pydantic.

Przykłady walidacji:

* nazwa użytkownika musi zawierać minimum 3 znaki,
* adres e-mail musi zawierać minimum 5 znaków,
* tytuł aukcji musi zawierać minimum 3 znaki,
* opis aukcji musi zawierać minimum 5 znaków,
* cena wywoławcza musi być większa od 0,
* kwota oferty musi być większa od aktualnej najwyższej oferty.

---

# 8. Dokumentacja API

Automatyczna dokumentacja OpenAPI (Swagger) jest dostępna pod adresem:

http://127.0.0.1:8001/docs

---

# 9. Instrukcja uruchomienia

### Utworzenie środowiska

```bash
python3 -m venv venv
source venv/bin/activate
```

### Instalacja zależności

```bash
pip install -r requirements.txt
```

### Uruchomienie aplikacji

```bash
uvicorn main:app --reload --port 8001
```

### Adresy aplikacji

Frontend:

```text
http://127.0.0.1:8001
```

Swagger:

```text
http://127.0.0.1:8001/docs
```

---

# 10. Podsumowanie

Projekt spełnia wymagania aplikacji REST API określone w specyfikacji zadania. Umożliwia zarządzanie użytkownikami, aukcjami oraz ofertami składanymi podczas licytacji. Dane przechowywane są w bazie SQLite, a interfejs użytkownika komunikuje się z backendem wyłącznie poprzez REST API.
