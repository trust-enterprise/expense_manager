from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.db.models import Sum
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.
def home(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Expense added successfully')
            return redirect('home')
    else:
        form = ExpenseForm()

    query = request.GET.get('q', '')
    expenses = Expense.objects.filter(title__icontains=query)

    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    paginator = Paginator(expenses, 5)
    expenses = paginator.get_page(request.GET.get('page'))


    return render(request, 'expenses/home.html',
                  {
                      'form':form,
                      'expenses':expenses,
                      'total': total
                  }
                  )

@require_POST
def delete_expense(request, id):
    expense = get_object_or_404(Expense, id = id)
    expense.delete()
    messages.success(request,'Expense deleted successfully')
    return redirect('home')

def edit_expense(request, id):
    expense = get_object_or_404(Expense, id = id)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save() 
        return redirect('home')
    else:
        form = ExpenseForm(instance=expense)
 

    return render(request, 'expenses/edit.html', 
                  {
                      'form':form 
                  }
                  )