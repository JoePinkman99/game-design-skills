import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "game-analysis" / "scripts"))
import matrix_analysis as ma

SCRIPT = str(Path(__file__).resolve().parent.parent
             / "game-analysis" / "scripts" / "matrix_analysis.py")
FIXTURES = Path(__file__).resolve().parent / "fixtures"

RPS = {"nodes": ["Rock", "Paper", "Scissors"],
       "matrix": [[0, -1, 1], [1, 0, -1], [-1, 1, 0]]}
# Hex-crawler (analysis-workflow.md): I beats P, P beats C, C beats R, R beats I;
# neutral: P-R, I-C.
HEX = {"nodes": ["Infantry", "Cavalry", "Ranged", "Pikemen"],
       "matrix": [[0, 0, -1, 1],
                  [0, 0, 1, -1],
                  [1, -1, 0, 0],
                  [-1, 1, 0, 0]]}
# Transitive chain A > B > C (A beats B and C; B beats C).
CHAIN = {"nodes": ["A", "B", "C"],
         "matrix": [[0, 1, 1], [-1, 0, 1], [-1, -1, 0]]}
# Weighted (Pokemon-style multipliers): Water beats Fire (2 > 0.5).
WEIGHTED = {"nodes": ["Fire", "Water"],
            "matrix": [[1, 0.5], [2, 1]]}


def write_fixture(data):
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
    json.dump(data, f)
    f.close()
    return f.name


class TestLoadInput(unittest.TestCase):
    def test_binary_mode_detected(self):
        nodes, matrix, mode = ma.load_input(write_fixture(RPS))
        self.assertEqual(nodes, RPS["nodes"])
        self.assertEqual(mode, "binary")

    def test_weighted_mode_detected(self):
        _, _, mode = ma.load_input(write_fixture(WEIGHTED))
        self.assertEqual(mode, "weighted")

    def test_rejects_non_square(self):
        bad = {"nodes": ["A", "B"], "matrix": [[0, 1]]}
        with self.assertRaises(ValueError):
            ma.load_input(write_fixture(bad))

    def test_rejects_duplicate_nodes(self):
        bad = {"nodes": ["A", "A"], "matrix": [[0, 1], [-1, 0]]}
        with self.assertRaises(ValueError):
            ma.load_input(write_fixture(bad))

    def test_rejects_binary_antisymmetry_violation(self):
        bad = {"nodes": ["A", "B"], "matrix": [[0, 1], [1, 0]]}
        with self.assertRaises(ValueError):
            ma.load_input(write_fixture(bad))

    def test_rejects_binary_nonzero_diagonal(self):
        bad = {"nodes": ["A", "B"], "matrix": [[1, 1], [-1, 0]]}
        with self.assertRaises(ValueError):
            ma.load_input(write_fixture(bad))


class TestOutcome(unittest.TestCase):
    def test_binary_outcomes(self):
        m = RPS["matrix"]
        self.assertEqual(ma.outcome(m, "binary", 0, 2), 1)   # Rock beats Scissors
        self.assertEqual(ma.outcome(m, "binary", 0, 1), -1)  # Rock loses to Paper
        self.assertEqual(ma.outcome(m, "binary", 1, 1), 0)   # diagonal neutral

    def test_weighted_outcomes(self):
        m = WEIGHTED["matrix"]
        self.assertEqual(ma.outcome(m, "weighted", 1, 0), 1)   # Water beats Fire
        self.assertEqual(ma.outcome(m, "weighted", 0, 1), -1)
        self.assertEqual(ma.outcome(m, "weighted", 0, 0), 0)


