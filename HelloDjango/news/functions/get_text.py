from bs4 import BeautifulSoup


def get_text(body):
    """Получаем текст из HTML"""
    soup = BeautifulSoup(body, 'html.parser')
    text = soup.get_text().strip()
    return text
