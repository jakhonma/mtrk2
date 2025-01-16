from letter.serializers.letter import LetterListSerializer, LetterCreateUpdateSerializer
from letter.serializers.letter_progress import (
    LetterProgressSerializer, 
    LetterProgressCreateApprovedSerializer, 
    LetterProgressCreateRejectedSerializer,
    LetterProgressCreateChannelEmployeeSerializer,
    LetterProgressCreateChannelDirectorOrChannelAssistantSerializer,
    LetterProgressCreateArchiveDirectorSerializer,
    LetterProgressCreateArchiveEmployeeSerializer
)
