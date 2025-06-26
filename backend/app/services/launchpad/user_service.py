from app.models.launchpad.user import User, Form, Widget
from sanic import Sanic

EXAMPLE_USER = User(
    id=1,
    name="John Doe",
    form=Form(
        tabs=["overview", "challenges", "assessments"],
        widgets={
            "overview": [Widget(widget_id=1, widget_name="Steps", value=10000)],
            "challenges": [Widget(widget_id=2, widget_name="Water Intake", value=2.5)],
            "assessments": [Widget(widget_id=3, widget_name="BMI", value=22.5)]
        }
    )
)

async def get_user_config(app: Sanic, user_id=1):
    user = await app.ctx.mongo.vitality_service_db.users.find_one({"id": user_id})
    if user:
        return User.parse_obj(user)
    return EXAMPLE_USER 