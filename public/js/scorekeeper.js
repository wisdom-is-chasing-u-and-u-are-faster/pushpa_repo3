// Courtside Scorekeeper Logic with WebSocket & Offline Sync
class ScorekeeperEngine {
    constructor(matchId = 'match_001') {
        this.matchId = matchId;
        this.homeScore = 42;
        this.awayScore = 38;
        this.homeFouls = 3;
        this.awayFouls = 4;
        this.clockSeconds = 420;
    }

    async addPoints(team, points, player = 'Player') {
        const idemKey = `evt_${this.matchId}_${Date.now()}_${Math.random().toString(36).substring(7)}`;
        const payload = {
            idempotency_key: idemKey,
            event_type: 'POINTS',
            team: team,
            player_id: player,
            points: points,
            game_clock_seconds: this.clockSeconds
        };

        if (navigator.onLine) {
            try {
                const res = await SportsAPI.recordMatchEvent(this.matchId, payload);
                this.updateScoreboard(res.home_score, res.away_score);
            } catch (err) {
                console.warn('Network failed, queueing offline in IndexedDB:', err);
                if (window.IndexedDBQueue) window.IndexedDBQueue.enqueueEvent(this.matchId, payload);
            }
        } else {
            if (window.IndexedDBQueue) window.IndexedDBQueue.enqueueEvent(this.matchId, payload);
        }
    }

    updateScoreboard(home, away) {
        this.homeScore = home;
        this.awayScore = away;
        const elHome = document.getElementById('home-score');
        const elAway = document.getElementById('away-score');
        if (elHome) elHome.innerText = home;
        if (elAway) elAway.innerText = away;
    }
}

window.ScorekeeperEngine = ScorekeeperEngine;
