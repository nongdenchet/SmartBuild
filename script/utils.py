import os
import subprocess
import re


def get_modules(settings_file_path):
    path = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(path, settings_file_path)) as settings_file:
        data = settings_file.read().replace('\n', '')
        data = re.sub("(include |'|:|)", "", data)
        modules = [s.strip() for s in data.split(',')]
        modules.remove("Data")
        return modules


def execute_command(command):
    result = ""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(process.stdout.readline, ''):
        result += line
    return result


def get_current_commit():
    return execute_command("git rev-parse --short HEAD").split("\n")[0]


def get_branch_commit(branch):
    return execute_command("git rev-parse --short {0}".format(branch)).split("\n")[0]


def directory_changes(compare_branch):
    current_commit = get_current_commit()
    current_branch_commit = get_branch_commit(compare_branch)
    return execute_command("git diff --name-only {0}...{1}".format(current_branch_commit, current_commit)).split("\n")


def detect_changed_modules(compare_branch):
    result = set()
    all_modules = get_modules("../settings.gradle")
    for dir in directory_changes(compare_branch):
        print dir
        if dir.startswith("Data/"):
            print "Data changing rebuild all"
            return all_modules
        for module in all_modules:
            if dir.startswith("{0}/".format(module)):
                result.add(module)
                break
    if len(result) == 0:
        result = set(all_modules)
    return list(result)


def run_command_on_subprocess(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(process.stdout.readline, ''):
        print line
    return process.poll()
