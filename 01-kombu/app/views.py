import datetime
import uuid
from http import HTTPStatus
from django.http import HttpResponse
from kombu import Connection

def index(request):
    with Connection(transport='memory') as conn:
        queue = conn.SimpleQueue('name_queue')
        message = '{uuid} hello, sent at {today}'.format(**{
                            'uuid': uuid.uuid4(),
                            'today': datetime.datetime.today()})
        queue.put(message)
        queue.close()
    return HttpResponse(status=HTTPStatus.CREATED)

def consumer(request):
    with Connection(transport='memory') as conn:
        queue = conn.SimpleQueue('name_queue')
        try:
            message = queue.get(timeout=1)

            print(message.payload)

            message.ack() # elimina mensaje de la cola
        except:
            return HttpResponse(status=HTTPStatus.NO_CONTENT)

        queue.close()

    return HttpResponse(status=HTTPStatus.ACCEPTED)
