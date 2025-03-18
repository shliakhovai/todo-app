import logging

from fastapi import FastAPI
from fastapi.responses import RedirectResponse


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


app = FastAPI(
    title="To-Do Application API",
    description="A simple and efficient to-do application API for quick task management and organization.",
    version="1.0.0"
)


@app.get("/", response_class=RedirectResponse)
async def root() -> dict[str, str]:
    return RedirectResponse(url="/docs")


_logger = logging.getLogger(__name__)
