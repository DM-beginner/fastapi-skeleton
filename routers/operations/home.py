from fastapi import APIRouter
from fastapi.responses import HTMLResponse, PlainTextResponse

router = APIRouter(tags=['Home'])


@router.get("/")
def get():
    return HTMLResponse(content='seo service routers.', status_code=200)


@router.get('/robots.txt', response_class=PlainTextResponse)
def robots():
    return """User-agent: *\nDisallow: /"""
