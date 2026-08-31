-- Moffat Bay Lodge ERD schema
-- Target: MySQL Community Server 8.4 LTS
-- Prerequisite: database/migrations/000_create_database.sql

USE moffat_bay;

CREATE TABLE IF NOT EXISTS customer (
    customer_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(254) NOT NULL,
    telephone VARCHAR(32) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT pk_customer PRIMARY KEY (customer_id),
    CONSTRAINT uk_customer_email UNIQUE (email),
    CONSTRAINT chk_customer_first_name_not_blank
        CHECK (CHAR_LENGTH(TRIM(first_name)) > 0),
    CONSTRAINT chk_customer_last_name_not_blank
        CHECK (CHAR_LENGTH(TRIM(last_name)) > 0),
    CONSTRAINT chk_customer_email_not_blank
        CHECK (CHAR_LENGTH(TRIM(email)) > 0),
    CONSTRAINT chk_customer_telephone_not_blank
        CHECK (CHAR_LENGTH(TRIM(telephone)) > 0),
    CONSTRAINT chk_customer_password_hash_not_blank
        CHECK (CHAR_LENGTH(TRIM(password_hash)) > 0)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS room_type (
    room_type_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    room_name VARCHAR(100) NOT NULL,
    room_size VARCHAR(100) NOT NULL,
    max_guests SMALLINT UNSIGNED NOT NULL,
    current_nightly_rate DECIMAL(10, 2) UNSIGNED NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT pk_room_type PRIMARY KEY (room_type_id),
    CONSTRAINT uk_room_type_room_name UNIQUE (room_name),
    CONSTRAINT chk_room_type_room_name_not_blank
        CHECK (CHAR_LENGTH(TRIM(room_name)) > 0),
    CONSTRAINT chk_room_type_room_size_not_blank
        CHECK (CHAR_LENGTH(TRIM(room_size)) > 0),
    CONSTRAINT chk_room_type_max_guests_positive CHECK (max_guests > 0),
    CONSTRAINT chk_room_type_rate_positive CHECK (current_nightly_rate > 0)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS reservation (
    reservation_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    customer_id BIGINT UNSIGNED NOT NULL,
    room_type_id SMALLINT UNSIGNED NOT NULL,
    guest_count SMALLINT UNSIGNED NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    number_of_nights SMALLINT UNSIGNED NOT NULL,
    nightly_rate DECIMAL(10, 2) UNSIGNED NOT NULL,
    total_cost DECIMAL(12, 2) UNSIGNED NOT NULL,
    confirmed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_reservation PRIMARY KEY (reservation_id),
    CONSTRAINT fk_reservation_customer FOREIGN KEY (customer_id)
        REFERENCES customer (customer_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    CONSTRAINT fk_reservation_room_type FOREIGN KEY (room_type_id)
        REFERENCES room_type (room_type_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    CONSTRAINT chk_reservation_guest_count_positive CHECK (guest_count > 0),
    CONSTRAINT chk_reservation_date_order CHECK (check_out_date > check_in_date),
    CONSTRAINT chk_reservation_nights_positive CHECK (number_of_nights > 0),
    CONSTRAINT chk_reservation_rate_positive CHECK (nightly_rate > 0),
    CONSTRAINT chk_reservation_total_positive CHECK (total_cost > 0),
    CONSTRAINT chk_reservation_night_count CHECK (
        number_of_nights = DATEDIFF(check_out_date, check_in_date)
    ),
    CONSTRAINT chk_reservation_total CHECK (
        total_cost = ROUND(nightly_rate * number_of_nights, 2)
    ),
    INDEX ix_reservation_customer_id (customer_id),
    INDEX ix_reservation_room_type_id (room_type_id),
    INDEX ix_reservation_stay_dates (check_in_date, check_out_date)
) ENGINE = InnoDB;

