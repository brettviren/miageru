from .base import BaseShCommand, find_path
import asyncio

default_config = dict(
    urls=None
)

# Erase the await
def translator_function(Translator, urls = None):

    def translate_sync(text: str, dest_lang: str = 'en') -> str:
        """
        Translates text using an async googletrans client in a synchronous context.
        """
        async def _async_translate():
            """Helper async function to perform the translation."""
            if urls:
                translator = Translator(service_urls = urls) 
            else:
                translator = Translator()
            result = await translator.translate(text, dest=dest_lang)
            return result

        # Run the async helper function within an asyncio event loop
        # asyncio.run() creates and manages the event loop for you.
        res = asyncio.run(_async_translate())
        return res.text

    return translate_sync

class Command(BaseShCommand):
    def __init__(self, urls=None, **kwds):
        super().__init__()

        try:
            from googletrans import Translator
        except ImportError:
            self._status='No googletrans package'
            return
        self._cmd = translator_function(Translator, urls)
        self._status = f'google translator available'
        
    def __call__(self, text, *args, **kwds):
        '''
        Call Google Translate text, return translation.
        '''
        return self._cmd(text)

