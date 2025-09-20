class Question:
    def __init__(self, position, title, text, image, possibleAnswers, id=None):
        self.id = id
        self.position = position
        self.title = title
        self.text = text
        self.image = image
        self.possibleAnswers = possibleAnswers

    def to_json(self):
        return {
            "id": self.id,
            "position": self.position,
            "title": self.title,
            "text": self.text,
            "image": self.image,
            "possibleAnswers": self.possibleAnswers
        }

    @staticmethod
    def from_json(data):
        return Question(
            id=int(data.get('id')) if data.get('id') is not None else None,
            position=data['position'],
            title=data['title'],
            text=data['text'],
            image=data['image'],
            possibleAnswers=data['possibleAnswers']
        )


