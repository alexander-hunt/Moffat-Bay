-- Module 4 verification queries. Run after the schema and development seed.

USE moffat_bay;

SELECT * FROM customer ORDER BY customer_id;
SELECT * FROM room_type ORDER BY room_type_id;
SELECT * FROM reservation ORDER BY reservation_id;

-- Integration view used to confirm both ERD relationships and stored totals.
SELECT
    r.reservation_id,
    c.email AS customer_email,
    rt.room_name,
    r.guest_count,
    r.check_in_date,
    r.check_out_date,
    r.number_of_nights,
    r.nightly_rate,
    r.total_cost,
    r.confirmed_at
FROM reservation AS r
JOIN customer AS c ON c.customer_id = r.customer_id
JOIN room_type AS rt ON rt.room_type_id = r.room_type_id
ORDER BY r.reservation_id;

