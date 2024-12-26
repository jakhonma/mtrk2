from rest_framework import viewsets, views, generics, response, permissions, status
from letter.models import Letter, Notification
from letter.serializers import LetterCreateUpdateSerializer
from letter.task import add_letter
from django.db import transaction


class LetterCreateAPIView(generics.CreateAPIView):
    """
        Create a model instance.
    """
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = LetterCreateUpdateSerializer
    queryset = Letter.objects.all()

    def create(self, request, *args, **kwargs):
        data = [
            {
                "i": 1,
                "id": 12,
                "title": "Ещё один футбол" "Матонат"
            },
            {
                "i": 2,
                "id": 13,
                "title": "14-Январь Ватан ҳимоячилари куни"
            },
            {
                "i": 3,
                "id": 14,
                "title": "Чегарамизни ҳимоя қилиш шарафли бурчдир!"
            },
            {
                "i": 4,
                "id": 561,
                "title": "Сарҳадлари тинч юртда эрикн ва ҳур фарзандлар туғилади!"
            },
            {
                "i": 5,
                "id": 13,
                "title": "14-Январь Ватан ҳимоячилари куни"
            },
            {
                "i": 6,
                "id": 14,
                "title": "Чегарамизни ҳимоя қилиш шарафли бурчдир!"
            },
            {
                "i": 7,
                "id": 561,
                "title": "Сарҳадлари тинч юртда эрикн ва ҳур фарзандлар туғилади!"
            },
            {
                "i": 8,
                "id": 13,
                "title": "14-Январь Ватан ҳимоячилари куни"
            },
            {
                "i": 9,
                "id": 14,
                "title": "Чегарамизни ҳимоя қилиш шарафли бурчдир!"
            },
            {
                "i": 10,
                "id": 561,
                "title": "Сарҳадлари тинч юртда эрикн ва ҳур фарзандлар туғилади!"
            },
            {
                "i": 11,
                "id": 13,
                "title": "14-Январь Ватан ҳимоячилари куни"
            },
            {
                "i": 12,
                "id": 14,
                "title": "Чегарамизни ҳимоя қилиш шарафли бурчдир!"
            },
            {
                "i": 13,
                "id": 561,
                "title": "Сарҳадлари тинч юртда эрикн ва ҳур фарзандлар туғилади!"
            },
            {
                "i": 14,
                "id": 13,
                "title": "14-Январь Ватан ҳимоячилари куни"
            },
            {
                "i": 15,
                "id": 14,
                "title": "Чегарамизни ҳимоя қилиш шарафли бурчдир!"
            },
            {
                "i": 16,
                "id": 561,
                "title": "Сарҳадлари тинч юртда эрикн ва ҳур фарзандлар туғилади!"
            }
        ]
        pdf, current_user = add_letter(request.data, data)
        serializer = LetterCreateUpdateSerializer(data=request.data)
        serializer.context['pdf'] = pdf
        serializer.context['request'] = request
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            letter = serializer.save()
            Notification.objects.create(
                recipient=current_user,
                letter=letter,
                message=f"Sizga yangi xat keldi: {letter.title}"
            )
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LetterUpdateAPIView(generics.UpdateAPIView):
    """
        Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return response.Response(serializer.data)
