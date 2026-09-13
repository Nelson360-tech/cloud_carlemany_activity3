class FileBO:
    def __init__(
        self,
        filename: str,
        description: str,
        owner_external_id: int,
        content: bytes | None = None,
        id: int | None = None,
    ):
        self.id = id
        self.filename = filename
        self.description = description
        self.owner_external_id = owner_external_id
        self.content = content