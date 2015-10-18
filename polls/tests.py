import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Questions
from django.core.urlresolvers import reverse


# Create your tests here.

class QuestionMethodTests(TestCase):
    def test_method_was_published_recently_with_future_question(self):
        # return false if pub_date in the future
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Questions(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_method_was_published_recently_with_old_question(self):
        # return false if pub_date in the future
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Questions(pub_date=time)
        self.assertEqual(old_question.was_published_recently(), False)

    def test_method_was_published_recently_with_recent_question(self):
        # this method expects true result with interval time 1 hour before recent time
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Questions(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Questions.objects.create(question_text=question_text, pub_date=time)


class QuestionViewTests(TestCase):
    def test_index_view_with_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_past_question(self):
        create_question('Past question', 30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Questions: Past question>'])

    def test_index_view_with_future_question(self):
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.", status_code=200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_future_question_and_past_question(self):
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Questions: Past question.>'])

    def test_index_view_with_two_past_questions(self):
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Questions: Past question 2.>', '<Questions: Past question 1.>']
        )