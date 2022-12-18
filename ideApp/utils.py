import uuid
import subprocess
import django
django.setup()

from .models import Submissions

def create_file(code, ext):
    file_name = str(uuid.uuid4()) + "." + ext
    with open("codeFiles/" + file_name, "w") as f:
        f.write(code)
    return file_name


def execute_file(file_name, language, sid):
    submission = Submissions.objects.get(pk=sid)
    if language == "cpp":
        result = subprocess.run(["g++", "codeFiles/" + file_name], stdout=subprocess.PIPE)
        if result.returncode != 0:
            submission.status = "E"
            submission.save()
            return
        result = subprocess.run(["./a.exe"], stdout=subprocess.PIPE)
        if result.returncode != 0:
            submission.status = "E"
            submission.save()
            return

        output = result.stdout.decode("utf-8")
        submission.output = output
        submission.status = "S"
        submission.save()
