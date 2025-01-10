TOKEN_STORAGE = dict()


def storage_token(token: str, file_id: int, position: int):
    if token not in TOKEN_STORAGE:
        TOKEN_STORAGE[token] = {}
    if file_id in TOKEN_STORAGE[token]:
        TOKEN_STORAGE[token][file_id].add(position)
    else:
        TOKEN_STORAGE[token][file_id] = {position}


def get_token_info(token: str) -> dict | None:
    return TOKEN_STORAGE.get(token)
