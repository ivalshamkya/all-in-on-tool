# import asyncio
from contextlib import asynccontextmanager
from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.responses import JSONResponse

from config import initiate_database
from controllers.example_controller import route as example_router
from controllers.image_controller import route as image_router
from helpers.format_response import format_response_error
from middlewares import limiter
from middlewares.exception import exception_handler_middleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    await initiate_database()
    yield
app = FastAPI(lifespan=lifespan)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
limiter.enabled = False

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom exception handler for rate limit exceeded
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        format_response_error(
            message="Too many requests. Please try again later.",
            code=HTTPStatus.TOO_MANY_REQUESTS,
            status=HTTPStatus.TOO_MANY_REQUESTS.name
        ),
        status_code=HTTPStatus.TOO_MANY_REQUESTS
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request=Request, exc=HTTPException):
    return await exception_handler_middleware(exc, request)


@app.middleware("http")
async def add_default_headers(request, call_next):
    response = await call_next(request)
    response.headers.update(
        {
            "Access-Control-Allow-Headers": "Content-Type, Accept, X-Requested-With",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
        }
    )
    return response


app.include_router(example_router, tags=["Examples"], prefix="/examples")
app.include_router(image_router, tags=["Image"], prefix="/image")
