from uuid import UUID
from app.services import utils
from fastapi import APIRouter, HTTPException
from app.models.Polls import Poll, PollCreate
from enum import Enum

router = APIRouter()

@router.post("/create")
def create_poll(poll: PollCreate):
    # return Poll(
    #     title="some placeholder title",
    #     options=["yes","no","maybe"]
    # )
    new_poll = poll.create_poll()
    utils.save_poll(new_poll)
        
    return {
        "detail": "Poll successfully created",
        "poll_id": new_poll.id,
        "poll": new_poll
    }
@router.get("/{poll_id}")   
def get_poll(poll_id: UUID):
    poll = utils.get_poll(poll_id)
    print(poll)
    if poll is None:
        raise HTTPException(status_code=404,
                            detail="Poll not found")
    return poll



class PollStatus(Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    ALL = "all"
    
    
@router.get("/")
def get_all_polls(status: PollStatus= PollStatus.ACTIVE):
    polls = utils.get_all_polls()
    if not polls:
        raise HTTPException(status_code=404,
                            detail="Polls not found")
        
    if status == PollStatus.ACTIVE:
        filtered_polls= [
            poll for poll in polls if poll.is_active()
        ]
    elif status == PollStatus.EXPIRED:
        filtered_polls= [
            poll for poll in polls if not poll.is_active()
        ]
    else:
        filtered_polls= polls
        
    return {
        "count": len(filtered_polls), 
        "polls": filtered_polls
            }

@router.get("/{poll_id}/results")
def get_results(poll_id: UUID):
    return utils.get_poll_results(poll_id)