class DialogsError(Exception):
    '''Base class for alice exceptions'''


class DialogsAPIError(Exception):
    '''Base Exception for API related requests'''
    __subclasses = []
    match = None

    def __init_subclass__(cls, match=None, **kwargs):
        super(DialogsAPIError, cls).__init_subclass__(**kwargs)
        if match is not None:
            cls.match = match.lower()
            cls.__subclasses.append(cls)

    @classmethod
    def detect(cls, description):
        """Detect API Error (match by response text)"""
        description = description.strip()
        match = description.lower()
        for err in cls.__subclasses:
            if err is cls:
                pass
            if err.match in match:
                raise err(description)
        raise cls(description)


class AuthRequired(Exception):
    '''Passed is skill_id of oauth_token is not provided'''


class ApiChanged(DialogsError):
    '''Is thrown if there are some unpredicted changes in API'''


class NetworkError(DialogsAPIError):
    '''Is thrown when aiohttp client throws an error'''


# class ClientError(DialogsAPIError):
#     '''Is thrown when response code is 4xx'''


# class ServerError(DialogsAPIError):
#     '''Is thrown when response code is 5xx'''


class Forbidden(DialogsAPIError, match='Forbidden'):
    '''Is thrown when Authorization failed (403)'''


class ContentNotProvided(DialogsAPIError, match='URL or FILE is needed'):
    '''Is thrown when no image is provided within request'''


class InvalidImageID(DialogsAPIError, match='Invalid image ID'):
    '''Is thrown if a wrong image_id is provided within request'''
