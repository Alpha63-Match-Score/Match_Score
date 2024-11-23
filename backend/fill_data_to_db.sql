

-- USERS -----------------------------------------------------------------

INSERT INTO "user" (id, email, password_hash, role, created_at)
VALUES
('e1111111-1111-4111-1111-111111111111', 'admin@example.com',
'$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO',
'ADMIN', CURRENT_TIMESTAMP),

('e2222222-2222-4222-2222-222222222222', 'director@example.com',
'$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO',
'DIRECTOR', CURRENT_TIMESTAMP),

('e3333333-3333-4333-3333-333333333333', 'user@example.com',
'$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO',
'USER', CURRENT_TIMESTAMP),

('e4444444-4444-4444-4444-444444444444', 'purr.programmer@example.com',
'$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO',
'PLAYER', CURRENT_TIMESTAMP),

('e5555555-5555-4555-5555-555555555555', 'whiskers.warrior@example.com',
'$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO',
'USER', CURRENT_TIMESTAMP),

('e6666666-6666-4666-6666-666666666666', 'meow.sniper@example.com',
'$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO',
'USER', CURRENT_TIMESTAMP),

('e7777777-7777-4777-7777-777777777777', 'kitty.sniper@example.com',
'$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO',
'USER', CURRENT_TIMESTAMP),

('e8888888-8888-4888-8888-888888888888', 'paw.striker@example.com',
'$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO',
'USER', CURRENT_TIMESTAMP),

('e9999999-9999-4999-9999-999999999999', 'ninja.cat@example.com',
'$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO',
'USER', CURRENT_TIMESTAMP),

('e0000000-0000-4000-0000-000000000000', 'furry.force@example.com',
'$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO',
'USER', CURRENT_TIMESTAMP);


-- TOURNAMENTS --------------------------------------------

INSERT INTO tournament (id, title, tournament_format, start_date, end_date, prize_pool, current_stage, director_id)
VALUES
-- PAST TOURNAMENT
('11111111-1111-4111-1111-111111111111',
'Kitten Strike Winter Championship 2024',
'SINGLE_ELIMINATION',
'2024-01-15 11:00:00',
'2024-02-01 23:59:59',
5000,
'FINISHED',
'e2222222-2222-4222-2222-222222222222'),

-- CURRENT TOURNAMENT
('33333333-3333-4333-3333-333333333333',
'Whiskers League Season 1',
'ROUND_ROBIN',
'2024-03-01 11:00:00',
'2024-04-15 23:59:59',
10000,
'GROUP_STAGE',
'e2222222-2222-4222-2222-222222222222'),

-- FUTURE TOURNAMENT
('44444444-4444-4444-4444-444444444444',
'Paw Masters Showdown',
'ONE_OFF_MATCH',
'2024-05-01 11:00:00',
'2024-05-01 23:59:59',
3000,
'FINAL',
'e2222222-2222-4222-2222-222222222222');



-- TEAMS --------------------------------------------

INSERT INTO team (id, name, played_games, won_games, tournament_id)
VALUES
-- Teams for the past tournament (FINISHED)
('aaaaaaaa-1111-4111-1111-111111111111', 'Purrfect Snipers', 45, 32, '11111111-1111-4111-1111-111111111111'),
('aaaaaaaa-2222-4222-2222-222222222222', 'Catnip Commandos', 38, 25, '11111111-1111-4111-1111-111111111111'),
('aaaaaaaa-3333-4333-3333-333333333333', 'Whisker Warriors', 42, 28, '11111111-1111-4111-1111-111111111111'),
('aaaaaaaa-4444-4444-4444-444444444444', 'Feline Force', 41, 29, '11111111-1111-4111-1111-111111111111'),

-- Teams for the current tournament (GROUP_STAGE)
('bbbbbbbb-1111-4111-1111-111111111111', 'Meow Mercenaries', 28, 18, '33333333-3333-4333-3333-333333333333'),
('bbbbbbbb-2222-4222-2222-222222222222', 'Claw Crushers', 25, 15, '33333333-3333-4333-3333-333333333333'),
('bbbbbbbb-3333-4333-3333-333333333333', 'Kitty Kombat', 30, 20, '33333333-3333-4333-3333-333333333333'),
('bbbbbbbb-4444-4444-4444-444444444444', 'Pawsome Predators', 27, 16, '33333333-3333-4333-3333-333333333333'),

-- Teams for the future tournament (FINAL)
('cccccccc-1111-4111-1111-111111111111', 'Furry Fury', 35, 22, '44444444-4444-4444-4444-444444444444'),
('cccccccc-2222-4222-2222-222222222222', 'Ninja Neko', 32, 21, '44444444-4444-4444-4444-444444444444'),

