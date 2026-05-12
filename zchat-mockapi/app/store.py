# In-memory store for user metadata.
# Keyed by user_personal_number.
# This is a mock — data is not persisted between server restarts.

user_contexts: dict[str, dict] = {}
