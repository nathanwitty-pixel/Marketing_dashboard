"""Pages build without a Google login: MONTHLY_TARGET falls back to a bare header, and the target total is still
the Odoo targets (lib/product_targets.monthly_target_sheet_rows + monthly_target_rows)."""
from lib import product_targets as pt


class _BrokenSheet:
    def worksheet(self, name):
        raise FileNotFoundError("No Google auth found")


def test_unreadable_sheet_gives_header_only():
    assert pt.monthly_target_sheet_rows(_BrokenSheet()) == [pt.MT_HEADER]


def test_target_total_is_the_odoo_targets_without_the_sheet():
    rows = pt.monthly_target_rows(pt.monthly_target_sheet_rows(_BrokenSheet()),
                                  targets={"JUMBO": 120, "NIZANA": 80, "KAI": 0}, key=str.upper)
    assert sum(int(r[2]) for r in rows[1:]) == 200
    assert all(len(r) == len(pt.MT_HEADER) for r in rows)      # room for the on-offer columns F/G/H
