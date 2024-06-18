from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .models import ReestrOt

User = get_user_model()

# class ProtokolSuccess(LoginRequiredMixin, generic.TemplateView):
#     """Страница успешного выполнения операции."""
#     template_name = 'ot/success.html'


class ReestrOtBase(LoginRequiredMixin):
    """Базовый класс для остальных CBV."""
    model = ReestrOt
    # success_url = reverse_lazy('ot:success')

    def get_queryset(self):
        """Пользователь может работать только со своими протоколами."""
        return self.model.objects.filter(author=self.request.user)


class ReestrOtList(ReestrOtBase, generic.ListView):
    """Список всех протоколов пользователя."""
    template_name = 'eisot/list.html'


class ReestrOtDetail(ReestrOtBase, generic.DetailView):
    """Протокол подробно."""
    template_name = 'eisot/detail.html'
