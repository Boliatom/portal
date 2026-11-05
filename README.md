Стек

Backend: Python, Django
BD: PostgreSQL (DBeaver)
Frontend: React, Parcel

Как запустить программу

Бэкенд

cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver


http://localhost:8000

Фронтенд

cd frontend
npm install
npm start

http://localhost:1234



БД:

CREATE TABLE users (
    user_id          BIGSERIAL    PRIMARY KEY,
    user_username    VARCHAR(64)  NOT NULL UNIQUE,
    user_email       VARCHAR(255) UNIQUE,
    user_last_name   VARCHAR(100) NOT NULL,
    user_first_name  VARCHAR(100) NOT NULL,
    user_middle_name VARCHAR(100),
    user_password    TEXT         NOT NULL,
    user_active      BOOLEAN      NOT NULL DEFAULT TRUE,
    user_created     TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE TABLE roles (
    role_id   BIGSERIAL    PRIMARY KEY,
    role_name VARCHAR(128) NOT NULL UNIQUE
);

CREATE TABLE modules (
    module_id   BIGSERIAL    PRIMARY KEY,
    module_name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE user_roles (
    user_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    role_id BIGINT NOT NULL REFERENCES roles(role_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
);

CREATE TABLE role_modules (
    role_id            BIGINT  NOT NULL REFERENCES roles(role_id)     ON DELETE CASCADE,
    module_id          BIGINT  NOT NULL REFERENCES modules(module_id) ON DELETE CASCADE,
    role_module_view   BOOLEAN NOT NULL DEFAULT TRUE,
    role_module_edit   BOOLEAN NOT NULL DEFAULT FALSE,
    role_module_delete BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (role_id, module_id)
);

INSERT INTO roles (role_name) VALUES
    ('Сотрудники'),
    ('Техподдержка');

INSERT INTO users (user_username, user_email, user_last_name, user_first_name, user_middle_name, user_password) VALUES
    ('admin',   'admin@gmail.com', 'Админ', 'Админ', NULL, 'admin'),
    ('test',  'test@gmail.com',  'Гончарова',  'Мария',  'Кирилловна',  'test1234');


INSERT INTO user_roles (user_id, role_id)
SELECT u.user_id, r.role_id FROM users u, roles r
WHERE (u.user_username, r.role_name) 
IN (('admin',   'Администратор'),
    ('admin',   'Сотрудники'),
    ('test',  'Сотрудники'));

ALTER TABLE users ADD COLUMN user_first_login TIMESTAMPTZ;
й


Модули (задание 3)

ALTER TABLE modules
    ADD COLUMN module_code    VARCHAR(64)  UNIQUE,
    ADD COLUMN module_url     VARCHAR(500) NOT NULL DEFAULT '',
    ADD COLUMN module_tag     VARCHAR(100) NOT NULL DEFAULT '',
    ADD COLUMN module_enabled BOOLEAN      NOT NULL DEFAULT TRUE;

Модуль «Объявления» запускается отдельно от ядра:

cd modules/announcements
python -m http.server 8001

Регистрация модуля (токен из POST /api/login/; в ответе будет id модуля):

curl -X POST http://localhost:8000/api/modules/ -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d "{\"name\":\"Объявления\",\"code\":\"announcements\",\"url\":\"http://localhost:8001/announcements.js\",\"tag\":\"announcements-module\"}"

Отк или вкл модуль (id из ответа на регистрацию или из таблицы modules):

curl -X PATCH http://localhost:8000/api/modules/<id>/ -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d "{\"enabled\":false}"
