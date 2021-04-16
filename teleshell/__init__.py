from telethon import events
from re import findall
from .classes import *


class ClientShell:
    def __init__(self, client, button_first=None, message_first=None, inline_first=None, first_occurrence=True,
                 from_me=False):
        self.client = client
        self.message_handlers = []
        self.inline_handlers = []
        self.button_handlers = []
        self.message_first = message_first
        self.inline_first = inline_first
        self.button_first = button_first
        self.first_occurrence = first_occurrence
        self.from_me = from_me

        @self.client.on(events.NewMessage())
        async def client_handler(event):
            if not self.from_me:
                if event.message.out:
                    return None
            for f in self.message_handlers:
                passed = False
                text = event.text
                ftext = f.get_text()

                if f.lower:
                    text = text.lower()
                if f.regular:
                    if ftext == '*':
                        passed = True
                    else:
                        r = findall(ftext, text)
                        if r:
                            passed = True
                else:
                    if text == ftext:
                        passed = True

                if passed:
                    if f.first:
                        ret = await f.first(event)
                        await f.func(event, ret)
                    else:
                        await f.func(event)
                    if self.first_occurrence:
                        return None

        @self.client.on(events.InlineQuery())
        async def client_handler(event):
            for f in self.inline_handlers:
                passed = False
                text = event.query.query
                ftext = f.get_text()

                if f.lower:
                    text = text.lower()
                if f.regular:
                    if ftext == '*':
                        passed = True
                    else:
                        r = findall(ftext, text)
                        if r:
                            passed = True
                else:
                    if text == ftext:
                        passed = True

                if passed:
                    if f.first:
                        ret = await f.first(event)
                        await f.func(event, ret)
                    else:
                        await f.func(event)
                    if self.first_occurrence:
                        return None

        @self.client.on(events.CallbackQuery())
        async def client_handler(event):
            for f in self.button_handlers:
                passed = False
                text = event.data
                ftext = f.get_text()

                if f.lower:
                    text = text.lower()
                if f.regular:
                    if ftext == b'*':
                        passed = True
                    else:
                        r = findall(ftext, text)
                        if r:
                            passed = True
                else:
                    if text == ftext:
                        passed = True

                if passed:
                    if f.first:
                        ret = await f.first(event)
                        await f.func(event, ret)
                    else:
                        await f.func(event)
                    if self.first_occurrence:
                        return None

    def handle(self, text=None, command=None, regular=False, first=False, lower=False):
        if first is False:
            first = self.message_first
        if command:
            text = command
            command = True
            regular = True
            lower = True

        def handler(func):
            if text is not None:
                obj = MessageFunc(func=func, regular=regular, text=text, command=command, first=first, lower=lower)
            else:
                obj = MessageFunc(func=func, regular=True, text='*', command=command, first=first, lower=False)
            self.message_handlers.append(obj)
        return handler

    def inline(self, text=None, command=None, regular=False, first=False, lower=False):
        if first is False:
            first = self.inline_first
        if command:
            text = command
            command = True
            regular = True

        def handler(func):
            if text is not None:
                obj = InlineFunc(func=func, command=command, regular=regular, text=text, first=first, lower=lower)
            else:
                obj = InlineFunc(func=func, command=command, regular=True, text='*', first=first, lower=False)
            self.inline_handlers.append(obj)
        return handler

    def button(self, text=None, command=None, regular=False, first=False, lower=False):
        if first is False:
            first = self.button_first
        if command:
            text = command
            command = True
            regular = True

        def handler(func):
            if text is not None:
                obj = ButtonFunc(func=func, command=command, regular=regular, text=text, first=first, lower=lower)
            else:
                obj = ButtonFunc(func=func, command=command, regular=True, text=b'*', first=first, lower=False)
            self.button_handlers.append(obj)
        return handler
