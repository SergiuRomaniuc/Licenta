from pvrecorder import PvRecorder
import wave
import struct


def record():
    recorder = PvRecorder(device_index=1, frame_length=512)
    audio = []
    path = 'input.wav'
    try:
        recorder.start()

        while True:
            frame = recorder.read()
            audio.extend(frame)
    except KeyboardInterrupt:
        recorder.stop()
        with wave.open(path, 'w') as f:
            f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
            f.writeframes(struct.pack("h" * len(audio), *audio))
    finally:
        recorder.delete()

# def main():
#     record

# if __name__=="__main__":
#     main()
