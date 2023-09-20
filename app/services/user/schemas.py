from pydantic import BaseModel, EmailStr


class UserRegistration(BaseModel):
    username: EmailStr = "anyemail@anyprovider.com"
    password: str = "ultrasecretpassword"


class UserLogin(BaseModel):
    username: str
    password: str


class Tokens(BaseModel):
    access_token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbnllbWFpbEBhbnlwcm92aWRlci5jb20iLCJzY29wZ" + \
                        "XMiOiJhY2Nlc3NfdG9rZW4iLCJleHAiOjE2OTEzODU0NjV9.6aR1kkg0-HxilnrXn_UN-DJPs4KH7YZ71ZG5d8CgQGU"
    token_type: str = "bearer"
    refresh_token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbnllbWFpbEBhbnlwcm92aWRlci5jb20iLCJzY29w" + \
                         "ZXMiOiJyZWZyZXNoX3Rva2VuIiwiZXhwIjoxNjkxOTg4NDY1fQ.UjNTD2hou-WnzsWagxY02JnRFc2ORNYP-gVRJb" + \
                         "56HZ4"


class TokenRefreshed(BaseModel):
    access_token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbnllbWFpbEBhbnlwcm92aWRlci5jb20iLCJzY29wZ" + \
                        "XMiOiJhY2Nlc3NfdG9rZW4iLCJleHAiOjE2OTEzODU0NjV9.6aR1kkg0-HxilnrXn_UN-DJPs4KH7YZ71ZG5d8CgQGU"
    token_type: str = "bearer"


class RefreshToken(BaseModel):
    refresh_token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbnllbWFpbEBhbnlwcm92aWRlci5jb20iLCJzY29w" + \
                         "ZXMiOiJyZWZyZXNoX3Rva2VuIiwiZXhwIjoxNjkxOTg4NDY1fQ.UjNTD2hou-WnzsWagxY02JnRFc2ORNYP-gVRJb" + \
                         "56HZ4"