-- Teams without tournament
('dddddddd-1111-4111-1111-111111111111', 'Scratch Squadron', 22, 12, NULL),
('dddddddd-2222-4222-2222-222222222222', 'Feline Phantoms', 20, 11, NULL),
('dddddddd-3333-4333-3333-333333333333', 'Cat Commandos Elite', 25, 15, NULL),
('dddddddd-4444-4444-4444-444444444444', 'Whisker Wizards', 18, 9, NULL),
('dddddddd-5555-4555-5555-555555555555', 'Paw Pirates', 15, 7, NULL),
('dddddddd-6666-4666-6666-666666666666', 'Kitty Knights', 28, 16, NULL),
('dddddddd-7777-4777-7777-777777777777', 'Meow Marines', 24, 13, NULL),
('dddddddd-8888-4888-8888-888888888888', 'Feline Fighters', 21, 10, NULL),
('dddddddd-9999-4999-9999-999999999999', 'Cat Crusaders', 19, 8, NULL),
('dddddddd-0000-4000-0000-000000000000', 'Purr Patrol', 17, 6, NULL);



-- PLAYERS --------------------------------------------

-- Purrfect Snipers (winners in tournament 1)
INSERT INTO player (id, username, first_name, last_name, country, played_games, won_games, user_id, team_id)
VALUES
('aaaaaaaa-1111-4111-1111-aaaaaaaaaaaa', 'WhiskerAim', 'Felix', 'Pawson', 'Bulgaria', 45, 32, 'e4444444-4444-4444-4444-444444444444', 'aaaaaaaa-1111-4111-1111-111111111111'),
('aaaaaaaa-2222-4222-2222-aaaaaaaaaaaa', 'PurrSniper', 'Luna', 'Clawford', 'Romania', 42, 30, NULL, 'aaaaaaaa-1111-4111-1111-111111111111'),
('aaaaaaaa-3333-4333-3333-aaaaaaaaaaaa', 'CatEye', 'Oscar', 'Whiskerston', 'Greece', 40, 28, NULL, 'aaaaaaaa-1111-4111-1111-111111111111'),
('aaaaaaaa-4444-4444-4444-aaaaaaaaaaaa', 'SneakyPaw', 'Milo', 'Kittenson', 'Serbia', 38, 25, NULL, 'aaaaaaaa-1111-4111-1111-111111111111'),
('aaaaaaaa-5555-4555-5555-aaaaaaaaaaaa', 'NinjaKitty', 'Leo', 'Scratchington', 'Bulgaria', 41, 29, NULL, 'aaaaaaaa-1111-4111-1111-111111111111');

-- Catnip Commandos (from past tournament)
INSERT INTO player (id, username, first_name, last_name, country, played_games, won_games, user_id, team_id)
VALUES
('a2222222-1111-4111-1111-111111111111', 'CatnipKing', 'Max', 'Meowster', 'Romania', 35, 22, NULL, 'aaaaaaaa-2222-4222-2222-222222222222'),
('a2222222-2222-4222-2222-222222222222', 'PawPatrol', 'Bella', 'Purrington', 'Bulgaria', 33, 20, NULL, 'aaaaaaaa-2222-4222-2222-222222222222'),
('a2222222-3333-4333-3333-333333333333', 'PurrMaster', 'Charlie', 'Furbottom', 'Greece', 34, 21, NULL, 'aaaaaaaa-2222-4222-2222-222222222222'),
('a2222222-4444-4444-4444-444444444444', 'ClawCommander', 'Lucy', 'Tailsworth', 'Serbia', 32, 19, NULL, 'aaaaaaaa-2222-4222-2222-222222222222'),
('a2222222-5555-4555-5555-555555555555', 'WhiskerOps', 'Tiger', 'Pawsome', 'Bulgaria', 31, 18, NULL, 'aaaaaaaa-2222-4222-2222-222222222222');

-- Whisker Warriors (from past tournament)
INSERT INTO player (id, username, first_name, last_name, country, played_games, won_games, user_id, team_id)
VALUES
('a3333333-1111-4111-1111-111111111111', 'FurryFury', 'Shadow', 'Clawson', 'Romania', 38, 24, NULL, 'aaaaaaaa-3333-4333-3333-333333333333'),
('a3333333-2222-4222-2222-222222222222', 'PurrPlatoon', 'Simba', 'Scratches', 'Bulgaria', 36, 23, NULL, 'aaaaaaaa-3333-4333-3333-333333333333'),
('a3333333-3333-4333-3333-333333333333', 'KittyKommando', 'Nala', 'Purrfect', 'Greece', 35, 22, NULL, 'aaaaaaaa-3333-4333-3333-333333333333'),
('a3333333-4444-4444-4444-444444444444', 'ShyTail', 'Rocky', 'Whiskers', 'Serbia', 33, 20, NULL, 'aaaaaaaa-3333-4333-3333-333333333333'),
('a3333333-5555-4555-5555-555555555555', 'StealthyPaws', 'Misty', 'Meowington', 'Bulgaria', 34, 21, NULL, 'aaaaaaaa-3333-4333-3333-333333333333');

