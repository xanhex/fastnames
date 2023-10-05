"""
Fastnames app.

A fully asynchronous Fast API service that provides the user with nickname
options and the ability to add them to the database.
"""
from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastnames import config, models, schemas
from fastnames.crud import create_nicknames, get_nicknames
from fastnames.database import init_models
from starlette.templating import _TemplateResponse


@asynccontextmanager
async def lifespan(app: FastAPI) -> FastAPI:
    """Add DB creation before app startup."""
    await init_models()
    yield


app = FastAPI(lifespan=lifespan)


@lru_cache()
def get_settings():
    """Get cashed settings."""
    return config.Settings()


conf = get_settings()

app.mount('/static', StaticFiles(directory=conf.static), name='static')

templates = Jinja2Templates(directory=conf.templates)


@app.get('/', response_class=HTMLResponse)
@app.post('/', response_class=HTMLResponse)
async def home(
    request: Request,
    limit: int = 100,
    male_start: Annotated[str, Form()] = None,
    female_start: Annotated[str, Form()] = None,
) -> _TemplateResponse:
    """
    Home route.

    All DB queries work asynchronously.
    """
    context = {'request': request}
    if request.method == 'GET':
        return templates.TemplateResponse('index.html', {'request': request})
    if male_start and not female_start:
        males: list[schemas.Nickname] = await get_nicknames(
            models.Male,
            limit,
            male_start,
        )
        context.update(males=males)
    elif female_start and not male_start:
        females: list[schemas.Nickname] = await get_nicknames(
            models.Female,
            limit,
            female_start,
        )
        context.update(females=females)
    else:
        males: list[schemas.Nickname] = await get_nicknames(
            models.Male,
            limit,
            male_start,
        )
        females: list[schemas.Nickname] = await get_nicknames(
            models.Female,
            limit,
            female_start,
        )
        context.update(males=males)
        context.update(females=females)
    return templates.TemplateResponse('index.html', context)


@app.get('/add/', response_class=HTMLResponse)
@app.post('/add/', response_class=HTMLResponse)
async def add_nicknames(
    request: Request,
    males: Annotated[str, Form()] = None,
    females: Annotated[str, Form()] = None,
) -> _TemplateResponse:
    """
    Route for creating new nicknames.

    All DB queries work asynchronously.
    """
    context = {'request': request}
    if request.method == 'GET':
        return templates.TemplateResponse('add.html', {'request': request})
    if males:
        males_q: list[schemas.Nickname] = await create_nicknames(
            models.Male,
            males.split(),
        )
        context.update(males=males_q)
    if females:
        females_q: list[schemas.Nickname] = await create_nicknames(
            models.Female,
            females.split(),
        )
        context.update(females=females_q)
    return templates.TemplateResponse('add.html', context)


@app.get('/get-names')
async def get_names(
    startswith: str | None = None,
    limit: int = 20,
) -> dict[str, list[schemas.Nickname]]:
    """Get nicknames in JSON format."""
    return {
        'males': await get_nicknames(models.Male, limit, startswith),
        'females': await get_nicknames(models.Female, limit, startswith),
    }


@app.get('/info')
async def info(settings: Annotated[config.Settings, Depends(get_settings)]):
    """Get app info from config."""
    return {
        'app_name': settings.app_name,
        'admin_email': settings.admin_email,
        'items_per_user': settings.items_per_user,
    }
