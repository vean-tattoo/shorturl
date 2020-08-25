from bson.objectid import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from .config import urls_db

def validate_object_id(id_: str):
    try:
        _id = ObjectId(id_)
    except Exception:
        raise HTTPException(status_code=400)
    return _id


async def _get_or_404(id_: str):
    _id = validate_object_id(id_)
    link = await urls_db.find_one({"_id": _id})
    if link:
        return link
    else:
        raise HTTPException(status_code=404, detail="Link not found")


def fix_id(link):
    link["id_"] = str(link["_id"])
    return link
