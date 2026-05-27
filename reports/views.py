from django.shortcuts import render

from .services import (
    active_borrow_report,
    inventory_summary,
    overdue_report,
    top_readers,
    unpaid_fine_report,
)


def dashboard(request):

    context = {
        "active_borrows": active_borrow_report(),
        "overdue": overdue_report(),
        "active_borrow_count": active_borrow_report().count(),
        "overdue_count": overdue_report().count(),
        "unpaid_fine_count": unpaid_fine_report().count(),
        "top_readers": top_readers()[:5],
        "inventory": inventory_summary(),
    }

    return render(request, "reports/dashboard.html", context)


def dashboard_metrics(request):

    context = {

        'active_borrow_count':
            active_borrow_report().count(),

        'overdue_count':
            overdue_report().count(),

        'unpaid_fine_count':
            unpaid_fine_report().count(),

    }

    return render(
        request,
        'reports/partials/dashboard_metrics.html',
        context
    )
