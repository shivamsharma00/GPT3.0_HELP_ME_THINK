import os
from re import L
import openai
from time import sleep
import json
from tqdm import tqdm

os.environ["API_KEY"] = "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"
# marmik api key - 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

openai.api_key = os.getenv("API_KEY")
# JSON variables
domain = ["Cognitive science", "Race and Ethnicity"]
task = ["public service announcements", "plays", "haikus", "stories", "tweets", "taglines", "jokes", "songs", "reports"]


# Change domain_index and task_index according to the task
#! NOTE : Remember to change name of generated files
domain_index = 0
task_index = 0

prompt_type = ["pre_question_prompt", "task_specific_prompt"]
instances="Instances"
qa_pair="QApair"
task_specific_prompt_extra_q = ["Write at least 70 words.", "Explain the importance.", "Make it informative."]

task_specific_p_1 = "Write a "
task_specific_p_2 = "using the question and answers above."
# Write a blog on cognitive science using the questions and answers above. Explain importance of cognitive science.

gpt3_res = ""
question = "\nQuestion"
context1 = "I am an expert in writing"
context2 = "I will ask some questions to collect information and then I will use the information to write a "

generated_q = ""
generated_ans = ""

generated_qa_dict_1 = {}
generated_qa_dict_2 = {}
generated_qa_dict_3 = {}
tempe_dict = {}


def ogpt3(prompt1):
    return openai.Completion.create(
        model="text-davinci-002",
        prompt= prompt1,
        temperature=0.7,
        max_tokens=256,
        echo=False,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )


def qa_spliter(result, flag):
    
    count = 0
    
    for i in result:
        count+=1
        if i == '?':
            break
    
    gen_q = result[1:count+2].replace("\n", "")
    gen_a = result[count+2:].replace("\n", " ")

    if flag==0:
        generated_qa_dict_1[gen_q]=gen_a
    elif flag==1:
        generated_qa_dict_2[gen_q]=gen_a
    else:
        generated_qa_dict_3[gen_q]=gen_a


# Intitialize task
pre_question_p = context1 + " " + task[task_index] + " on " + domain[domain_index] + ". " + context2 + task[task_index][:-1] + "."
task_specific_p = task_specific_p_1 + task[task_index][:-1] + " on " + domain[domain_index] + " " + task_specific_p_2 + " " + task_specific_prompt_extra_q[2] 

# for 1 task - 3 instances
for i in tqdm(range(3)):

    context = ""
    context = pre_question_p + question
    
    for j in tqdm(range(12)):

        gpt3_res = ogpt3(context)['choices'][0]['text']
        sleep(2)
        qa_spliter(gpt3_res, i)

        context = context + gpt3_res + question
    txt_file_name = domain[domain_index]+task[task_index] + str(i+1) + ".txt"
 
    with open(txt_file_name, 'w') as f:
        f.write(context)
    
glob_dict = {}
glob_dict['Domain']=domain[domain_index]
glob_dict['Task']=task[task_index]
glob_dict['Prompt']={prompt_type[0]:pre_question_p, prompt_type[1]:task_specific_p}
glob_dict['Instances']=[
    {qa_pair:[
        {"Question":item[0], "Answer":item[1]} for item in generated_qa_dict_1.items()
    ], "Output":"Your output here!"},
    {qa_pair:[
        {"Question":item[0], "Answer":item[1]} for item in generated_qa_dict_2.items()
    ], "Output":"Your output here!"},
    {qa_pair:[
        {"Question":item[0], "Answer":item[1]} for item in generated_qa_dict_3.items()
    ], "Output":"Your output here!"}
    ]
glob_dict['Preset_link']="preset link here"
glob_dict['screenshot_link'] = "https://drive.google.com/drive/folders/1jL3SrSflUMqeQ0Uqn0FuUJI5IvDdmM0J?usp=sharing"

js = json.dumps(glob_dict, indent=4, ensure_ascii=False)

#! Change file names according to task
with open("cg_task6_psa.json", "w") as g:
    g.write(js)

with open("cg_task6_psa.txt", "w") as r:
    r.write(js)


print("*"*100)
print("COMPLETED")
print("*"*100)

    


