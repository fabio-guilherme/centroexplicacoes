-- Consultar que professores lecionam determinada disciplina
SELECT professor.*
FROM professor
JOIN disciplina_has_professor ON professor.idProfessor = disciplina_has_professor.Professor_idProfessor
JOIN disciplina ON disciplina_has_professor.Disciplina_idDisciplina = disciplina.idDisciplina
WHERE disciplina.Designacao = 'NomeDisciplina';

-- Selecionar todos os alunos e seus detalhes
SELECT * FROM aluno;

-- Buscar disciplinas e seus respectivos valores
SELECT Designacao, valor FROM disciplina;

-- Listar todos os professores e suas informações de contato
SELECT Nome, Contato FROM professor;

-- Obter detalhes completos de todas as inscrições
SELECT inscrição.*, aluno.Nome AS NomeAluno, professor.Nome AS NomeProfessor, sala.idSala, disciplina.Designacao
FROM inscrição
JOIN aluno ON inscrição.Aluno_idAluno = aluno.idAluno
JOIN professor ON inscrição.Professor_idProfessor = professor.idProfessor
JOIN sala ON inscrição.Sala_idSala = sala.idSala
JOIN disciplina ON inscrição.Disciplina_idDisciplina = disciplina.idDisciplina;

-- Encontrar todas as aulas associadas a uma disciplina específica
SELECT aula.*
FROM aula
JOIN inscrição ON aula.Inscrição_idInscrição = inscrição.idInscrição
JOIN disciplina ON inscrição.Disciplina_idDisciplina = disciplina.idDisciplina
WHERE disciplina.Designacao = 'NomeDisciplina';

-- Adicionar um novo aluno ao banco de dados
INSERT INTO aluno (Nome, Contato, Nensino, Nif)
VALUES ('NovoAluno', 'ContatoAluno', 'NivelEnsino', 'NIFAluno');

-- Registrar uma nova disciplina no banco de dados
INSERT INTO disciplina (Designacao, valor)
VALUES ('NovaDisciplina', 'ValorDisciplina');

-- Atribuir um professor a uma disciplina (criar uma nova associação)
INSERT INTO disciplina_has_professor (Disciplina_idDisciplina, Professor_idProfessor)
VALUES (
    (SELECT idDisciplina FROM disciplina WHERE Designacao = 'NomeDisciplina'),
    (SELECT idProfessor FROM professor WHERE Nome = 'NomeProfessor')
);

-- Atualizar o contato de um aluno existente
UPDATE aluno
SET Contato = 'NovoContato'
WHERE Nome = 'NomeAluno';

-- Alterar o nome de uma disciplina existente
UPDATE disciplina
SET Designacao = 'NovoNome'
WHERE Designacao = 'NomeDisciplina';

-- Remover um aluno do banco de dados
DELETE FROM aluno
WHERE Nome = 'NomeAluno';

-- Desvincular um professor de uma disciplina
DELETE FROM disciplina_has_professor
WHERE Disciplina_idDisciplina = (SELECT idDisciplina FROM disciplina WHERE Designacao = 'NomeDisciplina')
  AND Professor_idProfessor = (SELECT idProfessor FROM professor WHERE Nome = 'NomeProfessor');

-- Encontrar todos os alunos inscritos em uma determinada disciplina
SELECT aluno.*
FROM aluno
JOIN inscrição ON aluno.idAluno = inscrição.Aluno_idAluno
JOIN disciplina ON inscrição.Disciplina_idDisciplina = disciplina.idDisciplina
WHERE disciplina.Designacao = 'NomeDisciplina';

-- Listar todas as disciplinas que um professor específico está ensinando
SELECT disciplina.*
FROM disciplina
JOIN disciplina_has_professor ON disciplina.idDisciplina = disciplina_has_professor.Disciplina_idDisciplina
JOIN professor ON disciplina_has_professor.Professor_idProfessor = professor.idProfessor
WHERE professor.Nome = 'NomeProfessor';

-- Contar o número de alunos inscritos por disciplina
SELECT disciplina.Designacao, COUNT(inscrição.Aluno_idAluno) AS NumeroAlunosInscritos
FROM disciplina
JOIN inscrição ON disciplina.idDisciplina = inscrição.Disciplina_idDisciplina
GROUP BY disciplina.Designacao;

-- Determinar o número de aulas que um professor está dando em um semestre
SELECT professor.Nome, COUNT(aula.idAula) AS NumeroAulas
FROM aula
JOIN inscrição ON aula.Inscrição_idInscrição = inscrição.idInscrição
JOIN professor ON inscrição.Professor_idProfessor = professor.idProfessor
WHERE professor.Nome = 'NomeProfessor'
GROUP BY professor.Nome;

-- Listar as salas de aula com capacidade acima de um certo número
SELECT * FROM sala
WHERE Capacidade > CapacidadeMinima;

-- Mostrar o horário das aulas para um aluno específico
SELECT aula.data, aula.hora, disciplina.Designacao
FROM aula
JOIN inscrição ON aula.Inscrição_idInscrição = inscrição.idInscrição
JOIN aluno ON inscrição.Aluno_idAluno = aluno.idAluno
JOIN disciplina ON inscrição.Disciplina_idDisciplina = disciplina.idDisciplina
WHERE aluno.Nome = 'NomeAluno';

-- Verificar quais disciplinas estão com a inscrição aberta com base em critérios como capacidade máxima não atingida
SELECT disciplina.Designacao, sala.idSala
FROM disciplina
JOIN inscrição ON inscrição.Disciplina_idDisciplina = disciplina.idDisciplina
JOIN sala on sala.idSala = inscrição.Sala_idSala
GROUP BY disciplina.idDisciplina, disciplina.Designacao, sala.idSala, sala.Capacidade
HAVING sala.Capacidade - COUNT(inscrição.idInscrição) > 0;

-- Listar alunos com base em um certo nível de ensino
SELECT * FROM aluno
WHERE Nensino = 'NivelEnsinoDesejado';