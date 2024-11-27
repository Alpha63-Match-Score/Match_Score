--
-- PostgreSQL database dump
--

-- Dumped from database version 14.13 (Homebrew)
-- Dumped by pg_dump version 14.13 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: ayselkaradayi
--

INSERT INTO public."user" VALUES ('admin@example.com', '$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO', 'ADMIN', '2024-11-27 10:54:39.123306+02', 'e1111111-1111-4111-1111-111111111111');
INSERT INTO public."user" VALUES ('director@example.com', '$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO', 'DIRECTOR', '2024-11-27 10:54:39.123306+02', 'e2222222-2222-4222-2222-222222222222');
INSERT INTO public."user" VALUES ('user@example.com', '$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO', 'USER', '2024-11-27 10:54:39.123306+02', 'e3333333-3333-4333-3333-333333333333');
INSERT INTO public."user" VALUES ('purr.programmer@example.com', '$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO', 'PLAYER', '2024-11-27 10:54:39.123306+02', 'e4444444-4444-4444-4444-444444444444');
INSERT INTO public."user" VALUES ('whiskers.warrior@example.com', '$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO', 'USER', '2024-11-27 10:54:39.123306+02', 'e5555555-5555-4555-5555-555555555555');
INSERT INTO public."user" VALUES ('meow.sniper@example.com', '$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO', 'USER', '2024-11-27 10:54:39.123306+02', 'e6666666-6666-4666-6666-666666666666');
INSERT INTO public."user" VALUES ('kitty.sniper@example.com', '$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO', 'USER', '2024-11-27 10:54:39.123306+02', 'e7777777-7777-4777-7777-777777777777');
INSERT INTO public."user" VALUES ('paw.striker@example.com', '$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO', 'USER', '2024-11-27 10:54:39.123306+02', 'e8888888-8888-4888-8888-888888888888');
INSERT INTO public."user" VALUES ('ninja.cat@example.com', '$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO', 'USER', '2024-11-27 10:54:39.123306+02', 'e9999999-9999-4999-9999-999999999999');
INSERT INTO public."user" VALUES ('furry.force@example.com', '$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO', 'USER', '2024-11-27 10:54:39.123306+02', 'e0000000-0000-4000-0000-000000000000');


--
-- Data for Name: tournament; Type: TABLE DATA; Schema: public; Owner: ayselkaradayi
--

INSERT INTO public.tournament VALUES ('Kitten Strike Winter Championship 2024', 'SINGLE_ELIMINATION', '2024-11-20 11:00:00', '2024-11-24 23:59:59', 5000, 'FINISHED', 'e2222222-2222-4222-2222-222222222222', '11111111-1111-4111-1111-111111111111');
INSERT INTO public.tournament VALUES ('Whiskers League Season 1', 'ROUND_ROBIN', '2024-12-11 11:00:00', '2024-12-14 23:59:59', 10000, 'GROUP_STAGE', 'e2222222-2222-4222-2222-222222222222', '33333333-3333-4333-3333-333333333333');
INSERT INTO public.tournament VALUES ('Paw Masters Showdown', 'ONE_OFF_MATCH', '2025-01-04 11:00:00', '2025-01-04 23:59:59', 3000, 'FINAL', 'e2222222-2222-4222-2222-222222222222', '44444444-4444-4444-4444-444444444444');
INSERT INTO public.tournament VALUES ('Catnip Cup Championship 2025', 'SINGLE_ELIMINATION', '2025-01-27 11:00:00', '2025-01-28 23:59:59', 500, 'SEMI_FINAL', 'e1111111-1111-4111-1111-111111111111', '2fa75271-3dd6-4e4b-b3b7-42fac6142393');
INSERT INTO public.tournament VALUES ('Whiskers & Headshots Masters', 'ONE_OFF_MATCH', '2025-02-13 11:00:00', '2025-02-13 23:59:59', 23000, 'FINAL', 'e1111111-1111-4111-1111-111111111111', '6da06af0-3c0a-4f1c-83d4-46f275f4dfd8');
INSERT INTO public.tournament VALUES ('Nine Lives League', 'ROUND_ROBIN', '2025-03-01 11:00:00', '2025-03-04 23:59:59', 55000, 'GROUP_STAGE', 'e1111111-1111-4111-1111-111111111111', 'd2b7e127-5a86-479e-b829-a4e137d3b716');
INSERT INTO public.tournament VALUES ('Purrfect Aim Championship', 'SINGLE_ELIMINATION', '2025-03-26 11:00:00', '2025-03-27 23:59:59', 1700, 'SEMI_FINAL', 'e1111111-1111-4111-1111-111111111111', 'd76ecc3c-db83-4f5b-a7c7-91b706871725');
INSERT INTO public.tournament VALUES ('Feline Fire Global Elite', 'ONE_OFF_MATCH', '2025-04-10 11:00:00', '2025-04-10 23:59:59', 13000, 'FINAL', 'e1111111-1111-4111-1111-111111111111', '9acfabd3-0095-41fd-8fda-6177b40ac8bf');
INSERT INTO public.tournament VALUES ('Whiskers & Headshots Summer Showdown 2024', 'SINGLE_ELIMINATION', '2024-08-15 12:00:00', '2024-08-19 23:59:59', 7500, 'FINISHED', 'e2222222-2222-4222-2222-222222222222', '11111111-2222-4222-2222-222222222222');
INSERT INTO public.tournament VALUES ('Purrfect Aim Masters Spring 2024', 'ROUND_ROBIN', '2024-05-10 10:00:00', '2024-05-14 23:59:59', 6000, 'FINISHED', 'e2222222-2222-4222-2222-222222222222', '11111111-3333-4333-3333-333333333333');
INSERT INTO public.tournament VALUES ('Catnip Cup Elite Series', 'ONE_OFF_MATCH', '2024-07-01 15:00:00', '2024-07-01 23:59:59', 3000, 'FINISHED', 'e2222222-2222-4222-2222-222222222222', '11111111-4444-4444-4444-444444444444');
INSERT INTO public.tournament VALUES ('Nine Lives League Championship', 'SINGLE_ELIMINATION', '2024-06-20 11:00:00', '2024-06-24 23:59:59', 8000, 'FINISHED', 'e2222222-2222-4222-2222-222222222222', '11111111-5555-4555-5555-555555555555');
INSERT INTO public.tournament VALUES ('Feline Fire Global Finals', 'ROUND_ROBIN', '2024-09-05 13:00:00', '2024-09-09 23:59:59', 10000, 'FINISHED', 'e2222222-2222-4222-2222-222222222222', '11111111-6666-4666-6666-666666666666');
INSERT INTO public.tournament VALUES ('Scratch & Snipe Invitational', 'ONE_OFF_MATCH', '2024-10-01 14:00:00', '2024-10-01 23:59:59', 4000, 'FINISHED', 'e2222222-2222-4222-2222-222222222222', '11111111-7777-4777-7777-777777777777');
INSERT INTO public.tournament VALUES ('Meow Mercenaries Challenge', 'SINGLE_ELIMINATION', '2024-04-15 12:00:00', '2024-04-19 23:59:59', 5500, 'FINISHED', 'e2222222-2222-4222-2222-222222222222', '11111111-8888-4888-8888-888888888888');
INSERT INTO public.tournament VALUES ('Kitty Combat Classic', 'ROUND_ROBIN', '2024-03-10 11:00:00', '2024-03-14 23:59:59', 7000, 'FINISHED', 'e2222222-2222-4222-2222-222222222222', '11111111-9999-4999-9999-999999999999');
INSERT INTO public.tournament VALUES ('Fuzzy Fraggers Championship', 'ONE_OFF_MATCH', '2024-02-01 15:00:00', '2024-02-01 23:59:59', 3500, 'FINISHED', 'e2222222-2222-4222-2222-222222222222', '11111111-aaaa-4aaa-aaaa-aaaaaaaaaaaa');
INSERT INTO public.tournament VALUES ('Purr Protocol Masters', 'SINGLE_ELIMINATION', '2024-01-20 10:00:00', '2024-01-24 23:59:59', 6500, 'FINISHED', 'e2222222-2222-4222-2222-222222222222', '11111111-bbbb-4bbb-bbbb-bbbbbbbbbbbb');
INSERT INTO public.tournament VALUES ('Claw Tactics Tournament', 'ROUND_ROBIN', '2024-10-15 13:00:00', '2024-10-19 23:59:59', 8500, 'FINISHED', 'e2222222-2222-4222-2222-222222222222', '11111111-cccc-4ccc-cccc-cccccccccccc');
INSERT INTO public.tournament VALUES ('Whisker Warriors League', 'ONE_OFF_MATCH', '2024-09-20 14:00:00', '2024-09-20 23:59:59', 4500, 'FINISHED', 'e2222222-2222-4222-2222-222222222222', '11111111-dddd-4ddd-dddd-dddddddddddd');
INSERT INTO public.tournament VALUES ('Feline Fury Faceoff', 'SINGLE_ELIMINATION', '2024-08-01 11:00:00', '2024-08-05 23:59:59', 7200, 'FINISHED', 'e2222222-2222-4222-2222-222222222222', '11111111-eeee-4eee-eeee-eeeeeeeeeeee');
INSERT INTO public.tournament VALUES ('Paw Precision Pro League', 'ROUND_ROBIN', '2024-07-15 12:00:00', '2024-07-19 23:59:59', 9000, 'FINISHED', 'e2222222-2222-4222-2222-222222222222', '11111111-ffff-4fff-ffff-ffffffffffff');
INSERT INTO public.tournament VALUES ('Sphynx Strike Series', 'ONE_OFF_MATCH', '2024-06-01 15:00:00', '2024-06-01 23:59:59', 3800, 'FINISHED', 'e2222222-2222-4222-2222-222222222222', '22222222-1111-4111-1111-111111111111');
INSERT INTO public.tournament VALUES ('Tabby Tactical Tournament', 'SINGLE_ELIMINATION', '2024-05-20 10:00:00', '2024-05-24 23:59:59', 6800, 'FINISHED', 'e2222222-2222-4222-2222-222222222222', '22222222-2222-4222-2222-222222222222');
INSERT INTO public.tournament VALUES ('Siamese Sharpshooter Showdown', 'ROUND_ROBIN', '2024-04-01 13:00:00', '2024-04-05 23:59:59', 8200, 'FINISHED', 'e2222222-2222-4222-2222-222222222222', '22222222-3333-4333-3333-333333333333');
INSERT INTO public.tournament VALUES ('Persian Prowess Championship', 'ONE_OFF_MATCH', '2024-03-01 14:00:00', '2024-03-01 23:59:59', 4200, 'FINISHED', 'e2222222-2222-4222-2222-222222222222', '22222222-4444-4444-4444-444444444444');
INSERT INTO public.tournament VALUES ('Bengal Battle Royale', 'SINGLE_ELIMINATION', '2024-02-15 11:00:00', '2024-02-19 23:59:59', 7800, 'FINISHED', 'e2222222-2222-4222-2222-222222222222', '22222222-5555-4555-5555-555555555555');
INSERT INTO public.tournament VALUES ('Ragdoll Rampage Cup', 'ROUND_ROBIN', '2024-01-05 12:00:00', '2024-01-09 23:59:59', 9500, 'FINISHED', 'e2222222-2222-4222-2222-222222222222', '22222222-6666-4666-6666-666666666666');


