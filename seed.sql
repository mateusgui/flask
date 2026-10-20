-- Dados de exemplo do Registro de Incidentes (NOC).
-- Uso:
--   docker compose exec -T db psql -U noc_user -d noc_incidentes < seed.sql
--
-- ATENÇÃO: este arquivo APAGA o conteúdo das tabelas antes de inserir,
-- para poder ser rodado quantas vezes você quiser. É só para desenvolvimento.
--
-- Senha de todos os usuários: senha123
--
-- Duas coisas explicam a sintaxe menos comum aqui:
--   1) as colunas id são GENERATED ALWAYS AS IDENTITY, então para gravar um id
--      escolhido na mão é preciso dizer OVERRIDING SYSTEM VALUE;
--   2) as datas são relativas (now() - interval ...), assim os dados continuam
--      "recentes" em qualquer dia que o seed for carregado.

BEGIN;

TRUNCATE TABLE
    incidente_atualizacoes,
    incidente_bairros,
    incidentes,
    equipamentos,
    bairros,
    usuarios
RESTART IDENTITY CASCADE;


-- Usuários ---------------------------------------------------------------------
INSERT INTO usuarios (id, nome, email, senha_hash, perfil, ativo) OVERRIDING SYSTEM VALUE VALUES
(1, 'Carla Mendes',  'carla.mendes@noc.local',  'scrypt:32768:8:1$nJNabDWyYe34GEiu$258d2e27f08266411f088018fe77e0b747f960936adc3080f88c74970e12bbafbc9230b3ca8a4c366c4afaf157b781d880073e76f586d4e771226963352f6e61', 'supervisor', true),
(2, 'Mateus Vilela', 'mateus.vilela@noc.local', 'scrypt:32768:8:1$nJNabDWyYe34GEiu$258d2e27f08266411f088018fe77e0b747f960936adc3080f88c74970e12bbafbc9230b3ca8a4c366c4afaf157b781d880073e76f586d4e771226963352f6e61', 'operador',   true),
(3, 'Rafael Souza',  'rafael.souza@noc.local',  'scrypt:32768:8:1$nJNabDWyYe34GEiu$258d2e27f08266411f088018fe77e0b747f960936adc3080f88c74970e12bbafbc9230b3ca8a4c366c4afaf157b781d880073e76f586d4e771226963352f6e61', 'operador',   true);


-- Bairros (Campo Grande / MS) --------------------------------------------------
INSERT INTO bairros (id, nome, regiao) OVERRIDING SYSTEM VALUE VALUES
(1,  'Centro',             'Centro'),
(2,  'Amambaí',            'Centro'),
(3,  'Tiradentes',         'Bandeira'),
(4,  'Moreninha',          'Bandeira'),
(5,  'Carandá Bosque',     'Prosa'),
(6,  'Coophavila II',      'Lagoa'),
(7,  'Aero Rancho',        'Anhanduizinho'),
(8,  'Nova Lima',          'Segredo'),
(9,  'Santo Antônio',      'Imbirussu'),
(10, 'Jardim dos Estados', 'Centro');


-- Equipamentos -----------------------------------------------------------------
INSERT INTO equipamentos (id, nome, tipo, ip, bairro_id, ativo) OVERRIDING SYSTEM VALUE VALUES
(1, 'OLT Centro 01',        'olt',      '10.10.1.1',   1,    true),
(2, 'OLT Aero Rancho 01',   'olt',      '10.10.7.1',   7,    true),
(3, 'Switch Tiradentes',    'switch',   '10.20.3.10',  3,    true),
(4, 'Roteador Borda Prosa', 'roteador', '10.0.0.5',    5,    true),
(5, 'Servidor RADIUS',      'servidor', '10.0.100.20', NULL, true);


-- Incidentes -------------------------------------------------------------------
-- Os dois resolvidos dão MTTR de 135 min (crítica) e 50 min (alta): média 92,5 min.
INSERT INTO incidentes (
    id, titulo, descricao, categoria, severidade, status, clientes_afetados,
    equipamento_id, aberto_por_id, responsavel_id, aberto_em, resolvido_em,
    causa_raiz, solucao
) OVERRIDING SYSTEM VALUE VALUES
(1,
 'Rompimento de fibra na Av. Afonso Pena',
 'Clientes do Centro e Amambaí sem conexão. Alarme de LOS em várias ONUs da OLT Centro 01.',
 'rompimento_fibra', 'critica', 'resolvido', 420,
 1, 2, 1,
 now() - interval '3 days 5 hours',
 now() - interval '3 days 2 hours 45 minutes',
 'Cabo de fibra rompido por obra da prefeitura na avenida.',
 'Equipe de campo fez a fusão de 48 fibras no ponto do rompimento.'),

