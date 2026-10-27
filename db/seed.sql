-- Seed Data for Sports Management Application
INSERT OR IGNORE INTO tenants (id, name, subdomain, plan, status) VALUES
('t_default', 'Metro Youth Athletic League', 'metro-youth', 'enterprise', 'active');

INSERT OR IGNORE INTO users (id, tenant_id, email, name, role, status) VALUES
('u_admin', 't_default', 'admin@sportsmgmt.io', 'Sarah Jenkins (League Admin)', 'admin', 'active'),
('u_coach1', 't_default', 'coach.marcus@thunderbolts.com', 'Marcus Vance (Coach)', 'coach', 'active'),
('u_scorekeeper', 't_default', 'official.david@sportsmgmt.io', 'David Miller (Scorekeeper)', 'scorekeeper', 'active');

INSERT OR IGNORE INTO tournaments (id, tenant_id, name, sport, format, status, start_date, end_date) VALUES
('tourn_001', 't_default', 'U14 Boys Championship 2026', 'Basketball', 'single_elimination', 'active', '2026-11-01', '2026-11-15'),
('tourn_002', 't_default', 'Summer Classic Invitational', 'Basketball', 'round_robin', 'draft', '2026-12-01', '2026-12-10');

INSERT OR IGNORE INTO divisions (id, tournament_id, name, age_min, age_max) VALUES
('div_u14', 'tourn_001', 'U14 Boys Division', 12, 14),
('div_u16', 'tourn_001', 'U16 Boys Division', 14, 16);

INSERT OR IGNORE INTO teams (id, tenant_id, division_id, name, coach_id, coach_name, eligibility_status) VALUES
('team_001', 't_default', 'div_u14', 'Thunderbolts', 'u_coach1', 'Marcus Vance', 'eligible'),
('team_002', 't_default', 'div_u14', 'Wildcats', 'u_coach1', 'Elena Rostova', 'eligible'),
('team_003', 't_default', 'div_u14', 'Eagles', 'u_coach1', 'James Wilson', 'eligible'),
('team_004', 't_default', 'div_u14', 'Vipers', 'u_coach1', 'Carlos Mendez', 'eligible');

INSERT OR IGNORE INTO athletes (id, team_id, first_name, last_name, jersey_number, position, dob, guardian_name, guardian_email, coppa_consent, waiver_signed, eligible) VALUES
('ath_001', 'team_001', 'Jordan', 'Miller', 23, 'Point Guard', '2012-04-15', 'David Miller', 'david.m@example.com', 1, 1, 1),
('ath_002', 'team_001', 'Lucas', 'Vance', 10, 'Shooting Guard', '2012-08-20', 'Marcus Vance', 'coach.marcus@thunderbolts.com', 1, 1, 1),
('ath_003', 'team_002', 'Sam', 'Peterson', 7, 'Center', '2012-02-10', 'Kelly Peterson', 'kelly.p@example.com', 1, 1, 1),
('ath_004', 'team_002', 'Tyler', 'Hayes', 12, 'Small Forward', '2012-06-05', 'Robert Hayes', 'robert.h@example.com', 1, 1, 1);

INSERT OR IGNORE INTO matches (id, tournament_id, division_id, home_team_id, away_team_id, home_team_name, away_team_name, home_score, away_score, period, game_clock_seconds, court, status) VALUES
('match_001', 'tourn_001', 'div_u14', 'team_001', 'team_002', 'Thunderbolts', 'Wildcats', 42, 38, 'Q3', 420, 'Court 1', 'live'),
('match_002', 'tourn_001', 'div_u14', 'team_003', 'team_004', 'Eagles', 'Vipers', 0, 0, 'Q1', 720, 'Court 2', 'scheduled');

INSERT OR IGNORE INTO standings (id, tournament_id, team_id, team_name, played, won, lost, points, point_diff, streak, rank) VALUES
('std_001', 'tourn_001', 'team_001', 'Thunderbolts', 3, 3, 0, 6, 28, 'W3', 1),
('std_002', 'tourn_001', 'team_002', 'Wildcats', 3, 2, 1, 4, 12, 'W1', 2),
('std_003', 'tourn_001', 'team_003', 'Eagles', 3, 1, 2, 2, -10, 'L1', 3),
('std_004', 'tourn_001', 'team_004', 'Vipers', 3, 0, 3, 0, -30, 'L3', 4);

INSERT OR IGNORE INTO audit_logs (id, tenant_id, actor_email, action, entity_type, entity_id, details) VALUES
('log_001', 't_default', 'admin@sportsmgmt.io', 'TOURNAMENT_CREATED', 'tournament', 'tourn_001', 'Created U14 Boys Championship 2026'),
('log_002', 't_default', 'coach.marcus@thunderbolts.com', 'ROSTER_SUBMITTED', 'team', 'team_001', 'Submitted 12 player roster with signed waivers');