-- Feline Force (from past tournament)
INSERT INTO player (id, username, first_name, last_name, country, played_games, won_games, user_id, team_id)
VALUES
('a4444444-1111-4111-1111-111111111111', 'KittyKiller', 'Jack', 'Furrington', 'Romania', 37, 25, NULL, 'aaaaaaaa-4444-4444-4444-444444444444'),
('a4444444-2222-4222-2222-222222222222', 'PawPunisher', 'Coco', 'Clawthorne', 'Bulgaria', 35, 23, NULL, 'aaaaaaaa-4444-4444-4444-444444444444'),
('a4444444-3333-4333-3333-333333333333', 'MeowMachine', 'Oliver', 'Scratchley', 'Greece', 34, 22, NULL, 'aaaaaaaa-4444-4444-4444-444444444444'),
('a4444444-4444-4444-4444-444444444444', 'ClawWrath', 'Lily', 'Pawsworth', 'Serbia', 33, 21, NULL, 'aaaaaaaa-4444-4444-4444-444444444444'),
('a4444444-5555-4555-5555-555555555555', 'FurryFatal', 'Milo', 'Kittensworth', 'Bulgaria', 32, 20, NULL, 'aaaaaaaa-4444-4444-4444-444444444444');

-- Meow Mercenaries (from current tournament)
INSERT INTO player (id, username, first_name, last_name, country, played_games, won_games, user_id, team_id)
VALUES
('b1111111-1111-4111-1111-111111111111', 'CatCrusher', 'Duke', 'Whiskerton', 'Romania', 28, 18, NULL, 'bbbbbbbb-1111-4111-1111-111111111111'),
('b1111111-2222-4222-2222-222222222222', 'PurrPredator', 'Luna', 'Scratchington', 'Bulgaria', 26, 16, NULL, 'bbbbbbbb-1111-4111-1111-111111111111'),
('b1111111-3333-4333-3333-333333333333', 'MeowMercenary', 'Salem', 'Pawstrong', 'Greece', 25, 15, NULL, 'bbbbbbbb-1111-4111-1111-111111111111'),
('b1111111-4444-4444-4444-444444444444', 'KittyKaos', 'Bella', 'Clawswell', 'Serbia', 24, 14, NULL, 'bbbbbbbb-1111-4111-1111-111111111111'),
('b1111111-5555-4555-5555-555555555555', 'WhiskerWar', 'Leo', 'Fursworth', 'Bulgaria', 23, 13, NULL, 'bbbbbbbb-1111-4111-1111-111111111111');

-- Claw Crushers (from current tournament)
INSERT INTO player (id, username, first_name, last_name, country, played_games, won_games, user_id, team_id)
VALUES
('b2222222-1111-4111-1111-111111111111', 'ClawCommando', 'Max', 'Purrkins', 'Romania', 25, 15, NULL, 'bbbbbbbb-2222-4222-2222-222222222222'),
('b2222222-2222-4222-2222-222222222222', 'NinjaNeko', 'Sophie', 'Whiskersmith', 'Bulgaria', 24, 14, NULL, 'bbbbbbbb-2222-4222-2222-222222222222'),
('b2222222-3333-4333-3333-333333333333', 'PawPatroller', 'Charlie', 'Meowton', 'Greece', 23, 13, NULL, 'bbbbbbbb-2222-4222-2222-222222222222'),
('b2222222-4444-4444-4444-444444444444', 'StealthScratch', 'Lucy', 'Clawton', 'Serbia', 22, 12, NULL, 'bbbbbbbb-2222-4222-2222-222222222222'),
('b2222222-5555-4555-5555-555555555555', 'WhiskerWarrior', 'Oliver', 'Furrington', 'Bulgaria', 21, 11, NULL, 'bbbbbbbb-2222-4222-2222-222222222222');

-- Kitty Kombat (from current tournament)
INSERT INTO player (id, username, first_name, last_name, country, played_games, won_games, user_id, team_id)
VALUES
('b3333333-1111-4111-1111-111111111111', 'KombatKitten', 'Milo', 'Scratchwell', 'Romania', 30, 20, NULL, 'bbbbbbbb-3333-4333-3333-333333333333'),
('b3333333-2222-4222-2222-222222222222', 'PurrPunch', 'Luna', 'Pawstrong', 'Bulgaria', 28, 18, NULL, 'bbbbbbbb-3333-4333-3333-333333333333'),
('b3333333-3333-4333-3333-333333333333', 'MeowMaster', 'Leo', 'Whiskerton', 'Greece', 27, 17, NULL, 'bbbbbbbb-3333-4333-3333-333333333333'),
('b3333333-4444-4444-4444-444444444444', 'ClawKombat', 'Bella', 'Furworth', 'Serbia', 26, 16, NULL, 'bbbbbbbb-3333-4333-3333-333333333333'),
('b3333333-5555-4555-5555-555555555555', 'WhiskerStrike', 'Tiger', 'Clawthorne', 'Bulgaria', 25, 15, NULL, 'bbbbbbbb-3333-4333-3333-333333333333');

