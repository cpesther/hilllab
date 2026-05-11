CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT NOT NULL,          -- Path to the file (relative to root)
    dir_path TEXT NOT NULL,      -- Path to directory only
    name TEXT NOT NULL,          -- File name only (no extension)
    extension TEXT DEFAULT NULL, -- File extension (last suffix)
    suffixes TEXT DEFAULT NULL,  -- All extensions (if multiple)
    size INTEGER DEFAULT NULL,   -- File size in bytes
    modified_time INTEGER,       -- Last modification time (Unix timestamp)
    created_time INTEGER,        -- Creation time (Unix timestamp)
    is_directory INTEGER DEFAULT 0, -- 1 if directory, 0 if file
    file_count INTEGER,          -- Number of files within the directory
    file_count_recursive INTEGER,-- Number of files in the directory and all sub dirs
    note TEXT,                   -- User-added note regarding this file
    note_content TEXT,           -- The actual content of the note w/o metadata for better searching
    ino TEXT,                    -- Inode ID or index number
    dev_id TEXT,                 -- Device ID
    nlink TEXT,                  -- Number of hard links to the file
    uid TEXT,                    -- User ID of file owner
    gid TEXT,                    -- Group ID of file owner

    -- This is all stuff that isn't related to the files but helps 
    -- manage and control the databse
    success INTEGER NOT NULL,    -- Whether the file was successfully scanned
    scanned_time INTEGER,        -- Time that this item was scanned
    scan_trigger TEXT,           -- What caused the most recent file scan
    scan_source TEXT             -- The username of the machine that scanned it

);

CREATE INDEX IF NOT EXISTS idx_files_path ON files(path);
CREATE INDEX IF NOT EXISTS idx_files_path ON files(dir_path);
CREATE INDEX IF NOT EXISTS idx_files_name ON files(name);
CREATE INDEX IF NOT EXISTS idx_files_extension ON files(extension);
CREATE INDEX IF NOT EXISTS idx_files_modified_time ON files(modified_time);

-- The table for storing the raw keywords
CREATE TABLE IF NOT EXISTS keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT UNIQUE NOT NULL
);

-- Create the join table for linking files to keywords
CREATE TABLE IF NOT EXISTS file_keywords (
    file_id INTEGER NOT NULL,
    keyword_id INTEGER NOT NULL,
    PRIMARY KEY (file_id, keyword_id),
    FOREIGN KEY (file_id) REFERENCES files(id),
    FOREIGN KEY (keyword_id) REFERENCES keywords(id)
);

-- Create table for storing metadata about the index
CREATE TABLE IF NOT EXISTS metadata (
    meta INTEGER PRIMARY KEY AUTOINCREMENT,
    index_name TEXT NOT NULL, 
    index_description TEXT NOT NULL,
    uuid TEXT NOT NULL,
    creation_source TEXT NOT NULL,
    creation_time TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS versioning (
    version INTEGER PRIMARY KEY AUTOINCREMENT,
    update_source TEXT,
    update_time TEXT,
    version_uuid TEXT
);

-- Create table for storing sector information
CREATE TABLE IF NOT EXISTS sectors (
    sector_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sector_name TEXT NOT NULL,
    sector_description TEXT NOT NULL,
    policy INTEGER
);

-- Create table for storing rules
CREATE TABLE IF NOT EXISTS rules (
    rule_id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_name TEXT NOT NULL,
    rule_description TEXT,
    rule_author TEXT,
    created_time INTEGER,
    rule_type TEXT NOT NULL,         -- e.g., 'extension', 'mtime', 'size', 'global'
    operator TEXT,                   -- e.g., '==', '>', '<=', etc. (null for global)
    value TEXT,                      -- e.g., 'zip', '7', '1024' (or null for global)
    units TEXT,                      -- e.g., 'days', 'MB', 'hours' (kept for value, null for global)
    directive TEXT NOT NULL,         -- 'rescan', 'ignore', 'rescan_every'
    ttl_hours REAL,                  -- only applies when directive is 'rescan_every'
    priority INTEGER NOT NULL DEFAULT 0
);

-- Create table for storing policies
CREATE TABLE IF NOT EXISTS policies (
    policy_id INTEGER PRIMARY KEY AUTOINCREMENT,
    policy_name TEXT NOT NULL,
    policy_description TEXT,
    policy_author TEXT,
    rule_ids TEXT,
    created_time INTEGER,
    master BOOLEAN NOT NULL DEFAULT 0
);
