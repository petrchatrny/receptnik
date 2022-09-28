import logging


def database_error(e):
    logging.log(logging.ERROR, f"DB ERROR: {e}")
    return {"message": "db_failure", "error": str(e)}, 400
