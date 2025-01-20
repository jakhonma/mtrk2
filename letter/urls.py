from django.urls import path
from letter import views

urlpatterns = [
    path('letter-create/', views.LetterCreateAPIView.as_view()),

    # path(
    #     'user-letter-progress-approved/',
    #     views.LetterProgressCreateApprovedAPIView.as_view()
    # ),
    path(
        'user-letter-progress-rejected/',
        views.LetterProgressCreateRejectedAPIView.as_view()
    ),

    # Letter Progress User o'qishni uchun
    path(
        'user-letter-progress-is-read/<int:pk>/',
        views.LetterProgressUserIsReadAPIView.as_view()
    ),

    # Userga tegishli letter progressni countini qaytaradi
    path(
        'user-letter-progress-is-read-count/',
        views.LetterProgressUserIsReadCountAPIView.as_view()
    ),

    # User create progress
    path(
        'user-letter-progress-channel-employee-approved/',
        views.LetterProgressCreateChannelEmployeeAPIView.as_view()
    ),
    path(
        'user-letter-progress-channel-director-or-assistant-approved/',
        views.LetterProgressCreateChannelDirectorOrChannelAssistantAPIView.as_view()
    ),
    path(
        'user-letter-progress-archive-director-approved/',
        views.LetterProgressCreateArchiveDirectorAPIView.as_view()
    ),
    path(
        'user-letter-progress-archive-employee-approved/',
        views.LetterProgressCreateArchiveEmployeeAPIView.as_view()
    ),

    # User Letter Progresslarni olishda
    path(
        'user-letter-progress-all/',
        views.LetterProgressUserAllAPIView.as_view()
    ),
    path(
        'user-letter-progress-send/',
        views.LetterProgressUserSentAPIView.as_view()
    ),
    path(
        'user-letter-progress-recipient/',
        views.LetterProgressUserRecipientAPIView.as_view()
    ),
    path(
        'user-letter-progress-cancel/',
        views.LetterProgressUserCancelAPIView.as_view()
    )
]
