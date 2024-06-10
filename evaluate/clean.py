import json
import os
model='chinese-alpaca-2-7b'
output_path=f'/home/qinxinyi/BiasBench/expr/{model}/bbq_zh.json'
clean_output_path=f'/home/qinxinyi/BiasBench/expr/{model}/bbq_zh_clean.json'
with open(output_path,'r',encoding='utf-8') as f,\
    open(clean_output_path,'a+',encoding='utf-8') as output_f:
    for line in f:
        line=line.replace('服务器。','服务员。')
        line=line.replace('售货员','销售员')
        line=line.replace('化学家','药剂师')
        line=line.replace('一线厨师','厨师')
        line=line.replace('有钱人一。','富人。')
        line=line.replace('富裕的一个。','富人。')
        line=line.replace('福利论。','领取福利的人。')
        line=line.replace('关于公共援助。','接受公共援助的人。')
        line=line.replace('标记。','马克。')
        line=line.replace("摩门教一。","摩门教徒。")
        
        line=line.replace("印度教一。","印度教徒。")
        line=line.replace("佛教一号。","佛教徒。")
        line=line.replace("新教一。","新教徒。")
        line=line.replace("犹太人的那个。","犹太人。")
        
        line=line.replace("锡克教一。","锡克教徒。")
        line=line.replace("天主教的一个。","天主教徒。")
        
        line=line.replace("无神论者之一。","无神论者。")
        
        
        
        line=json.loads(line)

        json.dump(line, output_f, ensure_ascii=False)
        output_f.write("\n")

os.remove(output_path)
os.rename(clean_output_path,output_path)