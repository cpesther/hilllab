# Christopher Esther, Hill Lab, 7/13/2026
import uuid
from datetime import datetime, timedelta
import platform
import os

from .database import Base, engine, get_session
from .models import Keyword, FileKeyword
from .config import ROOT_DIR, scan_rules
from .scanner import scan, traverse

# Database setup
def initalize_database():
    """Set up the database"""
    from .models import File  # noqa: F401
    Base.metadata.create_all(engine)


# Database API
def add_file(path):

    """Add a new file to the database"""

    # Perform a scan on the provided path
    file, keywords, keywords_present = scan(path)

    # Check if scan was successful
    if file is None:
        print(f'[add_file] unable to add file {path}')
        return

    # Generate an item_id UUID for this item
    item_id = str(uuid.uuid4())
    file.item_id = item_id

    # Update the scan information in this file object
    file.dt_found = datetime.now()
    file.dt_updated = datetime.now()
    file.dt_rescan = datetime.now() + timedelta(seconds=scan_rules['default_interval'])

    node = platform.node()
    user = os.getlogin()
    file.node_found = node
    file.user_found = user
    file.node_updated = node
    file.user_updated = user

    # Add keywords, if present
    if keywords_present:
        for keyword in keywords:
            add_keyword(file=file, keyword_text=keyword)

    # Add this file object to the database
    with get_session() as session:
        session.add(file)
        print(f'Added file {file.filename}{file.suffixes}')


def build():

    """
    Builds the database by adding all files in the specified root folder.
    """

    file_counter = 0
    for path in traverse(ROOT_DIR):
        add_file(path)
        file_counter += 1

        if file_counter % 100 == 0:
            with get_session() as session:
                print('[build] database commit')
                session.commit()

    with get_session() as session:
        print(f'[build] build complete at {datetime.now()}')
        session.commit()


def add_keyword(file, keyword_text):

    """
    Adds a keyword and its associated file to the database
    """
    
    with get_session() as session:
        # Find existing keyword or create new one
        keyword = session.query(Keyword).filter_by(keyword=keyword_text).first()

        if keyword is None:
            keyword = Keyword(keyword=keyword_text)
            session.add(keyword)
            session.flush()  # Get keyword.id without committing

        # Add association if it doesn't already exist
        association = session.query(FileKeyword).filter_by(
            item_id=file.item_id,
            keyword_id=keyword.keyword_id
        ).first()

        if association is None:
            association = FileKeyword(
                item_id=file.item_id,
                keyword_id=keyword.keyword_id
            )
            session.add(association)

        session.commit()
