// ============================================================
// Dice Chess — Sound Effects (Web Audio API)
// ============================================================

let audioCtx: AudioContext | null = null;

function getAudioContext(): AudioContext {
    if (!audioCtx) {
        audioCtx = new AudioContext();
    }
    return audioCtx;
}

function playTone(
    frequency: number,
    duration: number,
    type: OscillatorType = 'sine',
    volume: number = 0.15,
    delay: number = 0,
) {
    const ctx = getAudioContext();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = type;
    osc.frequency.setValueAtTime(frequency, ctx.currentTime + delay);
    gain.gain.setValueAtTime(volume, ctx.currentTime + delay);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + delay + duration);

    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start(ctx.currentTime + delay);
    osc.stop(ctx.currentTime + delay + duration);
}

function playNoise(duration: number, volume: number = 0.08) {
    const ctx = getAudioContext();
    const bufferSize = ctx.sampleRate * duration;
    const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
    const data = buffer.getChannelData(0);

    for (let i = 0; i < bufferSize; i++) {
        data[i] = Math.random() * 2 - 1;
    }

    const source = ctx.createBufferSource();
    source.buffer = buffer;

    const gain = ctx.createGain();
    gain.gain.setValueAtTime(volume, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration);

    const filter = ctx.createBiquadFilter();
    filter.type = 'highpass';
    filter.frequency.value = 2000;

    source.connect(filter);
    filter.connect(gain);
    gain.connect(ctx.destination);
    source.start();
}

// ── Public Sound Effects ────────────────────────────────────

/** Soft click for piece placement */
export function playMoveSound() {
    playTone(600, 0.08, 'sine', 0.12);
    playNoise(0.04, 0.05);
}

/** Heavier thud for capturing a piece */
export function playCaptureSound() {
    playTone(250, 0.12, 'triangle', 0.2);
    playTone(180, 0.15, 'sine', 0.15, 0.03);
    playNoise(0.08, 0.1);
}

/** Tense alert for check */
export function playCheckSound() {
    playTone(880, 0.1, 'square', 0.1);
    playTone(660, 0.15, 'square', 0.08, 0.1);
}

/** Fanfare for checkmate */
export function playCheckmateSound() {
    playTone(523, 0.2, 'triangle', 0.15);
    playTone(659, 0.2, 'triangle', 0.15, 0.15);
    playTone(784, 0.2, 'triangle', 0.15, 0.3);
    playTone(1047, 0.4, 'triangle', 0.2, 0.45);
}

/** Rattling dice roll */
export function playDiceRollSound() {
    for (let i = 0; i < 6; i++) {
        const freq = 300 + Math.random() * 400;
        playTone(freq, 0.04, 'square', 0.06, i * 0.07);
        playNoise(0.03, 0.04);
    }
    // Final landing click
    playTone(500, 0.08, 'sine', 0.12, 0.5);
}

/** Subtle click when selecting a piece */
export function playSelectSound() {
    playTone(800, 0.05, 'sine', 0.08);
}

/** Draw/stalemate sound */
export function playDrawSound() {
    playTone(440, 0.3, 'triangle', 0.1);
    playTone(350, 0.4, 'triangle', 0.08, 0.2);
}
