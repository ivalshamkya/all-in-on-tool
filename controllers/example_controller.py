from fastapi import APIRouter, HTTPException

from data.requests.example_request import Example as example_request
from data.responses.example_response import Example as example_response
from helpers.case_transform import camel_to_snake_case
from helpers.format_response import format_response_data, format_response_success
from services.example_service import (
    create_example_service,
    delete_example_service,
    get_example_by_id_service,
    get_example_service,
    update_example_service,
)

route = APIRouter()


@route.post("/create")
async def create_example(requests: example_request):
    try:
        data = camel_to_snake_case(requests.model_dump())
        created_data = create_example_service(data)

        return format_response_success(example_response, created_data)
    except HTTPException as exc:
        raise HTTPException(500, exc)


@route.get("/")
async def get_examples():
    try:
        examples = get_example_service()
        data = []
        for example in examples:
            if example.deleted_at is None:
                data.append(format_response_data(example_response, example))

        return format_response_success(data=data)
    except HTTPException as exc:
        raise HTTPException(500, exc)


@route.get("/{id}")
async def get_example_by_id(id: str):
    example = get_example_by_id_service(id)
    
    return format_response_success(example_response, example)


@route.delete("")
async def delete_example(id: str):
    get_example_by_id_service(id)

    try:
        deleted_data = delete_example_service(id)

        return format_response_success(example_response, deleted_data)
    except HTTPException as exc:
        raise HTTPException(500, exc)


@route.put("/{id}")
async def update_example(example: example_request, id: str):
    get_example_by_id_service(id)

    try:
        updated_data = update_example_service(example, id)

        return format_response_success(example_response, updated_data)
    except HTTPException as exc:
        raise HTTPException(500, exc)


@route.get("/check")
async def get_example(date: str):
    try:
        data = check_is_example_service(date)

        return format_response_success(data=data)
    except HTTPException as exc:
        raise HTTPException(500, exc)