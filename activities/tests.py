from django.test import TestCase, Client
from django.urls import reverse
from .models import Submission
from .forms import SubmissionForm


class SubmissionModelTest(TestCase):
    def setUp(self):
        self.submission = Submission.objects.create(
            full_name='John Doe', student_id='STU001',
            section='A', choice='industrial_visit',
        )

    def test_submission_creation(self):
        self.assertEqual(self.submission.full_name, 'John Doe')

    def test_submission_str(self):
        self.assertEqual(str(self.submission), 'John Doe (STU001)')

    def test_viva_submission(self):
        viva = Submission.objects.create(
            full_name='Jane', student_id='STU002',
            section='B', choice='tech_viva', viva_topic='ML',
        )
        self.assertEqual(viva.viva_topic, 'ML')


class SubmissionFormTest(TestCase):
    def test_valid_industrial_visit(self):
        form = SubmissionForm(data={
            'full_name': 'John', 'student_id': 'S1',
            'section': 'A', 'choice': 'industrial_visit', 'viva_topic': '',
        })
        self.assertTrue(form.is_valid())

    def test_valid_tech_viva(self):
        form = SubmissionForm(data={
            'full_name': 'Jane', 'student_id': 'S2',
            'section': 'B', 'choice': 'tech_viva', 'viva_topic': 'Cloud',
        })
        self.assertTrue(form.is_valid())

    def test_invalid_tech_viva_without_topic(self):
        form = SubmissionForm(data={
            'full_name': 'Jane', 'student_id': 'S2',
            'section': 'B', 'choice': 'tech_viva', 'viva_topic': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('viva_topic', form.errors)

    def test_required_fields(self):
        form = SubmissionForm(data={
            'full_name': '', 'student_id': '', 'section': '', 'choice': '', 'viva_topic': '',
        })
        self.assertFalse(form.is_valid())


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        r = self.client.get(reverse('home'))
        self.assertEqual(r.status_code, 200)

    def test_submit_choice_get(self):
        r = self.client.get(reverse('submit_choice'))
        self.assertEqual(r.status_code, 200)

    def test_submit_choice_post_valid(self):
        r = self.client.post(reverse('submit_choice'), {
            'full_name': 'John', 'student_id': 'S1',
            'section': 'A', 'choice': 'industrial_visit', 'viva_topic': '',
        })
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Submission.objects.count(), 1)

    def test_submit_choice_post_invalid(self):
        r = self.client.post(reverse('submit_choice'), {
            'full_name': '', 'student_id': '', 'section': '',
            'choice': 'tech_viva', 'viva_topic': '',
        })
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Submission.objects.count(), 0)

    def test_success_view(self):
        r = self.client.get(reverse('success'))
        self.assertEqual(r.status_code, 200)