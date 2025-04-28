from django.shortcuts import render, redirect
from .models import Todo
from .forms import TodoForm

# Create your views here.
# 전체리스트 보기
def todo_list(request):
    todos=Todo.objects.filter(complete=False)   # 완료되지 않은 Todo 목록만 표시
    return render(request, 'todo/todo_list.html', {'todos': todos})

# 상세보기
def todo_detail(request, pk):
    todo=Todo.objects.get(id=pk)
    return render(request, 'todo/todo_detail.html', {'todo': todo})

# Todo 생성 
def todo_post(request):
    if request.method=="POST":              # POST 요청이 들어왔을 때는 폼을 검증하고 데이터 저장
        form=TodoForm(request.POST)
        if form.is_valid():
            todo=form.save(commit=False)
            todo.save()
            return redirect('todo_list')
    else:                                   # GET 요청이 들어왔을 때는 폼을 포함한 템플릿 페이지 출력
        form=TodoForm()
    return render(request, 'todo/todo_post.html', {'form':form})

# Todo 수정 
def todo_edit(request, pk):
    todo=Todo.objects.get(id=pk)
    if request.method=="POST":
        form=TodoForm(request.POST, instance=todo)
        if form.is_valid():
            todo=form.save(commit=False)
            todo.save()
            return redirect('todo_list')
    else: 
        form=TodoForm(instance=todo)
    return render(request, 'todo/todo_post.html', {'form': form})

# Todo 완료목록
def done_list(request):
   dones=Todo.objects.filter(complete=True)
   return render(request, 'todo/done_list.html',{'dones':dones} )
        

# Todo 완료
def todo_done(request, pk):
    todo=Todo.objects.get(id=pk)
    todo.complete=True
    todo.save()
    return redirect('todo_list')