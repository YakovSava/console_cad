class Lexer:

    def __init__(self, command_filename:str="./home.cad", comma:str="//"):
        self._filename = command_filename
        self._comma = comma

    def _open(self) -> list[str]:
        with open(self._filename, 'r', encoding='utf-8') as file:
            return file.readlines()

    def _delete_comma_after(self, _line:str) -> str:
        try:
            return _line[:(_line.index(self._comma))-1]
        except:
            return _line

    def _delete_comma(self, _lexed:list[str]) -> list[str]:
        return list(map(self._delete_comma_after, filter(
            lambda x: not x.startswith(self._comma),
            _lexed
        )))

    def _separate(self, _lexed:list[str]) -> list[str]:
        _separated = []
        for _lex in _lexed:
            _separated.extend(_lex.split(';'))
        return _separated

    def _clean(self, _lexed:list[str]) -> list[str]:
        _cleaned = []
        for _lex in _lexed:
            _lex = _lex.replace('\n', '')
            if _lex:
                _cleaned.append(_lex.strip().rstrip())
        return _cleaned

    def compile(self) -> list[str]:
        return self._clean(
            self._separate(
                self._delete_comma(
                    self._open()
                )
            )
        )