from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_uoishelpers_is_declared_as_direct_github_zip_dependency():
    pyproject = (ROOT / 'pyproject.toml').read_text()
    assert 'uoishelpers @ https://github.com/hrbolek/uoishelpers/archive/refs/heads/main.zip' in pyproject


def test_project_does_not_vendor_uoishelpers():
    assert not (ROOT / 'uoishelpers').exists()
    assert not (ROOT / 'src' / 'uoishelpers').exists()
