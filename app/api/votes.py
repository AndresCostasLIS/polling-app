from typing import Union
from uuid import UUID
from app.services import utils
from fastapi import APIRouter, HTTPException, Depends
from app.models.Votes import Vote, VoteById, VoteByLabel, Voter
from app.models.Polls import Poll

router = APIRouter()


def common_validations(poll_id: UUID, vote: Union[VoteById, VoteByLabel]):
    poll= utils.get_poll(poll_id)
    
    voter_email = vote.voter.email

    if not poll:
        raise HTTPException(status_code=404,detail="Poll not found")
    if not poll.is_active():
        raise HTTPException(status_code=400,detail="The poll is expired")
    
    if utils.get_vote(poll_id, voter_email):
        raise HTTPException(status_code=400,detail="Already voted")
    return poll

@router.post("/{poll_id}/id/")
def create_vote_id(poll_id: UUID,
                   vote: VoteById,
                   poll: Poll = Depends(common_validations)):
    
    poll= utils.get_poll(poll_id)
    
    
    if vote.choice_id not in [choice.id for choice in poll.options]:
        raise HTTPException(status_code=400,detail="Invalid choice id specified")
    vote = Vote(
        poll_id = poll_id,
        choice_id=vote.choice_id,
        voter=Voter(
            **vote.voter.model_dump()
        )
    )
    utils.save_vote(poll_id,vote)
    return {"message":"Vote Recorded"}

@router.post("/{poll_id}/label/")
def create_vote_label(poll_id: UUID,
                      vote: VoteByLabel,
                      poll: Poll = Depends(common_validations)):
    
    choice_id = utils.get_choice_id_by_label(poll_id,vote.choice_label)
    
    if not choice_id:
        raise HTTPException(status_code=400, detail="Invalid choice label")
    vote = Vote(
        poll_id = poll_id,
        choice_id=choice_id,
        voter=Voter(
            **vote.voter.model_dump()
        )
    )
    utils.save_vote(poll_id,vote)
    return {"message":"Vote Recorded"}