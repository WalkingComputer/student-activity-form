from django import forms
from .models import Submission


class SubmissionForm(forms.ModelForm):
    """Form for student activity choice submission."""

    class Meta:
        model = Submission
        fields = ['full_name', 'student_id', 'section', 'choice', 'viva_topic']
        labels = {
            'full_name': 'Full Name',
            'student_id': 'Student ID',
            'section': 'Section',
            'choice': 'Select Activity',
            'viva_topic': 'Viva Topic',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
                'id': 'id_full_name',
            }),
            'student_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your student ID',
                'id': 'id_student_id',
            }),
            'section': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_section',
            }, choices=[('W1', 'W1'), ('W2', 'W2')]),
            'choice': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_choice',
            }),
            'viva_topic': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your viva topic',
                'id': 'id_viva_topic',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        choice = cleaned_data.get('choice')
        viva_topic = cleaned_data.get('viva_topic')

        if choice == 'tech_viva' and not viva_topic:
            self.add_error('viva_topic', 'Viva topic is required for Technology Viva.')

        return cleaned_data
