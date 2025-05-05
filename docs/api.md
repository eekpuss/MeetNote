# Dokumentasi API MeetNote

## Daftar Isi
1. [Ringkasan](#ringkasan)
2. [Autentikasi](#autentikasi)
3. [Endpoint User](#endpoint-user)
4. [Endpoint Meeting](#endpoint-meeting)
5. [Endpoint Todo](#endpoint-todo)
6. [Kode Status & Error](#kode-status--error)
7. [Format Data](#format-data)

## Ringkasan

API MeetNote dibangun menggunakan Flask dan menggunakan format respons JSON. Semua endpoint (kecuali autentikasi) memerlukan JWT token untuk otorisasi.

**Base URL**: `http://localhost:5000/api`

## Autentikasi

MeetNote menggunakan JWT (JSON Web Token) untuk autentikasi. Token harus disertakan dalam header HTTP "Authorization" dengan format:

```
Authorization: Bearer <token>
```

### Endpoint Autentikasi

#### Register User

```
POST /auth/register
```

**Request Body**:
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "is_admin": boolean (optional)
}
```

**Response (201)**:
```json
{
  "message": "User registered successfully"
}
```

#### Login

```
POST /auth/login
```

**Request Body**:
```json
{
  "email": "string",
  "password": "string"
}
```

**Response (200)**:
```json
{
  "message": "Login successful",
  "access_token": "string",
  "user": {
    "id": integer,
    "username": "string",
    "email": "string",
    "is_admin": boolean,
    "created_at": "datetime",
    "updated_at": "datetime"
  }
}
```

#### Get Current User

```
GET /auth/me
```

**Response (200)**:
```json
{
  "id": integer,
  "username": "string",
  "email": "string",
  "is_admin": boolean,
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## Endpoint Meeting

### Membuat Meeting Baru

```
POST /meetings/
```

**Request Body**:
```json
{
  "title": "string",
  "description": "string",
  "location": "string",
  "meeting_date": "ISO-date-string",
  "participant_ids": [integer]
}
```

**Response (201)**:
```json
{
  "id": integer,
  "title": "string",
  "description": "string",
  "location": "string",
  "meeting_date": "datetime",
  "creator_id": integer,
  "created_at": "datetime",
  "updated_at": "datetime",
  "participants": [User objects],
  "todos": [],
  "notes": null
}
```

### Mendapatkan Daftar Meeting

```
GET /meetings/
```

**Query Parameters**:
- `start_date` (opsional): Filter meeting dari tanggal tertentu
- `end_date` (opsional): Filter meeting sampai tanggal tertentu

**Response (200)**:
```json
[
  {
    "id": integer,
    "title": "string",
    "description": "string",
    "location": "string",
    "meeting_date": "datetime",
    "creator_id": integer,
    "created_at": "datetime",
    "updated_at": "datetime",
    "participants": [User objects],
    "todos": [Todo objects],
    "notes": MeetingNote object
  }
]
```

### Mendapatkan Detail Meeting

```
GET /meetings/{meeting_id}
```

**Response (200)**:
```json
{
  "id": integer,
  "title": "string",
  "description": "string",
  "location": "string",
  "meeting_date": "datetime",
  "creator_id": integer,
  "created_at": "datetime",
  "updated_at": "datetime",
  "participants": [User objects],
  "todos": [Todo objects],
  "notes": MeetingNote object
}
```

### Mengupdate Meeting

```
PUT /meetings/{meeting_id}
```

**Request Body**:
```json
{
  "title": "string",
  "description": "string",
  "location": "string",
  "meeting_date": "ISO-date-string",
  "participant_ids": [integer]
}
```

**Response (200)**:
```json
{
  "id": integer,
  "title": "string",
  "description": "string",
  "location": "string",
  "meeting_date": "datetime",
  "creator_id": integer,
  "created_at": "datetime",
  "updated_at": "datetime",
  "participants": [User objects],
  "todos": [Todo objects],
  "notes": MeetingNote object
}
```

### Mengupdate Notulen Meeting

```
PUT /meetings/{meeting_id}/notes
```

**Request Body**:
```json
{
  "content": "string (HTML)"
}
```

**Response (200)**:
```json
{
  "id": integer,
  "content": "string",
  "meeting_id": integer,
  "created_at": "datetime",
  "updated_at": "datetime",
  "updated_by": integer
}
```

### Mengekspor Meeting ke PDF

```
GET /meetings/{meeting_id}/export
```

**Response (200)**:
- File PDF dengan header:
  - `Content-Type: application/pdf`
  - `Content-Disposition: attachment; filename=meeting_{id}.pdf`

## Endpoint Todo

### Membuat Todo Baru

```
POST /todos/
```

**Request Body**:
```json
{
  "title": "string",
  "description": "string",
  "priority": "string (low, medium, high)",
  "deadline": "ISO-date-string",
  "meeting_id": integer,
  "assignee_id": integer
}
```

**Response (201)**:
```json
{
  "id": integer,
  "title": "string",
  "description": "string",
  "deadline": "datetime",
  "priority": "string",
  "status": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "meeting_id": integer,
  "assignee_id": integer,
  "creator_id": integer
}
```

### Mendapatkan Daftar Todo

```
GET /todos/
```

**Query Parameters**:
- `status` (opsional): Filter berdasarkan status (not_started, in_progress, completed)
- `priority` (opsional): Filter berdasarkan prioritas (low, medium, high)
- `meeting_id` (opsional): Filter todo untuk meeting tertentu
- `assignee_id` (opsional): Filter todo yang ditugaskan ke user tertentu

**Response (200)**:
```json
[
  {
    "id": integer,
    "title": "string",
    "description": "string",
    "deadline": "datetime",
    "priority": "string",
    "status": "string",
    "created_at": "datetime",
    "updated_at": "datetime",
    "meeting_id": integer,
    "assignee_id": integer,
    "creator_id": integer
  }
]
```

### Mendapatkan Detail Todo

```
GET /todos/{todo_id}
```

**Response (200)**:
```json
{
  "id": integer,
  "title": "string",
  "description": "string",
  "deadline": "datetime",
  "priority": "string",
  "status": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "meeting_id": integer,
  "assignee_id": integer,
  "creator_id": integer
}
```

### Mengupdate Todo

```
PUT /todos/{todo_id}
```

**Request Body**:
```json
{
  "title": "string",
  "description": "string",
  "priority": "string",
  "deadline": "ISO-date-string",
  "status": "string",
  "assignee_id": integer
}
```

**Response (200)**:
```json
{
  "id": integer,
  "title": "string",
  "description": "string",
  "deadline": "datetime",
  "priority": "string",
  "status": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "meeting_id": integer,
  "assignee_id": integer,
  "creator_id": integer
}
```

### Menghapus Todo

```
DELETE /todos/{todo_id}
```

**Response (200)**:
```json
{
  "message": "Todo deleted successfully"
}
```

## Kode Status & Error

MeetNote API menggunakan kode status HTTP standar:

- **200 OK**: Request berhasil
- **201 Created**: Resource berhasil dibuat
- **400 Bad Request**: Request tidak valid
- **401 Unauthorized**: Token autentikasi tidak ada atau tidak valid
- **403 Forbidden**: Tidak memiliki izin akses
- **404 Not Found**: Resource tidak ditemukan
- **500 Internal Server Error**: Terjadi kesalahan di server

Format respons error:

```json
{
  "error": "Pesan error"
}
```

## Format Data

### Data Format User

```json
{
  "id": integer,
  "username": "string",
  "email": "string",
  "is_admin": boolean,
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Data Format Meeting

```json
{
  "id": integer,
  "title": "string",
  "description": "string",
  "location": "string",
  "meeting_date": "datetime",
  "creator_id": integer,
  "created_at": "datetime",
  "updated_at": "datetime",
  "participants": [User objects],
  "todos": [Todo objects],
  "notes": MeetingNote object
}
```

### Data Format MeetingNote

```json
{
  "id": integer,
  "content": "string",
  "meeting_id": integer,
  "created_at": "datetime",
  "updated_at": "datetime",
  "updated_by": integer
}
```

### Data Format Todo

```json
{
  "id": integer,
  "title": "string",
  "description": "string",
  "deadline": "datetime",
  "priority": "string",
  "status": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "meeting_id": integer,
  "assignee_id": integer,
  "creator_id": integer
}
```