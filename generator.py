import os
import requests
import sensenova
import time
import openai
import json

class Generator():
    def build_client(self,model):
        if model=='gpt-3.5':
            openai.api_type = "azure"
            openai.api_base = os.getenv("OPENAI_BASE")
            openai.api_version = os.getenv("OPENAI_API_VERSION")
            openai.api_key = os.getenv("OPENAI_API_KEY")
            client= openai
        elif model=='minimax':
            api_key= os.environ.get("MINIMAX_API_KEY")
            group_id = os.environ.get("MINIMAX_GROUP_ID")
            self.url = f"https://api.minimax.chat/v1/text/chatcompletion_pro?GroupId={group_id}"
            self.headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            client=''
        elif model=='glm-4':
            from zhipuai import ZhipuAI
            client = ZhipuAI(api_key=os.environ.get("ZHIPU_API_KEY"))
        elif model=='ernie':
            import erniebot
            erniebot.api_type = os.environ.get("ERNIE_API_TYPE")
            erniebot.ak = os.environ.get("ERNIE_AK")
            erniebot.sk = os.environ.get("ERNIE_SK")
            client = erniebot
        elif model=='sensechat':
            sensenova.access_key_id = os.environ.get("SENSECHAT_KEY_ID")
            sensenova.secret_access_key = os.environ.get("SENSECHAT_SECRET_KEY")
            client = sensenova
        elif model=='qwen-turbo':
            import dashscope
            client=dashscope
        return client

    def chat_completion(self,client,model,user_prompt,system_info='',n=1,max_tokens=1024, temperature=0.9, top_p=0.95, timeout=60):
        message=[]
        if 'gpt-3.5' in model:
            if system_info:
                message.append({"role": "system","content": system_info})
            message.append({"role": "user","content": user_prompt})
            response = client.ChatCompletion.create(
                    messages=message,
                    engine="gpt-35-turbo-1106",
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    timeout=timeout,
                    n=n,
                )
            if n==1:
                result = response.choices[0].message.content
            else:
                result= [choice.message.content for choice in response["choices"]]
        
        elif "qwen-turbo" in model:
            if system_info:
                message.append({"role": "system","content": system_info})
            message.append({"role": "user","content": user_prompt})
            response = client.Generation.call(
                    "qwen-turbo",
                    messages=message,
                    result_format='message',
                )
            result=response["output"]["choices"][0]["message"]["content"]

        elif "minimax" in model:
            if not system_info:
                system_info='你是一款由MiniMax自研的，没有调用其他产品的接口的大型语言模型。MiniMax是一家中国科技公司，一直致力于进行大模型相关的研究。'
            message.append({
                        "sender_type": "USER", #必须是USER、BOT、或FUNCTION
                        "sender_name":"user",
                        "text": user_prompt,
                    })
            request_body = {
                "model": "abab5.5-chat",
                "temperature":temperature,
                "tokens_to_generate": max_tokens,
                "reply_constraints": {"sender_type": "BOT", "sender_name": "BOT"},
                "messages": message,
                "bot_setting": [
                    {
                        "bot_name": "BOT",
                        "content": system_info,
                    }
                ],
            }
            response = requests.post(self.url, headers=self.headers, json=request_body,timeout=timeout)
            response = response.json()
            result = response["choices"][0]["messages"][0]["text"]

        elif 'glm-4' in model:
            if system_info:
                message.append({"role": "system","content": system_info})
            message.append({"role": "user","content": user_prompt})
            response = client.chat.completions.create(
                        model=model,
                        messages = message,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        timeout=timeout,
                    )
            result = response.choices[0].message.content

        elif "ernie" in model:
            if system_info:
                message.append({"role": "system","content": system_info})
            message.append({"role": "user","content": user_prompt})
            response = client.ChatCompletion.create(
                        model="ernie-3.5",
                        messages=message,
                    )
            result = response.get_result()

        elif 'sensechat' in model:
            if system_info:
                message.append({"role": "system","content": system_info})
            message.append({"role": "user","content": user_prompt})
            response = client.ChatCompletion.create(
                    model="SenseChat",
                    messages=message,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p)
                    
            result = response.data.choices[0].message
        return result
        

if __name__ == "__main__":
    model='internlm2' #minimax/glm-4/sensechat/ernie/gpt-3.5/qwen-turbo
    generator=Generator()
    client = generator.build_client(model)
    user_prompt='今天是几号'
    response=generator.chat_completion(client,model,user_prompt)
    print(response)
    # while True:
    #     try:
    #         response=generator.chat_completion(client,model,user_prompt,n=5)
    #         print(response)
    #         break
    #     except sensenova.error.RateLimitError or openai.error.RateLimitError:
    #         print('got rate limit, sleep...')
    #         time.sleep(30)
    #     except Exception as e:
    #         print(str(e))