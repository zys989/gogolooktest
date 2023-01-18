from redis_om import (EmbeddedJsonModel, Field, JsonModel)


class Task(JsonModel):
    # Indexed for exact text matching
    name: str = Field(index=True)
    status: bool = Field(index=True)


