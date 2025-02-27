from fastapi import HTTPException

def success_response(data, message="Success"):
    return {
        "status": "success",
        "message": message,
        "data": data
    }

def error_response(message, status_code=400):
    raise HTTPException(status_code=status_code, detail={
        "status": "error",
        "message": message
    })
