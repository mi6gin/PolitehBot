class HTTPHeaders:
    def __init__(self,
                 user_agent,
                 accept,
                 referer,
                 upgrade_insecure_requests,
                 accept_language
                 ):
        self.headers = {
            "User-Agent": user_agent,
            "Accept": accept,
            "Accept-Language": accept_language,
            "Referer": referer,
            "Upgrade-Insecure-Requests": upgrade_insecure_requests
        }

    def Language(self, lang):
        headers = self.headers.copy()  # Создаем копию текущих заголовков
        headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"
        headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
        headers["Referer"] = "http://univer.kstu.kz/student/bachelor/"
        headers["Upgrade-Insecure-Requests"] = "1"
        headers["Accept-Language"] = f'{lang}-{lang.upper()},{lang};q=0.5'
        return headers