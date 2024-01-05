    -- Eliminar tabelas se existirem
DROP TABLE IF EXISTS `disciplina_has_professor`;
DROP TABLE IF EXISTS `aula`;
DROP TABLE IF EXISTS `inscrição`;
DROP TABLE IF EXISTS `sala`;
DROP TABLE IF EXISTS `aluno`;
DROP TABLE IF EXISTS `professor`;
DROP TABLE IF EXISTS `disciplina`;

-- Tabela 'aluno'
CREATE TABLE `aluno` (
    `idAluno` int AUTO_INCREMENT NOT NULL,
    `Nome` varchar(45) DEFAULT NULL,
    `Contato` char(9) DEFAULT NULL,
    `Nensino` varchar(45) DEFAULT NULL,
    `Nif` char(9) DEFAULT NULL,
    PRIMARY KEY (`idAluno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Tabela 'disciplina'
CREATE TABLE `disciplina` (
    `idDisciplina` int AUTO_INCREMENT NOT NULL,
    `Designacao` varchar(45) DEFAULT NULL,
    `valor` varchar(45) DEFAULT NULL,
    PRIMARY KEY (`idDisciplina`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Tabela 'professor'
CREATE TABLE `professor` (
    `idProfessor` int AUTO_INCREMENT NOT NULL,
    `Nome` varchar(45) DEFAULT NULL,
    `Contato` char(9) DEFAULT NULL,
    `Nif` char(9) DEFAULT NULL,
    PRIMARY KEY (`idProfessor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Tabela 'disciplina_has_professor'
CREATE TABLE `disciplina_has_professor` (
    `Disciplina_idDisciplina` int NOT NULL,
    `Professor_idProfessor` int NOT NULL,
    PRIMARY KEY (`Disciplina_idDisciplina`,`Professor_idProfessor`),
    KEY `Professor_idProfessor` (`Professor_idProfessor`),
    CONSTRAINT `disciplina_has_professor_ibfk_1` FOREIGN KEY (`Disciplina_idDisciplina`) REFERENCES `disciplina` (`idDisciplina`),
    CONSTRAINT `disciplina_has_professor_ibfk_2` FOREIGN KEY (`Professor_idProfessor`) REFERENCES `professor` (`idProfessor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Tabela 'sala'
CREATE TABLE `sala` (
    `idSala` int AUTO_INCREMENT NOT NULL,
    `Capacidade` int DEFAULT NULL,
    PRIMARY KEY (`idSala`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Tabela 'inscrição'
CREATE TABLE `inscrição` (
    `idInscrição` int AUTO_INCREMENT NOT NULL,
    `Aluno_idAluno` int DEFAULT NULL,
    `Professor_idProfessor` int DEFAULT NULL,
    `Sala_idSala` int DEFAULT NULL,
    `Disciplina_idDisciplina` int DEFAULT NULL,
    PRIMARY KEY (`idInscrição`),
    KEY `Aluno_idAluno` (`Aluno_idAluno`),
    KEY `Professor_idProfessor` (`Professor_idProfessor`),
    KEY `Sala_idSala` (`Sala_idSala`),
    KEY `Disciplina_idDisciplina` (`Disciplina_idDisciplina`),
    CONSTRAINT `inscrição_ibfk_1` FOREIGN KEY (`Aluno_idAluno`) REFERENCES `aluno` (`idAluno`),
    CONSTRAINT `inscrição_ibfk_2` FOREIGN KEY (`Professor_idProfessor`) REFERENCES `professor` (`idProfessor`),
    CONSTRAINT `inscrição_ibfk_3` FOREIGN KEY (`Sala_idSala`) REFERENCES `sala` (`idSala`),
    CONSTRAINT `inscrição_ibfk_4` FOREIGN KEY (`Disciplina_idDisciplina`) REFERENCES `disciplina` (`idDisciplina`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Tabela 'aula'
CREATE TABLE `aula` (
    `idAula` int AUTO_INCREMENT NOT NULL,
    `data` date DEFAULT NULL,
    `hora` varchar(45) DEFAULT NULL,
    `Inscrição_idInscrição` int DEFAULT NULL,
    PRIMARY KEY (`idAula`),
    KEY `Inscrição_idInscrição` (`Inscrição_idInscrição`),
    CONSTRAINT `aula_ibfk_1` FOREIGN KEY (`Inscrição_idInscrição`) REFERENCES `inscrição` (`idInscrição`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
