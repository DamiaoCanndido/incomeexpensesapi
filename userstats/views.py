from typing import cast
from rest_framework.views import APIView
import datetime
from expenses.models import Expense
from incomes.models import Income
from rest_framework import status, response
from rest_framework import permissions


class ExpenseSummaryStats(APIView):

    permission_classes = (permissions.IsAuthenticated,)

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



class IncomeSourcesSummaryStats(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get_sources(self, income):
        return income.source

    def get_amount_for_sources(self, income_list, source):
        incomes = income_list.filter(source=source)
        amount = 0
        for income in incomes:
            amount += income.amount
        return {'amount': str(amount)}

    def get(self, request):
        todays_date = datetime.date.today()
        ayear_ago = todays_date-datetime.timedelta(days=30*12)
        incomes = Income.objects.filter(owner=request.user)

        final = {}
        sources = list(set(map(self.get_sources, incomes)))

        for income in incomes:
            for source in sources:
                final[source] = self.get_amount_for_sources(incomes, source)

        return response.Response({'income_source_data': final}, status=status.HTTP_200_OK)
        

