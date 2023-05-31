from pydantic import BaseModel


class Header:
    token: str


class User(BaseModel):
    first_name: str
    last_name: str | None = None
    email: str
    address: str | None = None

    # class Config:
    #     orm_mode = True

    class Config:
        orm_mode = True


class ReadUser(User):
    id: int | None

    class Config:
        orm_mode = True
