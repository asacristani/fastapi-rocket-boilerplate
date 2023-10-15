from fastapi import status

responses_content = {
    "UserSuccessfullyRegistered": {
        status.HTTP_201_CREATED: {
            "description": "User successfully registered",
            "content": {
                "application/json": {
                    "example": "User 'anyemail@anyprovider.com' created"
                }
            },
        }
    },
    "UserAlreadyRegistered": {
        status.HTTP_400_BAD_REQUEST: {
            "description": "User already registered",
            "content": {
                "application/json": {
                    "example": "This user is already registered"
                }
            },
        }
    },
    "InvalidCredentials": {
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid credentials",
            "content": {
                "application/json": {
                    "example": "Invalid credentials"
                }
            },
        }
    },
    "UnauthorizedOrRevoked": {
        status.HTTP_400_BAD_REQUEST: {
            "description": "Unauthorized or revoked token",
            "content": {
                "application/json": {
                    "example": "Not authorized"
                }
            },
        }
    },
    "LoginInvalidCredentials": {
            status.HTTP_400_BAD_REQUEST: {
                "description": "Invalid credentials",
                "content": {
                    "application/json": {"example": "Invalid credentials"}
                }
            }
        },
        "TokenUnauthorizedOrRevoked": {
            status.HTTP_400_BAD_REQUEST: {
                "description": "Unauthorized or revoked token",
                "content": {
                    "application/json": {"example": "Not authorized"}
                }
            }
        },
        "TokenSuccessfullyRevoked": {
            status.HTTP_200_OK: {
                "description": "Token successfully revoked",
                "content": {
                    "application/json": {"example": {"message": "Refresh token successfully revoked"}}
                }
            }
        },
        "ProtectedRouteAccess": {
            status.HTTP_200_OK: {
                "description": "Protected route accessed",
                "content": {
                    "application/json": {"example": {"message": "¡Hola, username! This is a protected url and you are inside!"}}
                }
            }
        }
}
