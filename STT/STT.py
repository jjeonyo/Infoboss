# Copyrighted by ZOAS(STT ver1.0)
"""패키지는 ,,  세개 하면 됩니다.
sudo apt-get update && sudo apt-get install google
google-cloud-sdk-app-engine-python
pip install google-cloud
pip install google-cloud-storage
https://weejw.tistory.com/49
JSON 파일은 환경변수에 지정해두면 매번 불러올 필요 없으니 코드에 안 적어뒀음."""

from google.cloud import storage
from google.cloud import speech_v1p1beta1 as speech
import os
import sys

""" 업로드하는 부분 """


def upload_blob(source_file_name):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/jangwoo/zoas/myzoas.json"
    storage_client = storage.Client()
    destination_blob_name = source_file_name + ".flac"
    bucket_name = "zoastts-1"
    source_file_name = "media/" + source_file_name + ".flac"
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

    print(
        "File {} 가 {} 이름으로 업로드 되었습니다.".format(source_file_name, destination_blob_name )
    )
    print("Upload complete!")

def google_transcribe(filename):
    gcs_uri = 'gs://zoastts-1/' + filename + ".flac"
    transcript = ""
    buffer =""

    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=gcs_uri)
    speech_context = speech.SpeechContext(phrases=['인공지능','소프트웨어공학','컴퓨터공학']) # https://cloud.google.com/speech-to-text/docs/context-strength , https://cloud.google.com/speech-to-text/docs/speech-adaptation text adaptation 할 곳.

    config = speech.RecognitionConfig(
    sample_rate_hertz = 16000,  # 헤르츠 부분
    language_code = "ko-KR",  # 인식언어 부분
    encoding = speech.RecognitionConfig.AudioEncoding.FLAC,  # 오디오 포맷 바꿀때 여기만 건들기 ex. LINEAR16,FLAC,등등...
    enable_automatic_punctuation = True,  # 자동구두점 부분
    enable_word_time_offsets = True,  # 타임스탬프 삽입부분
    speech_contexts = [speech_context],  # 스피치 컨텍스트 부분
    profanity_filter = False, #욕설 필터링 부분
    )
    operation = client.long_running_recognize(config=config, audio=audio)

    response = operation.result()  # 타임아웃 옵션 없음
    f = open("timestamp/" + filename + ".txt", 'w', encoding='UTF-8')
    for result in response.results:
        alternative = result.alternatives[0]
        transcript += alternative.transcript + "\n" # transcript 저장 부분
        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            buffer = buffer + word + "," + str(start_time.total_seconds()) + "\n"
    f.write(buffer)
    f.close()
    transcript_filename = "stt/"+filename+".txt"
    f = open(transcript_filename, 'w', encoding='UTF-8')
    f.write(transcript)
    f.close()