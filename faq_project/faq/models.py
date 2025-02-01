from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator

class FAQ(models.Model):
    question_en = models.TextField()
    question_hi = models.TextField(blank=True)
    question_bn = models.TextField(blank=True)
    answer = RichTextField()

    def get_translated_question(self, lang):
        lang = lang if lang in ['hi', 'bn'] else 'en'
        return getattr(self, f'question_{lang}', self.question_en)

    def save(self, *args, **kwargs):
        translator = Translator()
        try:
            if not self.question_hi:
                self.question_hi = translator.translate(self.question_en, dest='hi').text
            if not self.question_bn:
                self.question_bn = translator.translate(self.question_en, dest='bn').text
        except Exception as e:
            pass 
        super().save(*args, **kwargs)