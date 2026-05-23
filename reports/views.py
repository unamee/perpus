from django.shortcuts import render

from .services import active_borrow_report, overdue_report


def dashboard(request):

    context = {

        'active_borrows':
            active_borrow_report(),

        'overdue':
            overdue_report(),

    }

    return render(
        request,
        'reports/dashboard.html',
        context
    )