-- Pawsome Predators (from current tournament)
INSERT INTO player (id, username, first_name, last_name, country, played_games, won_games, user_id, team_id)
VALUES
('b4444444-1111-4111-1111-111111111111', 'PredatorPurr', 'Shadow', 'Meowington', 'Romania', 27, 16, NULL, 'bbbbbbbb-4444-4444-4444-444444444444'),
('b4444444-2222-4222-2222-222222222222', 'ClawCrusher', 'Luna', 'Pawsworth', 'Bulgaria', 26, 15, NULL, 'bbbbbbbb-4444-4444-4444-444444444444'),
('b4444444-3333-4333-3333-333333333333', 'WhiskerWrath', 'Max', 'Furrington', 'Greece', 25, 14, NULL, 'bbbbbbbb-4444-4444-4444-444444444444'),
('b4444444-4444-4444-4444-444444444444', 'PawProwler', 'Sofia', 'Clawthorne', 'Serbia', 24, 13, NULL, 'bbbbbbbb-4444-4444-4444-444444444444'),
('b4444444-5555-4555-5555-555555555555', 'NightStalker', 'Viktor', 'Scratchev', 'Bulgaria', 23, 12, NULL, 'bbbbbbbb-4444-4444-4444-444444444444');

-- Furry Fury (from future tournament)
INSERT INTO player (id, username, first_name, last_name, country, played_games, won_games, user_id, team_id)
VALUES
('c1111111-1111-4111-1111-111111111111', 'FuryFang', 'Radu', 'Miaunu', 'Romania', 35, 22, NULL, 'cccccccc-1111-4111-1111-111111111111'),
('c1111111-2222-4222-2222-222222222222', 'RageClaw', 'Dimitar', 'Kotev', 'Bulgaria', 34, 21, NULL, 'cccccccc-1111-4111-1111-111111111111'),
('c1111111-3333-4333-3333-333333333333', 'FurStrike', 'Elena', 'Pisica', 'Greece', 33, 20, NULL, 'cccccccc-1111-4111-1111-111111111111'),
('c1111111-4444-4444-4444-444444444444', 'AngerPaw', 'Nikola', 'Mačka', 'Serbia', 32, 19, NULL, 'cccccccc-1111-4111-1111-111111111111'),
('c1111111-5555-4555-5555-555555555555', 'RageTail', 'Ivan', 'Furiev', 'Bulgaria', 31, 18, NULL, 'cccccccc-1111-4111-1111-111111111111');

-- Ninja Neko (from future tournament)
INSERT INTO player (id, username, first_name, last_name, country, played_games, won_games, user_id, team_id)
VALUES
('c2222222-1111-4111-1111-111111111111', 'ShadowCat', 'Ana', 'Sensei', 'Romania', 32, 21, NULL, 'cccccccc-2222-4222-2222-222222222222'),
('c2222222-2222-4222-2222-222222222222', 'SilentPaw', 'Boris', 'Ninja', 'Bulgaria', 31, 20, NULL, 'cccccccc-2222-4222-2222-222222222222'),
('c2222222-3333-4333-3333-333333333333', 'StealthFur', 'Maria', 'Tiho', 'Greece', 30, 19, NULL, 'cccccccc-2222-4222-2222-222222222222'),
('c2222222-4444-4444-4444-444444444444', 'QuietClaw', 'Dragan', 'Senko', 'Serbia', 29, 18, NULL, 'cccccccc-2222-4222-2222-222222222222'),
('c2222222-5555-4555-5555-555555555555', 'NightWhisker', 'Peter', 'Yamato', 'Bulgaria', 28, 17, NULL, 'cccccccc-2222-4222-2222-222222222222');

-- Teams without tournament below
-- Scratch Squadron
INSERT INTO player (id, username, first_name, last_name, country, played_games, won_games, user_id, team_id)
VALUES
('d1111111-1111-4111-1111-111111111111', 'ScratchMaster', 'Viktor', 'Kotev', 'Bulgaria', 22, 12, NULL, 'dddddddd-1111-4111-1111-111111111111'),
('d1111111-2222-4222-2222-222222222222', 'SquadronPaw', 'Elena', 'Whiskerova', 'Bulgaria', 20, 10, NULL, 'dddddddd-1111-4111-1111-111111111111'),
('d1111111-3333-4333-3333-333333333333', 'AirClaw', 'Boris', 'Pawlov', 'Bulgaria', 19, 9, NULL, 'dddddddd-1111-4111-1111-111111111111'),
('d1111111-4444-4444-4444-444444444444', 'WingTail', 'Maria', 'Kotova', 'Serbia', 18, 8, NULL, 'dddddddd-1111-4111-1111-111111111111'),
('d1111111-5555-4555-5555-555555555555', 'SkyWhisker', 'Ivan', 'Meowov', 'Romania', 17, 7, NULL, 'dddddddd-1111-4111-1111-111111111111');

