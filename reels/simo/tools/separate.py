"""How src/assets/audio/speech.m4a was made: the music of the original montage is removed from its soundtrack
with the UVR-MDX-NET-Voc_FT model (sherpa-onnx), leaving the speakers' voices.
Usage: python3 tools/separate.py MODEL.onnx   (needs sherpa-onnx, soundfile, numpy, ffmpeg)
Model: https://github.com/k2-fsa/sherpa-onnx/releases/download/source-separation-models/UVR-MDX-NET-Voc_FT.onnx
"""
import os, subprocess, sys, tempfile
import numpy as np, soundfile as sf, sherpa_onnx as so

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sep = so.OfflineSourceSeparation(so.OfflineSourceSeparationConfig(model=so.OfflineSourceSeparationModelConfig(
    uvr=so.OfflineSourceSeparationUvrModelConfig(model=sys.argv[1]), num_threads=8)))
with tempfile.TemporaryDirectory() as d:
    wav = os.path.join(d, 'a.wav')
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', os.path.join(ROOT, 'src', 'assets', 'source.mp4'), '-vn', '-ac', '2', '-ar', '44100', wav], check=True)
    x, sr = sf.read(wav, dtype='float32', always_2d=True); x = x.T.copy()
    parts = [np.asarray(sep.process(sr, np.ascontiguousarray(x[:, i:i + sr * 30])).stems[0].data) for i in range(0, x.shape[1], sr * 30)]
    sf.write(os.path.join(d, 'v.wav'), np.concatenate(parts, axis=1).T, sr)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', os.path.join(d, 'v.wav'), '-ac', '1', '-c:a', 'aac', '-b:a', '192k',
                    os.path.join(ROOT, 'src', 'assets', 'audio', 'speech.m4a')], check=True)
print('wrote src/assets/audio/speech.m4a')
