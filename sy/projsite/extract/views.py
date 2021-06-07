from django.shortcuts import render

#요청이 들어오면 home.html 파일을 open
def base(request):
    return render(request, 'base.html')

def result(request):
    origin_text = request.GET['original-text']
    

    return render(request, 'result.html', { 'origins' : origin_text})