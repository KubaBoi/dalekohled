import io
from threading import Condition

class StreamingOutput(object):
    
    @staticmethod
    def init():
        StreamingOutput.frame = None
        StreamingOutput.buffer = io.BytesIO()
        StreamingOutput.condition = Condition()

    @staticmethod
    def write(buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            StreamingOutput.buffer.truncate()
            with StreamingOutput.condition:
                StreamingOutput.frame = StreamingOutput.buffer.getvalue()
                StreamingOutput.condition.notify_all()
            StreamingOutput.buffer.seek(0)
        return StreamingOutput.buffer.write(buf)