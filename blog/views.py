import json
import subprocess
import tempfile

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Post


def post_list(request):
    posts = Post.objects.all()
    unlocked = request.session.get("unlocked_posts", [])
    return render(
        request, "blog/post_list.html", {"posts": posts, "unlocked": unlocked}
    )


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    unlocked = request.session.get("unlocked_posts", [])

    if post.private and post.slug not in unlocked:
        error = None
        if request.method == "POST":
            if post.check_password(request.POST.get("password", "")):
                unlocked.append(post.slug)
                request.session["unlocked_posts"] = unlocked
                return redirect(post)
            else:
                error = "Wrong password."
        return render(
            request,
            "blog/post_password.html",
            {"post": post, "error": error},
        )

    return render(request, "blog/post_detail.html", {"post": post})


@csrf_exempt
@require_POST
def run_python(request):
    try:
        body = json.loads(request.body)
        code = body.get("code", "")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"ok": False, "output": "Invalid request."}, status=400)

    if not code.strip():
        return JsonResponse({"ok": False, "output": "(empty)"})

    try:
        proc = subprocess.run(
            ["python", "-c", code],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if proc.returncode == 0:
            output = proc.stdout
            if proc.stderr:
                output += proc.stderr
            if not output.strip():
                output = "(no output)"
            return JsonResponse({"ok": True, "output": output})
        else:
            return JsonResponse({"ok": False, "output": proc.stderr or proc.stdout})
    except subprocess.TimeoutExpired:
        return JsonResponse(
            {"ok": False, "output": "TimeoutError: code took too long."}
        )
