import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_new_token(self, db_value):
        response = requests.get(f"{self.base_url}/api/new_token", params={'db': db_value})
        data = response.json()
        return data['token']

    def send_prompt(self, token, prompt_text):
        payload = {'token': token, 'prompt': prompt_text}
        response = requests.post(f"{self.base_url}/api/prompt", json=payload)
        data = response.json()
        return data['result']

    def get_overview(self):
        response = requests.get(f"{self.base_url}/api/overview")
        data = response.json()
        return data

    def get_statistics(self):
        response = requests.get(f"{self.base_url}/api/statistics")
        data = response.json()
        return data

    def get_recommendation(self):
        response = requests.get(f"{self.base_url}/api/recommendation")
        data = response.json()
        return data


class CmdInterface:
    def __init__(self):
        self.connector = None
        self.token = None

    def connect(self, base_url: str, db: int):
        self.connector = APIClient(base_url)
        self.token = self.connector.get_new_token(db)

    def overview(self):
        overview_info = self.connector.get_overview()
        print(overview_info['message'])

    def statistics(self):
        stats_info = self.connector.get_statistics()
        print(f"총 상품수: {stats_info['total_items']}")

    def recommendation(self):
        recommendation_info = self.connector.get_recommendation()
        for item in recommendation_info['items']:
            print(f"추천 제품: {item['name']} - 설명: {item['description']}")

    def prompt(self, prompt_text: str):
        if not self.connector or not self.token:
            raise ValueError("Connector 또는 Token이 설정되어 있지 않습니다.")
        return self.connector.send_prompt(self.token, prompt_text)


def main():
    base_url = 'http://localhost:5000'
    db_value = 1
    cli = CmdInterface()
    cli.connect(base_url, db_value)

    cli.overview()
    cli.statistics()

    while True:
        prompt = input("prompt (또는 '추천'을 입력하여 제품 추천을 받으세요) >> ")

        if prompt.lower() in ['', 'q', 'ㅂ']:
            if prompt.lower() in ['q', 'ㅂ']:
                break
            continue
        
        if prompt.lower() == '추천':
            cli.recommendation()
        else:
            answer = cli.prompt(prompt)
            print(f"Answer: {answer}")


if __name__ == '__main__':
    main()