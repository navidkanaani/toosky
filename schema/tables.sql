BEGIN;

-- DROP TABLE IF EXISTS FilterTable;
-- DROP TABLE IF EXISTS WordTable;
-- DROP TABLE IF EXISTS NodeTable;
-- DROP TABLE IF EXISTS NodeRelationTable;


CREATE TABLE IF NOT EXISTS FilterTable (
    eid VARCHAR(31) NOT NULL UNIQUE,

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

    rule_eid INTEGER NOT NULL,
    
    FOREIGN KEY (rule_eid) REFERENCES RuleTable(eid)
);

CREATE TABLE IF NOT EXISTS WordTable (
    eid VARCHAR(31) NOT NULL UNIQUE,
    word VARCHAR(255) NOT NULL,
    filter_eid INTEGER,
    FOREIGN KEY (filter_eid) REFERENCES FilterTable(rowid)
);

CREATE TABLE IF NOT EXISTS RuleTable (
    eid VARCHAR(31) NOT NULL UNIQUE,
    rule_name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS NodeTable (
    eid VARCHAR(31) NOT NULL UNIQUE,
    node_name VARCHAR(255) NOT NULL UNIQUE,
    description VARCHAR(1023),
    parent_eid VARCHAR(31),
    rule_eid VARCHAR(31),
    level INTEGER,
    FOREIGN KEY (rule_eid) REFERENCES RuleTable(eid),
    FOREIGN KEY (parent_eid) REFERENCES NodeTable(eid)

);

-- CREATE TABLE IF NOT EXISTS NodeRelationTable (
--     eid VARCHAR(31) NOT NULL UNIQUE,
--     parent_eid INTEGER NOT NULL,
--     child_eid INTEGER NOT NULL,
--     FOREIGN KEY (parent_eid) REFERENCES NodeTable(rowid),
--     FOREIGN KEY (child_eid) REFERENCES NodeTable(rowid),
--     UNIQUE (parent_eid, child_eid),
-- );

COMMIT;
