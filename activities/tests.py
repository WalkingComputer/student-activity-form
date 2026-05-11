from django.test import TestCase, Client
from django.urls import reverse
from .models import Submission, DynamicForm, FormField, DynamicSubmission, FieldResponse
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


class DynamicFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.dform = DynamicForm.objects.create(name='Test Survey', slug='test-survey')
        self.field1 = FormField.objects.create(
            form=self.dform, label='Your Name', field_type='short_text',
            is_required=True, order=1,
        )
        self.field2 = FormField.objects.create(
            form=self.dform, label='Favorite Color', field_type='dropdown',
            is_required=False, order=2, options='Red, Blue, Green',
        )

    def test_dynamic_form_str(self):
        self.assertEqual(str(self.dform), 'Test Survey')

    def test_formfield_options_list(self):
        self.assertEqual(self.field2.get_options_list(), ['Red', 'Blue', 'Green'])

    def test_dynamic_form_get(self):
        r = self.client.get(reverse('dynamic_form', kwargs={'slug': 'test-survey'}))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Test Survey')
        self.assertContains(r, 'Your Name')

    def test_dynamic_form_post_valid(self):
        r = self.client.post(reverse('dynamic_form', kwargs={'slug': 'test-survey'}), {
            f'field_{self.field1.pk}': 'Alice',
            f'field_{self.field2.pk}': 'Blue',
        })
        self.assertEqual(r.status_code, 302)
        self.assertEqual(DynamicSubmission.objects.count(), 1)
        self.assertEqual(FieldResponse.objects.count(), 2)

    def test_dynamic_form_post_missing_required(self):
        r = self.client.post(reverse('dynamic_form', kwargs={'slug': 'test-survey'}), {
            f'field_{self.field1.pk}': '',
            f'field_{self.field2.pk}': 'Blue',
        })
        self.assertEqual(r.status_code, 200)
        self.assertEqual(DynamicSubmission.objects.count(), 0)

    def test_dynamic_form_success(self):
        r = self.client.get(reverse('dynamic_form_success', kwargs={'slug': 'test-survey'}))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Test Survey')

    def test_inactive_form_404(self):
        self.dform.is_active = False
        self.dform.save()
        r = self.client.get(reverse('dynamic_form', kwargs={'slug': 'test-survey'}))
        self.assertEqual(r.status_code, 404)
