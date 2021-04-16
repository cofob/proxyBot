class MessageFunc:
    def __init__(self, func, regular=False, text=None, command=False, first=None, lower=False):
        self.func = func
        self.regular = regular
        self.text = text
        self.command = command
        self.first = first
        self.lower = lower

    def get_text(self):
        if self.command:
            return r'^/'+self.text+r'(@\w+)?'
        return self.text


class InlineFunc:
    def __init__(self, func, command=False, regular=False, text=None, first=None, lower=False):
        self.func = func
        self.regular = regular
        self.text = text
        self.first = first
        self.lower = lower
        self.command = command

    def get_text(self):
        if self.command:
            return r'^'+self.text
        return self.text


class ButtonFunc:
    def __init__(self, func, command=False, regular=False, text=None, first=None, lower=False):
        self.func = func
        self.regular = regular
        self.text = text
        self.first = first
        self.lower = lower
        self.command = command

    def get_text(self):
        if self.command:
            return b'^'+self.text
        return self.text
