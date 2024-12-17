from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    AdminUserCreationForm,
    UserChangeForm,
)
from django.db import transaction, router
from django.http import HttpResponseRedirect, Http404
from django.urls import path, reverse
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.template.response import TemplateResponse
from django.contrib import messages
from django.contrib.admin.utils import unquote
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from placarfutmesa.base.models import User

# Decoradores para proteção CSRF e parâmetros sensíveis
csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Template para adicionar um novo usuário
    add_form_template = "admin/auth/user/add_form.html"
    change_user_password_template = None

    # Definição dos campos que aparecem no formulário de edição do usuário
    fieldsets = (
        (None, {"fields": ("first_name", "last_name", "cpf", "nickname", "use_nickname", "email", "password")}),
        (_("Associations and Birth Info"), {"fields": ("association", "birth_year", "category")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                "first_name", "last_name", "cpf", "nickname", "use_nickname", "email", "password1", "password2"),
            },
        ),
    )

    # Formulários utilizados
    form = UserChangeForm
    add_form = AdminUserCreationForm
    change_password_form = AdminPasswordChangeForm

    # Campos a serem exibidos na lista de usuários
    list_display = ("cpf", "first_name", "last_name", "is_staff", "category")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", "association")
    search_fields = ("cpf", "first_name", "last_name", "email")
    ordering = ("first_name",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    # Métod para customizar o formulário de criação de usuário
    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults["form"] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    # Métod para definir URLs adicionais para o admin
    def get_urls(self):
        return [
            path(
                "<id>/password/",
                self.admin_site.admin_view(self.user_change_password),
                name="auth_user_password_change",
            ),
        ] + super().get_urls()

    # Adaptação para o processo de adição de um novo usuário
    @sensitive_post_parameters_m
    @csrf_protect_m
    def add_view(self, request, form_url="", extra_context=None):
        with transaction.atomic(using=router.db_for_write(self.model)):
            return self._add_view(request, form_url, extra_context)

    def _add_view(self, request, form_url="", extra_context=None):
        # Verificação de permissões
        if not self.has_change_permission(request):
            raise Http404('Your user does not have permission to change users.')
        if extra_context is None:
            extra_context = {}
        return super().add_view(request, form_url, extra_context)

    # Definir comportamento após adicionar um usuário
    def response_add(self, request, obj, post_url_continue=None):
        if "_addanother" not in request.POST:
            request.POST = request.POST.copy()
            request.POST["_continue"] = 1
        return super().response_add(request, obj, post_url_continue)

    # Alterações de senha no admin
    @sensitive_post_parameters_m
    def user_change_password(self, request, id, form_url=""):
        user = self.get_object(request, unquote(id))
        if not self.has_change_permission(request, user):
            raise PermissionDenied
        if user is None:
            raise Http404(_("User with primary key %(key)r does not exist.") % {"key": escape(id)})
        if request.method == "POST":
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                user = form.save()
                messages.success(request, _("Password changed successfully."))
                update_session_auth_hash(request, form.user)
                return HttpResponseRedirect(
                    reverse("admin:%s_%s_change" % (user._meta.app_label, user._meta.model_name), args=(user.pk,)))
        else:
            form = self.change_password_form(user)

        # Renderiza o formulário de alteração de senha
        fieldsets = [(None, {"fields": list(form.base_fields)})]
        admin_form = admin.helpers.AdminForm(form, fieldsets, {})
        title = _("Change password: %s")
        context = {
            "title": title % escape(user.get_username()),
            "adminForm": admin_form,
            "form_url": form_url,
            "form": form,
            "is_popup": False,
            "opts": self.opts,
            "original": user,
            "save_as": False,
            "show_save": True,
            **self.admin_site.each_context(request),
        }
        request.current_app = self.admin_site.name
        return TemplateResponse(request, self.change_user_password_template or "admin/auth/user/change_password.html",
                                context)
