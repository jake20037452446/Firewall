revoked_tokens = set()


def add_token(jti):
    revoked_tokens.add(jti)


def is_token_revoked(jti):
    return jti in revoked_tokens
