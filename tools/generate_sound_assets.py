from pathlib import Path
import math
import struct
import wave


ROOT = Path(__file__).resolve().parents[1]
SOUND_DIR = ROOT / "asset" / "Sound"
SAMPLE_RATE = 44100


def _envelope(index, total, attack=0.02, release=0.28):
    t = index / max(1, total - 1)
    if t < attack:
        return t / attack
    if t > 1 - release:
        return max(0, (1 - t) / release)
    return 1


def _write_wave(name, samples):
    SOUND_DIR.mkdir(parents=True, exist_ok=True)
    path = SOUND_DIR / name
    with wave.open(str(path), "w") as file:
        file.setnchannels(2)
        file.setsampwidth(2)
        file.setframerate(SAMPLE_RATE)
        for sample in samples:
            value = max(-1.0, min(1.0, sample))
            packed = struct.pack("<h", int(value * 32767))
            file.writeframesraw(packed + packed)


def _tone(duration, start_freq, end_freq=None, volume=0.42, wave_shape="sine"):
    end_freq = start_freq if end_freq is None else end_freq
    total = int(SAMPLE_RATE * duration)
    phase = 0
    samples = []
    for index in range(total):
        t = index / max(1, total - 1)
        freq = start_freq + (end_freq - start_freq) * t
        phase += (math.tau * freq) / SAMPLE_RATE
        if wave_shape == "square":
            raw = 1.0 if math.sin(phase) >= 0 else -1.0
        elif wave_shape == "triangle":
            raw = 2 / math.pi * math.asin(math.sin(phase))
        else:
            raw = math.sin(phase)
        samples.append(raw * volume * _envelope(index, total))
    return samples


def _noise(duration, volume=0.22, pitch=0.0):
    total = int(SAMPLE_RATE * duration)
    seed = 0xACE1
    samples = []
    for index in range(total):
        seed ^= (seed << 7) & 0xFFFF
        seed ^= seed >> 9
        seed ^= (seed << 8) & 0xFFFF
        noise = ((seed & 0xFFFF) / 32768) - 1
        ring = math.sin(index * pitch) if pitch else 1
        samples.append(noise * ring * volume * _envelope(index, total, 0.01, 0.55))
    return samples


def _mix(*tracks):
    length = max(len(track) for track in tracks)
    mixed = [0.0] * length
    for track in tracks:
        for index, value in enumerate(track):
            mixed[index] += value
    return [sample / max(1, len(tracks) * 0.75) for sample in mixed]


def _join(*parts):
    samples = []
    for part in parts:
        samples.extend(part)
    return samples


def main():
    _write_wave("jump.wav", _tone(0.18, 360, 880, 0.38, "triangle"))
    _write_wave("land.wav", _mix(_tone(0.09, 140, 82, 0.28, "triangle"), _noise(0.11, 0.16)))
    _write_wave(
        "crash.wav",
        _mix(_tone(0.34, 180, 44, 0.42, "square"), _noise(0.36, 0.34, 0.2)),
    )
    _write_wave(
        "start.wav",
        _join(
            _tone(0.07, 392, 523, 0.28, "triangle"),
            _tone(0.07, 523, 659, 0.30, "triangle"),
            _tone(0.12, 659, 988, 0.34, "triangle"),
        ),
    )
    _write_wave(
        "restart.wav",
        _join(
            _tone(0.06, 440, 660, 0.25, "triangle"),
            _tone(0.06, 660, 880, 0.28, "triangle"),
        ),
    )
    _write_wave("toggle.wav", _tone(0.08, 760, 520, 0.22, "sine"))
    _write_wave(
        "milestone.wav",
        _join(
            _tone(0.07, 523, 784, 0.28, "triangle"),
            _tone(0.07, 659, 988, 0.30, "triangle"),
            _tone(0.16, 988, 1319, 0.36, "triangle"),
        ),
    )


if __name__ == "__main__":
    main()
