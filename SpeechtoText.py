import os
import pyaudio 
import wave
import threading 
import whisper


def RecordAudio(): 
    chunk =2048
    FORMAT = pyaudio.paInt16
    channels = 1

    sample_rate = 44100
    record_seconds = 5

    p = pyaudio.PyAudio()

    for i in range(p.get_device_count()):
        print(p.get_device_info_by_index(i))

    selection = int(input("Select the device index: "))

    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    output=True,
                    input_device_index=selection,
                    frames_per_buffer=chunk)
    frames = []

    print("Recording... Enter to stop")
    global recording
    recording = True 

    def record(): 
        while recording:
    # for i in range (int(sample_rate*record_seconds/chunk)):
            data = stream.read(chunk, exception_on_overflow=False)
            frames.append(data)

    record_Thread = threading.Thread(target=record)
    record_Thread.start()
    recording = True

    input ("Press Enter to stop recording")
    recording = False
    record_Thread.join()


    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open("filename.wav", "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(sample_rate)
    wf.writeframes(b"".join(frames))
    wf.close()


def SpeechtoText():

    model = whisper.load_model("tiny.en")
    result = model.transcribe("filename.wav")
    print(result["text"])


RecordAudio()
print("Hello")