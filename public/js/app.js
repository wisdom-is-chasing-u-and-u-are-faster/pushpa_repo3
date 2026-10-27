// Global app initialization
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Sports Management Application initialized.');
    try {
        const health = await SportsAPI.getHealth();
        console.log('Backend Status:', health.status);
    } catch (e) {
        console.warn('Backend not responding yet:', e.message);
    }
});
