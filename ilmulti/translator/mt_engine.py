import ilmulti

class MTEngine:
    def __init__(self, translator, segmenter, tokenizer):
        self.segmenter = segmenter
        self.tokenizer = tokenizer
        self.translator = translator

    def __call__(self, source, tgt_lang, src_lang=None, detokenize=True):
        lang, lines = self.segmenter(source)
        sources = []
        for line in lines:
            lang, tokens = self.tokenizer(line)
            src_lang = src_lang or lang
            # Unsupervised tokenization.
            tokens = [ilmulti.utils.language_token(tgt_lang)] + tokens
            content = ' '.join(tokens)
            sources.append(content)

        export = self.translator(sources)
        if detokenize:
            export = self._detokenize(export)
        return export

    def _detokenize(self, export):
        _exports = []
        for entry in export:
            for key in ['src', 'tgt']:
                entry[key] = self.tokenizer.detokenize(entry[key])
            entry['src'] = entry['src'][9:]
            _exports.append(entry)
        return _exports
