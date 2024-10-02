import sqlite3
import json
from langchain_core.prompts import PromptTemplate

def generate_response(intent, relevant_docs, image_descriptions, llm):
    product_info = ''
    for doc in relevant_docs:
        image_urls = doc.metadata.get('image_urls', [])
        image_info = ''
        for img_url in image_urls:
            img_desc = next((img['description'] for img in image_descriptions if img['url'] == img_url), '')
            image_info += f"Image URL: {img_url}\nImage Description: {img_desc}\n"
        product_info += f"Product ID: {doc.metadata.get('product_id')}\nTitle: {doc.metadata.get('title')}\nURL: {doc.metadata['url']}\nDescription: {doc.page_content}\n{image_info}\n"

    prompt_template = """
    你是Dr Wu的專業保養顧問，根據以下用戶的意圖和相關的產品資訊，給出適當的產品推薦和建議。

    用戶意圖：
    {intent}

    相關產品資訊：
    {product_info}

    請以以下格式輸出：
    {{
        "product": {{
            "title": "產品標題",
            "product_id": "產品ID",
            "url": "產品的URL",
            "description": "產品的描述"
        }},
        "description": "選擇這個商品的原因",
        "advice": "針對用戶問題的處理建議"
    }}
    """
    prompt = PromptTemplate(
        input_variables=["intent", "product_info"],
        template=prompt_template
    )
    chain = prompt | llm

    # invoke the chain
    response = chain.invoke({"intent": intent, "product_info": product_info})

    try:
        import re
        def extract_json(text):
            if '```json' in text and '```' in text:
                json_str = re.sub(r'^```json\s*', '', text, flags=re.MULTILINE)
                json_str = re.sub(r'\s*```$', '', json_str, flags=re.MULTILINE)
                return json_str
            else:
                return text
        response_content = extract_json(response.content)
        response_data = json.loads(response_content)
    except json.JSONDecodeError:
        return {"error": "Failed to parse response data."}

    product = response_data.get('product', {})
    product_id = product.get('product_id')
    title = product.get('title')
    url = product.get('url')
    description = product.get('description')

    # check if the product ID exists in the database
    conn = sqlite3.connect('db/products.db')
    cursor = conn.cursor()
    cursor.execute("SELECT product_id, title, url FROM products WHERE product_id = ?", (product_id,))
    result = cursor.fetchone()

    if result:
        db_product_id, db_title, db_url = result
        corrections_made = False
        if title != db_title or url != db_url:
            corrections_made = True
        if corrections_made:
            new_prompt_template = """
            你是Dr Wu的專業保養顧問，根據以下用戶的意圖和產品資訊，給出選擇這個商品的原因和針對用戶問題的處理建議。

            用戶意圖：
            {intent}

            產品資訊：
            {{
                "title": "{title}",
                "product_id": "{product_id}",
                "url": "{url}",
                "description": "{description}"
            }}

            請以以下格式輸出：
            {{
                "product": {{
                    "title": "{title}",
                    "product_id": "{product_id}",
                    "url": "{url}",
                    "description": "{description}"
                }},
                "description": "選擇這個商品的原因",
                "advice": "針對用戶問題的處理建議"
            }}
            """
            new_prompt = PromptTemplate(
                input_variables=["intent", "title", "product_id", "url", "description"],
                template=new_prompt_template
            )
            chain = new_prompt | llm

            # 使用正确的产品信息重新调用链条
            response = chain.invoke({
                "intent": intent,
                "title": db_title,
                "product_id": db_product_id,
                "url": db_url,
                "description": description
            })

    else:
        # To-do: Handle the case where the product ID is not found in the database
        return {"Error": f"Pproduct_id : {product_id} not found in the database."}

    conn.close()

    return response.content
