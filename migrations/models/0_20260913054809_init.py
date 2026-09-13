from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "files" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "filename" VARCHAR(255) NOT NULL,
    "description" TEXT NOT NULL,
    "content" BYTEA,
    "owner_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztmG1v2jAQx78KyqtO2qaWtWu1d4HB1rUDiWZTq2myTGKCVcdObWcUdXz32U5CTB4oSO"
    "1UKt7B33f2+Wf77uDBiViAiHj/QyDufGo9OBRGSH1Y0d+2HBjHhaoFCcfEGCbKwihwLCSH"
    "vlTiBBKBlBQg4XMcS8yoUmlCiBaZrwwxDQspofguQUCyEMmpCeTXbyVjGqB7JPKv8S2YYE"
    "SClThxoNc2OpDz2GjnVPaNoV5tDHxGkogWxvFcThldWmMqtRoiijiUSE8veaLD19Fl28x3"
    "lEZamKQhWj4BmsCESGu7Y1BoDgCDoQeueh4AzhaAfEY1XBWqMLsPdQjv2kfHp8dnHz4eny"
    "kTE+ZSOV2kSxdgUkeDZ+A5CzMOJUwtDOMCKoogJlWu3Snk9WCXDiW2Kugy25zky4UbwXtA"
    "EA3lVBM9OVmD8qc76n51RwfK6o1ekqkHkD6LQTbUTsc074JvDIWYMV5zdZsR2z5PQzkXCs"
    "zFu91dzjpTTG6ta62FMfRvZ5AHYGWkOJAJJkhUT6OTufUvRohAs8Eq/SxT9tUUO3gKi/ye"
    "5Wr22gxH1mZNIKtDUTsqK5DC0GxJr61XslnVVJucYXO1WR7Uvtq8mmqjz9R83iIb2j77bL"
    "hZ1bEjq6D20H3DNS65/T/ajvO8Oa8Orde79vTMkRB3xCZ68N29NrCjeTZyORx8yc2tE+he"
    "Djsl8Gp5idJ3X6ovmEI+r8duOZWQj+cyzYGPQM9yxEu54WuodzQzm7qC3jkfuKObeuy5fc"
    "yEDLmZyOnceD23BJ7NFCCwVdK2XR5P3buQWJ4ge1d6qhLiKt8+4wiH9AKlt/tchQSpX5eu"
    "Sz80d4xuU/ukZA5nyw5i5VqpzastI5mWOPeq637uOYvmNvU5OzEXcexP63qxbGRtNwYLm3"
    "07tksPel079gdxUdsiNHdjlsu+GdusGdOPagvCmfkrpHt0eLgBXWXVSNeMbdhxfbsaDrbt"
    "twLsy9bfFsFiF+v/Grgaxvpmt9zXlnouPUFnu/9cnr6YLf4B0mRCsQ=="
)
