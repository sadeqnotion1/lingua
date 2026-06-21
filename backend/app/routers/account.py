"""Account endpoints: profile + settings shown on the Account screen."""
from fastapi import APIRouter

router = APIRouter(prefix="/account", tags=["account"])


@router.get("")
def get_account() -> dict:
    """Return the current user's account/profile. TODO: implement auth + user."""
    return {
        "username": "",
        "email": "",
        "tier": "free",
        "member_since": None,
    }
