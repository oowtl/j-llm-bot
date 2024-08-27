from crewai import Crew, Agent, Task
from langchain_ollama import ChatOllama
# from langchain_openai import ChatOpenAI

# 뭘로 실행할지 정해주는 것
llm = ChatOllama(
  # model 이름 넣어주기
  model = 'llama3.1',
  # api key 를 넣어주거나 base_url을 넣어주거나.
  base_url='http://127.0.0.1:11434'
)

# Crew : 조직원 => N명 (조직)
# Agent : 요원 => 1명 (조직원)
# Task : 미션

user_question = input('편하게 질문해주세요 : )')

# 쇼핑몰
book_agent = Agent(
  role='책 구매 어시스턴트',
  goal='고객이 어떤 상황인지 설명을 하면 해당 상황에 맞는 우리 서점에 있는 책을 소개합니다.',
  backstory='당신은 우리 서점의 모든 책 정보를 알고있으며, 사람들의 상황에 맞는 책을 소개하는데 전문가입니다.',
  # 상품 정보는 나중에 REST API 로 넘겨줘야한다.
  llm=llm
)

review_agent = Agent(
  role='책 리뷰 어시스턴트',
  goal='추천받은 책들의 도서에 대한 리뷰를 제공하고, 해당도서에 대한 심도있는 평가를 제공합니다.',
  backstory='당신은 우리 서점의 모든 책 정보를 알고 있으며, 추천받은 책에 대한 전문가 수준의 리뷰를 제공합니다.',
  llm=llm
)

# task 는 계속 늘릴 수 있다. (비용이 커질 뿐)
recommend_book_task = Task(
  # description='고객의 상황에 맞는 최고의 추천 도서 제안하기',
  description=user_question,  #input 으로 받을 수도 있다.
  expected_output='고객의 상황에 맞는 5개의 도서를 추천하고 해당 도서를 추천한 이유를 알려줘',
  agent=book_agent,
  output_file='recommend_book_task.md'
)

review_task = Task(
  description='고객이 선택한 책에 대한 리뷰를 제공합니다.',
  expected_output='고객이 선택한 책에 대한 리뷰를 제공합니다.',
  agent=review_agent,
  output_file='review_task.md'
)

# 요원과 미션을 관리한다.
crew = Crew(
  agents=[book_agent, review_agent],
  tasks=[recommend_book_task, review_task],
  verbose=True
)

result = crew.kickoff()

print(result)