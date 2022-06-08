from app.api.utils.constants import RESOURCE_NOT_FOUND


def base_response(message=RESOURCE_NOT_FOUND):
    return {"message": message}
