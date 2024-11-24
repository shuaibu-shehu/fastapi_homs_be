from typing import Any, Callable
from fastapi import Request, status, FastAPI
from fastapi.responses import JSONResponse

from lib.error_logger import error_logger

# Define custom exceptions
class BaseException(Exception):
    """This is the base class for all errors"""
    pass

class InvalidToken(BaseException):
    """User has provided an invalid or expired token"""
    pass

class RevokedToken(BaseException):
    """User has provided a token that has been revoked"""
    pass

class AccessTokenRequired(BaseException):
    """User has provided a refresh token when an access token is needed"""
    pass

class RefreshTokenRequired(BaseException):
    """User has provided an access token when a refresh token is needed"""
    pass
 
class UserAlreadyExists(BaseException):
    """User has provided an email for a user who exists during sign up."""
    pass

class InvalidCredentials(BaseException):
    """User has provided wrong email or password during log in."""
    pass

class InsufficientPermission(BaseException):
    """User does not have the necessary permissions to perform an action."""
    pass

class HospitalNotFound(BaseException):
    """Hospital Not found"""
    pass

class DepartmentNotFound(BaseException):
    """Department Not found"""
    pass

class HospitalAlreadyExists(BaseException):
    """Hospital already exists"""
    pass

class UserNotFound(BaseException):
    """User Not found"""
    pass

class UserOrHospitalNotFound(BaseException):
    """Resource Not found"""
    pass

class DepartmentAlreadyExists(BaseException):
    """Department already exists"""
    pass

# Function to create custom exception handlers
def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: BaseException):
        # Log the exception details
        error_logger.error(
            f"Error occurred: {exc.__class__.__name__} - {exc} - Request: {request.method} {request.url}"
        )
        # print(f"\nError occurred: {exc.__class__.__name__} - {exc} - Request: {request.method} {request.url}\n")        
        
        return JSONResponse(content=initial_detail, status_code=status_code)
 
    return exception_handler
 
# Register error handlers
def register_error_handlers(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "User with email already exists",
                "error_code": "user_exists",
            },
        ),
    )

    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "User not found",
                "error_code": "user_not_found",
            },
        ),
    )
    app.add_exception_handler(
        HospitalNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Hospital not found",
                "error_code": "hospital_not_found",
            },
        ),
    )
    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Invalid Email Or Password",
                "error_code": "invalid_email_or_password",
            },
        ),
    )

    app.add_exception_handler(
        DepartmentNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Department not found",
                "error_code": "department_not_found",
            },
        ),
    )

    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid or expired",
                "resolution": "Please get a new token",
                "error_code": "invalid_token",
            },
        ),
    )
    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid or has been revoked",
                "resolution": "Please get a new token",
                "error_code": "token_revoked",
            },
        ),
    )
    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Please provide a valid access token",
                "resolution": "Please get an access token",
                "error_code": "access_token_required",
            },
        ),
    )
    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Please provide a valid refresh token",
                "resolution": "Please get a refresh token",
                "error_code": "refresh_token_required",
            },
        ),
    )
    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "You do not have enough permissions to perform this action",
                "error_code": "insufficient_permissions",
            },
        ),
    )

    app.add_exception_handler(
        HospitalAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Hospital already exists",
                "error_code": "hospital_exists",
            },
        ),
    )

    app.add_exception_handler(
        UserOrHospitalNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "No user or hospital found with this email",
                "error_code": "user_or_hospital_not_found",
            },
        )
    )

    app.add_exception_handler(
        DepartmentAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_detail={
                "message": "Department with the same name already exists",
                "error_code": "department_exists",
            },
        )
    )
    
    @app.exception_handler(500)
    async def internal_server_error(request, exc):
        # Log the error details
        error_logger.error(
            f"Internal Server Error: {exc} - Request: {request.method} {request.url}",
            exc_info=True,  # Include traceback in the log
        )
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )