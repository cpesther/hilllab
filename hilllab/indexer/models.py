# Christopher Esther, Hill Lab, 7/13/2026
from sqlalchemy import String, BigInteger, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .api import Base

class File(Base):
    __tablename__ = 'files'

    # Database ID and UUID
    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[str] = mapped_column(String, unique=True, index=True)

    # Path, name, and type information
    path: Mapped[str] = mapped_column(String, index=True)
    dir_path: Mapped[str | None] = mapped_column(String, index=True)
    dir_id: Mapped[str | None] = mapped_column(String, unique=True, index=True)
    filename: Mapped[str] = mapped_column(String, index=True)
    extension: Mapped[str | None] = mapped_column(String, index=True)
    suffixes: Mapped[str | None] = mapped_column(String)

    # Directory-specific information
    is_directory: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    file_count: Mapped[bool] = mapped_column(BigInteger, default=0)
    file_count_recusrive: Mapped[bool] = mapped_column(BigInteger, default=0)

    # Existence metadata
    exists: Mapped[bool] = mapped_column(Boolean, default=True)
    size: Mapped[int | None] = mapped_column(BigInteger)
    dt_created: Mapped[DateTime | None] = mapped_column(DateTime)
    dt_modified: Mapped[DateTime | None] = mapped_column(DateTime)

    # File system parameters
    ino: Mapped[str | None] = mapped_column(String, index=True)
    dev_id: Mapped[str | None] = mapped_column(String)
    nlink: Mapped[str | None] = mapped_column(String)
    uid: Mapped[str | None] = mapped_column(String)
    gid: Mapped[str | None] = mapped_column(String)

    # Scan information
    dt_found: Mapped[DateTime | None] = mapped_column(DateTime)
    dt_updated: Mapped[DateTime | None] = mapped_column(DateTime)
    dt_rescan: Mapped[DateTime | None] = mapped_column(DateTime)
    node_found: Mapped[str | None] = mapped_column(String)
    user_found: Mapped[str | None] = mapped_column(String)
    node_updated: Mapped[str | None] = mapped_column(String)
    user_updated: Mapped[str | None] = mapped_column(String)
    disposition: Mapped[str | None] = mapped_column(String)

    # Keyword
    keywords: Mapped[list['Keyword']] = relationship(
        'Keyword',
        secondary='file_keywords',
        back_populates='files'
    )


class Keyword(Base):
    __tablename__ = 'keywords'

    keyword_id: Mapped[int] = mapped_column(primary_key=True)
    keyword: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    files: Mapped[list['File']] = relationship(
        'File',
        secondary='file_keywords',
        back_populates='keywords'
    )


class FileKeyword(Base):
    __tablename__ = 'file_keywords'

    item_id: Mapped[int] = mapped_column(ForeignKey('files.item_id'), primary_key=True)
    keyword_id: Mapped[int] = mapped_column(ForeignKey('keywords.keyword_id'), primary_key=True)
