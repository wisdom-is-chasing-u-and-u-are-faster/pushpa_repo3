// Sports Management Application API Client
const API_BASE = '/api/v1';

async function fetchJson(url, options = {}) {
    try {
        const res = await fetch(url, {
            headers: { 'Content-Type': 'application/json', ...options.headers },
            ...options
        });
        if (!res.ok) {
            throw new Error(`HTTP Error ${res.status}: ${res.statusText}`);
        }
        return await res.json();
    } catch (err) {
        console.error(`API Fetch Error [${url}]:`, err);
        throw err;
    }
}

const SportsAPI = {
    getHealth: () => fetchJson('/health'),
    getDashboardStats: () => fetchJson(`${API_BASE}/dashboard/stats`),
    getTournaments: () => fetchJson(`${API_BASE}/tournaments`),
    createTournament: (data) => fetchJson(`${API_BASE}/tournaments`, { method: 'POST', body: JSON.stringify(data) }),
    getStandings: (tournId) => fetchJson(`${API_BASE}/tournaments/${tournId}/standings`),
    generateBracket: (tournId, format = 'single_elimination') => fetchJson(`${API_BASE}/tournaments/${tournId}/generate-bracket`, { method: 'POST', body: JSON.stringify({ format }) }),
    getTeams: () => fetchJson(`${API_BASE}/teams`),
    createTeam: (data) => fetchJson(`${API_BASE}/teams`, { method: 'POST', body: JSON.stringify(data) }),
    getTeamRoster: (teamId) => fetchJson(`${API_BASE}/teams/${teamId}/roster`),
    addAthleteToRoster: (teamId, data) => fetchJson(`${API_BASE}/teams/${teamId}/roster`, { method: 'POST', body: JSON.stringify(data) }),
    getMatch: (matchId) => fetchJson(`${API_BASE}/matches/${matchId}`),
    recordMatchEvent: (matchId, eventData) => fetchJson(`${API_BASE}/matches/${matchId}/events`, { method: 'POST', body: JSON.stringify(eventData) }),
    registerAthlete: (data) => fetchJson(`${API_BASE}/athletes/register`, { method: 'POST', body: JSON.stringify(data) }),
    getTenants: () => fetchJson(`${API_BASE}/admin/tenants`),
    getUsers: () => fetchJson(`${API_BASE}/admin/users`),
    getAuditLogs: () => fetchJson(`${API_BASE}/admin/audit-logs`)
};

window.SportsAPI = SportsAPI;
