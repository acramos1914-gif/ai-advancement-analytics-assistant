from advancement_ai.analytics import calculate_analytics


def test_kpis_and_fiscal_year(clean):
    a = calculate_analytics(clean)
    assert a["total_giving"] == 2100
    assert a["total_gifts"] == 6
    assert a["unique_donors"] == 4
    assert a["fiscal_year"] == 2025
    assert a["average_gift"] == 350
    assert a["median_gift"] == 350
    assert a["largest_gift"] == 600


def test_lifecycle_classification(clean):
    a = calculate_analytics(clean)
    assert a["new_donors"] == 1
    assert a["retained_donors"] == 1
    assert a["recovered_donors"] == 1
    assert a["lybunt_donors"] == 1
    assert a["donor_retention_rate"] == 0.5


def test_yoy_changes(clean):
    a = calculate_analytics(clean)
    assert a["yoy_giving_change"] == 1.0
    assert a["yoy_donor_change"] == 0.5
