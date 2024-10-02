from langchain_core.prompts import PromptTemplate
import json

def get_intent(question, llm):
    intent_prompt_template = """
    你是Dr Wu的專業保養顧問，請根據以下用戶的問題，分析其意圖，並以簡潔的方式總結其查詢需求。

    用戶問題：
    {question}

    請以以下格式輸出：
    {{
        "intent": "用戶的意圖描述"
    }}
    """

    intent_prompt = PromptTemplate(
        input_variables=["question"],
        template=intent_prompt_template,
    )

    intent_chain = intent_prompt | llm
    response = intent_chain.invoke({"question": question})
    intent_json = json.loads(response.content)
    return intent_json["intent"]