-- Feline Phantoms
INSERT INTO player (id, username, first_name, last_name, country, played_games, won_games, user_id, team_id)
VALUES
('d2222222-1111-4111-1111-111111111111', 'GhostCat', 'Nikolai', 'Purrski', 'Bulgaria', 20, 11, NULL, 'dddddddd-2222-4222-2222-222222222222'),
('d2222222-2222-4222-2222-222222222222', 'SpectralPaw', 'Ana', 'Miacic', 'Serbia', 18, 9, NULL, 'dddddddd-2222-4222-2222-222222222222'),
('d2222222-3333-4333-3333-333333333333', 'ShadowClaw', 'Dragan', 'Felinus', 'Serbia', 17, 8, NULL, 'dddddddd-2222-4222-2222-222222222222'),
('d2222222-4444-4444-4444-444444444444', 'MistWhisker', 'Elena', 'Pisica', 'Romania', 16, 7, NULL, 'dddddddd-2222-4222-2222-222222222222'),
('d2222222-5555-4555-5555-555555555555', 'PhantomPurr', 'Radu', 'Catescu', 'Romania', 15, 6, NULL, 'dddddddd-2222-4222-2222-222222222222');

-- Cat Commandos Elite
INSERT INTO player (id, username, first_name, last_name, country, played_games, won_games, user_id, team_id)
VALUES
('d3333333-1111-4111-1111-111111111111', 'ElitePaw', 'Stefan', 'Kotarov', 'Bulgaria', 25, 15, NULL, 'dddddddd-3333-4333-3333-333333333333'),
('d3333333-2222-4222-2222-222222222222', 'CommanderClaw', 'Mira', 'Purric', 'Serbia', 23, 14, NULL, 'dddddddd-3333-4333-3333-333333333333'),
('d3333333-3333-4333-3333-333333333333', 'TacticalTail', 'Alex', 'Feline', 'Romania', 21, 13, NULL, 'dddddddd-3333-4333-3333-333333333333'),
('d3333333-4444-4444-4444-444444444444', 'StealthWhisker', 'Diana', 'Pisoi', 'Romania', 20, 12, NULL, 'dddddddd-3333-4333-3333-333333333333'),
('d3333333-5555-4555-5555-555555555555', 'SpecOpsCat', 'Vlad', 'Miaunu', 'Romania', 19, 11, NULL, 'dddddddd-3333-4333-3333-333333333333');

-- Whisker Wizards
INSERT INTO player (id, username, first_name, last_name, country, played_games, won_games, user_id, team_id)
VALUES
('d4444444-1111-4111-1111-111111111111', 'SpellPaw', 'Boris', 'Magickov', 'Bulgaria', 18, 9, NULL, 'dddddddd-4444-4444-4444-444444444444'),
('d4444444-2222-4222-2222-222222222222', 'MysticMeow', 'Katya', 'Wizardova', 'Bulgaria', 17, 8, NULL, 'dddddddd-4444-4444-4444-444444444444'),
('d4444444-3333-4333-3333-333333333333', 'RunicPurr', 'Marko', 'Čarobni', 'Serbia', 16, 8, NULL, 'dddddddd-4444-4444-4444-444444444444'),
('d4444444-4444-4444-4444-444444444444', 'ArcaneWhisker', 'Ion', 'Vrajitoru', 'Romania', 15, 7, NULL, 'dddddddd-4444-4444-4444-444444444444'),
('d4444444-5555-4555-5555-555555555555', 'ScrollClaw', 'Maria', 'Magica', 'Romania', 14, 6, NULL, 'dddddddd-4444-4444-4444-444444444444');

-- Paw Pirates
INSERT INTO player (id, username, first_name, last_name, country, played_games, won_games, user_id, team_id)
VALUES
('d5555555-1111-4111-1111-111111111111', 'CaptainClaw', 'Petar', 'Morski', 'Bulgaria', 15, 7, NULL, 'dddddddd-5555-4555-5555-555555555555'),
('d5555555-2222-4222-2222-222222222222', 'SeaPaw', 'Nina', 'Piratova', 'Bulgaria', 14, 6, NULL, 'dddddddd-5555-4555-5555-555555555555'),
('d5555555-3333-4333-3333-333333333333', 'BuccaneerPurr', 'Luka', 'Gusar', 'Serbia', 13, 6, NULL, 'dddddddd-5555-4555-5555-555555555555'),
('d5555555-4444-4444-4444-444444444444', 'SailWhisker', 'Andrei', 'Piratu', 'Romania', 12, 5, NULL, 'dddddddd-5555-4555-5555-555555555555'),
('d5555555-5555-4555-5555-555555555555', 'MarauderMeow', 'Elena', 'Corsaru', 'Romania', 11, 4, NULL, 'dddddddd-5555-4555-5555-555555555555');

