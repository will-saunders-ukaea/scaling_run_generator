import os
import shutil


class BaseFile:
    def __init__(self, filename):
        self.filename = os.path.abspath(filename)

    def process(self, subs, directory):
        pass

    def get_arg(self, directory):
        pass


class Static(BaseFile):
    def __init__(self, filename):
        super().__init__(filename)

    def get_arg(self, directory):
        return self.filename


class Template(BaseFile):
    def __init__(self, filename):
        super().__init__(filename)
        self.basename = os.path.basename(self.filename)

    def _output_name(self, directory):
        return os.path.join(directory, self.basename)

    def process(self, subs, directory):
        s = open(self.filename).read()

        for sub in subs.items():
            sub_string = "{{{{{KEY}}}}}".format(KEY=sub[0])
            s = s.replace(sub_string, str(sub[1]))

        with open(self._output_name(directory), "w") as fh:
            fh.write(s)

    def get_arg(self, directory):
        return os.path.join("./", self.basename)


class Copy(BaseFile):
    def __init__(self, filename):
        super().__init__(filename)
        self.basename = os.path.basename(self.filename)

    def _output_name(self, directory):
        return os.path.join(directory, self.basename)

    def process(self, subs, directory):
        shutil.copyfile(self.filename, self._output_name(directory))

    def get_arg(self, directory):
        return os.path.join("./", self.basename)
