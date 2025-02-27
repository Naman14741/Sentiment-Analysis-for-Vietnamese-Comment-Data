import re
from pyvi import ViTokenizer
from abbreviation import Dictionary

def Test():
    text = input()
    pre_processing = PreProcessing(text)
    processed_comment = pre_processing.norm()
    print(processed_comment)


class PreProcessing:

    def __init__(self, comment: str = ''):
        self.comment = comment

    def remove_icon(self):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"
                                   u"\U0001F300-\U0001F5FF"
                                   u"\U0001F680-\U0001F6FF"
                                   u"\U0001F1E0-\U0001F1FF"
                                   u"\u2702-\u27B0"
                                   u"\u24C2-\U0001F251"
                                   u"\U0001f926-\U0001f937"
                                   u'\U00010000-\U0010ffff'
                                   u"\u200d"
                                   u"\u2640-\u2642"
                                   u"\u2600-\u2B55"
                                   u"\u23cf"
                                   u"\u23e9"
                                   u"\u231a"
                                   u"\u3030"
                                   u"\ufe0f"
                                   "]+", flags=re.UNICODE)

        self.comment = emoji_pattern.sub(' ', self.comment)
        return self

    def lowercase(self):
        self.comment = self.comment.lower()
        return self

    # Lỗi
    def abbreviation_processing(self):
        words = self.comment.split(" ")
        for word in words:
            if word in Dictionary.keys():
                self.comment = re.sub(rf'\b{re.escape(word)}\b', Dictionary[word], self.comment)
        return self

    def money_and_time_processing(self):
        self.comment = re.sub(r'(\d+)tr\b', r'\1 triệu', self.comment)
        self.comment = re.sub(r'(\d+)tr/th\b', r'\1 triệu mỗi tháng', self.comment)
        self.comment = re.sub(r'(\d+)k\b', r'\1 nghìn', self.comment)
        self.comment = re.sub(r'(\d+)h\b', r'\1 giờ', self.comment)
        self.comment = re.sub(r'(\d+)t\b', r'\1 tuổi', self.comment)

        self.comment = re.sub(r'(\d+)tr(\d)\b', r'\1 triệu \2 trăm nghìn', self.comment)
        return self

    def remove_stopwords(self):
        try:
            with open("data/vietnamese-stopwords.txt", encoding="utf-8") as f:
                stopwords = set(f.read().splitlines())  # Đưa vào set để tối ưu hóa
            self.comment = ' '.join([word for word in self.comment.split() if word not in stopwords])
        except FileNotFoundError:
            print("Error: File 'vietnamese-stopwords.txt' not found.")
        return self

    def remove_duplicate_characters(self):
        self.comment = re.sub(r'([a-zA-Zàáâãèéêìíòóôõùúăđĩũơưạảấầẩẫậắằẳẵặẹẻẽềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ])\1+', lambda m: m.group(1), self.comment)
        return self

    def remove_punctuation(self):
        self.comment = re.sub(r'[^\w\s\u00C0-\u1EF9]', ' ', self.comment)
        return self

    def remove_duplicate_words(self):
        self.comment = re.sub(r'\b(\w+)\s+\1\b', r'\1', self.comment)
        return self

    def remove_duplicate_spaces(self):
        self.comment = re.sub(r'\s+', ' ', self.comment).strip()
        return self

    def tokenize(self):
        self.comment = ViTokenizer.tokenize(self.comment)
        return self

    def norm(self):
        self.remove_icon() \
            .lowercase() \
            .abbreviation_processing() \
            .money_and_time_processing() \
            .remove_duplicate_characters() \
            .remove_duplicate_words() \
            .tokenize() \
            .remove_punctuation() \
            .remove_duplicate_spaces()

        return self.comment

    def process(self, sources):
        temp_df = sources.copy()
        temp_df['content'] = temp_df['content'].apply(
            lambda content: self.norm() if isinstance(content, str) else content
        )
        temp_df = temp_df.dropna(subset=['content'])
        return temp_df


