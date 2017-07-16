from utils import *
import sys


def run_command(cmd):
    print "Running command {0}".format(cmd)
    return run_command_on_subprocess(cmd)


def main():
    modules = detect_changed_modules("origin/develop")
    print "Building on these modules {0}".format(modules)
    for module in modules:
        result = run_command("./gradlew :{0}:check".format(module))
        if result != 0: sys.exit(result)
        result = run_command("cp -r ${{HOME}}/${{CIRCLE_PROJECT_REPONAME}}/{0}/build/reports $CIRCLE_ARTIFACTS".format(module))
        if result != 0: sys.exit(result)


if __name__ == "__main__": main()
