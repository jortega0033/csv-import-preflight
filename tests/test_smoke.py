import importlib
import subprocess
import sys
import unittest

MODULES = ["contracts", "dialect", "mapping", "rules", "classify", "exports", "store", "server"]


def run(*args):
    return subprocess.run([sys.executable, "-m", "csv_preflight", *args], capture_output=True, text=True)


class ModuleImports(unittest.TestCase):
    def test_each_module_imports(self):
        for name in MODULES:
            with self.subTest(module=name):
                importlib.import_module(f"csv_preflight.{name}")


class EntryPoint(unittest.TestCase):
    def test_help_and_version(self):
        self.assertEqual(run("--help").returncode, 0)
        self.assertEqual(run("--version").returncode, 0)

    def test_serve_is_a_stub(self):
        result = run("serve", "--data-dir", "x")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not implemented yet: see #2", result.stderr)


if __name__ == "__main__":
    unittest.main()
