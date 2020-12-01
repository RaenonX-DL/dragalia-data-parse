from dlparse.mono.asset import TextAsset


def test_override(asset_master_dir: str, asset_custom_dir: str):
    asset_text = TextAsset(asset_dir=asset_master_dir, asset_dir_custom=asset_custom_dir)

    assert asset_text.to_text("TEST_TEXT_LABEL") == "Test"