(2,
 'Queda de energia no POP Aero Rancho',
 'OLT Aero Rancho 01 sem resposta ao ping. Nobreak esgotou a bateria.',
 'queda_energia', 'alta', 'resolvido', 180,
 2, 3, 3,
 now() - interval '1 day 8 hours',
 now() - interval '1 day 7 hours 10 minutes',
 'Falta de energia da concessionária por mais tempo que a autonomia do nobreak.',
 'Gerador ligado e energia restabelecida. Aberto chamado para trocar baterias do nobreak.'),

(3,
 'Perda de pacotes no Switch Tiradentes',
 'Clientes reclamando de lentidão. Monitoramento mostra 15% de perda de pacotes no uplink.',
 'falha_equipamento', 'media', 'em_andamento', 95,
 3, 2, 2,
 now() - interval '2 hours',
 NULL, NULL, NULL),

(4,
 'Clientes sem autenticação PPPoE na Coophavila II',
 'Vários clientes com erro de autenticação desde o fim da tarde.',
 'outro', 'alta', 'aberto', 60,
 NULL, 3, NULL,
 now() - interval '35 minutes',
 NULL, NULL, NULL),

(5,
 'Manutenção programada no Roteador Borda Prosa',
 'Atualização de firmware agendada para a madrugada. Interrupção prevista de 20 minutos.',
 'manutencao_programada', 'baixa', 'aberto', 250,
 4, 1, 1,
 now() - interval '1 hour',
 NULL, NULL, NULL),

(6,
 'Alarme de queda no Nova Lima',
 'Alarme disparou, mas os clientes estavam navegando normalmente.',
 'outro', 'baixa', 'cancelado', 0,
 NULL, 2, 1,
 now() - interval '5 days',
 NULL, NULL, NULL);


-- Bairros afetados por cada incidente (N:N) ------------------------------------
INSERT INTO incidente_bairros (incidente_id, bairro_id) VALUES
(1, 1), (1, 2), (1, 10),
(2, 7),
(3, 3), (3, 4),
(4, 6),
(5, 5),
(6, 8);


-- Linha do tempo dos incidentes ------------------------------------------------
INSERT INTO incidente_atualizacoes (id, incidente_id, usuario_id, mensagem, status_novo, criado_em) OVERRIDING SYSTEM VALUE VALUES
(1, 1, 1, 'Assumi o incidente. Equipe de campo acionada.',                    'em_andamento', now() - interval '3 days 4 hours 50 minutes'),
(2, 1, 1, 'Rompimento localizado próximo à Rua 14 de Julho.',                 NULL,           now() - interval '3 days 4 hours'),
(3, 1, 1, 'Fusão concluída, clientes voltando a conectar.',                   'resolvido',    now() - interval '3 days 2 hours 45 minutes'),
(4, 2, 3, 'Concessionária confirmou falta de energia na região.',             'em_andamento', now() - interval '1 day 7 hours 55 minutes'),
(5, 2, 3, 'Gerador ligado, OLT respondendo de novo.',                         'resolvido',    now() - interval '1 day 7 hours 10 minutes'),
(6, 3, 2, 'Analisando logs do switch. Suspeita de porta de uplink com erro.', 'em_andamento', now() - interval '1 hour 45 minutes'),
(7, 6, 1, 'Confirmado alarme falso com os clientes. Cancelando.',             'cancelado',    now() - interval '4 days 23 hours 40 minutes');


-- Os ids acima foram inseridos na mão, então as sequências precisam ser avançadas,
-- senão o próximo cadastro feito pela aplicação tentaria repetir o id 1.
SELECT setval(pg_get_serial_sequence('usuarios', 'id'),               (SELECT max(id) FROM usuarios));
SELECT setval(pg_get_serial_sequence('bairros', 'id'),                (SELECT max(id) FROM bairros));
SELECT setval(pg_get_serial_sequence('equipamentos', 'id'),           (SELECT max(id) FROM equipamentos));
SELECT setval(pg_get_serial_sequence('incidentes', 'id'),             (SELECT max(id) FROM incidentes));
SELECT setval(pg_get_serial_sequence('incidente_atualizacoes', 'id'), (SELECT max(id) FROM incidente_atualizacoes));

COMMIT;