--
-- Data for Name: team; Type: TABLE DATA; Schema: public; Owner: ayselkaradayi
--

INSERT INTO public.team VALUES ('Purrfect Snipers', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/teams/20241125_121825_98bc7567.JPG', 45, 32, '11111111-1111-4111-1111-111111111111', 'aaaaaaaa-1111-4111-1111-111111111111');
INSERT INTO public.team VALUES ('Catnip Commandos', 'https://kittenstrike.s3.amazonaws.com/teams/20241127_112924_558c7135.png', 38, 25, '11111111-1111-4111-1111-111111111111', 'aaaaaaaa-2222-4222-2222-222222222222');
INSERT INTO public.team VALUES ('Whisker Warriors', 'https://kittenstrike.s3.amazonaws.com/teams/20241127_112947_4ceaf52c.png', 42, 28, '11111111-1111-4111-1111-111111111111', 'aaaaaaaa-3333-4333-3333-333333333333');
INSERT INTO public.team VALUES ('Feline Force', 'https://kittenstrike.s3.amazonaws.com/teams/20241127_113009_03bd25ae.png', 41, 29, '11111111-1111-4111-1111-111111111111', 'aaaaaaaa-4444-4444-4444-444444444444');
INSERT INTO public.team VALUES ('Meow Mercenaries', 'https://kittenstrike.s3.amazonaws.com/teams/20241127_113027_f0d43893.png', 28, 18, '33333333-3333-4333-3333-333333333333', 'bbbbbbbb-1111-4111-1111-111111111111');
INSERT INTO public.team VALUES ('Claw Crushers', 'https://kittenstrike.s3.amazonaws.com/teams/20241127_113045_c485431f.png', 25, 15, '33333333-3333-4333-3333-333333333333', 'bbbbbbbb-2222-4222-2222-222222222222');
INSERT INTO public.team VALUES ('Kitty Kombat', 'https://kittenstrike.s3.amazonaws.com/teams/20241127_120053_730211b4.png', 30, 20, '33333333-3333-4333-3333-333333333333', 'bbbbbbbb-3333-4333-3333-333333333333');
INSERT INTO public.team VALUES ('Pawsome Predators', 'https://kittenstrike.s3.amazonaws.com/teams/20241127_121958_72ec0ad7.png', 27, 16, '33333333-3333-4333-3333-333333333333', 'bbbbbbbb-4444-4444-4444-444444444444');
INSERT INTO public.team VALUES ('Furry Fury', 'https://kittenstrike.s3.amazonaws.com/teams/20241127_122112_7d1a9efe.png', 35, 22, '44444444-4444-4444-4444-444444444444', 'cccccccc-1111-4111-1111-111111111111');
INSERT INTO public.team VALUES ('Ninja Neko', 'https://kittenstrike.s3.amazonaws.com/teams/20241127_122141_d56358c1.png', 32, 21, '44444444-4444-4444-4444-444444444444', 'cccccccc-2222-4222-2222-222222222222');
INSERT INTO public.team VALUES ('Purr Patrol', 'https://kittenstrike.s3.amazonaws.com/teams/20241127_122211_3a9e30c8.png', 17, 6, '2fa75271-3dd6-4e4b-b3b7-42fac6142393', 'dddddddd-0000-4000-0000-000000000000');
INSERT INTO public.team VALUES ('Scratch Squadron', 'https://kittenstrike.s3.amazonaws.com/teams/20241127_122247_92915713.png', 22, 12, '2fa75271-3dd6-4e4b-b3b7-42fac6142393', 'dddddddd-1111-4111-1111-111111111111');
INSERT INTO public.team VALUES ('Feline Phantoms', 'https://kittenstrike.s3.amazonaws.com/teams/20241127_122301_e87b2c4e.png', 20, 11, '2fa75271-3dd6-4e4b-b3b7-42fac6142393', 'dddddddd-2222-4222-2222-222222222222');
INSERT INTO public.team VALUES ('Cat Commandos Elite', 'https://kittenstrike.s3.amazonaws.com/teams/20241127_122321_1c97cf42.png', 25, 15, '2fa75271-3dd6-4e4b-b3b7-42fac6142393', 'dddddddd-3333-4333-3333-333333333333');
INSERT INTO public.team VALUES ('Whisker Wizards', 'https://kittenstrike.s3.amazonaws.com/teams/20241127_122343_f6d548b5.png', 18, 9, '6da06af0-3c0a-4f1c-83d4-46f275f4dfd8', 'dddddddd-4444-4444-4444-444444444444');
INSERT INTO public.team VALUES ('Paw Pirates', 'https://kittenstrike.s3.amazonaws.com/teams/20241127_122359_c5ab5b67.png', 15, 7, '6da06af0-3c0a-4f1c-83d4-46f275f4dfd8', 'dddddddd-5555-4555-5555-555555555555');
INSERT INTO public.team VALUES ('Kitty Knights', 'https://kittenstrike.s3.amazonaws.com/teams/20241127_122435_5f64016a.png', 28, 16, 'd2b7e127-5a86-479e-b829-a4e137d3b716', 'dddddddd-6666-4666-6666-666666666666');
INSERT INTO public.team VALUES ('Meow Marines', 'https://kittenstrike.s3.amazonaws.com/teams/20241127_122455_880de288.png', 24, 13, 'd2b7e127-5a86-479e-b829-a4e137d3b716', 'dddddddd-7777-4777-7777-777777777777');
INSERT INTO public.team VALUES ('Feline Fighters', 'https://kittenstrike.s3.amazonaws.com/teams/20241127_122517_eeb756c0.png', 21, 10, 'd2b7e127-5a86-479e-b829-a4e137d3b716', 'dddddddd-8888-4888-8888-888888888888');
INSERT INTO public.team VALUES ('Cat Crusaders', 'https://kittenstrike.s3.amazonaws.com/teams/20241127_122534_8fa23267.png', 19, 8, 'd2b7e127-5a86-479e-b829-a4e137d3b716', 'dddddddd-9999-4999-9999-999999999999');
INSERT INTO public.team VALUES ('Tiger Titans', 'https://kittenstrike.s3.amazonaws.com/teams/20241127_122553_b305b641.png', 23, 14, 'd76ecc3c-db83-4f5b-a7c7-91b706871725', 'dddddddd-aaaa-4aaa-aaaa-aaaaaaaaaaaa');
INSERT INTO public.team VALUES ('Claw Champions', 'https://kittenstrike.s3.amazonaws.com/teams/20241127_122624_6ce9ec83.png', 26, 17, 'd76ecc3c-db83-4f5b-a7c7-91b706871725', 'dddddddd-bbbb-4bbb-bbbb-bbbbbbbbbbbb');
INSERT INTO public.team VALUES ('Feline Ninjas', 'https://kittenstrike.s3.amazonaws.com/teams/20241127_122641_edc5d8b2.png', 19, 11, 'd76ecc3c-db83-4f5b-a7c7-91b706871725', 'dddddddd-cccc-4ccc-cccc-cccccccccccc');
INSERT INTO public.team VALUES ('Samurai Siamese', 'https://kittenstrike.s3.amazonaws.com/teams/20241127_122657_db4a24af.png', 21, 12, 'd76ecc3c-db83-4f5b-a7c7-91b706871725', 'dddddddd-dddd-4ddd-dddd-dddddddddddd');
INSERT INTO public.team VALUES ('Samurai Cats', 'https://kittenstrike.s3.amazonaws.com/teams/20241127_122716_d38d2bce.png', 24, 15, '9acfabd3-0095-41fd-8fda-6177b40ac8bf', 'dddddddd-eeee-4eee-eeee-eeeeeeeeeeee');
INSERT INTO public.team VALUES ('Whisker Fighters', 'https://kittenstrike.s3.amazonaws.com/teams/20241127_122732_91f4b60e.png', 20, 13, '9acfabd3-0095-41fd-8fda-6177b40ac8bf', 'dddddddd-ffff-4fff-ffff-ffffffffffff');


--
-- Data for Name: match; Type: TABLE DATA; Schema: public; Owner: ayselkaradayi
--

INSERT INTO public.match VALUES ('MR15', '2024-01-15 11:00:00', true, 'SEMI_FINAL', 'aaaaaaaa-1111-4111-1111-111111111111', 'aaaaaaaa-2222-4222-2222-222222222222', 16, 14, 'aaaaaaaa-1111-4111-1111-111111111111', '11111111-1111-4111-1111-111111111111', 'a1111111-1111-4111-1111-111111111111');
INSERT INTO public.match VALUES ('MR15', '2024-01-18 11:00:00', true, 'SEMI_FINAL', 'aaaaaaaa-3333-4333-3333-333333333333', 'aaaaaaaa-4444-4444-4444-444444444444', 13, 16, 'aaaaaaaa-4444-4444-4444-444444444444', '11111111-1111-4111-1111-111111111111', 'a1111111-2222-4222-2222-222222222222');
INSERT INTO public.match VALUES ('MR15', '2024-02-01 11:00:00', true, 'FINAL', 'aaaaaaaa-1111-4111-1111-111111111111', 'aaaaaaaa-4444-4444-4444-444444444444', 16, 12, 'aaaaaaaa-1111-4111-1111-111111111111', '11111111-1111-4111-1111-111111111111', 'a1111111-3333-4333-3333-333333333333');
INSERT INTO public.match VALUES ('MR12', '2024-03-01 11:00:00', true, 'GROUP_STAGE', 'bbbbbbbb-1111-4111-1111-111111111111', 'bbbbbbbb-2222-4222-2222-222222222222', 13, 8, 'bbbbbbbb-1111-4111-1111-111111111111', '33333333-3333-4333-3333-333333333333', 'a2222222-1111-4111-1111-111111111111');
INSERT INTO public.match VALUES ('MR12', '2024-03-01 14:00:00', true, 'GROUP_STAGE', 'bbbbbbbb-3333-4333-3333-333333333333', 'bbbbbbbb-4444-4444-4444-444444444444', 13, 10, 'bbbbbbbb-3333-4333-3333-333333333333', '33333333-3333-4333-3333-333333333333', 'a2222222-2222-4222-2222-222222222222');
INSERT INTO public.match VALUES ('MR12', '2024-03-01 17:00:00', false, 'GROUP_STAGE', 'bbbbbbbb-1111-4111-1111-111111111111', 'bbbbbbbb-3333-4333-3333-333333333333', 0, 0, NULL, '33333333-3333-4333-3333-333333333333', 'a2222222-3333-4333-3333-333333333333');
INSERT INTO public.match VALUES ('MR12', '2024-03-01 20:00:00', false, 'GROUP_STAGE', 'bbbbbbbb-2222-4222-2222-222222222222', 'bbbbbbbb-4444-4444-4444-444444444444', 0, 0, NULL, '33333333-3333-4333-3333-333333333333', 'a2222222-4444-4444-4444-444444444444');
INSERT INTO public.match VALUES ('MR12', '2024-03-02 11:00:00', false, 'GROUP_STAGE', 'bbbbbbbb-1111-4111-1111-111111111111', 'bbbbbbbb-4444-4444-4444-444444444444', 0, 0, NULL, '33333333-3333-4333-3333-333333333333', 'a2222222-5555-4555-5555-555555555555');
INSERT INTO public.match VALUES ('MR12', '2024-03-02 14:00:00', false, 'GROUP_STAGE', 'bbbbbbbb-2222-4222-2222-222222222222', 'bbbbbbbb-3333-4333-3333-333333333333', 0, 0, NULL, '33333333-3333-4333-3333-333333333333', 'a2222222-6666-4666-6666-666666666666');
INSERT INTO public.match VALUES ('MR15', '2024-05-01 11:00:00', false, 'FINAL', 'cccccccc-1111-4111-1111-111111111111', 'cccccccc-2222-4222-2222-222222222222', 0, 0, NULL, '44444444-4444-4444-4444-444444444444', 'a3333333-1111-4111-1111-111111111111');
INSERT INTO public.match VALUES ('MR15', '2025-01-27 11:00:00', false, 'SEMI_FINAL', 'dddddddd-1111-4111-1111-111111111111', 'dddddddd-0000-4000-0000-000000000000', 0, 0, NULL, '2fa75271-3dd6-4e4b-b3b7-42fac6142393', '7c545fcc-8742-47be-80fd-3f894792f93d');
INSERT INTO public.match VALUES ('MR15', '2025-01-27 14:00:00', false, 'SEMI_FINAL', 'dddddddd-3333-4333-3333-333333333333', 'dddddddd-2222-4222-2222-222222222222', 0, 0, NULL, '2fa75271-3dd6-4e4b-b3b7-42fac6142393', '99f668b8-572a-4adf-8820-e2394a745690');
INSERT INTO public.match VALUES ('MR15', '2025-02-13 11:00:00', false, 'FINAL', 'dddddddd-5555-4555-5555-555555555555', 'dddddddd-4444-4444-4444-444444444444', 0, 0, NULL, '6da06af0-3c0a-4f1c-83d4-46f275f4dfd8', '1eeb3d5d-70ff-4ca2-a7db-8750a9b228b7');
INSERT INTO public.match VALUES ('MR12', '2025-03-01 11:00:00', false, 'GROUP_STAGE', 'dddddddd-6666-4666-6666-666666666666', 'dddddddd-7777-4777-7777-777777777777', 0, 0, NULL, 'd2b7e127-5a86-479e-b829-a4e137d3b716', '05b2caff-1a1e-49d3-9e6a-14e5c93f9a62');
INSERT INTO public.match VALUES ('MR12', '2025-03-01 14:00:00', false, 'GROUP_STAGE', 'dddddddd-6666-4666-6666-666666666666', 'dddddddd-8888-4888-8888-888888888888', 0, 0, NULL, 'd2b7e127-5a86-479e-b829-a4e137d3b716', 'e8597052-876c-4515-8865-79af51afb413');
INSERT INTO public.match VALUES ('MR12', '2025-03-01 17:00:00', false, 'GROUP_STAGE', 'dddddddd-6666-4666-6666-666666666666', 'dddddddd-9999-4999-9999-999999999999', 0, 0, NULL, 'd2b7e127-5a86-479e-b829-a4e137d3b716', '472cb4cb-0907-45aa-bbc2-fd1047590332');
INSERT INTO public.match VALUES ('MR12', '2025-03-01 20:00:00', false, 'GROUP_STAGE', 'dddddddd-7777-4777-7777-777777777777', 'dddddddd-8888-4888-8888-888888888888', 0, 0, NULL, 'd2b7e127-5a86-479e-b829-a4e137d3b716', '932196b4-d0bf-4a88-a364-4c6ca5b384d0');
INSERT INTO public.match VALUES ('MR12', '2025-03-02 11:00:00', false, 'GROUP_STAGE', 'dddddddd-7777-4777-7777-777777777777', 'dddddddd-9999-4999-9999-999999999999', 0, 0, NULL, 'd2b7e127-5a86-479e-b829-a4e137d3b716', '0919f83a-4c2f-4ff2-b02c-247377f60bcb');
INSERT INTO public.match VALUES ('MR12', '2025-03-02 14:00:00', false, 'GROUP_STAGE', 'dddddddd-8888-4888-8888-888888888888', 'dddddddd-9999-4999-9999-999999999999', 0, 0, NULL, 'd2b7e127-5a86-479e-b829-a4e137d3b716', 'a2b73c72-0ce7-4d87-9e01-fabc7fa270c4');
INSERT INTO public.match VALUES ('MR15', '2025-03-26 11:00:00', false, 'SEMI_FINAL', 'dddddddd-bbbb-4bbb-bbbb-bbbbbbbbbbbb', 'dddddddd-aaaa-4aaa-aaaa-aaaaaaaaaaaa', 0, 0, NULL, 'd76ecc3c-db83-4f5b-a7c7-91b706871725', '700c7bd8-732d-49ab-a793-eab22feb91a5');
INSERT INTO public.match VALUES ('MR15', '2025-03-26 14:00:00', false, 'SEMI_FINAL', 'dddddddd-dddd-4ddd-dddd-dddddddddddd', 'dddddddd-cccc-4ccc-cccc-cccccccccccc', 0, 0, NULL, 'd76ecc3c-db83-4f5b-a7c7-91b706871725', '5e71268b-81e8-4de3-b0cf-7561e6f2b36b');
INSERT INTO public.match VALUES ('MR15', '2025-04-10 11:00:00', false, 'FINAL', 'dddddddd-eeee-4eee-eeee-eeeeeeeeeeee', 'dddddddd-ffff-4fff-ffff-ffffffffffff', 0, 0, NULL, '9acfabd3-0095-41fd-8fda-6177b40ac8bf', '0f10d296-4279-4408-a276-11d9518a69f5');


--
-- Data for Name: player; Type: TABLE DATA; Schema: public; Owner: ayselkaradayi
--

INSERT INTO public.player VALUES ('ClawCommando', 'Max', 'Purrkins', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125124_f83eaf9a.png', 25, 15, NULL, 'bbbbbbbb-2222-4222-2222-222222222222', 'b2222222-1111-4111-1111-111111111111');
INSERT INTO public.player VALUES ('WhiskerStrike', 'Tiger', 'Clawthorne', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125504_808025dd.png', 25, 15, NULL, 'bbbbbbbb-3333-4333-3333-333333333333', 'b3333333-5555-4555-5555-555555555555');
INSERT INTO public.player VALUES ('WhiskerWrath', 'Max', 'Furrington', 'Greece', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125556_097384f6.png', 25, 14, NULL, 'bbbbbbbb-4444-4444-4444-444444444444', 'b4444444-3333-4333-3333-333333333333');
INSERT INTO public.player VALUES ('AngryPaw', 'Boris', 'Ninja', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125818_388d7e45.png', 31, 20, NULL, 'cccccccc-2222-4222-2222-222222222222', 'c2222222-2222-4222-2222-222222222222');
INSERT INTO public.player VALUES ('PawPatroller', 'Charlie', 'Meowton', 'Greece', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125150_e456392f.png', 23, 13, NULL, 'bbbbbbbb-2222-4222-2222-222222222222', 'b2222222-3333-4333-3333-333333333333');
INSERT INTO public.player VALUES ('NightStalker', 'Viktor', 'Scratchev', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125623_74662d8e.png', 23, 12, NULL, 'bbbbbbbb-4444-4444-4444-444444444444', 'b4444444-5555-4555-5555-555555555555');
INSERT INTO public.player VALUES ('FurStrike', 'Elena', 'Pisica', 'Greece', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125712_5ed6942d.png', 33, 20, NULL, 'cccccccc-1111-4111-1111-111111111111', 'c1111111-3333-4333-3333-333333333333');
INSERT INTO public.player VALUES ('QuietClaw', 'Dragan', 'Senko', 'Serbia', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125856_00d3fd81.png', 29, 18, NULL, 'cccccccc-2222-4222-2222-222222222222', 'c2222222-4444-4444-4444-444444444444');
INSERT INTO public.player VALUES ('SquadronPaw', 'Elena', 'Whiskerova', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125937_ea9fcd35.png', 20, 10, NULL, 'dddddddd-1111-4111-1111-111111111111', 'd1111111-2222-4222-2222-222222222222');
INSERT INTO public.player VALUES ('WhiskerWarrior', 'Oliver', 'Furrington', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125247_fc379774.png', 21, 11, NULL, 'bbbbbbbb-2222-4222-2222-222222222222', 'b2222222-5555-4555-5555-555555555555');
INSERT INTO public.player VALUES ('MeowMaster', 'Leo', 'Whiskerton', 'Greece', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125430_25e91952.png', 27, 17, NULL, 'bbbbbbbb-3333-4333-3333-333333333333', 'b3333333-3333-4333-3333-333333333333');
INSERT INTO public.player VALUES ('RageTail', 'Ivan', 'Furiev', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125751_400acb77.png', 31, 18, NULL, 'cccccccc-1111-4111-1111-111111111111', 'c1111111-5555-4555-5555-555555555555');
INSERT INTO public.player VALUES ('WingTail', 'Maria', 'Kotova', 'Serbia', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130003_546b2749.png', 18, 8, NULL, 'dddddddd-1111-4111-1111-111111111111', 'd1111111-4444-4444-4444-444444444444');
INSERT INTO public.player VALUES ('GhostCat', 'Nikolai', 'Purrski', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130030_b3a19f24.png', 20, 11, NULL, 'dddddddd-2222-4222-2222-222222222222', 'd2222222-1111-4111-1111-111111111111');
INSERT INTO public.player VALUES ('SpectralPaw', 'Ana', 'Miacic', 'Serbia', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130045_c4b28e35.png', 18, 9, NULL, 'dddddddd-2222-4222-2222-222222222222', 'd2222222-2222-4222-2222-222222222222');
INSERT INTO public.player VALUES ('SilverClaw', 'Dragan', 'Felinus', 'Serbia', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130100_d5c37d46.png', 17, 8, NULL, 'dddddddd-2222-4222-2222-222222222222', 'd2222222-3333-4333-3333-333333333333');
INSERT INTO public.player VALUES ('MistWhisker', 'Elena', 'Pisica', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130115_e6d46c57.png', 16, 7, NULL, 'dddddddd-2222-4222-2222-222222222222', 'd2222222-4444-4444-4444-444444444444');
INSERT INTO public.player VALUES ('PhantomPurr', 'Radu', 'Catescu', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130130_f7e55b68.png', 15, 6, NULL, 'dddddddd-2222-4222-2222-222222222222', 'd2222222-5555-4555-5555-555555555555');
INSERT INTO public.player VALUES ('ElitePaw', 'Stefan', 'Kotarov', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130145_08f64a79.png', 25, 15, NULL, 'dddddddd-3333-4333-3333-333333333333', 'd3333333-1111-4111-1111-111111111111');
INSERT INTO public.player VALUES ('CommanderClaw', 'Mira', 'Purric', 'Serbia', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130200_19g73b80.png', 23, 14, NULL, 'dddddddd-3333-4333-3333-333333333333', 'd3333333-2222-4222-2222-222222222222');
INSERT INTO public.player VALUES ('TacticalTail', 'Alex', 'Feline', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130215_20h82c91.png', 21, 13, NULL, 'dddddddd-3333-4333-3333-333333333333', 'd3333333-3333-4333-3333-333333333333');
INSERT INTO public.player VALUES ('StealthWhisker', 'Diana', 'Pisoi', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130230_31i91d02.png', 20, 12, NULL, 'dddddddd-3333-4333-3333-333333333333', 'd3333333-4444-4444-4444-444444444444');
INSERT INTO public.player VALUES ('SpecOpsCat', 'Vlad', 'Miaunu', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130245_42j00e13.png', 19, 11, NULL, 'dddddddd-3333-4333-3333-333333333333', 'd3333333-5555-4555-5555-555555555555');
INSERT INTO public.player VALUES ('SpellPaw', 'Boris', 'Magickov', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130300_53k19f24.png', 18, 9, NULL, 'dddddddd-4444-4444-4444-444444444444', 'd4444444-1111-4111-1111-111111111111');
INSERT INTO public.player VALUES ('MysticMeow', 'Katya', 'Wizardova', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130315_64l28e35.png', 17, 8, NULL, 'dddddddd-4444-4444-4444-444444444444', 'd4444444-2222-4222-2222-222222222222');
INSERT INTO public.player VALUES ('RunicPurr', 'Marko', 'Čarobni', 'Serbia', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130330_75m37d46.png', 16, 8, NULL, 'dddddddd-4444-4444-4444-444444444444', 'd4444444-3333-4333-3333-333333333333');
INSERT INTO public.player VALUES ('ArcaneWhisker', 'Ion', 'Vrajitoru', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130345_86n46c57.png', 15, 7, NULL, 'dddddddd-4444-4444-4444-444444444444', 'd4444444-4444-4444-4444-444444444444');
INSERT INTO public.player VALUES ('ScrollClaw', 'Maria', 'Magica', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130400_97o55b68.png', 14, 6, NULL, 'dddddddd-4444-4444-4444-444444444444', 'd4444444-5555-4555-5555-555555555555');
INSERT INTO public.player VALUES ('CaptainClaw', 'Petar', 'Morski', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130415_08p64a79.png', 15, 7, NULL, 'dddddddd-5555-4555-5555-555555555555', 'd5555555-1111-4111-1111-111111111111');
INSERT INTO public.player VALUES ('SeaPaw', 'Nina', 'Piratova', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130430_19q73b80.png', 14, 6, NULL, 'dddddddd-5555-4555-5555-555555555555', 'd5555555-2222-4222-2222-222222222222');
INSERT INTO public.player VALUES ('BuccaneerPurr', 'Luka', 'Gusar', 'Serbia', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130445_20r82c91.png', 13, 6, NULL, 'dddddddd-5555-4555-5555-555555555555', 'd5555555-3333-4333-3333-333333333333');
INSERT INTO public.player VALUES ('SailWhisker', 'Andrei', 'Piratu', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130500_31s91d02.png', 12, 5, NULL, 'dddddddd-5555-4555-5555-555555555555', 'd5555555-4444-4444-4444-444444444444');
INSERT INTO public.player VALUES ('MarauderMeow', 'Elena', 'Corsaru', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130515_42t00e13.png', 11, 4, NULL, 'dddddddd-5555-4555-5555-555555555555', 'd5555555-5555-4555-5555-555555555555');
INSERT INTO public.player VALUES ('SirPurr', 'Kaloyan', 'Ritarev', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130530_53u19f24.png', 28, 16, NULL, 'dddddddd-6666-4666-6666-666666666666', 'd6666666-1111-4111-1111-111111111111');
INSERT INTO public.player VALUES ('LadyWhisker', 'Yana', 'Dvorqnova', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130545_64v28e35.png', 26, 15, NULL, 'dddddddd-6666-4666-6666-666666666666', 'd6666666-2222-4222-2222-222222222222');
INSERT INTO public.player VALUES ('PaladinPaw', 'Nemanja', 'Vitez', 'Serbia', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130600_75w37d46.png', 24, 14, NULL, 'dddddddd-6666-4666-6666-666666666666', 'd6666666-3333-4333-3333-333333333333');
INSERT INTO public.player VALUES ('CrusaderClaw', 'Tudor', 'Cavaler', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130615_86x46c57.png', 22, 13, NULL, 'dddddddd-6666-4666-6666-666666666666', 'd6666666-4444-4444-4444-444444444444');
INSERT INTO public.player VALUES ('NobleNeko', 'Ioana', 'Nobilă', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130630_97y55b68.png', 20, 12, NULL, 'dddddddd-6666-4666-6666-666666666666', 'd6666666-5555-4555-5555-555555555555');
INSERT INTO public.player VALUES ('SiameseWarrior', 'Monika', 'Stefanova', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131210_w0d82c91.png', 18, 9, NULL, 'dddddddd-dddd-4ddd-dddd-dddddddddddd', 'e5555555-4444-4444-4444-444444444444');
INSERT INTO public.player VALUES ('HonorPaw', 'Kristian', 'Angelov', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131225_x1c91d02.png', 17, 8, NULL, 'dddddddd-dddd-4ddd-dddd-dddddddddddd', 'e5555555-5555-4555-5555-555555555555');
INSERT INTO public.player VALUES ('GoldenFang', 'Plamen', 'Kolev', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131240_y2b00e13.png', 24, 15, NULL, 'dddddddd-eeee-4eee-eeee-eeeeeeeeeeee', 'e6666666-1111-4111-1111-111111111111');
INSERT INTO public.player VALUES ('RageWhiskers', 'Gabriela', 'Todorova', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131255_z3a19f24.png', 23, 14, NULL, 'dddddddd-eeee-4eee-eeee-eeeeeeeeeeee', 'e6666666-2222-4222-2222-222222222222');
INSERT INTO public.player VALUES ('FurStorm', 'Deyan', 'Popov', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131310_a4b28e35.png', 22, 13, NULL, 'dddddddd-eeee-4eee-eeee-eeeeeeeeeeee', 'e6666666-3333-4333-3333-333333333333');
INSERT INTO public.player VALUES ('WhiskerRage', 'Simona', 'Nikolova', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131325_b5c37d46.png', 21, 12, NULL, 'dddddddd-eeee-4eee-eeee-eeeeeeeeeeee', 'e6666666-4444-4444-4444-444444444444');
INSERT INTO public.player VALUES ('FuryPounce', 'Anton', 'Marinov', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131340_c6d46c57.png', 20, 11, NULL, 'dddddddd-eeee-4eee-eeee-eeeeeeeeeeee', 'e6666666-5555-4555-5555-555555555555');
INSERT INTO public.player VALUES ('WarriorPaw', 'Dimitar', 'Stoyanov', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131355_d7e55b68.png', 20, 13, NULL, 'dddddddd-ffff-4fff-ffff-ffffffffffff', 'e7777777-1111-4111-1111-111111111111');
INSERT INTO public.player VALUES ('BattleWhisker', 'Kalina', 'Mihaylova', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131410_e8f64a79.png', 19, 12, NULL, 'dddddddd-ffff-4fff-ffff-ffffffffffff', 'e7777777-2222-4222-2222-222222222222');
INSERT INTO public.player VALUES ('WhiskerBlade', 'Yavor', 'Kovachev', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131425_f9g73b80.png', 18, 11, NULL, 'dddddddd-ffff-4fff-ffff-ffffffffffff', 'e7777777-3333-4333-3333-333333333333');
INSERT INTO public.player VALUES ('StrikePaw', 'Daniela', 'Ilieva', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131440_g0h82c91.png', 17, 10, NULL, 'dddddddd-ffff-4fff-ffff-ffffffffffff', 'e7777777-4444-4444-4444-444444444444');
INSERT INTO public.player VALUES ('WarriorFang', 'Petar', 'Yordanov', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131455_h1i91d02.png', 16, 9, NULL, 'dddddddd-ffff-4fff-ffff-ffffffffffff', 'e7777777-5555-4555-5555-555555555555');
INSERT INTO public.player VALUES ('AdmiralPaw', 'Georgi', 'Morqkov', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131855_x7y55b68.png', 24, 13, NULL, 'dddddddd-7777-4777-7777-777777777777', 'd7777777-1111-4111-1111-111111111111');
INSERT INTO public.player VALUES ('CatnipKing', 'Max', 'Meowster', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_123009_02194df1.png', 35, 22, NULL, 'aaaaaaaa-2222-4222-2222-222222222222', 'a2222222-1111-4111-1111-111111111111');
INSERT INTO public.player VALUES ('PawPatrol', 'Bella', 'Purrington', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_123123_5ca24ab3.png', 33, 20, NULL, 'aaaaaaaa-2222-4222-2222-222222222222', 'a2222222-2222-4222-2222-222222222222');
INSERT INTO public.player VALUES ('PurrMaster', 'Charlie', 'Furbottom', 'Greece', 'https://kittenstrike.s3.amazonaws.com/players/20241127_123145_3fb30411.png', 34, 21, NULL, 'aaaaaaaa-2222-4222-2222-222222222222', 'a2222222-3333-4333-3333-333333333333');
INSERT INTO public.player VALUES ('ClawCommander', 'Lucy', 'Tailsworth', 'Serbia', 'https://kittenstrike.s3.amazonaws.com/players/20241127_124514_d9b7b50a.png', 32, 19, NULL, 'aaaaaaaa-2222-4222-2222-222222222222', 'a2222222-4444-4444-4444-444444444444');
INSERT INTO public.player VALUES ('WhiskerOps', 'Tiger', 'Pawsome', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_124530_bb2ab86f.png', 31, 18, NULL, 'aaaaaaaa-2222-4222-2222-222222222222', 'a2222222-5555-4555-5555-555555555555');
INSERT INTO public.player VALUES ('FurryFury', 'Shadow', 'Clawson', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_124544_4e0eb30b.png', 38, 24, NULL, 'aaaaaaaa-3333-4333-3333-333333333333', 'a3333333-1111-4111-1111-111111111111');
INSERT INTO public.player VALUES ('PurrPlatoon', 'Simba', 'Scratches', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_124602_b001a537.png', 36, 23, NULL, 'aaaaaaaa-3333-4333-3333-333333333333', 'a3333333-2222-4222-2222-222222222222');
INSERT INTO public.player VALUES ('KittyKommando', 'Nala', 'Purrfect', 'Greece', 'https://kittenstrike.s3.amazonaws.com/players/20241127_124625_5f140174.png', 35, 22, NULL, 'aaaaaaaa-3333-4333-3333-333333333333', 'a3333333-3333-4333-3333-333333333333');
INSERT INTO public.player VALUES ('ShyTail', 'Rocky', 'Whiskers', 'Serbia', 'https://kittenstrike.s3.amazonaws.com/players/20241127_124641_07320677.png', 33, 20, NULL, 'aaaaaaaa-3333-4333-3333-333333333333', 'a3333333-4444-4444-4444-444444444444');
INSERT INTO public.player VALUES ('StealthyPaws', 'Misty', 'Meowington', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_124656_9f415c2f.png', 34, 21, NULL, 'aaaaaaaa-3333-4333-3333-333333333333', 'a3333333-5555-4555-5555-555555555555');
INSERT INTO public.player VALUES ('KittyKiller', 'Jack', 'Furrington', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_124713_40be47e6.png', 37, 25, NULL, 'aaaaaaaa-4444-4444-4444-444444444444', 'a4444444-1111-4111-1111-111111111111');
INSERT INTO public.player VALUES ('PawPunisher', 'Coco', 'Clawthorne', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_124728_4ebb248e.png', 35, 23, NULL, 'aaaaaaaa-4444-4444-4444-444444444444', 'a4444444-2222-4222-2222-222222222222');
INSERT INTO public.player VALUES ('MeowMachine', 'Oliver', 'Scratchley', 'Greece', 'https://kittenstrike.s3.amazonaws.com/players/20241127_124744_f307aa76.png', 34, 22, NULL, 'aaaaaaaa-4444-4444-4444-444444444444', 'a4444444-3333-4333-3333-333333333333');
INSERT INTO public.player VALUES ('ClawWrath', 'Lily', 'Pawsworth', 'Serbia', 'https://kittenstrike.s3.amazonaws.com/players/20241127_124759_3df60fe5.png', 33, 21, NULL, 'aaaaaaaa-4444-4444-4444-444444444444', 'a4444444-4444-4444-4444-444444444444');
INSERT INTO public.player VALUES ('FurryFatal', 'Milo', 'Kittensworth', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_124819_a03980f9.png', 32, 20, NULL, 'aaaaaaaa-4444-4444-4444-444444444444', 'a4444444-5555-4555-5555-555555555555');
INSERT INTO public.player VALUES ('WhiskerAim', 'Felix', 'Pawson', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_124833_72e4b3f8.png', 45, 32, 'e4444444-4444-4444-4444-444444444444', 'aaaaaaaa-1111-4111-1111-111111111111', 'aaaaaaaa-1111-4111-1111-aaaaaaaaaaaa');
INSERT INTO public.player VALUES ('PurrSniper', 'Luna', 'Clawford', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_124846_398d141e.png', 42, 30, NULL, 'aaaaaaaa-1111-4111-1111-111111111111', 'aaaaaaaa-2222-4222-2222-aaaaaaaaaaaa');
INSERT INTO public.player VALUES ('CatEye', 'Oscar', 'Whiskerston', 'Greece', 'https://kittenstrike.s3.amazonaws.com/players/20241127_124900_31df2c18.png', 40, 28, NULL, 'aaaaaaaa-1111-4111-1111-111111111111', 'aaaaaaaa-3333-4333-3333-aaaaaaaaaaaa');
INSERT INTO public.player VALUES ('KittyKaos', 'Bella', 'Clawswell', 'Serbia', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125056_2450e2c5.png', 24, 14, NULL, 'bbbbbbbb-1111-4111-1111-111111111111', 'b1111111-4444-4444-4444-444444444444');
INSERT INTO public.player VALUES ('SneakyPaw', 'Milo', 'Kittenson', 'Serbia', 'https://kittenstrike.s3.amazonaws.com/players/20241127_124938_09d33e01.png', 38, 25, NULL, 'aaaaaaaa-1111-4111-1111-111111111111', 'aaaaaaaa-4444-4444-4444-aaaaaaaaaaaa');
INSERT INTO public.player VALUES ('NinjaKitty', 'Leo', 'Scratchington', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_124954_d44ebf2e.png', 41, 29, NULL, 'aaaaaaaa-1111-4111-1111-111111111111', 'aaaaaaaa-5555-4555-5555-aaaaaaaaaaaa');
INSERT INTO public.player VALUES ('CatCrusher', 'Duke', 'Whiskerton', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125008_3859f407.png', 28, 18, NULL, 'bbbbbbbb-1111-4111-1111-111111111111', 'b1111111-1111-4111-1111-111111111111');
INSERT INTO public.player VALUES ('PurrPredator', 'Luna', 'Scratchington', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125024_9468085c.png', 26, 16, NULL, 'bbbbbbbb-1111-4111-1111-111111111111', 'b1111111-2222-4222-2222-222222222222');
INSERT INTO public.player VALUES ('MeowMercenary', 'Salem', 'Pawstrong', 'Greece', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125039_ad82155f.png', 25, 15, NULL, 'bbbbbbbb-1111-4111-1111-111111111111', 'b1111111-3333-4333-3333-333333333333');
INSERT INTO public.player VALUES ('WhiskerWar', 'Leo', 'Fursworth', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125110_6d792842.png', 23, 13, NULL, 'bbbbbbbb-1111-4111-1111-111111111111', 'b1111111-5555-4555-5555-555555555555');
INSERT INTO public.player VALUES ('NinjaNeko', 'Sophie', 'Whiskersmith', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125136_395f04ce.png', 24, 14, NULL, 'bbbbbbbb-2222-4222-2222-222222222222', 'b2222222-2222-4222-2222-222222222222');
INSERT INTO public.player VALUES ('StealthScratch', 'Lucy', 'Clawton', 'Serbia', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125224_191beaef.png', 22, 12, NULL, 'bbbbbbbb-2222-4222-2222-222222222222', 'b2222222-4444-4444-4444-444444444444');
INSERT INTO public.player VALUES ('KombatKitten', 'Milo', 'Scratchwell', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125316_50b9d3fa.png', 30, 20, NULL, 'bbbbbbbb-3333-4333-3333-333333333333', 'b3333333-1111-4111-1111-111111111111');
INSERT INTO public.player VALUES ('PurrPunch', 'Luna', 'Pawstrong', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125413_d9ac5b00.png', 28, 18, NULL, 'bbbbbbbb-3333-4333-3333-333333333333', 'b3333333-2222-4222-2222-222222222222');
INSERT INTO public.player VALUES ('ClawKombat', 'Bella', 'Furworth', 'Serbia', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125449_d2416e61.png', 26, 16, NULL, 'bbbbbbbb-3333-4333-3333-333333333333', 'b3333333-4444-4444-4444-444444444444');
INSERT INTO public.player VALUES ('PredatorPurr', 'Shadow', 'Meowington', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125519_164abf8a.png', 27, 16, NULL, 'bbbbbbbb-4444-4444-4444-444444444444', 'b4444444-1111-4111-1111-111111111111');
INSERT INTO public.player VALUES ('ClawCrusher', 'Luna', 'Pawsworth', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125538_8593cd1e.png', 26, 15, NULL, 'bbbbbbbb-4444-4444-4444-444444444444', 'b4444444-2222-4222-2222-222222222222');
INSERT INTO public.player VALUES ('PawProwler', 'Sofia', 'Clawthorne', 'Serbia', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125608_b848f99e.png', 24, 13, NULL, 'bbbbbbbb-4444-4444-4444-444444444444', 'b4444444-4444-4444-4444-444444444444');
INSERT INTO public.player VALUES ('FuryFang', 'Radu', 'Miaunu', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125642_97657080.png', 35, 22, NULL, 'cccccccc-1111-4111-1111-111111111111', 'c1111111-1111-4111-1111-111111111111');
INSERT INTO public.player VALUES ('RageClaw', 'Dimitar', 'Kotev', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125656_f097c811.png', 34, 21, NULL, 'cccccccc-1111-4111-1111-111111111111', 'c1111111-2222-4222-2222-222222222222');
INSERT INTO public.player VALUES ('AngerPaw', 'Nikola', 'Mačka', 'Serbia', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125732_cc1190b6.png', 32, 19, NULL, 'cccccccc-1111-4111-1111-111111111111', 'c1111111-4444-4444-4444-444444444444');
INSERT INTO public.player VALUES ('ShadowCat', 'Ana', 'Sensei', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125805_6e95cefa.png', 32, 21, NULL, 'cccccccc-2222-4222-2222-222222222222', 'c2222222-1111-4111-1111-111111111111');
INSERT INTO public.player VALUES ('StealthFur', 'Maria', 'Tiho', 'Greece', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125832_64daa280.png', 30, 19, NULL, 'cccccccc-2222-4222-2222-222222222222', 'c2222222-3333-4333-3333-333333333333');
INSERT INTO public.player VALUES ('NightWhisker', 'Peter', 'Yamato', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125909_467ea824.png', 28, 17, NULL, 'cccccccc-2222-4222-2222-222222222222', 'c2222222-5555-4555-5555-555555555555');
INSERT INTO public.player VALUES ('ScratchMaster', 'Viktor', 'Kotev', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125922_603ea037.png', 22, 12, NULL, 'dddddddd-1111-4111-1111-111111111111', 'd1111111-1111-4111-1111-111111111111');
INSERT INTO public.player VALUES ('AirClaw', 'Boris', 'Pawlov', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_125949_773fcc96.png', 19, 9, NULL, 'dddddddd-1111-4111-1111-111111111111', 'd1111111-3333-4333-3333-333333333333');
INSERT INTO public.player VALUES ('SkyWhisker', 'Ivan', 'Meowov', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130017_e239043a.png', 17, 7, NULL, 'dddddddd-1111-4111-1111-111111111111', 'd1111111-5555-4555-5555-555555555555');
INSERT INTO public.player VALUES ('PatrolPaw', 'Viktor', 'Patrolski', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131510_i2j00e13.png', 22, 12, NULL, 'dddddddd-0000-4000-0000-000000000000', 'e1111111-1111-4111-1111-111111111111');
INSERT INTO public.player VALUES ('TemplarNeko', 'Ivan', 'Templar', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131525_j3k19f24.png', 15, 7, NULL, 'dddddddd-9999-4999-9999-999999999999', 'd9999999-5555-4555-5555-555555555555');
INSERT INTO public.player VALUES ('SquirePurr', 'Elena', 'Vitezova', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131540_k4l28e35.png', 16, 8, NULL, 'dddddddd-9999-4999-9999-999999999999', 'd9999999-4444-4444-4444-444444444444');
INSERT INTO public.player VALUES ('PaladinWhisker', 'Dragan', 'Paladin', 'Serbia', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131555_l5m37d46.png', 17, 9, NULL, 'dddddddd-9999-4999-9999-999999999999', 'd9999999-3333-4333-3333-333333333333');
INSERT INTO public.player VALUES ('KnightClaw', 'Ana', 'Vitez', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131610_m6n46c57.png', 18, 10, NULL, 'dddddddd-9999-4999-9999-999999999999', 'd9999999-2222-4222-2222-222222222222');
INSERT INTO public.player VALUES ('CrusaderPaw', 'Nikola', 'Krstaš', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131625_n7o55b68.png', 20, 11, NULL, 'dddddddd-9999-4999-9999-999999999999', 'd9999999-1111-4111-1111-111111111111');
INSERT INTO public.player VALUES ('DefenderNeko', 'Ivan', 'Branitelj', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131640_o8p64a79.png', 17, 8, NULL, 'dddddddd-8888-4888-8888-888888888888', 'd8888888-5555-4555-5555-555555555555');
INSERT INTO public.player VALUES ('ChampionPurr', 'Ana', 'Borkinja', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131655_p9q73b80.png', 18, 9, NULL, 'dddddddd-8888-4888-8888-888888888888', 'd8888888-4444-4444-4444-444444444444');
INSERT INTO public.player VALUES ('GladiatorWhisker', 'Dragan', 'Borac', 'Serbia', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131710_q0r82c91.png', 19, 10, NULL, 'dddddddd-8888-4888-8888-888888888888', 'd8888888-3333-4333-3333-333333333333');
INSERT INTO public.player VALUES ('WarriorClaw', 'Maria', 'Borkinja', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131725_r1s91d02.png', 20, 11, NULL, 'dddddddd-8888-4888-8888-888888888888', 'd8888888-2222-4222-2222-222222222222');
INSERT INTO public.player VALUES ('FighterPaw', 'Ivan', 'Borec', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131740_s2t00e13.png', 22, 12, NULL, 'dddddddd-8888-4888-8888-888888888888', 'd8888888-1111-4111-1111-111111111111');
INSERT INTO public.player VALUES ('SailorPurr', 'Elena', 'Mornarova', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131755_t3u19f24.png', 16, 9, NULL, 'dddddddd-7777-4777-7777-777777777777', 'd7777777-5555-4555-5555-555555555555');
INSERT INTO public.player VALUES ('NavyWhisker', 'Bogdan', 'Marinar', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131810_u4v28e35.png', 18, 10, NULL, 'dddddddd-7777-4777-7777-777777777777', 'd7777777-4444-4444-4444-444444444444');
INSERT INTO public.player VALUES ('MarineMeow', 'Vuk', 'Mornar', 'Serbia', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131825_v5w37d46.png', 20, 11, NULL, 'dddddddd-7777-4777-7777-777777777777', 'd7777777-3333-4333-3333-333333333333');
INSERT INTO public.player VALUES ('CaptainPaw', 'Irina', 'Flotova', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131840_w6x46c57.png', 22, 12, NULL, 'dddddddd-7777-4777-7777-777777777777', 'd7777777-2222-4222-2222-222222222222');
INSERT INTO public.player VALUES ('GuardianClaw', 'Ana', 'Guardianova', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130640_a8z64a79.png', 20, 11, NULL, 'dddddddd-0000-4000-0000-000000000000', 'e1111111-2222-4222-2222-222222222222');
INSERT INTO public.player VALUES ('DefenderWhisker', 'Dragan', 'Defender', 'Serbia', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130655_b9y73b80.png', 19, 10, NULL, 'dddddddd-0000-4000-0000-000000000000', 'e1111111-3333-4333-3333-333333333333');
INSERT INTO public.player VALUES ('ProtectorPurr', 'Elena', 'Zashtitnik', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130710_c0x82c91.png', 18, 9, NULL, 'dddddddd-0000-4000-0000-000000000000', 'e1111111-4444-4444-4444-444444444444');
INSERT INTO public.player VALUES ('SafeguardNeko', 'Ivan', 'Zashtitnikov', 'Romania', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130725_d1w91d02.png', 17, 8, NULL, 'dddddddd-0000-4000-0000-000000000000', 'e1111111-5555-4555-5555-555555555555');
INSERT INTO public.player VALUES ('TigerFang', 'Martin', 'Petrov', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130740_e2v00e13.png', 23, 14, NULL, 'dddddddd-aaaa-4aaa-aaaa-aaaaaaaaaaaa', 'e2222222-1111-4111-1111-111111111111');
INSERT INTO public.player VALUES ('StripedWarrior', 'Nina', 'Kovacheva', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130755_f3u19f24.png', 21, 12, NULL, 'dddddddd-aaaa-4aaa-aaaa-aaaaaaaaaaaa', 'e2222222-2222-4222-2222-222222222222');
INSERT INTO public.player VALUES ('JungleProwler', 'Boris', 'Ivanov', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130810_g4t28e35.png', 20, 11, NULL, 'dddddddd-aaaa-4aaa-aaaa-aaaaaaaaaaaa', 'e2222222-3333-4333-3333-333333333333');
INSERT INTO public.player VALUES ('RoaringThunder', 'Maria', 'Dimitrova', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130825_h5s37d46.png', 19, 10, NULL, 'dddddddd-aaaa-4aaa-aaaa-aaaaaaaaaaaa', 'e2222222-4444-4444-4444-444444444444');
INSERT INTO public.player VALUES ('TigerStripe', 'Georgi', 'Todorov', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130840_i6r46c57.png', 18, 9, NULL, 'dddddddd-aaaa-4aaa-aaaa-aaaaaaaaaaaa', 'e2222222-5555-4555-5555-555555555555');
INSERT INTO public.player VALUES ('ClawMaster', 'Stefan', 'Nikolov', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130855_j7q55b68.png', 26, 17, NULL, 'dddddddd-bbbb-4bbb-bbbb-bbbbbbbbbbbb', 'e3333333-1111-4111-1111-111111111111');
INSERT INTO public.player VALUES ('SharpClaw', 'Diana', 'Petrova', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130910_k8p64a79.png', 24, 15, NULL, 'dddddddd-bbbb-4bbb-bbbb-bbbbbbbbbbbb', 'e3333333-2222-4222-2222-222222222222');
INSERT INTO public.player VALUES ('ClawStrike', 'Veselin', 'Georgiev', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130925_l9o73b80.png', 23, 14, NULL, 'dddddddd-bbbb-4bbb-bbbb-bbbbbbbbbbbb', 'e3333333-3333-4333-3333-333333333333');
INSERT INTO public.player VALUES ('ClawHunter', 'Silvia', 'Stoyanova', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130940_m0n82c91.png', 22, 13, NULL, 'dddddddd-bbbb-4bbb-bbbb-bbbbbbbbbbbb', 'e3333333-4444-4444-4444-444444444444');
INSERT INTO public.player VALUES ('ClawLegend', 'Kaloyan', 'Ivanov', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_130955_n1m91d02.png', 21, 12, NULL, 'dddddddd-bbbb-4bbb-bbbb-bbbbbbbbbbbb', 'e3333333-5555-4555-5555-555555555555');
INSERT INTO public.player VALUES ('NekoShadow', 'Rumen', 'Hristov', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131010_o2l00e13.png', 19, 11, NULL, 'dddddddd-cccc-4ccc-cccc-cccccccccccc', 'e4444444-1111-4111-1111-111111111111');
INSERT INTO public.player VALUES ('SilentPaw', 'Viktoria', 'Angelova', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131025_p3k19f24.png', 18, 10, NULL, 'dddddddd-cccc-4ccc-cccc-cccccccccccc', 'e4444444-2222-4222-2222-222222222222');
INSERT INTO public.player VALUES ('NinjaWhisker', 'Pavel', 'Dimitrov', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131040_q4j28e35.png', 17, 9, NULL, 'dddddddd-cccc-4ccc-cccc-cccccccccccc', 'e4444444-3333-4333-3333-333333333333');
INSERT INTO public.player VALUES ('StealthCat', 'Anita', 'Koleva', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131055_r5i37d46.png', 16, 8, NULL, 'dddddddd-cccc-4ccc-cccc-cccccccccccc', 'e4444444-4444-4444-4444-444444444444');
INSERT INTO public.player VALUES ('ShadowClaw', 'Stoyan', 'Petkov', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131110_s6h46c57.png', 15, 7, NULL, 'dddddddd-cccc-4ccc-cccc-cccccccccccc', 'e4444444-5555-4555-5555-555555555555');
INSERT INTO public.player VALUES ('SamuraiKitty', 'Todor', 'Vasilev', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131125_t7g55b68.png', 21, 12, NULL, 'dddddddd-dddd-4ddd-dddd-dddddddddddd', 'e5555555-1111-4111-1111-111111111111');
INSERT INTO public.player VALUES ('BushidoCat', 'Ralitsa', 'Ivanova', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131140_u8f64a79.png', 20, 11, NULL, 'dddddddd-dddd-4ddd-dddd-dddddddddddd', 'e5555555-2222-4222-2222-222222222222');
INSERT INTO public.player VALUES ('KatanaPaw', 'Angel', 'Georgiev', 'Bulgaria', 'https://kittenstrike.s3.amazonaws.com/players/20241127_131155_v9e73b80.png', 19, 10, NULL, 'dddddddd-dddd-4ddd-dddd-dddddddddddd', 'e5555555-3333-4333-3333-333333333333');


--
-- Data for Name: prizecut; Type: TABLE DATA; Schema: public; Owner: ayselkaradayi
--

INSERT INTO public.prizecut VALUES (1, 3500, '11111111-1111-4111-1111-111111111111', 'aaaaaaaa-1111-4111-1111-111111111111', 'aa111111-1111-4111-1111-111111111111');
INSERT INTO public.prizecut VALUES (2, 1500, '11111111-1111-4111-1111-111111111111', 'aaaaaaaa-4444-4444-4444-444444444444', 'aa222222-2222-4222-2222-222222222222');
INSERT INTO public.prizecut VALUES (1, 7000, '33333333-3333-4333-3333-333333333333', NULL, 'aa333333-3333-4333-3333-333333333333');
INSERT INTO public.prizecut VALUES (2, 3000, '33333333-3333-4333-3333-333333333333', NULL, 'aa444444-4444-4444-4444-444444444444');
INSERT INTO public.prizecut VALUES (1, 2100, '44444444-4444-4444-4444-444444444444', NULL, 'aa555555-5555-4555-5555-555555555555');
INSERT INTO public.prizecut VALUES (2, 900, '44444444-4444-4444-4444-444444444444', NULL, 'aa666666-6666-4666-6666-666666666666');
INSERT INTO public.prizecut VALUES (1, 350, '2fa75271-3dd6-4e4b-b3b7-42fac6142393', NULL, 'b5914ee5-9be5-4d6f-b27f-da243dd7b9de');
INSERT INTO public.prizecut VALUES (2, 150, '2fa75271-3dd6-4e4b-b3b7-42fac6142393', NULL, '3275df58-4a65-42c7-a656-5f43df877b6d');
INSERT INTO public.prizecut VALUES (1, 16100, '6da06af0-3c0a-4f1c-83d4-46f275f4dfd8', NULL, 'a47b3345-ab64-43e2-a492-70397cea7e0a');
INSERT INTO public.prizecut VALUES (2, 6900, '6da06af0-3c0a-4f1c-83d4-46f275f4dfd8', NULL, '247569ff-1d3c-43cd-afef-65fb5aa388e7');
INSERT INTO public.prizecut VALUES (1, 38500, 'd2b7e127-5a86-479e-b829-a4e137d3b716', NULL, '56017ce2-71aa-45ba-b449-376f08a96898');
INSERT INTO public.prizecut VALUES (2, 16500, 'd2b7e127-5a86-479e-b829-a4e137d3b716', NULL, 'e4111c9a-eac7-43de-9844-765ab1fd1fb3');
INSERT INTO public.prizecut VALUES (1, 1190, 'd76ecc3c-db83-4f5b-a7c7-91b706871725', NULL, '9791b5cd-487a-4e9d-86cd-67c9c98582ef');
INSERT INTO public.prizecut VALUES (2, 510, 'd76ecc3c-db83-4f5b-a7c7-91b706871725', NULL, 'cbeb8850-929d-43a8-86fa-948094328de6');
INSERT INTO public.prizecut VALUES (1, 9100, '9acfabd3-0095-41fd-8fda-6177b40ac8bf', NULL, '9c136a00-2bd5-4918-a25f-af0aad979798');
INSERT INTO public.prizecut VALUES (2, 3900, '9acfabd3-0095-41fd-8fda-6177b40ac8bf', NULL, 'd05ea68f-3603-4db2-a337-e59c923410a5');
INSERT INTO public.prizecut VALUES (1, 5250, '11111111-2222-4222-2222-222222222222', 'aaaaaaaa-1111-4111-1111-111111111111', 'ac111111-1111-4111-1111-111111111111');
INSERT INTO public.prizecut VALUES (2, 2250, '11111111-2222-4222-2222-222222222222', 'dddddddd-1111-4111-1111-111111111111', 'ac111111-1112-4111-1112-111111111112');
INSERT INTO public.prizecut VALUES (1, 4200, '11111111-3333-4333-3333-333333333333', 'aaaaaaaa-2222-4222-2222-222222222222', 'ac111111-1113-4111-1113-111111111113');
INSERT INTO public.prizecut VALUES (2, 1800, '11111111-3333-4333-3333-333333333333', 'dddddddd-2222-4222-2222-222222222222', 'ac111111-1114-4111-1114-111111111114');
INSERT INTO public.prizecut VALUES (1, 2100, '11111111-4444-4444-4444-444444444444', 'aaaaaaaa-1111-4111-1111-111111111111', 'ac111111-1115-4111-1115-111111111115');
INSERT INTO public.prizecut VALUES (2, 900, '11111111-4444-4444-4444-444444444444', 'dddddddd-3333-4333-3333-333333333333', 'ac111111-1116-4111-1116-111111111116');
INSERT INTO public.prizecut VALUES (1, 5600, '11111111-5555-4555-5555-555555555555', 'aaaaaaaa-3333-4333-3333-333333333333', 'ac111111-1117-4111-1117-111111111117');
INSERT INTO public.prizecut VALUES (2, 2400, '11111111-5555-4555-5555-555555555555', 'dddddddd-4444-4444-4444-444444444444', 'ac111111-1118-4111-1118-111111111118');
INSERT INTO public.prizecut VALUES (1, 7000, '11111111-6666-4666-6666-666666666666', 'aaaaaaaa-1111-4111-1111-111111111111', 'ac111111-1119-4111-1119-111111111119');
INSERT INTO public.prizecut VALUES (2, 3000, '11111111-6666-4666-6666-666666666666', 'dddddddd-5555-4555-5555-555555555555', 'ac111111-1120-4111-1120-111111111120');
INSERT INTO public.prizecut VALUES (1, 2800, '11111111-7777-4777-7777-777777777777', 'aaaaaaaa-2222-4222-2222-222222222222', 'ac111111-1121-4111-1121-111111111121');
INSERT INTO public.prizecut VALUES (2, 1200, '11111111-7777-4777-7777-777777777777', 'dddddddd-6666-4666-6666-666666666666', 'ac111111-1122-4111-1122-111111111122');
INSERT INTO public.prizecut VALUES (1, 3850, '11111111-8888-4888-8888-888888888888', 'aaaaaaaa-1111-4111-1111-111111111111', 'ac111111-1123-4111-1123-111111111123');
INSERT INTO public.prizecut VALUES (2, 1650, '11111111-8888-4888-8888-888888888888', 'dddddddd-7777-4777-7777-777777777777', 'ac111111-1124-4111-1124-111111111124');
INSERT INTO public.prizecut VALUES (1, 4900, '11111111-9999-4999-9999-999999999999', 'aaaaaaaa-3333-4333-3333-333333333333', 'ac111111-1125-4111-1125-111111111125');
INSERT INTO public.prizecut VALUES (2, 2100, '11111111-9999-4999-9999-999999999999', 'dddddddd-8888-4888-8888-888888888888', 'ac111111-1126-4111-1126-111111111126');
INSERT INTO public.prizecut VALUES (1, 2450, '11111111-aaaa-4aaa-aaaa-aaaaaaaaaaaa', 'aaaaaaaa-2222-4222-2222-222222222222', 'ac111111-1127-4111-1127-111111111127');
INSERT INTO public.prizecut VALUES (2, 1050, '11111111-aaaa-4aaa-aaaa-aaaaaaaaaaaa', 'dddddddd-9999-4999-9999-999999999999', 'ac111111-1128-4111-1128-111111111128');
INSERT INTO public.prizecut VALUES (1, 4550, '11111111-bbbb-4bbb-bbbb-bbbbbbbbbbbb', 'aaaaaaaa-1111-4111-1111-111111111111', 'ac111111-1129-4111-1129-111111111129');
INSERT INTO public.prizecut VALUES (2, 1950, '11111111-bbbb-4bbb-bbbb-bbbbbbbbbbbb', 'dddddddd-aaaa-4aaa-aaaa-aaaaaaaaaaaa', 'ac111111-1130-4111-1130-111111111130');
INSERT INTO public.prizecut VALUES (1, 5950, '11111111-cccc-4ccc-cccc-cccccccccccc', 'aaaaaaaa-3333-4333-3333-333333333333', 'ac111111-1131-4111-1131-111111111131');
INSERT INTO public.prizecut VALUES (2, 2550, '11111111-cccc-4ccc-cccc-cccccccccccc', 'dddddddd-bbbb-4bbb-bbbb-bbbbbbbbbbbb', 'ac111111-1132-4111-1132-111111111132');
INSERT INTO public.prizecut VALUES (1, 3150, '11111111-dddd-4ddd-dddd-dddddddddddd', 'aaaaaaaa-2222-4222-2222-222222222222', 'ac111111-1133-4111-1133-111111111133');
INSERT INTO public.prizecut VALUES (2, 1350, '11111111-dddd-4ddd-dddd-dddddddddddd', 'dddddddd-cccc-4ccc-cccc-cccccccccccc', 'ac111111-1134-4111-1134-111111111134');
INSERT INTO public.prizecut VALUES (1, 5040, '11111111-eeee-4eee-eeee-eeeeeeeeeeee', 'aaaaaaaa-1111-4111-1111-111111111111', 'ac111111-1135-4111-1135-111111111135');
INSERT INTO public.prizecut VALUES (2, 2160, '11111111-eeee-4eee-eeee-eeeeeeeeeeee', 'dddddddd-dddd-4ddd-dddd-dddddddddddd', 'ac111111-1136-4111-1136-111111111136');
INSERT INTO public.prizecut VALUES (1, 6300, '11111111-ffff-4fff-ffff-ffffffffffff', 'aaaaaaaa-3333-4333-3333-333333333333', 'ac111111-1137-4111-1137-111111111137');
INSERT INTO public.prizecut VALUES (2, 2700, '11111111-ffff-4fff-ffff-ffffffffffff', 'dddddddd-eeee-4eee-eeee-eeeeeeeeeeee', 'ac111111-1138-4111-1138-111111111138');
INSERT INTO public.prizecut VALUES (1, 2660, '22222222-1111-4111-1111-111111111111', 'aaaaaaaa-2222-4222-2222-222222222222', 'ac111111-1139-4111-1139-111111111139');
INSERT INTO public.prizecut VALUES (2, 1140, '22222222-1111-4111-1111-111111111111', 'dddddddd-ffff-4fff-ffff-ffffffffffff', 'ac111111-1140-4111-1140-111111111140');
INSERT INTO public.prizecut VALUES (1, 4760, '22222222-2222-4222-2222-222222222222', 'aaaaaaaa-1111-4111-1111-111111111111', 'ac111111-1141-4111-1141-111111111141');
INSERT INTO public.prizecut VALUES (2, 2040, '22222222-2222-4222-2222-222222222222', 'dddddddd-1111-4111-1111-111111111111', 'ac111111-1142-4111-1142-111111111142');
INSERT INTO public.prizecut VALUES (1, 5740, '22222222-3333-4333-3333-333333333333', 'aaaaaaaa-3333-4333-3333-333333333333', 'ac111111-1143-4111-1143-111111111143');
INSERT INTO public.prizecut VALUES (2, 2460, '22222222-3333-4333-3333-333333333333', 'dddddddd-2222-4222-2222-222222222222', 'ac111111-1144-4111-1144-111111111144');
INSERT INTO public.prizecut VALUES (1, 2940, '22222222-4444-4444-4444-444444444444', 'aaaaaaaa-2222-4222-2222-222222222222', 'ac111111-1145-4111-1145-111111111145');
INSERT INTO public.prizecut VALUES (2, 1260, '22222222-4444-4444-4444-444444444444', 'dddddddd-3333-4333-3333-333333333333', 'ac111111-1146-4111-1146-111111111146');
INSERT INTO public.prizecut VALUES (1, 5460, '22222222-5555-4555-5555-555555555555', 'aaaaaaaa-1111-4111-1111-111111111111', 'ac111111-1147-4111-1147-111111111147');
INSERT INTO public.prizecut VALUES (2, 2340, '22222222-5555-4555-5555-555555555555', 'dddddddd-4444-4444-4444-444444444444', 'ac111111-1148-4111-1148-111111111148');
INSERT INTO public.prizecut VALUES (1, 6650, '22222222-6666-4666-6666-666666666666', 'aaaaaaaa-3333-4333-3333-333333333333', 'ac111111-1149-4111-1149-111111111149');
INSERT INTO public.prizecut VALUES (2, 2850, '22222222-6666-4666-6666-666666666666', 'dddddddd-5555-4555-5555-555555555555', 'ac111111-1150-4111-1150-111111111150');


--
-- Data for Name: request; Type: TABLE DATA; Schema: public; Owner: ayselkaradayi
--

INSERT INTO public.request VALUES ('PENDING', '2024-03-15 14:30:00+02', NULL, 'LINK_USER_TO_PLAYER', 'e7777777-7777-4777-7777-777777777777', 'ClawCommando', NULL, 'f1111111-1111-4111-1111-111111111111');
INSERT INTO public.request VALUES ('PENDING', '2024-03-18 09:15:00+02', NULL, 'LINK_USER_TO_PLAYER', 'e8888888-8888-4888-8888-888888888888', 'KombatKitten', NULL, 'f2222222-2222-4222-2222-222222222222');
INSERT INTO public.request VALUES ('PENDING', '2024-03-20 11:45:00+02', NULL, 'PROMOTE_USER_TO_DIRECTOR', 'e9999999-9999-4999-9999-999999999999', NULL, NULL, 'f3333333-3333-4333-3333-333333333333');
INSERT INTO public.request VALUES ('PENDING', '2024-03-22 16:20:00+02', NULL, 'PROMOTE_USER_TO_DIRECTOR', 'e0000000-0000-4000-0000-000000000000', NULL, NULL, 'f4444444-4444-4444-4444-444444444444');


--
-- PostgreSQL database dump complete
--

