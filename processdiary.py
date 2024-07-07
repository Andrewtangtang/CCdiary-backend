import os
import get_password
os.environ["OPENAI_API_KEY"] = get_password.getpass()
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import re


class DiaryFeedback:
    """
    A class to process diary feedback and diagnose mental health issues
    INPUT: diary description, language
    OUTPUT: feedback and diagnosis
    """
    def __init__(self):
        """
        initialize the model
        """
        self.model_35 = ChatOpenAI(model="gpt-3.5-turbo")
        self.model_40 = ChatOpenAI(model="gpt-4")
        self.promptForFeedback = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful friend and you would read a diary provided. "
                    "Providing advice or positive encouragement based on the feelings and diary description provided."
                ),
                # This placeholder will be replaced by the structured human message constructed below
                MessagesPlaceholder(variable_name="messages"),

                (
                    "system",
                    "Answer all questions to the best of your ability in {language}.")
            ]
        )
        self.feedbackChain = self.promptForFeedback | self.model_35
        self.promptForDiagnose = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "閱讀以下6種心靈疾病的描述，並回答以下問題。"
                    "1.焦慮症：焦慮症包括了廣泛性焦慮症、社交焦慮症、恐慌症和特定恐懼症等。這些症狀可能包括過度擔憂、緊張、恐慌發作等。"
                    "2.抑鬱症：抑鬱症是一種常見的情緒障礙，特徵是持續的悲傷、失去興趣或快樂感、疲勞、睡眠問題、食慾改變、自我價值低下等。"
                    "3.創傷後壓力症候群（PTSD）：PTSD通常發生在經歷了極端的創傷事件後，如戰爭、自然災害、暴力攻擊或嚴重事故等。主要症狀包括持續的回憶、惡夢、避免與創傷相關的情境、情緒麻木和過度警覺。"
                    "4.躁鬱症（雙相情感障礙）：這種疾病導致情緒狀態極端波動，從極度興奮或躁狂到深度抑鬱。躁狂期可能表現為過度自信、睡眠需求減少和衝動行為；而抑鬱期則可能出現悲傷、無力感和自殺想法。"
                    "5.思覺失調症（精神分裂症）：這是一種嚴重的精神疾病，特徵是對現實的錯誤感知、異常的思想和感知、幻聽、妄想、思維混亂以及社交和情感隔離。"
                    "6.妄想症：妄想症是一種精神疾病，其主要特徵是持久的妄想，即不根據現實的堅定信念。這些妄想可能涉及被迫害、嫉妒、身體健康或其他誤認為真實的情節，而沒有其他明顯的精神病性症狀。"
                    "並閱讀以下的日記"
                ),
                # This placeholder will be replaced by the structured human message constructed below
                MessagesPlaceholder(variable_name="messages"),

                (
                     "system"
                     "先判斷日記的內容是正面的還是負面的"
                     "如果如果日記的內容是正向的，則回答'你的心靈狀態健康'"
                     "如果日記的內容偏向負面則判斷他可能有哪些上述6種潛在的心理疾病風險，僅輸出心理疾病的字串就好不要多做回覆"
                     "例如：'抑鬱症'或'焦慮症'"
                     "將答案用{language}回覆"
                     ),
            ]
        )

        self.diagnoseChain = self.promptForDiagnose | self.model_40

    def invoke_diagnose_model(self, diary_description, language):
        # Prepare the structured message
        human_message = HumanMessage(content=diary_description)
        # Invoke the model chain with the structured message and specified language
        response = self.diagnoseChain.invoke(
            {
                "messages": [human_message],
                "language": language
            }
        )
        return response

    def invoke_feedback_model(self, diary_description, language):
        # Prepare the structured message
        human_message = HumanMessage(
            content=f" Diary description: {diary_description}")

        # Invoke the model chain with the structured message and specified language
        response = self.feedbackChain.invoke(
            {
                "messages": [human_message],
                "language": language
            }
        )
        return response

    def process(self, diary_description, language):
        response1 = self.invoke_feedback_model(diary_description, language)
        response2 = self.invoke_diagnose_model(diary_description, language)
        response1 = response1.content
        response2 = response2.content
        response1 = re.sub(r'\n+', '\n', response1)
        if language == "Traditional Chinese":
            if "健康" in response2 or "正" in response2:
                return response1+'\n'+"心靈狀態健康"
            else:
                return response1+'\n'+'潛在的風險:'+response2
        else:
            if "healthy" in response2 or "positive" in response2:
                return response1+'\n'+"your mental state is healthy."
            else:
                return response1+'\n'+'potential disease:'+response2

