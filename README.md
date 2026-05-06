# KanMind Backend

**KanMind** ist eine Kanban-Board-Anwendung zur Aufgabenverwaltung im Team. Dieses Repository enthält das **Django REST Framework Backend**.

> Dieses Projekt ist ein **Lernprojekt** und mein erstes selbst entwickeltes Backend. Es wurde im Rahmen meiner Weiterbildung erstellt.

Das zugehörige Frontend befindet sich hier: [KanMind FrontEnd](https://github.com/croser93/KanMind_FrontEnd.git)

---

## Inhaltsverzeichnis

- [Technologien](#technologien)
- [Features](#features)
- [Projektstruktur](#projektstruktur)
- [Installation & Setup](#installation--setup)
- [API Endpoints](#api-endpoints)
- [Authentifizierung](#authentifizierung)
- [Datenmodell](#datenmodell)

---

## Technologien

| Technologie | Version |
|---|---|
| Python | 3.x |
| Django | 6.0.4 |
| Django REST Framework | 3.17.1 |
| SQLite3 | (Dateibasiert) |
| django-cors-headers | - |

---

## Features

- Benutzerregistrierung und Login mit Token-Authentifizierung
- Boards anlegen, bearbeiten und löschen
- Mitglieder zu Boards hinzufügen
- Aufgaben (Tasks) mit Status, Priorität, Fälligkeitsdatum, Bearbeiter und Reviewer anlegen
- Kommentare zu Aufgaben schreiben
- Eigene zugewiesene Aufgaben und Review-Aufgaben abrufen
- Berechtigungssystem (Eigentümer, Bearbeiter, Reviewer)

---

## Projektstruktur

```
KanMind_BackEnd/
├── core/               # Django Projektkonfiguration (settings, urls)
├── auth_app/           # Registrierung, Login, Logout
├── board_app/          # Board-Verwaltung und Mitglieder
├── task_app/           # Aufgaben und Kommentare
├── manage.py
├── requirements.txt
└── db.sqlite3
```

---

## Installation & Setup

### Voraussetzungen

- Python 3.x installiert
- `pip` verfügbar

### Schritte

1. **Repository klonen**

   ```bash
   git clone <repository-url>
   cd KanMind_BackEnd
   ```

2. **Virtuelle Umgebung erstellen und aktivieren**

   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # macOS / Linux
   source .venv/bin/activate
   ```

3. **Abhängigkeiten installieren**

   ```bash
   pip install -r requirements.txt
   ```

4. **Datenbank migrieren**

   ```bash
   python manage.py migrate
   ```

5. **Entwicklungsserver starten**

   ```bash
   python manage.py runserver
   ```

Der Server läuft anschließend unter `http://127.0.0.1:8000/`.

---

## API Endpoints

Alle Endpoints beginnen mit dem Präfix `/api/`.

### Authentifizierung

| Methode | Endpoint | Beschreibung | Auth erforderlich |
|---|---|---|---|
| `POST` | `/api/registration/` | Neuen Benutzer registrieren | Nein |
| `POST` | `/api/login/` | Einloggen, Token erhalten | Nein |
| `POST` | `/api/logout/` | Ausloggen, Token löschen | Ja |

### Boards

| Methode | Endpoint | Beschreibung |
|---|---|---|
| `GET` | `/api/boards/` | Alle eigenen Boards abrufen |
| `POST` | `/api/boards/` | Neues Board erstellen |
| `GET` | `/api/boards/<id>/` | Board-Details abrufen |
| `PATCH` | `/api/boards/<id>/` | Board bearbeiten (nur Eigentümer) |
| `DELETE` | `/api/boards/<id>/` | Board löschen (nur Eigentümer) |
| `GET` | `/api/email-check/?email=<email>` | Benutzer per E-Mail suchen |

### Tasks

| Methode | Endpoint | Beschreibung |
|---|---|---|
| `GET` | `/api/tasks/` | Alle Tasks abrufen |
| `POST` | `/api/tasks/` | Neuen Task erstellen |
| `GET` | `/api/tasks/<id>/` | Task-Details abrufen |
| `PATCH` | `/api/tasks/<id>/` | Task bearbeiten |
| `DELETE` | `/api/tasks/<id>/` | Task löschen |
| `GET` | `/api/tasks/assigned-to-me/` | Mir zugewiesene Tasks |
| `GET` | `/api/tasks/reviewing/` | Tasks, bei denen ich Reviewer bin |

### Kommentare

| Methode | Endpoint | Beschreibung |
|---|---|---|
| `GET` | `/api/tasks/<id>/comments/` | Kommentare eines Tasks abrufen |
| `POST` | `/api/tasks/<id>/comments/` | Kommentar erstellen |
| `DELETE` | `/api/tasks/<task_id>/comments/<comment_id>/` | Kommentar löschen |

---

## Authentifizierung

Die API verwendet **Token-Authentifizierung** (DRF AuthToken).

Nach erfolgreichem Login wird ein Token zurückgegeben:

```json
{
  "token": "abc123...",
  "fullname": "Max Mustermann",
  "email": "max@example.com",
  "id": 1
}
```

Alle geschützten Endpoints erfordern den Token im Header:

```
Authorization: Token abc123...
```

---

## Datenmodell

### Board

| Feld | Typ | Beschreibung |
|---|---|---|
| `title` | CharField | Name des Boards |
| `owner_id` | ForeignKey(User) | Eigentümer des Boards |
| `members` | ManyToManyField(User) | Mitglieder des Boards |

### Task

| Feld | Typ | Beschreibung |
|---|---|---|
| `board` | ForeignKey(Board) | Zugehöriges Board |
| `title` | CharField | Titel der Aufgabe |
| `description` | TextField | Beschreibung |
| `status` | CharField | `to-do`, `in-progress`, `review`, `done` |
| `priority` | CharField | `low`, `medium`, `high` |
| `assignee_id` | ForeignKey(User) | Bearbeiter (optional) |
| `reviewer_id` | ForeignKey(User) | Reviewer (optional) |
| `due_date` | DateField | Fälligkeitsdatum |

### Comment

| Feld | Typ | Beschreibung |
|---|---|---|
| `task` | ForeignKey(Task) | Zugehöriger Task |
| `author` | ForeignKey(User) | Autor des Kommentars |
| `content` | CharField | Kommentarinhalt (max. 500 Zeichen) |
| `created_at` | DateTimeField | Erstellungsdatum (automatisch) |

---

## Hinweis

Dieses Backend ist für den **lokalen Entwicklungsbetrieb** ausgelegt. Für einen Produktiveinsatz wären weitere Schritte notwendig (z. B. Umgebungsvariablen für den Secret Key, Datenbankwechsel, DEBUG deaktivieren).