-- Kitty Knights
INSERT INTO player (id, username, first_name, last_name, country, played_games, won_games, user_id, team_id)
VALUES
('d6666666-1111-4111-1111-111111111111', 'SirPurr', 'Kaloyan', 'Ritarev', 'Bulgaria', 28, 16, NULL, 'dddddddd-6666-4666-6666-666666666666'),
('d6666666-2222-4222-2222-222222222222', 'LadyWhisker', 'Yana', 'Dvorqnova', 'Bulgaria', 26, 15, NULL, 'dddddddd-6666-4666-6666-666666666666'),
('d6666666-3333-4333-3333-333333333333', 'PaladinPaw', 'Nemanja', 'Vitez', 'Serbia', 24, 14, NULL, 'dddddddd-6666-4666-6666-666666666666'),
('d6666666-4444-4444-4444-444444444444', 'CrusaderClaw', 'Tudor', 'Cavaler', 'Romania', 22, 13, NULL, 'dddddddd-6666-4666-6666-666666666666'),
('d6666666-5555-4555-5555-555555555555', 'NobleNeko', 'Ioana', 'Nobilă', 'Romania', 20, 12, NULL, 'dddddddd-6666-4666-6666-666666666666');

-- Meow Marines
INSERT INTO player (id, username, first_name, last_name, country, played_games, won_games, user_id, team_id)
VALUES
('d7777777-1111-4111-1111-111111111111', 'AdmiralPaw', 'Georgi', 'Morqkov', 'Bulgaria', 24, 13, NULL, 'dddddddd-7777-4777-7777-777777777777'),
('d7777777-2222-4222-2222-222222222222', 'CaptainPaw', 'Irina', 'Flotova', 'Bulgaria', 22, 12, NULL, 'dddddddd-7777-4777-7777-777777777777'),
('d7777777-3333-4333-3333-333333333333', 'MarineMeow', 'Vuk', 'Mornar', 'Serbia', 20, 11, NULL, 'dddddddd-7777-4777-7777-777777777777'),
('d7777777-4444-4444-4444-444444444444', 'NavyWhisker', 'Bogdan', 'Marinar', 'Romania', 18, 10, NULL, 'dddddddd-7777-4777-7777-777777777777'),
('d7777777-5555-4555-5555-555555555555', 'SailorPurr', 'Elena', 'Mornarova', 'Romania', 16, 9, NULL, 'dddddddd-7777-4777-7777-777777777777');

-- Feline Fighters
INSERT INTO player (id, username, first_name, last_name, country, played_games, won_games, user_id, team_id)
VALUES
('d8888888-1111-4111-1111-111111111111', 'FighterPaw', 'Ivan', 'Borec', 'Bulgaria', 22, 12, NULL, 'dddddddd-8888-4888-8888-888888888888'),
('d8888888-2222-4222-2222-222222222222', 'WarriorClaw', 'Maria', 'Borkinja', 'Bulgaria', 20, 11, NULL, 'dddddddd-8888-4888-8888-888888888888'),
('d8888888-3333-4333-3333-333333333333', 'GladiatorWhisker', 'Dragan', 'Borac', 'Serbia', 19, 10, NULL, 'dddddddd-8888-4888-8888-888888888888'),
('d8888888-4444-4444-4444-444444444444', 'ChampionPurr', 'Ana', 'Borkinja', 'Romania', 18, 9, NULL, 'dddddddd-8888-4888-8888-888888888888'),
('d8888888-5555-4555-5555-555555555555', 'DefenderNeko', 'Ivan', 'Branitelj', 'Romania', 17, 8, NULL, 'dddddddd-8888-4888-8888-888888888888');

-- Cat Crusaders
INSERT INTO player (id, username, first_name, last_name, country, played_games, won_games, user_id, team_id)
VALUES
('d9999999-1111-4111-1111-111111111111', 'CrusaderPaw', 'Nikola', 'Krstaš', 'Bulgaria', 20, 11, NULL, 'dddddddd-9999-4999-9999-999999999999'),
('d9999999-2222-4222-2222-222222222222', 'KnightClaw', 'Ana', 'Vitez', 'Bulgaria', 18, 10, NULL, 'dddddddd-9999-4999-9999-999999999999'),
('d9999999-3333-4333-3333-333333333333', 'PaladinWhisker', 'Dragan', 'Paladin', 'Serbia', 17, 9, NULL, 'dddddddd-9999-4999-9999-999999999999'),
('d9999999-4444-4444-4444-444444444444', 'SquirePurr', 'Elena', 'Vitezova', 'Romania', 16, 8, NULL, 'dddddddd-9999-4999-9999-999999999999'),
('d9999999-5555-4555-5555-555555555555', 'TemplarNeko', 'Ivan', 'Templar', 'Romania', 15, 7, NULL, 'dddddddd-9999-4999-9999-999999999999');

