import gradio as gr
import openai

openai.api_key = open('key.txt','r').read().strip('\n')
#make the chatbot as health expert advisor:
message_history =[{"role": "user", "content": f"You are a health expert bot. I will specify the health matter in my messages, and you will reply with a therapy that includes the subjects I mention in my messages. Reply only with therapies to further input. If you understand, say OK."},
                   {"role": "assistant", "content": f"OK"}]
def predict(input):
    # tokenize the new input sentence
    global message_history
    message_history.append({"role":"user","content":input})
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = message_history)
    reply_content = completion.choices[0].message.content
    print(reply_content)
    message_history.append({"role":"assistant","content":reply_content})
    response = [(message_history[i]["content"], message_history[i+1]["content"]) for i in range(2, len(message_history)-1, 2)]  # convert to tuples of list
    return response

# creates a new Blocks app and assigns it to the variable demo    
with gr.Blocks() as demo:
    # creates a new Chatbot instance and assigns it to the variable chatbot.
    chatbot = gr.Chatbot()
    # creates a new Row component
    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Type your health concern here").style(container=False)
        txt.submit(predict,txt,chatbot)
        txt.submit(None,None,txt, _js="() => {''}")

demo.launch()