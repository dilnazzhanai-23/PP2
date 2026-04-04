CREATE OR REPLACE FUNCTION show_name_or_phone(pattern VARCHAR)
RETURNS TABLE(id INT, name VARCHAR(100), number VARCHAR(100)) 
LANGUAGE plpgsql
AS $$
BEGIN 
    RETURN QUERY
        SELECT p.id, p.name, p.number
        FROM phonebook2 p
        WHERE p.name ILIKE '%' || pattern || '%'
        OR p.number ILIKE '%' || pattern || '%';
END;
$$;

CREATE OR REPLACE FUNCTION get_phonebook_paginated(p_limit INT, p_offset INT )
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
