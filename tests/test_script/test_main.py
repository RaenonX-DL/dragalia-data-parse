import pytest


@pytest.mark.slow
def test_chara_overview():
    from script_chara_overview import main

    main()


@pytest.mark.slow
def test_check_skill():
    from script_check_skill import main

    main()


@pytest.mark.slow
def test_diff():
    from script_chara_overview import main

    main()


@pytest.mark.slow
def test_export():
    from script_chara_overview import main

    main()


@pytest.mark.slow
def test_view_hit_attr():
    from script_chara_overview import main

    main()