class TestStructure(unittest.TestCase):
    def graph(self, fx):
        return ma.beats_graph(fx["nodes"], fx["matrix"],
                              "binary"), len(fx["nodes"])

    def test_rps_is_tournament_hex_is_not(self):
        self.assertTrue(ma.is_tournament(RPS["nodes"], RPS["matrix"], "binary"))
        self.assertFalse(ma.is_tournament(HEX["nodes"], HEX["matrix"], "binary"))

    def test_rps_cycle_found(self):
        g, n = self.graph(RPS)
        cyc = ma.find_cycle(g, n)
        self.assertEqual(cyc, [0, 2, 1])  # Rock -> Scissors -> Paper -> (Rock)

    def test_hex_has_4cycle_but_zero_3cycles(self):
        g, n = self.graph(HEX)
        self.assertEqual(ma.find_cycle(g, n), [0, 3, 1, 2])  # I -> P -> C -> R
        self.assertEqual(ma.three_cycle_count(g, n), 0)

    def test_rps_has_one_3cycle(self):
        g, n = self.graph(RPS)
        self.assertEqual(ma.three_cycle_count(g, n), 1)

    def test_chain_is_dag_with_hierarchy(self):
        g, n = self.graph(CHAIN)
        self.assertIsNone(ma.find_cycle(g, n))
        self.assertEqual(ma.topological_order(g, n), [0, 1, 2])  # A, B, C


class TestDominance(unittest.TestCase):
    def test_rps_has_no_dominated_nodes(self):
        self.assertEqual(ma.dominated_nodes(RPS["nodes"], RPS["matrix"], "binary"), [])

    def test_hex_has_no_dominated_nodes(self):
        self.assertEqual(ma.dominated_nodes(HEX["nodes"], HEX["matrix"], "binary"), [])

    def test_chain_dominance(self):
        got = set(ma.dominated_nodes(CHAIN["nodes"], CHAIN["matrix"], "binary"))
        self.assertEqual(got, {("B", "A"), ("C", "A"), ("C", "B")})


class TestDoomStacks(unittest.TestCase):
    def test_rps_all_three_pairs_unbeatable(self):
        got = ma.doom_stacks(RPS["nodes"], RPS["matrix"], "binary", 2)
        self.assertEqual(len(got), 3)  # 2-Paradox impossible at 3 nodes

    def test_hex_all_six_pairs_unbeatable_incl_cavalry_ranged(self):
        got = ma.doom_stacks(HEX["nodes"], HEX["matrix"], "binary", 2)
        self.assertEqual(len(got), 6)
        self.assertIn(("Cavalry", "Ranged"), got)

    def test_chain_pairs_with_A_are_unbeatable_only(self):
        got = ma.doom_stacks(CHAIN["nodes"], CHAIN["matrix"], "binary", 2)
        self.assertEqual(got, [("A", "B"), ("A", "C")])

    def test_guard_returns_none_for_huge_search(self):
        n = 300
        nodes = [f"n{i}" for i in range(n)]
        matrix = [[0] * n for _ in range(n)]
        self.assertIsNone(ma.doom_stacks(nodes, matrix, "binary", 3))


class TestCentrality(unittest.TestCase):
    def test_rps_uniform(self):
        scores = dict(ma.eigenvector_centrality(RPS["nodes"], RPS["matrix"], "binary"))
        for v in scores.values():
            self.assertAlmostEqual(v, 1 / 3, places=6)

    def test_hex_uniform_by_symmetry(self):
        scores = dict(ma.eigenvector_centrality(HEX["nodes"], HEX["matrix"], "binary"))
        for v in scores.values():
            self.assertAlmostEqual(v, 1 / 4, places=6)

    def test_chain_ranks_A_first_C_last(self):
        ranked = ma.eigenvector_centrality(CHAIN["nodes"], CHAIN["matrix"], "binary")
        self.assertEqual([name for name, _ in ranked], ["A", "B", "C"])


