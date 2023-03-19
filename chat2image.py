import gradio as gr
import openai
from diffusers import StableDiffusionPipeline
import torch
import uuid

openai.api_key = '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'

model_id = 'dreamlike-art/dreamlike-photoreal-2.0'
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
#pipe = pipe.to('cuda')


def answer(state, state_chatbot, text):
    if '그림' in text:
        prompt = state[-1]['content']

        img = pipe(prompt).images[0]

        img_path = f'imgs/{uuid.uuid4()}.jpg'
        img.save(img_path)

        state_chatbot = state_chatbot + [(text, f'![](/file={img_path})')]
    else:
        messages = state + [{
            'role': 'user',
            'content': text
        }]

        res = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages
        )

        msg = res['choices'][0]['message']['content']

        new_state = [{
            'role': 'user',
            'content': text
        }, {
            'role': 'assistant',
            'content': msg
        }]

        state = state + new_state
        state_chatbot = state_chatbot + [(text, msg)]

    print(state)

    return state, state_chatbot, state_chatbot


with gr.Blocks(css='#chatbot .overflow-y-auto{height:500px}') as demo:
    state = gr.State([{
        'role': 'system',
        'content': '친절한 대한민국 경북 경찰'
    }])
    state_chatbot = gr.State([])

    with gr.Row():
        gr.HTML("""<div style="text-align: center; max-width: 500px; margin: 0 auto;">
            <div>
                <h1>경북 경찰 챗봇</h1>
            </div>
            <p style="margin-bottom: 10px; font-size: 94%">
                경북청 정보화장비과
            </p>
        </div>""")

    with gr.Row():
        chatbot = gr.Chatbot(elem_id='chatbot')

    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder='무엇이든 물어보세요').style(container=False)

    txt.submit(answer, [state, state_chatbot, txt], [state, state_chatbot, chatbot])
    txt.submit(lambda: '' , None, txt)


demo.launch(debug=True, share=True)
