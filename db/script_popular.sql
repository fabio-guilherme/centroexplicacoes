-- Populando a tabela 'aluno'
INSERT INTO aluno (Nome, Contato, Nensino, Nif)
VALUES
    ('João Silva', '123456789', '9º Ano', '123456789'),
    ('Maria Oliveira', '987654321', '12º Ano', '987654321'),
    ('Carlos Santos', '111222333', '10º Ano', '111222333');

-- Populando a tabela 'professor'
INSERT INTO professor (Nome, Contato, Nif)
VALUES
    ('Ana Pereira', '555666777', '555666777'),
    ('Rui Martins', '999888777', '999888777'),
    ('Isabel Sousa', '444333222', '444333222');

-- Populando a tabela 'disciplina'
INSERT INTO disciplina (Designacao, valor)
VALUES
    ('Matemática', '150'),
    ('Português', '120'),
    ('Ciências', '180');

-- Populando a tabela 'sala'
INSERT INTO sala (Capacidade)
VALUES
    (30),
    (25),
    (35);