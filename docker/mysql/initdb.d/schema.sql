CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(30) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    email VARCHAR(30) NOT NULL,
    name VARCHAR(30) NOT NULL,
    disabled BOOLEAN NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE soal (
    kodeSoal INT NOT NULL,
    pertanyaan VARCHAR(256) NOT NULL,
    pilihanJawaban VARCHAR(256) NOT NULL,
    kunciJawaban VARCHAR(256) NOT NULL,
    kodePaket CHAR(16) NOT NULL,
    PRIMARY KEY (kodeSoal)
    FOREIGN KEY (kodePaket) REFERENCES paketSoal(kodePaket)
);

CREATE TABLE jawaban (
    username VARCHAR(30) NOT  NULL,
    kodePaket CHAR(16) NOT NULL,
    kodeSoal INT NOT NULL,
    jawaban INT,
    PRIMARY KEY (username, kodePaket, kodeSoal),
    FOREIGN KEY (username) REFERENCES user(username),
    FOREIGN KEY (kodePaket) REFERENCES paketSoal(kodePaket),
    FOREIGN KEY (kodeSoal) REFERENCES soal(kodeSoal)
);