from enum import Enum


class CALCERGEBNISTYPE(str, Enum):
    CALCULATE = "CALCULATE"
    STRING = "STRING"
    ERROR = "ERROR"


class CALCMODE(str, Enum):
    MAXIMA = "MAXIMA"
    LOESUNG = "LOESUNG"
    EQUALS = "EQUALS"
    VIEW = "VIEW"


class IMAGEUNIT(str, Enum):
    none = "none"
    px = "px"
    pt = "pt"
    cm = "cm"
    percent = "percent"
    em = "em"


class InputElement(str, Enum):
    TextField = "TextField"
    TextArea = "TextArea"
    Button = "Button"
    MULTICHOICE = "MULTICHOICE"
    XHTML = "XHTML"
    SourceCode = "SourceCode"
    JAVASCRIPT = "JAVASCRIPT"


class ORIENTATIONX(str, Enum):
    LEFT = "LEFT"
    CENTER = "CENTER"
    RIGHT = "RIGHT"


class ORIENTATIONY(str, Enum):
    BOTTOM = "BOTTOM"
    CENTER = "CENTER"
    TOP = "TOP"


class SHOWPOTENZ(str, Enum):
    AUTO = "AUTO"
    POW = "POW"
    SQRT = "SQRT"

    @classmethod
    def parse(cls, s: str) -> "SHOWPOTENZ":
        try:
            return cls(s.upper())
        except ValueError:
            return cls.AUTO


class Score(str, Enum):
    NotScored = "NotScored"
    OK = "OK"
    FALSCH = "FALSCH"
    TEILWEISE_OK = "TEILWEISE_OK"
    EINHEITENFEHLER = "EINHEITENFEHLER"
    OK_Lehrer = "OK_Lehrer"
    FALSCH_Lehrer = "FALSCH_Lehrer"
    TEILWEISE_OK_Lehrer = "TEILWEISE_OK_Lehrer"
    EINHEITENFEHLER_Lehrer = "EINHEITENFEHLER_Lehrer"
    ANGABEFEHLER_EH = "ANGABEFEHLER_EH"
    PARSERFEHLER_SYSTEM = "PARSERFEHLER_SYSTEM"
    NichtEntschieden = "NichtEntschieden"
    MEHRFACHANTWORT_OK = "MEHRFACHANTWORT_OK"
    MEHRFACHANTWORT_OK_LEHRER = "MEHRFACHANTWORT_OK_LEHRER"
    MEHRFACHANTWORT_TW_RICHTIG = "MEHRFACHANTWORT_TW_RICHTIG"
    MEHRFACHANTWORT_TW_RICHTIG_LEHRER = "MEHRFACHANTWORT_TW_RICHTIG_LEHRER"

    def get_score_tex_color(self) -> str:
        color_map = {
            Score.OK: "green",
            Score.FALSCH: "red",
            Score.TEILWEISE_OK: "orange",
            Score.EINHEITENFEHLER: "orange",
            Score.OK_Lehrer: "green",
            Score.FALSCH_Lehrer: "red",
            Score.TEILWEISE_OK_Lehrer: "orange",
            Score.EINHEITENFEHLER_Lehrer: "orange",
            Score.NotScored: "gray",
            Score.NichtEntschieden: "gray",
        }
        return color_map.get(self, "black")

    def html_color(self, text: str) -> str:
        color = self.get_score_tex_color()
        return f'<span style="color:{color}">{text}</span>'


class TOLERANZMODE(str, Enum):
    RELATIV = "RELATIV"
    ABSOLUT = "ABSOLUT"
