import line.out_event 

send_text = line.out_event.TextMessage()

class TextMessage(object):
    def __init__(self):
        pass

    def core(self, event):
        text_inp = event.message.text.lower()
        #send_text.push(event.source.user_id, text_inp)
        print(event)
        send_text.push(event.room_id, text_inp)
        send_text.push('R5a8df70a7425c3c8b60204f8176dcbcc', text_inp)
        send_text.reply(event.reply_token, 'ควยปั้น')
        #print('in_event')