from unittest.mock import patch

from base import BaseTest
from embit.psbt import PSBT

from seedsigner.controller import Controller
from seedsigner.models.seed import Seed
from seedsigner.models.settings import SettingsConstants
from seedsigner.views import scan_views
from seedsigner.views.psbt_views import PSBTSelectSeedView


# No input derivation metadata (single-address style PSBT)
PSBT_NO_DERIVATIONS_BASE64 = (
    "cHNidP8BAFUCAAAAAdC0JNDzdftNoelOBEKWPGQ9BXs3GzG6u4v+523x2+8ZAAAAAAD9////"
    "AVAmAAAAAAAAGXapFJ+wCM/fK1vBwwrLuZP+e4mgfZvwiKyCHQ0AAAEBIhAnAAAAAAAAGXap"
    "FHCzxXgPwziJsbmYr93rfCiiTgfgiKwAAA=="
)

# Includes input derivation metadata (xpub/seed-signable style PSBT)
PSBT_WITH_DERIVATIONS_BASE64 = (
    "cHNidP8BAHICAAAAAQDo5ey+2HIrNUkExsFhsImv1OK1cYA9x/bRjYQD+0UaAQAAAAD9////"
    "Apg6AAAAAAAAF6kUVuVZEcdpQ2zgABa9dRUNYHD4VuaHgSYAAAAAAAAWABQaLE4t0JbDRg4p"
    "Nnmcf+cAWIcyawAAAAAAAQEfqGEAAAAAAAAWABRyuw9od6yuS0yiZljV0X12wG9e5CIGA/Zl"
    "EZvQubb6PmcnK+vlnd8aftYnrQ8wHYSxsD8tDp61GIshjoFUAACAAQAAgAAAAIAAAAAAAAAA"
    "AAAAAA=="
)


class TestPSBTSelectSeedView(BaseTest):
    def test_psbt_supports_seed_signing_false_without_derivations(self):
        self.controller.psbt = PSBT.from_string(PSBT_NO_DERIVATIONS_BASE64)
        view = PSBTSelectSeedView()

        assert view._psbt_supports_seed_signing() is False

    def test_psbt_supports_seed_signing_true_with_derivations(self):
        self.controller.psbt = PSBT.from_string(PSBT_WITH_DERIVATIONS_BASE64)
        view = PSBTSelectSeedView()

        assert view._psbt_supports_seed_signing() is True

    def test_run_shows_only_wif_option_without_derivations(self):
        self.controller.psbt = PSBT.from_string(PSBT_NO_DERIVATIONS_BASE64)
        self.controller.psbt_seed = Seed(["abandon"] * 11 + ["about"])
        self.controller.storage.seeds.append(Seed(["bacon"] * 24))
        self.settings.set_value(SettingsConstants.SETTING__ELECTRUM_SEEDS, SettingsConstants.OPTION__ENABLED)

        captured_button_data = []

        def run_screen_side_effect(_view, _screen_cls, **kwargs):
            captured_button_data.extend(kwargs["button_data"])
            return kwargs["button_data"].index(PSBTSelectSeedView.SCAN_WIF)

        with patch.object(PSBTSelectSeedView, "run_screen", autospec=True, side_effect=run_screen_side_effect):
            destination = PSBTSelectSeedView().run()

        assert captured_button_data == [PSBTSelectSeedView.SCAN_WIF]
        assert destination.View_cls == scan_views.ScanWIFKeyView
        assert self.controller.psbt_seed is None
        assert self.controller.resume_main_flow == Controller.FLOW__PSBT

    def test_run_keeps_seed_options_with_derivations(self):
        self.controller.psbt = PSBT.from_string(PSBT_WITH_DERIVATIONS_BASE64)
        self.controller.storage.seeds.append(Seed(["abandon"] * 11 + ["about"]))
        self.settings.set_value(SettingsConstants.SETTING__ELECTRUM_SEEDS, SettingsConstants.OPTION__ENABLED)

        captured_button_data = []

        def run_screen_side_effect(_view, _screen_cls, **kwargs):
            captured_button_data.extend(kwargs["button_data"])
            return kwargs["button_data"].index(PSBTSelectSeedView.SCAN_SEED)

        with patch.object(PSBTSelectSeedView, "run_screen", autospec=True, side_effect=run_screen_side_effect):
            destination = PSBTSelectSeedView().run()

        assert PSBTSelectSeedView.SCAN_SEED in captured_button_data
        assert PSBTSelectSeedView.SCAN_WIF in captured_button_data
        assert PSBTSelectSeedView.TYPE_12WORD in captured_button_data
        assert PSBTSelectSeedView.TYPE_24WORD in captured_button_data
        assert PSBTSelectSeedView.TYPE_ELECTRUM in captured_button_data
        assert destination.View_cls == scan_views.ScanSeedQRView
