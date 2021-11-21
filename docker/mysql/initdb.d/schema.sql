CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(30) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    email VARCHAR(30) NOT NULL,
    name VARCHAR(30) NOT NULL,
    disabled BOOLEAN NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE paketSoal (
    kodePaket VARCHAR(30) NOT NULL,
    tanggal VARCHAR(255),
    deskripsi VARCHAR(255),
    PRIMARY KEY (kodePaket)
);

CREATE TABLE soal (
    id INT NOT NULL AUTO_INCREMENT,
    kodeSoal INT NOT NULL,
    pertanyaan VARCHAR(255) NOT NULL,
    pilihanJawaban VARCHAR(255) NOT NULL,
    kunciJawaban VARCHAR(255) NOT NULL,
    kodePaket VARCHAR(30) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE jawaban (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(30) NOT NULL,
    kodePaket VARCHAR(30) NOT NULL,
    kodeSoal INT NOT NULL,
    jawaban VARCHAR(30),
    PRIMARY KEY (id)
);

CREATE TABLE pembelian (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(30) NOT NULL,
    kodePaket VARCHAR(30) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE hasil (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(30) NOT NULL,
    kodePaket VARCHAR(30) NOT NULL,
    nilai INT,
    ranking INT,
    PRIMARY KEY (id)
);