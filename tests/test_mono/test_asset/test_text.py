from dlparse.mono.asset import TextAsset


def test_override(asset_master_dir: str, asset_custom_dir: str):
    text_asset = TextAsset(asset_dir=asset_master_dir, asset_dir_custom=asset_custom_dir)

    assert text_asset.to_text("TEST_TEXT_LABEL") == "Test"
