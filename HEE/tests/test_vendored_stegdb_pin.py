import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "HEE" / "tools" / "verify_stegdb_hee_import.py"


def load_tool():
    spec = importlib.util.spec_from_file_location("verify_stegdb_hee_import", TOOL)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class VendoredStegDBPinTest(unittest.TestCase):
    def test_vendored_bytes_verify_without_network(self):
        tool = load_tool()
        with tempfile.TemporaryDirectory() as tmp:
            validation, lock = tool.run_import(tool.DEFAULT_CONFIG, Path(tmp))
        self.assertEqual(validation["state"], "COMPLETE", validation)
        self.assertEqual(len(lock["protocols"]), 7)

    def test_tampered_bytes_fail_closed(self):
        tool = load_tool()
        config = json.loads(tool.DEFAULT_CONFIG.read_text())
        pin = json.loads((ROOT / config["pin_manifest_path"]).read_text())
        path = config["required_paths"][0]
        with tempfile.TemporaryDirectory() as tmp:
            vendor = Path(tmp) / "vendor"
            shutil.copytree(ROOT / pin["vendor_root"], vendor)
            target = vendor / path
            target.write_bytes(target.read_bytes() + b" ")
            pin["vendor_root"] = str(vendor)
            with self.assertRaises(tool.PinError) as ctx:
                tool.read_pinned_bytes(pin, path)
        self.assertEqual(ctx.exception.code, "vendored_sha256_mismatch")


if __name__ == "__main__":
    unittest.main()
