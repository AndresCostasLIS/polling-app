from app.models.Polls import Poll, PollCreate
from fastapi import FastAPI

app = FastAPI()

@app.get("/test")
def test():
    return {"message:" "hello world"}


@app.post("/polls/create")
def create_poll(poll: PollCreate):
    # return Poll(
    #     title="some placeholder title",
    #     options=["yes","no","maybe"]
    # )
    new_poll = poll.create_poll()
    
    return {
        "detail": "Poll successfully created",
        "poll_id": new_poll.uuid,
        "poll": new_poll
    }
    
from upstash_redis import Redis

redis = Redis(
    url=
    token=
)