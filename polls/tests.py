import datetime

from django.contrib.auth.models import AnonymousUser, User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone

from selenium.webdriver.firefox.webdriver import WebDriver

from .models import Question, Choice
from .views import create_question

# Every function/method with a comment that starts with a '*' was copied from the official Django tutorial.
# The others I created by myself.

def create_test_question(question_text, days):
    """
    *Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

def create_test_question_owned(question_text, author):
    """
    Create a question created now by the given author with the given question text.
    """
    return Question.objects.create(question_text=question_text, pub_date=timezone.now(), author=author)

def create_test_choice(question, choice_text, votes):
    """
    Create a choice with the given 'choice_text' and 'votes' that is part of
    the choice_set of the given Question 'question'.
    """
    return Choice.objects.create(question=question, choice_text=choice_text, votes=votes)


class QuestionModelTests(TestCase):

    def test_total_votes_two_choices(self):
        """
        total_votes() returns 12 for a question with choices of 7 and 5 votes.
        """
        question = create_test_question("question", 0)
        create_test_choice(question, "choice1", 7)
        create_test_choice(question, "choice2", 5)
        self.assertEqual(question.total_votes(), 12)

    def test_total_votes_four_choices(self):
        """
        total_votes() returns 18 for a question with choices of 0, 5, 6, 7 votes.
        """
        question = create_test_question("question", 0)
        create_test_choice(question, "choice1", 0)
        create_test_choice(question, "choice2", 5)
        create_test_choice(question, "choice3", 6)
        create_test_choice(question, "choice4", 7)
        self.assertEqual(question.total_votes(), 18)

    def test_was_published_recently_with_future_question(self):
        """
        *was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        *was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        *was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """
        *If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        *Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_test_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        *Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_test_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        *Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_test_question(question_text="Past question.", days=-30)
        create_test_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        *The questions index page may display multiple questions.
        """
        create_test_question(question_text="Past question 1.", days=-30)
        create_test_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

    def test_total_votes_displayed(self):
        """
        The total votes of a question are properly displayed on the index page.
        """
        question = create_test_question("question", 0)
        create_test_choice(question, "choice1", 17)
        create_test_choice(question, "choice2", 22)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, '39')


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        *The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_test_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        *The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_test_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionResultsViewTests(TestCase):
    def test_future_question(self):
        """
        *The results view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_test_question(question_text='Future question.', days=5)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        *The results view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_test_question(question_text='Past Question.', days=-5)
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionCreateViewTests(TestCase):
    # === Sample post data ===
    # <QueryDict: {'csrfmiddlewaretoken': ['TRM5CNKVnb4pZrAwkhklBTW04bR9u0TGnegpWlS4euta8CNMOomDb06hhNoqoYXE'],
    # 'question_text': ['Question'], 'form-TOTAL_FORMS': ['2'], 'form-INITIAL_FORMS': ['0'],
    # 'form-MIN_NUM_FORMS': ['0'], 'form-MAX_NUM_FORMS': ['1000'],
    # 'form-0-choice_text': ['Choice 1'], 'form-1-choice_text': ['']}>
    def setUp(self):
        self.url = reverse('polls:create')
        # the default post data for an empty form and formset page with 2 choices
        self.default_post_data = {'question_text': [''], 'form-TOTAL_FORMS': ['2'], 'form-INITIAL_FORMS': ['0'],
                                  'form-MIN_NUM_FORMS': ['0'], 'form-MAX_NUM_FORMS': ['1000'],
                                  'form-0-choice_text': [''], 'form-1-choice_text': ['']}
        # create a user and login as them
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_login(self.user)
        # every test needs access to the request factory
        self.factory = RequestFactory()

    def test_200_get(self):
        """
        Make sure we are getting an OK status code when making a GET request.
        """
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_200_post_empty_form(self):
        """
        Make sure we are getting an OK status code when making a POST request with an empty form.
        """
        response = self.client.post(self.url, self.default_post_data)
        self.assertEquals(response.status_code, 200)

    def test_no_redirect_empty_form(self):
        """
        Should not be redirected when the form is completely empty.
        """
        response = self.client.post(self.url, self.default_post_data, follow=True)
        self.assertQuerysetEqual(response.redirect_chain, [])

    def test_no_redirect_no_question_text_with_choices(self):
        """
        Should not be redirected when the question_text field is not filled in. Even if the 2 choices are filled in.
        """
        post_data = self.default_post_data
        post_data['form-0-choice_text'] = 'Choice 1'
        post_data['form-1-choice_text'] = 'Choice 2'
        response = self.client.post(self.url, post_data, follow=True)
        self.assertQuerysetEqual(response.redirect_chain, [])

    def test_no_redirect_one_choice(self):
        """
        Should not be redirected when only one choice is filled in (as we want at least 2 choices)
        """
        post_data = self.default_post_data
        post_data['question_text'] = 'Question'
        post_data['form-0-choice_text'] = 'Choice 1'
        response = self.client.post(self.url, post_data, follow=True)
        self.assertQuerysetEqual(response.redirect_chain, [])

    def test_redirect_question_text_2_choices(self):
        """
        Should be redirected to index if the question text and 2 choices are filled in.
        """
        post_data = self.default_post_data
        post_data.update({'question_text': ['Question'], 'form-0-choice_text': ['Choice 1'],
                          'form-1-choice_text': ['Choice 2']})
        response = self.client.post(self.url, post_data)
        self.assertRedirects(response, '/polls/')

    def test_cannot_access_when_not_authorized(self):
        """
        Redirect (shown by 302 status_code) when not logged in.
        """
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)

    def test_sent_to_login_when_not_authorized(self):
        """
        Should be redirected to login screen with create set to next if not logged in.
        """
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, '/polls/login/?next=/polls/create/')

    # ====================
    # RequestFactory tests
    # (From my understanding, these are for testing JUST the views whereas the test Client acts like a browser and
    # for that reason, these could be a bit faster at the cost of not fully testing the entire process.)
    # ====================
    def test_request_get_logged_in(self):
        """
        RequestFactory test for create_question view when we are logged in.
        Should get a 200 status code when logged in.
        """
        request = self.factory.get(self.url)
        request.user = self.user
        # test create_question as if it were deployed at /polls/create
        response = create_question(request)
        self.assertEqual(response.status_code, 200)

    def test_request_get_not_logged_in(self):
        """
        RequestFactory test for create_question view when we are NOT logged in.
        Should get a 302 status code when not logged in as we are redirected to the login page.
        """
        request = self.factory.get(self.url)
        request.user = AnonymousUser()
        response = create_question(request)
        self.assertEqual(response.status_code, 302)


class QuestionDeleteViewTests(TestCase):
    """
    Testing the delete view itself. i.e. AFTER the user presses the "yes" button when asked to delete the Question or
    when going to the url directly.
    [Note: I tested myself using isinstance(x, int) that the id of a question is an integer.]
    """
    def setUp(self):
        # create a user and login as them
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_login(self.user)
        # create a second user to create other questions
        self.user2 = User.objects.create_user(username='otheruser', password='otherpass')

    def test_404_if_question_not_exist(self):
        """
        Trying to delete a question that does not exist should result in a 404 error.
        """
        url = reverse('polls:delete', kwargs={'question_id': 100})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_302_if_question_owned(self):
        """
        A status code of 302 should be returned if the question is owned by the user. This is because on success, the
        user is redirected to 'my_polls' view.
        """
        question = create_test_question_owned('question', self.user)
        url = reverse('polls:delete', kwargs={'question_id': question.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_question_deleted_if_question_owned(self):
        """
        Ensure the question is actually deleted if the user that owned the question went to its delete view.
        """
        question = create_test_question_owned('question', self.user)
        question_id = question.id
        url = reverse('polls:delete', kwargs={'question_id': question_id})
        self.client.get(url)
        self.assertRaises(Question.DoesNotExist, Question.objects.get, id=question_id)

    def test_403_and_question_not_deleted_if_question_not_owned(self):
        """
        Should be status code of 403:Forbidden if the user is not the author of the question.
        Also make sure teh question is not deleted.
        """
        question = create_test_question_owned('question', self.user2)
        url = reverse('polls:delete', kwargs={'question_id': question.id})
        response = self.client.get(url)
        Question.objects.get(id=question.id)  # this would give a Question.DoesNotExist exception if it did not exist
        self.assertEquals(response.status_code, 403)

    def test_403_and_question_not_deleted_anonymous_user(self):
        """
        Make sure Anonymous Users can't randomly delete things. (I dunno maybe something goes horribly wrong)
        """
        question = create_test_question_owned('question', self.user)
        self.client.logout()
        url = reverse('polls:delete', kwargs={'question_id': question.id})
        response = self.client.get(url)
        Question.objects.get(id=question.id)  # this would give a Question.DoesNotExist exception if it did not exist
        self.assertEquals(response.status_code, 403)


class SeleniumTests(StaticLiveServerTestCase):
    """ Selenium tests for Firefox """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        # cls.selenium.quit()
        super().tearDownClass()

    def test_open(self):
        url = self.live_server_url + "/polls/"
        self.selenium.get(url)

