# faq/serializers.py
from django.utils.html import strip_tags
from rest_framework import serializers
from .models import FAQ
from googletrans import Translator

class FAQSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()

    class Meta:
        model = FAQ
        fields = ['question', 'answer']

    def get_question(self, obj):
        """
        Returns the translated question based on the `lang` query parameter.
        """
        request = self.context.get('request')
        lang = request.query_params.get('lang', 'en') if request else 'en'
        return obj.get_translated_question(lang)

    def get_answer(self, obj):
        """
        Returns the cleaned and translated answer based on the `lang` query parameter.
        """
        plain_text_answer = strip_tags(obj.answer)
        clean_answer = self.clean_text(plain_text_answer)
        request = self.context.get('request')
        lang = request.query_params.get('lang', 'en') if request else 'en'
        return self.translate_text(clean_answer, lang)

    def clean_text(self, text):
        """
        Cleans the text by removing unwanted characters and extra spaces.
        """
        text = text.replace('\r\n', ' ').replace('&nbsp;', ' ')
        text = ' '.join(text.split())
        return text.strip()

    def translate_text(self, text, lang):
        """
        Translates the text to the specified language using Google Translate API.
        If translation fails, returns the original text as a fallback.
        """
        if not text:  
            return text

        translator = Translator()
        try:
            translated = translator.translate(text, dest=lang)
            return translated.text
        except Exception as e:
            print(f"Translation failed for text: {text}, lang: {lang}. Error: {e}")
            # Fallback to the original text if translation fails
            return text