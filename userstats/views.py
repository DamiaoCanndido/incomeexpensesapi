from rest_framework.views import APIView
import datetime
from expenses.models import Expense


class ExpenseSummaryStats(APIView):
    def get(self, request):
        todays_date = datetime.date.today()
        ayear_ago = todays_date-datetime.timedelta(days=30*12)
        expenses = Expense.objects.filter(owner=request.user, date__gte=ayear_ago, date__lte=todays_date)
