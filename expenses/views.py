from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.db.models import Sum
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request,'Expense added successfully')
            return redirect('home')
    else:
        form = ExpenseForm()

    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    
    categories = Expense.objects.filter(user = request.user).values_list('category', flat=True).distinct()
    expenses = Expense.objects.filter(user = request.user, title__icontains=query)
    
    if category:
        expenses = expenses.filter(category=category)
    
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    paginator = Paginator(expenses, 5)
    expenses = paginator.get_page(request.GET.get('page'))


    return render(request, 'expenses/home.html',
                  {
                      'form':form,
                      'categories': categories,
                      'expenses':expenses,
                      'total': total,
                  }
                  )

@require_POST
@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id = expense_id, user = request.user)
    expense.delete()
    messages.success(request,'Expense deleted successfully')
    return redirect('home')

@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id = expense_id, user = request.user)

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

def register(request):
    if request.method=="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'expenses/register.html', {'form':form})