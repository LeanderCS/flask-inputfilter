try:
    from .InputFilter import InputFilter
except ImportError:
    import pyximport

    pyximport.install()
    from .InputFilter import InputFilter