class TestCLI(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, SCRIPT, *args],
                              capture_output=True, text=True)

    def test_rps_golden(self):
        r = self.run_cli(str(FIXTURES / "rps.json"))
        self.assertEqual(r.returncode, 0)
        out = r.stdout
        self.assertIn("Mode: binary", out)
        self.assertIn("Tournament: yes", out)
        self.assertIn("INTRANSITIVE", out)
        self.assertIn("Rock -> Scissors -> Paper -> Rock", out)
        self.assertIn("Dominated nodes: none", out)
        self.assertIn("3 unbeatable subset(s) of size 2", out)
        self.assertIn("2-Paradox property does NOT hold", out)

    def test_hex_golden(self):
        r = self.run_cli(str(FIXTURES / "hex.json"))
        self.assertEqual(r.returncode, 0)
        out = r.stdout
        self.assertIn("Tournament: no", out)
        self.assertIn("Infantry -> Pikemen -> Cavalry -> Ranged -> Infantry", out)
        self.assertIn("3-cycles: 0", out)
        self.assertIn("6 unbeatable subset(s) of size 2", out)
        self.assertIn("('Cavalry', 'Ranged')", out.replace('"', "'"))

    def test_bad_input_exits_1(self):
        bad = write_fixture({"nodes": ["A", "B"], "matrix": [[0, 1], [1, 0]]})
        r = self.run_cli(bad)
        self.assertEqual(r.returncode, 1)
        self.assertIn("antisymmetry", r.stderr)

    def test_weighted_golden(self):
        r = self.run_cli(str(FIXTURES / "weighted.json"))
        self.assertEqual(r.returncode, 0)
        out = r.stdout
        self.assertIn("Mode: weighted", out)
        self.assertIn("INTRANSITIVE", out)


class TestWeightedMode(unittest.TestCase):
    """End-to-end coverage for weighted mode through the analysis functions.
    Fixture (tests/fixtures/weighted.json): Fire/Water/Grass effectiveness
    matrix forming a clean 3-cycle (Water beats Fire, Fire beats Grass,
    Grass beats Water) — symmetric and analogous to RPS."""

    @classmethod
    def setUpClass(cls):
        cls.nodes, cls.matrix, cls.mode = ma.load_input(str(FIXTURES / "weighted.json"))

    def test_mode_is_weighted(self):
        self.assertEqual(self.mode, "weighted")

    def test_no_dominated_nodes(self):
        self.assertEqual(ma.dominated_nodes(self.nodes, self.matrix, self.mode), [])

    def test_all_three_pairs_unbeatable(self):
        got = ma.doom_stacks(self.nodes, self.matrix, self.mode, 2)
        self.assertEqual(len(got), 3)

    def test_centrality_uniform(self):
        scores = dict(ma.eigenvector_centrality(self.nodes, self.matrix, self.mode))
        for v in scores.values():
            self.assertAlmostEqual(v, 1 / 3, places=4)


class TestSignedWeighted(unittest.TestCase):
    """Signed (negative-valued) weighted matrices: outcome semantics stay valid,
    but eigenvector centrality is meaningless on signed weights (power iteration
    assumes non-negative entries) and must be skipped, not reported.
    Fixture: zero-sum differential encoding of weighted RPS — the same game as a
    non-negative points encoding, but centrality would return a negative
    'viability' (observed: Rock -1.755)."""

    SIGNED = {"nodes": ["Rock", "Paper", "Scissors"],
              "matrix": [[0, -2, 1], [2, 0, -3], [-1, 3, 0]]}

    def test_outcomes_still_valid_on_signed_input(self):
        m = self.SIGNED["matrix"]
        self.assertEqual(ma.outcome(m, "weighted", 1, 0), 1)   # Paper beats Rock (2 > -2)
        self.assertEqual(ma.outcome(m, "weighted", 0, 2), 1)   # Rock beats Scissors (1 > -1)

    def test_centrality_skipped_on_signed_weighted(self):
        self.assertIsNone(ma.eigenvector_centrality(
            self.SIGNED["nodes"], self.SIGNED["matrix"], "weighted"))

    def test_cli_signed_input_warns_and_completes(self):
        r = subprocess.run([sys.executable, SCRIPT, write_fixture(self.SIGNED)],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        self.assertIn("Dominated nodes: none", r.stdout)
        self.assertIn("skipped — weighted matrix contains negative values", r.stdout)
        self.assertNotIn("Rock: -", r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
