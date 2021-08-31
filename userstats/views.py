from typing import cast
from rest_framework.views import APIView
import datetime
from expenses.models import Expense
from rest_framework import status, response


class ExpenseSummaryStats(APIView):

    def get_categories(self, expense):
        return expense.category

    def get_amount_for_category(self, expense_list, category):
        expenses = expense_list.filter(category=category)
        amount = 0
        for expense in expenses:
            amount += expense.amount
        return {'amount': str(amount)}

    def get(self, request):
        todays_date = datetime.date.today()
        ayear_ago = todays_date-datetime.timedelta(days=30*12)
        expenses = Expense.objects.filter(owner=request.user)

        final = {}
        categories = list(set(map(self.get_categories, expenses)))

        for expense in expenses:
            for category in categories:
                final[category] = self.get_amount_for_category(expenses, category)

        return response.Response({'category_data': final}, status=status.HTTP_200_OK)
        

