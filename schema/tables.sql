BEGIN;

-- DROP TABLE IF EXISTS ClauseTable;
-- DROP TABLE IF EXISTS WordTable;
-- DROP TABLE IF EXISTS NodeTable;
-- DROP TABLE IF EXISTS NodeRelationTable;


CREATE TABLE IF NOT EXISTS ClauseTable (
    /*
        inclusion_type 0 => include
        inclusion_type 1 => exclude
    */
    inclusion_type INTEGER CHECK(inclusion_type in (0, 1)),
    /*
        threshold_type 0 => integer
        threshold_type 1 => percentage
    */
    threshold_type INTEGER CHECK(threshold_type in (0, 1)),
    threshold_value INTEGER,

    node_id INTEGER NOT NULL,
    
    FOREIGN KEY (node_id) REFERENCES NodeTable(rowid)
);

CREATE TABLE IF NOT EXISTS WordTable (
    word VARCHAR(255) NOT NULL,
    clause_id INTEGER,
    FOREIGN KEY (clause_id) REFERENCES ClauseTable(rowid)
);

CREATE TABLE IF NOT EXISTS NodeTable (
    node_name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS NodeRelationTable (
    parent_id INTEGER NOT NULL,
    child_id INTEGER NOT NULL,
    FOREIGN KEY (parent_id) REFERENCES NodeTable(rowid),
    FOREIGN KEY (child_id) REFERENCES NodeTable(rowid),
    UNIQUE (parent_id, child_id)
);

COMMIT;
