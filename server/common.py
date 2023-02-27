from server import crud, schemas
from server.models.user import User


def deduct_credit(db, user: User, deduct_tokens):
    recurring_credits = user.recurring_credits
    daily_credits = user.daily_credits

    if recurring_credits >= deduct_tokens:
        recurring_credits -= deduct_tokens
    else:
        deduct_tokens -= recurring_credits
        recurring_credits = 0

        if daily_credits >= deduct_tokens:
            daily_credits -= deduct_tokens
        else:
            daily_credits = 0

    return crud.user.update(
        db,
        db_obj=user,
        obj_in=schemas.UserUpdate(
            daily_credits=daily_credits, recurring_credits=recurring_credits
        ),
    )


def dict_history(history):
    return {
        "id": str(history.id),
        "input_prompt": history.input_prompt,
        "raw_completion": history.raw_completion,
        "tokens": history.tokens,
        "service": history.service.value,
        "created_date": str(history.created_date),
        "updated_date": str(history.updated_date),
    }
