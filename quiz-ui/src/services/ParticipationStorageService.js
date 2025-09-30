const NAME_KEY = 'playerName';
const SCORE_KEY = 'participationScore';
const BEST_KEY = 'participationBestScore';
const COUNT_KEY = 'participationCount';
const DURATION_KEY = 'lastQuizDurationSeconds';
export default {
  savePlayerName(n) {
    localStorage.setItem(NAME_KEY, n);
  },
  getPlayerName() {
    return localStorage.getItem(NAME_KEY);
  },
  saveParticipationScore(s) {
    localStorage.setItem(SCORE_KEY, String(s));
    const best = this.getBestScore();
    if (best === null || s > best) localStorage.setItem(BEST_KEY, String(s));
  },
  getParticipationScore() {
    const v = localStorage.getItem(SCORE_KEY);
    return v ? Number(v) : 0;
  },
  getBestScore() {
    const v = localStorage.getItem(BEST_KEY);
    return v ? Number(v) : null;
  },
  incrementParticipationCount() {
    const c = this.getParticipationCount() + 1;
    localStorage.setItem(COUNT_KEY, String(c));
    return c;
  },
  getParticipationCount() {
    const v = localStorage.getItem(COUNT_KEY);
    return v ? Number(v) : 0;
  },
  saveLastDuration(seconds) {
    localStorage.setItem(DURATION_KEY, String(seconds));
  },
  getLastDuration() {
    const v = localStorage.getItem(DURATION_KEY);
    return v ? Number(v) : null;
  },
  clear() {
    localStorage.removeItem(NAME_KEY);
    localStorage.removeItem(SCORE_KEY);
    localStorage.removeItem(BEST_KEY);
    localStorage.removeItem(COUNT_KEY);
    localStorage.removeItem(DURATION_KEY);
  },
};
