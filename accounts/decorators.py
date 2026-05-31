from django.http import HttpResponseForbidden


def role_required(roles):

    def decorator(view_func):

        def wrapper(
            request,
            *args,
            **kwargs
        ):

            if request.user.role in roles:

                return view_func(
                    request,
                    *args,
                    **kwargs
                )

            return HttpResponseForbidden(
                'Permission denied.'
            )

        return wrapper

    return decorator
