from dotenv import load_dotenv
from fastapi import APIRouter,Request
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
import os
from fastapi.responses import RedirectResponse
load_dotenv()


app = APIRouter()

app.add_middleware(SessionMiddleware, secret_key=os.getenv('SESSION_SECRET'))


oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid'}
)

@app.get('/login/google')
async def login_google(request: Request):
    # формируем URI для колбэка по имени функции ниже
    redirect_uri = request.url_for('auth_google')
    # редиректим на Google
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get('/auth/google')
async def auth_google(request: Request):
    # обмениваем code на access_token и id_token
    token = await oauth.google.authorize_access_token(request)

    # парсим id_token, чтобы достать payload
    user_info = await oauth.google.parse_id_token(request, token)
    # сохраняем в сессии, например только уникальный sub
    request.session['user'] = {'sub': user_info['sub']}
    # отправляем пользователя внутрь приложения
    return RedirectResponse(url='/')

'''
oauth.register(
    name='github',
    client_id=os.getenv('GITHUB_CLIENT_ID'),
    client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
    authorize_url='https://github.com/login/oauth/authorize',
    access_token_url='https://github.com/login/oauth/access_token',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'}
)
'''