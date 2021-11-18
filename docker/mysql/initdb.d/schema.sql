CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(30) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    email VARCHAR(30) NOT NULL,
    name VARCHAR(30) NOT NULL,
    disabled BOOLEAN NOT NULL,
    PRIMARY KEY (id)
);