from datetime import datetime
from typing import List

from bson import ObjectId
from fastapi import HTTPException
from mongoengine import DoesNotExist

from models.example import Example


def create(data: dict) -> Example:
    try:
        example = Example(**data)
        example.save()
        return example
    except HTTPException as e:
        error_message = f"Type error occurred: {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)


def list() -> List[Example]:
    examples = Example.objects.all()
    return examples


def detail(oid: ObjectId) -> Example:
    try:
        return Example.objects.get(_id=oid)
    except DoesNotExist:
        return None


def delete(id: str) -> Example:
    example = detail(ObjectId(id))
    example["deleted_at"] = datetime.now
    example.save()
    return example


def update(data: dict, id: str) -> Example:
    example = detail(ObjectId(id))

    for key, value in data:
        setattr(example, key, value)

    example.save()
    return example


def check_is_example(
    date,
) -> bool:
    if isinstance(date, str):
        date = datetime.strptime(date, "%d-%m-%Y")
    else:
        date = datetime.combine(date, datetime.min.time())
    query = {
        "date": date,
    }
    example = Example.objects(__raw__=query)

    if len(example) == 0:
        return False

    return True
