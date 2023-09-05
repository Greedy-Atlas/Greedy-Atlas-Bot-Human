from flask import Flask, request, Response, stream_with_context
from server.streamer import Streamer

app = Flask(__name__)

streamer = Streamer()

@app.route('/stream')
def stream():   # URL 호출 시 진행
    src = request.args.get('src', default=0, type=int)

    try:
        return Response(
            stream_with_context(stream_gen(src)),
            mimetype='multipart/x-mixed-replace; boundary=frame'
        )
    except Exception as e:
        print('[SerBot] stream error : ', str(e))

def stream_gen(src):     # Streamer 클래스의 영상 바이너리 코드를 실시간 처리
    try:
        streamer.run(src)

        while True:
            frame = streamer.bytescode()
            yield (b'--frame\r\n'
                   b'Content-Type : image/jpeg\r\n\r\n' + frame + b'\r\n')
            
    except GeneratorExit :
        print('[SerBot] disconnected stream')
        streamer.stop()