CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE v_contact_id INT;
BEGIN
    SELECT id INTO v_contact_id FROM phonebook2 
    WHERE first_name ILIKE '%' || p_contact_name || '%' LIMIT 1;
    IF v_contact_id IS NOT NULL THEN
        INSERT INTO phones (contact_id, phone, type) VALUES (v_contact_id, p_phone, p_type);
    ELSE
        RAISE NOTICE 'Contact % not found', p_contact_name;
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE v_contact_id INT; v_group_id INT;
BEGIN
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    IF v_group_id IS NULL THEN
        INSERT INTO groups (name) VALUES (p_group_name) RETURNING id INTO v_group_id;
    END IF;
    SELECT id INTO v_contact_id FROM phonebook2 
    WHERE first_name ILIKE '%' || p_contact_name || '%' LIMIT 1;
    IF v_contact_id IS NOT NULL THEN
        UPDATE phonebook2 SET group_id = v_group_id WHERE id = v_contact_id;
    ELSE
        RAISE NOTICE 'Contact % not found', p_contact_name;
    END IF;
END;
$$;


CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(id INT, first_name TEXT, second_name TEXT, email VARCHAR, phone VARCHAR, group_name VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT c.id, c.first_name, c.second_name, c.email, p.phone, g.name
    FROM phonebook2 c
    LEFT JOIN phones p ON c.id = p.contact_id
    LEFT JOIN groups g ON c.group_id = g.id
    WHERE c.first_name ILIKE '%' || p_query || '%'
       OR c.second_name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%';
END;
$$ LANGUAGE plpgsql;