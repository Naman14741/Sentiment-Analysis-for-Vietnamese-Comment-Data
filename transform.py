import re
from pyvi import ViTokenizer
from abbrevation import Dictionary


def Test():
    text = input()
    pre_processing = PreProcessing(text)
    processed_comment = pre_processing.process()
    print(processed_comment)


class PreProcessing:

    def __init__(self, comment: str = ''):
        self.comment = comment

    def remove_icon(self):
        self.comment = re.sub(r'[^\w\s,.!@#$%^&*()_+=\-\[\]{};:"\'|\\<>/?`~\u00C0-\u1EF9]', ' ', self.comment)
        return self

    def lowercase(self):
        self.comment = self.comment.lower()
        return self

    def abbreviation_processing(self):
        for word in self.comment.split():
            if word in Dictionary.keys():
                self.comment = self.comment.replace(word, Dictionary[word])
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

    def process(self):
        self.lowercase() \
            .abbreviation_processing() \
            .money_and_time_processing() \
            .remove_duplicate_characters() \
            .remove_punctuation() \
            .remove_duplicate_words() \
            .remove_duplicate_spaces() \
            .tokenize() \
            .remove_stopwords()

        return self.comment