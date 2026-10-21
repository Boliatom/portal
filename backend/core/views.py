import json
from django.core import signing
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from .models import Module, Role, User

TOKEN_MAX_AGE = 60 * 60 * 12


def get_user(request):
    header = request.headers.get('Authorization', '')
    if not header.startswith('Bearer '):
        return None
    try:
        data = signing.loads(header[7:], max_age=TOKEN_MAX_AGE)
    except signing.BadSignature:
        return None
    return User.objects.filter(id=data['user_id'], active=True).first()


def user_to_dict(user):
    return {
        'id': user.id,
        'username': user.username,
        'last_name': user.last_name,
        'first_name': user.first_name,
        'middle_name': user.middle_name,
        'email': user.email,
        'active': user.active,
    }


@require_POST
def login(request):
    try:
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
    except (ValueError, KeyError, TypeError):
        return JsonResponse({'error': 'Введите логин и пароль'}, status=400)
    user = User.objects.filter(username=username, password=password, active=True).first()
    if user is None:
        return JsonResponse({'error': 'Неверный логин или пароль'}, status=401)
    User.objects.filter(id=user.id, first_login_at__isnull=True).update(first_login_at=timezone.now())
    return JsonResponse({'token': signing.dumps({'user_id': user.id})})


@require_GET
def home(request):
    user = get_user(request)
    if user is None:
        return JsonResponse({'error': 'Нужно войти'}, status=401)

    groups = Role.objects.filter(userrole__user=user).order_by('name')
    return JsonResponse({
        'username': user.username,
        'last_name': user.last_name,
        'first_name': user.first_name,
        'middle_name': user.middle_name,
        'email': user.email,
        'created_at': user.created_at,
        'first_login_at': user.first_login_at,
        'groups': [g.name for g in groups],
    })


@require_GET
def user_info(request, user_id):
    if get_user(request) is None:
        return JsonResponse({'error': 'Нужно войти'}, status=401)

    user = User.objects.filter(id=user_id).first()
    if user is None:
        return JsonResponse({'error': 'Пользователь не найден'}, status=404)
    return JsonResponse(user_to_dict(user))


@require_GET
def user_groups(request, user_id):
    if get_user(request) is None:
        return JsonResponse({'error': 'Нужно войти'}, status=401)

    groups = Role.objects.filter(userrole__user=user_id).order_by('name')
    return JsonResponse({'groups': [{'id': g.id, 'name': g.name} for g in groups]})


@require_GET
def group_users(request, group_id):
    if get_user(request) is None:
        return JsonResponse({'error': 'Нужно войти'}, status=401)

    users = User.objects.filter(userrole__role=group_id).order_by('last_name', 'first_name')
    return JsonResponse({'users': [user_to_dict(u) for u in users]})


@require_GET
def check_auth(request):
    user = get_user(request)
    if user is None:
        return JsonResponse({'error': 'Нужно войти'}, status=401)
    return JsonResponse({'authorized': True, 'user_id': user.id})


@require_GET
def module_list(request):
    if get_user(request) is None:
        return JsonResponse({'error': 'Нужно войти'}, status=401)

    modules = Module.objects.order_by('id')
    return JsonResponse({'modules': [{'id': m.id, 'name': m.name} for m in modules]})
