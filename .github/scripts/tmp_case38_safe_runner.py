from pathlib import Path

original_unlink = Path.unlink
preserve = {
    '.github/workflows/tmp-case38-s3500-independent-validation.yml',
    '.github/scripts/tmp_case38_s3500_integrate.py',
    '.github/scripts/tmp_case38_safe_runner.py',
}

def safe_unlink(self, *args, **kwargs):
    if self.as_posix() in preserve:
        print(f'preserving temporary integration file during Actions commit: {self}')
        return None
    return original_unlink(self, *args, **kwargs)

Path.unlink = safe_unlink
script = Path('.github/scripts/tmp_case38_s3500_integrate.py')
code = compile(script.read_text(encoding='utf-8'), str(script), 'exec')
exec(code, {'__name__': '__main__'})
