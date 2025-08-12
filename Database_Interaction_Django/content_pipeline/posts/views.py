from django.shortcuts import render, redirect
from .models import Post

def create_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        body = request.POST.get("body")
        pdf_file = request.FILES.get("pdf_file")

        post = Post.objects.create(title=title, body=body, pdf_file=pdf_file)
        
        if pdf_file:
            post.extract_pdf_to_text()

        return redirect("post_list")
    return render(request, "posts/create_post.html")

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, "posts/post_list.html", {"posts": posts})
