CREATE TABLE Doctor(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE History(
    id SERIAl PRIMARY KEY,
    doctor_id INTEGER REFERENCES Doctor(id),
    patient_name VARCHAR(100) NOT NULL,
    date_of_treatment TIMESTAMP NOT NULL
);