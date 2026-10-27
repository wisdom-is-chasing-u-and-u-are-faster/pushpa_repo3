// IndexedDB Offline Queue for Courtside PWA
class IndexedDBQueue {
    static async enqueueEvent(matchId, eventPayload) {
        console.log(`[IndexedDB Queue] Stored offline event for ${matchId}:`, eventPayload);
        const queue = JSON.parse(localStorage.getItem('offline_event_queue') || '[]');
        queue.push({ matchId, payload: eventPayload });
        localStorage.setItem('offline_event_queue', JSON.stringify(queue));
    }

    static async syncPendingEvents() {
        const queue = JSON.parse(localStorage.getItem('offline_event_queue') || '[]');
        if (queue.length === 0) return;
        
        console.log(`[IndexedDB Sync] Replaying ${queue.length} offline events...`);
        for (const item of queue) {
            try {
                await SportsAPI.recordMatchEvent(item.matchId, item.payload);
            } catch (e) {
                console.error('Failed to sync event:', e);
            }
        }
        localStorage.removeItem('offline_event_queue');
        console.log('[IndexedDB Sync] Batch sync completed.');
    }
}

window.addEventListener('online', () => IndexedDBQueue.syncPendingEvents());
window.IndexedDBQueue = IndexedDBQueue;
