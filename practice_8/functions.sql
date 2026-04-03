CREATE OR REPLACE FUNCTION show_name_or_phone(pattern VARCHAR):
RETURNS TABLE(id INT, name VARCHAR(100), number VARCHAR(100)) 
LANGUAGE plpgsql
AS $$
BEGIN 
    RETURN QUERY
        SELECT * 
        FROM phonebook2 
        WHERE name ILIKE '%' || pattern || '%'
        OR number ILIKE '%' || pattern || '%';
END;
$$;

CREATE OR REPLACE FUNCTION get_phonebook_paginated(p_limit INT, p_offset INT ):
RETURNS TABLE(id INT,name VARCHAR, number VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN 
    RETURN QUERY 
        SELECT *
        FROM phonebook2
        ORDER BY id
        LIMIT p_limit OFFSET p_offset;
END;
$$;





CREATE OR REPLACE FUNCTION update_number(p_name VARCHAR, p_number VARCHAR) :
RETURN TEXT
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE  phonebook2 
    SET number=p_number
    WHERE name=p_name;
    IF FOUND THEN:
        RETURN "Updated"
    ELSE 
        RETURN "User not found"
END;
$$;