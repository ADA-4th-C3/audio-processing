import os
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

INPUT_DIR = 'raw'
OUTPUT_DIR = 'output'


def process_audio(file_path, out_path, is_note=False):
    audio = AudioSegment.from_file(file_path)
    # 무음 제거
    silence_thresh = audio.dBFS - 30  # 기준보다 30dB 낮은 구간을 무음으로 간주
    min_silence_len = 200  # 200ms 이상의 무음 구간
    nonsilent_ranges = detect_nonsilent(
        audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    if nonsilent_ranges:
        start_trim = nonsilent_ranges[0][0]
        end_trim = nonsilent_ranges[-1][1]
        audio = audio[start_trim:end_trim]

    # 소리 증폭
    peak_target = -0.1
    change_in_dBFS = peak_target - audio.max_dBFS
    audio = audio.apply_gain(change_in_dBFS)

    # note 폴더 내부는 2초 이내로 자르고 fade out 적용
    if is_note:
        max_duration_ms = 2000
        fade_out_ms = 500

        if len(audio) > max_duration_ms:
            audio = audio[:max_duration_ms]
        if len(audio) > fade_out_ms:
            audio = audio.fade_out(fade_out_ms)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    audio.export(out_path, format='wav')


for subfolder in ['note', 'extra']:
    in_dir = os.path.join(INPUT_DIR, subfolder)
    out_dir = os.path.join(OUTPUT_DIR, INPUT_DIR, subfolder)

    for filename in os.listdir(in_dir):
        if filename.lower().endswith(('.wav', '.mp3', '.flac', '.ogg')):
            in_path = os.path.join(in_dir, filename)
            out_path = os.path.join(out_dir, filename)
            process_audio(in_path, out_path, is_note=(subfolder == 'note'))
