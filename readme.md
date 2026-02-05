## Р—Р°РїСѓСЃРє РїСЂРѕРµРєС‚Р°

### Р’Р°СЂРёР°РЅС‚ 1. Р§РµСЂРµР· Docker Compose (СЂРµРєРѕРјРµРЅРґСѓРµС‚СЃСЏ)

1. РЎРѕР±РµСЂРёС‚Рµ Рё Р·Р°РїСѓСЃС‚РёС‚Рµ СЃРµСЂРІРёСЃС‹:

```bash
docker compose up --build
```

2. РџСЂРёР»РѕР¶РµРЅРёРµ Р±СѓРґРµС‚ РґРѕСЃС‚СѓРїРЅРѕ РїРѕ Р°РґСЂРµСЃСѓ:

- Auth API: `http://localhost:8001`
- Articles API: `http://localhost:8002`
- Profile API: `http://localhost:8003`
- Interactions API: `http://localhost:8004`

3. РРЅРёС†РёР°Р»РёР·РёСЂСѓР№С‚Рµ Р±Р°Р·Сѓ РґР°РЅРЅС‹С… (СЃРѕР·РґР°СЃС‚ С‚Р°Р±Р»РёС†С‹):

```bash
curl -X POST http://localhost:8001/init-db
```

### Р’Р°СЂРёР°РЅС‚ 2. Р›РѕРєР°Р»СЊРЅРѕ Р±РµР· Docker

1. РЎРѕР·РґР°Р№С‚Рµ РІРёСЂС‚СѓР°Р»СЊРЅРѕРµ РѕРєСЂСѓР¶РµРЅРёРµ Рё СѓСЃС‚Р°РЅРѕРІРёС‚Рµ Р·Р°РІРёСЃРёРјРѕСЃС‚Рё:

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r backend/entrance/requirements.txt
```

2. РЈР±РµРґРёС‚РµСЃСЊ, С‡С‚Рѕ PostgreSQL Рё Redis Р·Р°РїСѓС‰РµРЅС‹, Рё РїР°СЂР°РјРµС‚СЂС‹ РїРѕРґРєР»СЋС‡РµРЅРёСЏ РєРѕСЂСЂРµРєС‚РЅС‹.
   РџРѕ СѓРјРѕР»С‡Р°РЅРёСЋ РёСЃРїРѕР»СЊР·СѓСЋС‚СЃСЏ:
   - PostgreSQL: `postgresql+asyncpg://appuser:strongpass@postgres:5432/full_db`
   - Redis: `redis://redis:6379/0`

3. Р—Р°РїСѓСЃС‚РёС‚Рµ СЃРµСЂРІРёСЃС‹ (РІ СЂР°Р·РЅС‹С… С‚РµСЂРјРёРЅР°Р»Р°С…):

```bash
uvicorn backend.entrance.main:app --host 0.0.0.0 --port 8001 --reload
uvicorn backend.articles_service.main:app --host 0.0.0.0 --port 8002 --reload
uvicorn backend.profile_service.main:app --host 0.0.0.0 --port 8003 --reload
uvicorn backend.interactions_service.main:app --host 0.0.0.0 --port 8004 --reload
```

4. РРЅРёС†РёР°Р»РёР·РёСЂСѓР№С‚Рµ Р±Р°Р·Сѓ РґР°РЅРЅС‹С…:

```bash
curl -X POST http://localhost:8001/init-db
```

## РћСЃРЅРѕРІРЅС‹Рµ СЌРЅРґРїРѕРёРЅС‚С‹

Auth (8001):
- `POST /registration` вЂ” СЂРµРіРёСЃС‚СЂР°С†РёСЏ
- `POST /entrance` вЂ” РІС…РѕРґ (РїРѕР»СѓС‡РµРЅРёРµ access/refresh С‚РѕРєРµРЅРѕРІ)
- `POST /refresh` вЂ” РѕР±РЅРѕРІР»РµРЅРёРµ access С‚РѕРєРµРЅР°

Profile (8003):
- `GET /profile` вЂ” РїРѕР»СѓС‡РёС‚СЊ РїСЂРѕС„РёР»СЊ (email/phone)
- `GET /profile/{login}` -- view profile by login
- `PATCH /profile` вЂ” РѕР±РЅРѕРІРёС‚СЊ/РѕС‡РёСЃС‚РёС‚СЊ email РёР»Рё phone

Articles (8002):
- `POST /articles` вЂ” СЃРѕР·РґР°С‚СЊ СЃС‚Р°С‚СЊСЋ
- `GET /articles` вЂ” СЃРїРёСЃРѕРє СЃРІРѕРёС… СЃС‚Р°С‚РµР№
- `GET /articles/{id}` вЂ” РїРѕР»СѓС‡РёС‚СЊ СЃРІРѕСЋ СЃС‚Р°С‚СЊСЋ
- `PATCH /articles/{id}` вЂ” СЂРµРґР°РєС‚РёСЂРѕРІР°С‚СЊ СЃС‚Р°С‚СЊСЋ
- `DELETE /articles/{id}` вЂ” СѓРґР°Р»РёС‚СЊ СЃС‚Р°С‚СЊСЋ

Interactions (8004):
- `POST /comments` -- create comment
- `GET /comments/article/{article_id}` -- list comments for article
- `DELETE /comments/{comment_id}` -- delete own comment
- `POST /likes/{article_id}` -- like article
- `DELETE /likes/{article_id}` -- unlike article
- `GET /likes/{article_id}` -- likes count
- `POST /views/{article_id}` -- register view
- `GET /views/{article_id}` -- views count

Р’СЃРµ Р·Р°С‰РёС‰С‘РЅРЅС‹Рµ Р·Р°РїСЂРѕСЃС‹ С‚СЂРµР±СѓСЋС‚ Р·Р°РіРѕР»РѕРІРѕРє:

```
Authorization: Bearer <access_token>
```

## РўРµСЃС‚С‹

Р—Р°РїСѓСЃРє С‚РµСЃС‚РѕРІ РёР· РєРѕСЂРЅСЏ СЂРµРїРѕР·РёС‚РѕСЂРёСЏ:

```bash
pytest
```




