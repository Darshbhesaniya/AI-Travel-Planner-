from fastapi import APIRouter

from config.interests import INTERESTS,MAX_INTERESTS
from tools.airport_tools import STATE_REGION_CODES,get_origin_list

router = APIRouter(tags=["meta"])

@router.get("/origins")
def origins():
    return get_origin_list()

@router.get("/states")
def states():
    return sorted(STATE_REGION_CODES.keys())

@router.get("/interests")
def interests():
    return {
        "max": MAX_INTERESTS, "items": INTERESTS
    }


