# Library Service API
- An API service for library management, written in Django REST Framework

## Features
- Management of borrowings and book returns
- It is possible to create books with two types of covers - Hard and Soft.
- It is possible to filter borrows by status and customer (user) id.
- Supports JWT authentication.
- Swagger documentation.
- Telegram-support - you get an alert when new borrowing is created, and statistics about overdue borrowings every day (Celery).

## There are such endpoints:

### User:

- [POST] /users/register/   (register your user)
- [GET] /users/me   (info about yourself)
- [PUT] /users/me   (update all info about yourself)
- [PATCH] /users/me  (partial update of info about yourself)
- [POST] /users/token (get your JWT token for access)
- [POST] /users/token/refresh (update your access token)

### Book :

- [POST] /api/books/   (create nem book)
- [GET] /api/books/   (list of all books)
- [GET] /api/books/{id}   (detail info about book)
- [PUT] /api/books/{id}   (update all book instance)
- [PATCH] /api/books/{id}   (partial update of book instance)
- [DELETE] /api/books/{id}   (delete book with chosen id)

### Borrows:

- [GET] /api/borrowings/   (list of all borrowings)
- [GET] /api/borrowings/{id}   (detail info about borrow)
- [PUT] /api/borrowings/{id}   (update all borrow instance)
- [PATCH] /api/borrowings/{id}   (partial update of borrow instance)
- [DELETE] /api/borrowings/{id}   (delete borrow with chosen id)
- [DELETE] /api/borrowings/{id}/return   (return book with given borrow id)

## How to run
Note: Requires Docker to be locally installed

- Copy this repo from github:
```git
git clone https://github.com/ochernyi/library-service.git
```
- Create venv and activate it through terminal:
```git
python -m venv myvenv

#Windows activaition:
myvenv\Scripts\activate

#Unix or Linux activation:
source myvenv/bin/activate
```
- Copy .env.sample file, rename it to .env. Populate it with all required data.
- Run app via Docker through terminal:
```git
docker-compose up --build
```
- Create admin user & Create schedule for running sync in DB

## Pre-installed test users:
You can test this service by using pre-installed test users.
Admin:
```git
email: admin@admin.com
password: 1q2w3e4rq
```


## How to register:
- Create user at /api/user/register/ endpoint
- Get user token at /api/user/token/ endpoint
- Authorize with it on /api/doc/swagger/ or use ModHeader wtih Request header:
```
Header: Authorization
Value: Bearer <Your access token> 
```