from django.contrib import admin

from .models import Choice, Question, AboutSection


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    # When viewing list of existing questions
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']
    list_per_page = 20

    # When creating/editing questions
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]


class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_order', 'content')
    ordering = ('display_order',)

admin.site.register(Question, QuestionAdmin)
admin.site.register(AboutSection, AboutSectionAdmin)
