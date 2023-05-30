from datetime import date
from typing import Optional
from pydantic import BaseModel


class Page(BaseModel):
    parent_page_id: int | None
    page_name: str
    page_description: str | None
    color: Optional[str]

    class Config:
        orm_mode = True


class ReadPage(Page):
    id: int
    create_date: Optional[date]
    last_edit: Optional[date]

    class Config:
        orm_mode = True


class SinglePageList(BaseModel):
    id: int
    page_name: str
    color: str

    class Config:
        orm_mode = True


class PageListView(BaseModel):
    pages: list[SinglePageList]
