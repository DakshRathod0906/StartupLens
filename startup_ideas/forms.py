from django import forms
from .models import StartupIdea, Industry, Tag
from .constants import StartupIdeaStatus, StartupStage

class StartupIdeaForm(forms.ModelForm):
    class Meta:
        model = StartupIdea
        fields = [
            'title', 'short_description', 'problem_statement', 
            'proposed_solution', 'target_audience', 'industry', 
            'business_model', 'revenue_model', 'startup_stage', 
            'status', 'tags', 'version'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. AI Resume Builder'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'problem_statement': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'proposed_solution': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'target_audience': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'industry': forms.Select(attrs={'class': 'form-select'}),
            'business_model': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'revenue_model': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'startup_stage': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'version': forms.HiddenInput(),
        }

class SearchForm(forms.Form):
    keyword = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search ideas...'}))
    industry = forms.ModelChoiceField(queryset=Industry.objects.all(), required=False, empty_label="All Industries", widget=forms.Select(attrs={'class': 'form-select'}))
    status = forms.ChoiceField(choices=[('', 'All Statuses')] + StartupIdeaStatus.choices, required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    stage = forms.ChoiceField(choices=[('', 'All Stages')] + StartupStage.choices, required=False, widget=forms.Select(attrs={'class': 'form-select'}))
