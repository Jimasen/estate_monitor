from pydantic import BaseModel


class PageCreate(BaseModel):

    title: str

    slug: str

    content: str


class PageUpdate(BaseModel):

    title: str

    content: str

    is_published: bool


class PageResponse(BaseModel):

    title: str

    slug: str

    content: str

    class Config:

        orm_mode = True

