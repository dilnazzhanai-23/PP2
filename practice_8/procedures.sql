CREATE OR REPLACE PROCEDURE insert_or_update(p_name VARCHAR, p_number VARCHAR):
LANGUAGE plpgsql
AS $$
BEGIN 
    IF EXIST(SELESCT 1 FROM phonebook2 WHERE name=p_name ) THEN
        UPDATE phonebook2
        SET number=p_number
        WHERE name=p_name;
    ELSE 
        INSERT INTO phonebook2(name,number)
        VALUES(p_name,p_number);
    END IF;   
END;
$$;

CREATE OR REPLACE PROCEDURE insert_many_users( p_name TEXT[], p_number TEXT[])
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(p_name, 1) LOOP

        IF p_number[i] ~ '^[+]{1}[0-9]{11}$'
        OR p_number[i] ~ '^[8]{1}[0-9]{10}$' THEN
            INSERT INTO phonebook2(name, number)
            VALUES (p_name[i], p_number[i])
            ON CONFLICT (number) DO NOTHING;

        ELSE
            RAISE NOTICE 'Invalid phone: %, %', p_name[i], p_number[i];
        END IF;
    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE delete(p_value VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN 
    DELETE FROM phonebook2
    WHERE name = p_value
    OR number = p_value;
END;
$$;
