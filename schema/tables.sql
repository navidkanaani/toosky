CREATE TABLE ClauseTable (
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
    threshold_value INTEGER
);

CREATE TABLE WordTable (
	word VARCHAR(255),
    clause_id INTEGER,
    FOREIGN KEY (clause_id) REFERENCES ClauseTable(rowid)
);

