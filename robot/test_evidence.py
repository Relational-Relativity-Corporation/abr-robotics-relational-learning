import contextlib
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from verify_evidence import verify


class Evidence(unittest.TestCase):
    def test_saved_experiment_integrity_and_behavior(self):
        artifact=Path(__file__).parent/'evidence/stage3-first-closed-loop.zip'
        with contextlib.redirect_stdout(io.StringIO()):result=verify(artifact)
        self.assertEqual(result['trial_samples'],[166,118])
        self.assertEqual(result['persistence_pairs'],283)

    def test_changed_evidence_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            artifact=Path(directory)/'corrupt.zip'
            with zipfile.ZipFile(artifact,'x') as z:
                z.writestr('manifest.json',json.dumps({'observation.json':'0'*64}))
                z.writestr('observation.json','{"altered":true}')
            with self.assertRaisesRegex(AssertionError,'hash mismatch'):
                verify(artifact)


if __name__=='__main__':unittest.main(verbosity=2)
