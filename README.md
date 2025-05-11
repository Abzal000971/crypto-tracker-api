## CryptoTracker

Простое API-приложение на FastAPI для отслеживания цен криптовалют. Есть авторизация, список избранного и обновление данных с CoinGecko.

### Возможности

Регистрация и вход по JWT

Список криптовалют с ценами

Избранные монеты (watchlist)

Обновление цен каждые 5 минут (фоново)

pip install -r requirements.txt

.env файл:

DATABASE_URL=postgresql://<пользователь>:<пароль>@localhost:5432/cryptotracker

SECRET_KEY=секретный_ключ

ALGORITHM=HS256

uvicorn app.main:app --reload

API доступно по адресу http://localhost:8000

#### Эндпоинты

POST /auth/register — регистрация

POST /auth/login — вход

GET /cryptos/ — список монет

POST /watchlist/ — добавить в избранное

GET /watchlist/ — мои монеты

Для данных о крипте используется CoinGecko API. База данных — PostgreSQL.