-- Purr Patrol
INSERT INTO player (id, username, first_name, last_name, country, played_games, won_games, user_id, team_id)
VALUES
('e1111111-1111-4111-1111-111111111111', 'PatrolPaw', 'Viktor', 'Patrolski', 'Bulgaria', 22, 12, NULL, 'dddddddd-0000-4000-0000-000000000000'),
('e1111111-2222-4222-2222-222222222222', 'GuardianClaw', 'Ana', 'Guardianova', 'Bulgaria', 20, 11, NULL, 'dddddddd-0000-4000-0000-000000000000'),
('e1111111-3333-4333-3333-333333333333', 'DefenderWhisker', 'Dragan', 'Defender', 'Serbia', 19, 10, NULL, 'dddddddd-0000-4000-0000-000000000000'),
('e1111111-4444-4444-4444-444444444444', 'ProtectorPurr', 'Elena', 'Zashtitnik', 'Romania', 18, 9, NULL, 'dddddddd-0000-4000-0000-000000000000'),
('e1111111-5555-4555-5555-555555555555', 'SafeguardNeko', 'Ivan', 'Zashtitnikov', 'Romania', 17, 8, NULL, 'dddddddd-0000-4000-0000-000000000000');


-- REQUESTS ---------------------------------------------------------------

-- LINK_USER_TO_PLAYER requests
INSERT INTO request (id, status, request_date, response_date, request_type, user_id, username, admin_id)
VALUES
('f1111111-1111-4111-1111-111111111111',
'PENDING',
'2024-03-15 14:30:00',
NULL,
'LINK_USER_TO_PLAYER',
'e7777777-7777-4777-7777-777777777777', -- kitty.sniper user
'ClawCommando',
NULL),

('f2222222-2222-4222-2222-222222222222',
'PENDING',
'2024-03-18 09:15:00',
NULL,
'LINK_USER_TO_PLAYER',
'e8888888-8888-4888-8888-888888888888', -- paw.striker user
'KombatKitten',
NULL);

-- PROMOTE_USER_TO_DIRECTOR requests
INSERT INTO request (id, status, request_date, response_date, request_type, user_id, username, admin_id)
VALUES
('f3333333-3333-4333-3333-333333333333',
'PENDING',
'2024-03-20 11:45:00',
NULL,
'PROMOTE_USER_TO_DIRECTOR',
'e9999999-9999-4999-9999-999999999999', -- ninja.cat user
NULL,
NULL),

('f4444444-4444-4444-4444-444444444444',
'PENDING',
'2024-03-22 16:20:00',
NULL,
'PROMOTE_USER_TO_DIRECTOR',
'e0000000-0000-4000-0000-000000000000', -- furry.force user
NULL,
NULL);


-- MATCHES ---------------------------------------------------------------

-- Past Tournament Matches (Kitten Strike Winter Championship 2024)
INSERT INTO match (id, match_format, start_time, is_finished, stage, team1_id, team2_id, team1_score, team2_score, winner_team_id, tournament_id)
VALUES
-- Semi-Final 1
('a1111111-1111-4111-1111-111111111111',
'MR15',
'2024-01-15 11:00:00',
TRUE,
'SEMI_FINAL',
'aaaaaaaa-1111-4111-1111-111111111111',  -- Purrfect Snipers
'aaaaaaaa-2222-4222-2222-222222222222',  -- Catnip Commandos
16,
14,
'aaaaaaaa-1111-4111-1111-111111111111',  -- Purrfect Snipers win
'11111111-1111-4111-1111-111111111111'),

-- Semi-Final 2
('a1111111-2222-4222-2222-222222222222',
'MR15',
'2024-01-18 11:00:00',
TRUE,
'SEMI_FINAL',
'aaaaaaaa-3333-4333-3333-333333333333',  -- Whisker Warriors
'aaaaaaaa-4444-4444-4444-444444444444',  -- Feline Force
13,
16,
'aaaaaaaa-4444-4444-4444-444444444444',  -- Feline Force win
'11111111-1111-4111-1111-111111111111'),

-- Final
('a1111111-3333-4333-3333-333333333333',
'MR15',
'2024-02-01 11:00:00',
TRUE,
'FINAL',
'aaaaaaaa-1111-4111-1111-111111111111',  -- Purrfect Snipers
'aaaaaaaa-4444-4444-4444-444444444444',  -- Feline Force
16,
12,
'aaaaaaaa-1111-4111-1111-111111111111',  -- Purrfect Snipers win tournament
'11111111-1111-4111-1111-111111111111');

