from dlparse.mono.manager import AssetManager


def test_get_story_entries_of_an_unit(asset_manager: AssetManager):
    var_id = (100015, 8)  # Summer Chelle

    story_entries = asset_manager.asset_story_unit.get_data_by_variation_identifier(var_id)

    assert [story.id for story in story_entries] == [100015081, 100015082, 100015083, 100015084, 100015085]


def test_get_story_entries_of_a_chapter(asset_manager: AssetManager):
    story_entries = asset_manager.asset_story_main.get_data_by_group_id(10020)

    assert [story.id for story in story_entries] == list(range(1002001, 1002014))
