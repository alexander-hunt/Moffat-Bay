-- Fictional development data. Do not use in production.
-- Idempotent for the fixed natural keys and IDs below.

USE moffat_bay;

INSERT INTO room_type (
    room_type_id, room_name, room_size, max_guests,
    current_nightly_rate, active
) VALUES
    (1, 'Pinewood Studio',
     'Cozy room for 1 or 2. Some views of Joviedsa forest area.',
     2, 145.00, TRUE),

    (2, 'Alder Suite',
     'Large bedroom with open entertainment room. Amazing views of the Puget Sound.',
     5, 195.00, TRUE),

    (3, 'Maple Cabin',
     '3 bedrooms and a spacious family room. Direct access to Joviedsa hiking trails and canoeing access to the Puget Sound.',
     6, 245.00, TRUE),

    (4, 'Douglas Fir Outpost',
     'Ultimate Family Retreat. Large private cabin with 5 bedrooms, family room, game room, seating areas indoors/outdoors.',
     10, 495.00, TRUE)

ON DUPLICATE KEY UPDATE
    room_name = VALUES(room_name),
    room_size = VALUES(room_size),
    max_guests = VALUES(max_guests),
    current_nightly_rate = VALUES(current_nightly_rate),
    active = VALUES(active);


-- Passwords are fictional development-only values hashed in Werkzeug's
-- pbkdf2:sha256 format; plaintext is intentionally not stored here.

INSERT INTO customer (
    customer_id, first_name, last_name, email, telephone, password_hash
) VALUES
    (1, 'Maya', 'Chen', 'maya.chen@example.com', '360-555-0101',
     'pbkdf2:sha256:1000000$moffatseed01$534379c2396b57fd16a02ba88baa53af39fa3e0a454eee21dfd07e35df7c04a6'),

    (2, 'Daniel', 'Ruiz', 'daniel.ruiz@example.com', '360-555-0102',
     'pbkdf2:sha256:1000000$moffatseed02$927ccdd86474ff5a878027c76d5bfc40c0ac4108ed3e0eed62292d493941a185'),

    (3, 'Priya', 'Patel', 'priya.patel@example.com', '360-555-0103',
     'pbkdf2:sha256:1000000$moffatseed03$961d42779b06d0104cfa50c43f731f16fe29773603d943bf93b090a27abc14d8a')

ON DUPLICATE KEY UPDATE
    first_name = VALUES(first_name),
    last_name = VALUES(last_name),
    telephone = VALUES(telephone),
    password_hash = VALUES(password_hash);


INSERT INTO reservation (
    reservation_id, customer_id, room_type_id, guest_count,
    check_in_date, check_out_date, number_of_nights,
    nightly_rate, total_cost, confirmed_at
) VALUES
    (1, 1, 2, 2, '2026-09-14', '2026-09-18',
     4, 195.00, 780.00, '2026-08-28 10:00:00'),

    (2, 2, 4, 2, '2026-10-02', '2026-10-05',
     3, 495.00, 1485.00, '2026-08-28 10:05:00'),

    (3, 3, 3, 4, '2026-11-20', '2026-11-25',
     5, 245.00, 1225.00, '2026-08-28 10:10:00')

ON DUPLICATE KEY UPDATE
    customer_id = VALUES(customer_id),
    room_type_id = VALUES(room_type_id),
    guest_count = VALUES(guest_count),
    check_in_date = VALUES(check_in_date),
    check_out_date = VALUES(check_out_date),
    number_of_nights = VALUES(number_of_nights),
    nightly_rate = VALUES(nightly_rate),
    total_cost = VALUES(total_cost),
    confirmed_at = VALUES(confirmed_at);