-- Current Tournament Matches (Whiskers League Season 1)
INSERT INTO match (id, match_format, start_time, is_finished, stage, team1_id, team2_id, team1_score, team2_score, winner_team_id, tournament_id)
VALUES
-- Group Stage Match 1
('a2222222-1111-4111-1111-111111111111',
'MR12',
'2024-03-01 11:00:00',
TRUE,
'GROUP_STAGE',
'bbbbbbbb-1111-4111-1111-111111111111', -- Meow Mercenaries
'bbbbbbbb-2222-4222-2222-222222222222', -- Claw Crushers
13,
8,
'bbbbbbbb-1111-4111-1111-111111111111',
'33333333-3333-4333-3333-333333333333'),

-- Group Stage Match 2
('a2222222-2222-4222-2222-222222222222',
'MR12',
'2024-03-01 14:00:00',
TRUE,
'GROUP_STAGE',
'bbbbbbbb-3333-4333-3333-333333333333', -- Kitty Kombat
'bbbbbbbb-4444-4444-4444-444444444444', -- Pawsome Predators
13,
10,
'bbbbbbbb-3333-4333-3333-333333333333',
'33333333-3333-4333-3333-333333333333'),

-- Remaining Group Stage Matches (Not finished)
('a2222222-3333-4333-3333-333333333333',
'MR12',
'2024-03-01 17:00:00',
FALSE,
'GROUP_STAGE',
'bbbbbbbb-1111-4111-1111-111111111111', -- Meow Mercenaries
'bbbbbbbb-3333-4333-3333-333333333333', -- Kitty Kombat
0,
0,
NULL,
'33333333-3333-4333-3333-333333333333'),

('a2222222-4444-4444-4444-444444444444',
'MR12',
'2024-03-01 20:00:00',
FALSE,
'GROUP_STAGE',
'bbbbbbbb-2222-4222-2222-222222222222', -- Claw Crushers
'bbbbbbbb-4444-4444-4444-444444444444', -- Pawsome Predators
0,
0,
NULL,
'33333333-3333-4333-3333-333333333333'),

('a2222222-5555-4555-5555-555555555555',
'MR12',
'2024-03-02 11:00:00',
FALSE,
'GROUP_STAGE',
'bbbbbbbb-1111-4111-1111-111111111111', -- Meow Mercenaries
'bbbbbbbb-4444-4444-4444-444444444444', -- Pawsome Predators
0,
0,
NULL,
'33333333-3333-4333-3333-333333333333'),

('a2222222-6666-4666-6666-666666666666',
'MR12',
'2024-03-02 14:00:00',
FALSE,
'GROUP_STAGE',
'bbbbbbbb-2222-4222-2222-222222222222', -- Claw Crushers
'bbbbbbbb-3333-4333-3333-333333333333', -- Kitty Kombat
0,
0,
NULL,
'33333333-3333-4333-3333-333333333333');

-- Future Tournament Match (Paw Masters Showdown)
INSERT INTO match (id, match_format, start_time, is_finished, stage, team1_id, team2_id, team1_score, team2_score, winner_team_id, tournament_id)
VALUES
('a3333333-1111-4111-1111-111111111111',
'MR15',
'2024-05-01 11:00:00',
FALSE,
'FINAL',
'cccccccc-1111-4111-1111-111111111111', -- Furry Fury
'cccccccc-2222-4222-2222-222222222222', -- Ninja Neko
0,
0,
NULL,
'44444444-4444-4444-4444-444444444444');




-- PRIZES ----------------------------------------------------------------

INSERT INTO prizecut (id, place, prize_cut, tournament_id, team_id)
VALUES
-- Past tournament prizes (assigned)
('aa111111-1111-4111-1111-111111111111',
1,
3500,
'11111111-1111-4111-1111-111111111111',
'aaaaaaaa-1111-4111-1111-111111111111'),

('aa222222-2222-4222-2222-222222222222',
2,
1500,
'11111111-1111-4111-1111-111111111111',
'aaaaaaaa-4444-4444-4444-444444444444');

-- Current tournament prizes (unassigned)
INSERT INTO prizecut (id, place, prize_cut, tournament_id, team_id)
VALUES
('aa333333-3333-4333-3333-333333333333',
1,
7000,
'33333333-3333-4333-3333-333333333333',
NULL),

('aa444444-4444-4444-4444-444444444444',
2,
3000,
'33333333-3333-4333-3333-333333333333',
NULL);

-- Future tournament prizes (unassigned)
INSERT INTO prizecut (id, place, prize_cut, tournament_id, team_id)
VALUES
('aa555555-5555-4555-5555-555555555555',
1,
2100,
'44444444-4444-4444-4444-444444444444',
NULL),

('aa666666-6666-4666-6666-666666666666',
2,
900,
'44444444-4444-4444-4444-444444444444',
NULL);