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
                    "1.焦慮症：包括廣泛性焦慮症、社交焦慮症、恐慌症等，這些都是因為過度擔心未來的事件或恐懼特定社交情境而導致的。"
                    "2.抑鬱症：長期的悲傷、無力感或喪失興趣和樂趣，可能影響日常生活和功能。"
                    "3.創傷後壓力症候群（PTSD）：在經歷或目睹極端創傷事件後發展的疾病，表現為持續的恐懼、焦慮和創傷相關的回想。"
                    "4.躁鬱症（雙相情感障礙）：一種涉及情緒極端波動的疾病，包括躁狂期（極端興奮或煩躁）和抑鬱期"
                    "5.思覺失調症（精神分裂症）：這是一種複雜的精神健康疾病，主要表現為思維失序、感知異常（如幻聽和妄想），以及情感鈍化。患者可能經歷現實感的嚴重扭曲，導致日常生活和社交功能受到重大影響。"
                    "6.妄想症：一種精神疾病，以持續的、往往是不合理的妄想（錯誤信念）為主要特徵，通常缺乏其他精神病性症狀。"
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

