from pathlib import Path

path = Path("src/network-workloads/model-net-fluid-switch.cxx")
text = path.read_text()

old = """static tw_lpid get_switch_gid(int switch_id) {
    tw_lpid gid = 0;
    codes_mapping_get_lp_id(GROUP_NAME, SWITCH_LP_NAME, NULL, 1, switch_id, 0, &gid);
    return gid;
}

static tw_lpid get_terminal_gid(int terminal_id) {
    tw_lpid gid = 0;
    codes_mapping_get_lp_id(GROUP_NAME, TERMINAL_LP_NAME, NULL, 1, terminal_id, 0, &gid);
    return gid;
}
"""

new = """static tw_lpid get_switch_gid(int switch_id) {
    if (switch_id < 0 || switch_id >= (int)switches.size()) {
        tw_error(TW_LOC, "switch id %d out of range [0, %zu)", switch_id, switches.size());
    }

    tw_lpid gid = 0;

    /*
     * LPGROUPS has one FLUID_GRP repetition containing all switch LPs.
     * The switch index is therefore the LP-type offset, not the group repetition.
     */
    codes_mapping_get_lp_id(GROUP_NAME, SWITCH_LP_NAME, NULL, 1, 0, switch_id, &gid);

    return gid;
}

static tw_lpid get_terminal_gid(int terminal_id) {
    if (terminal_id < 0 || terminal_id >= (int)terminals.size()) {
        tw_error(TW_LOC, "terminal id %d out of range [0, %zu)", terminal_id, terminals.size());
    }

    tw_lpid gid = 0;

    /*
     * LPGROUPS has one FLUID_GRP repetition containing all terminal LPs.
     * The terminal index is therefore the LP-type offset, not the group repetition.
     */
    codes_mapping_get_lp_id(GROUP_NAME, TERMINAL_LP_NAME, NULL, 1, 0, terminal_id, &gid);

    return gid;
}
"""

if old not in text:
    raise SystemExit("Could not find the old get_switch_gid/get_terminal_gid block.")

text = text.replace(old, new, 1)
path.write_text(text)

print(f"patched {path}")
