# tests_feature_fallback.py
from add_interface_features import _render_with_fallback
from interface_features_schemas import FeatureChange

# IPV6_ND_DAD_ATTEMPTS exists on 1715, not on 1612/173/179/1712
change = FeatureChange.model_validate({
    "train": "1715",                          # declared as 1715
    "interfaces": [{
        "interface": {"parent": "GigabitEthernet", "name": "1/0/1"},
        "features": [{"feature": "ipv6_nd_dad_attempts", "attempts": 3}],
    }],
})

# but device is on 16.12 — fallback should try 1612, 173, 179, 1712 (all fail)
# then 1715 (pass)
rendered, train_used, errors = _render_with_fallback(change, "16.12.3")
print(f"train_used: {train_used}")
print(f"payloads:   {len(rendered)}")
print(f"errors:     {errors}")