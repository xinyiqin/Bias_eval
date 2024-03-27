from google.cloud import translate_v2 as translate

# 创建一个 Translate 客户端
client = translate.Client()

# 要翻译的文本
text = 'Hello, world!'

# 翻译文本
result = client.translate(text, target_language='zh-CN')['translatedText']

# 打印翻译结果
print(result)

# export GOOGLE_APPLICATION_CREDENTIALS="/home/qinxinyi/translate/translation-api-credentials.json"
# export GOOGLE_APPLICATION_CREDENTIALS="/home/qinxinyi/translate/translation-api-credentials.json"
