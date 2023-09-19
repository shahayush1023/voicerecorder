import wave
import pyaudio
import matplotlib.pyplot as plt
import numpy as np

Frames_per_buffer = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

pa = pyaudio.PyAudio()

stream = pa.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=Frames_per_buffer
)

print("start recording")

seconds = 8
frames = []
second_tracking = 0
second_count = 0

for i in range(0, int(RATE/Frames_per_buffer*seconds)):
    data = stream.read(Frames_per_buffer)
    frames.append(data)
    second_tracking += 1
    if second_tracking == RATE/Frames_per_buffer:
        second_count += 1
        second_tracking = 0
        print(f'time left:{seconds - second_count}')


stream.stop_stream()
stream.close()
pa.terminate()

obj = wave.open('aps.wav', 'wb')
obj.setnchannels(CHANNELS)
obj.setsampwidth(pa.get_sample_size(FORMAT))
obj.setframerate(RATE)
obj.writeframes(b''.join(frames))
obj.close()

file = wave.open('aps.wav', 'rb')
sample_freq = file.getframerate()
frames = file.getnframes()
signal_wave = file.readframes(-1)
file.close()

time = frames/sample_freq
audio_Array = np.frombuffer(signal_wave, dtype=np.int16)
times = np.linspace(0, time, num=frames)
plt.figure(figsize=(15, 5))
plt.plot(times, audio_Array)
plt.ylabel('Signal Wave')
plt.xlabel('Time(s)')
plt.xlim(0, time)
plt.title('The thing I just recorded')
plt.show()
