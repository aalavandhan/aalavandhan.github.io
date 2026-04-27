"""
Prep IMF bilateral trade data + World Bank GDP for D3 network visualization.
Outputs JSON with nodes (countries + GDP) and edges (exports as % of GDP).
"""

import csv
import json
import math
import random
import urllib.request
from collections import defaultdict

CSV_PATH = "/Users/nithin/Downloads/dataset_2026-04-24T20_05_44.127766702Z_DEFAULT_INTEGRATION_IMF.STA_IMTS_1.0.0.csv"
OUT_PATH = "/Users/nithin/projects/personal/blog/apps/global-trade/trade_data.json"

# ── Regional aggregates to exclude ──────────────────────────
AGGREGATES = {
    "World", "Advanced Economies", "Emerging Market and Developing Economies",
    "EMDEs by Source of Export Earnings: Nonfuel", "EMDEs by Source of Export Earnings: Fuel",
    "European Union (EU)", "Emerging and Developing Asia", "Euro Area (EA)",
    "Europe", "Emerging and Developing Europe", "Middle East and Central Asia", "CIS",
    "Latin America and the Caribbean (LAC)",
    "Middle East, North Africa, Afghanistan, and Pakistan",
    "Middle East", "Sub-Saharan Africa (SSA)", "ASEAN", "Africa",
    "Asia", "Western Hemisphere", "APEC",
}

SKIP_TERMS = [
    "not specified", "Advanced Econ", "Emerging", "Euro Area", "European Union",
    "Sub-Saharan", "Middle East", "Latin America", "CIS", "ASEAN", "EMDEs",
    "Special Categories", "Areas n.i.e.", "Free Zones", "Bunkers",
]

# ── IMF name → short display name ──────────────────────────
SHORT_NAMES = {
    "China, People's Republic of": "China",
    "Hong Kong Special Administrative Region, People's Republic of China": "Hong Kong",
    "Macao Special Administrative Region, People's Republic of China": "Macao",
    "Korea, Republic of": "South Korea",
    "Korea, Democratic People's Republic of": "North Korea",
    "Russian Federation": "Russia",
    "Iran, Islamic Republic of": "Iran",
    "Netherlands, The": "Netherlands",
    "Türkiye, Republic of": "Turkey",
    "Türkiye": "Turkey",
    "United Arab Emirates": "UAE",
    "Saudi Arabia, Kingdom of": "Saudi Arabia",
    "Venezuela, República Bolivariana de": "Venezuela",
    "Egypt, Arab Republic of": "Egypt",
    "Congo, Democratic Republic of the": "DR Congo",
    "Congo, Republic of": "Congo",
    "Tanzania, United Republic of": "Tanzania",
    "Lao People's Democratic Republic": "Laos",
    "Brunei Darussalam": "Brunei",
    "Côte d'Ivoire": "Ivory Coast",
    "Czech Republic": "Czechia",
    "Slovak Republic": "Slovakia",
    "Poland, Republic of": "Poland",
    "Slovenia, Republic of": "Slovenia",
    "Croatia, Republic of": "Croatia",
    "Serbia, Republic of": "Serbia",
    "Moldova, Republic of": "Moldova",
    "Kosovo, Republic of": "Kosovo",
    "North Macedonia, Republic of": "N. Macedonia",
    "Montenegro, Republic of": "Montenegro",
    "Bosnia and Herzegovina": "Bosnia",
    "Bahrain, Kingdom of": "Bahrain",
    "Oman, Sultanate of": "Oman",
    "Qatar, State of": "Qatar",
    "Kuwait": "Kuwait",
    "Timor-Leste, Dem. Rep. of": "Timor-Leste",
    "Micronesia, Federated States of": "Micronesia",
    "Marshall Islands, Republic of the": "Marshall Is.",
    "Equatorial Guinea, Republic of": "Eq. Guinea",
    "Central African Republic": "CAR",
    "Dominican Republic": "Dominican Rep.",
    "Papua New Guinea": "PNG",
    "Trinidad and Tobago": "Trinidad",
    "Antigua and Barbuda": "Antigua",
    "St. Kitts and Nevis": "St. Kitts",
    "St. Vincent and the Grenadines": "St. Vincent",
    "São Tomé and Príncipe, Dem. Rep. of": "São Tomé",
    "Eswatini, Kingdom of": "Eswatini",
    "Lesotho, Kingdom of": "Lesotho",
    "Gambia, The": "Gambia",
    "Belarus, Republic of": "Belarus",
    "Armenia, Republic of": "Armenia",
    "Azerbaijan, Republic of": "Azerbaijan",
    "Georgia": "Georgia",
    "Kazakhstan, Republic of": "Kazakhstan",
    "Kyrgyz Republic": "Kyrgyzstan",
    "Tajikistan, Republic of": "Tajikistan",
    "Turkmenistan": "Turkmenistan",
    "Uzbekistan, Republic of": "Uzbekistan",
    "Afghanistan, Islamic Republic of": "Afghanistan",
    "Madagascar, Republic of": "Madagascar",
    "Mozambique, Republic of": "Mozambique",
    "Namibia, Republic of": "Namibia",
    "Ethiopia, The Federal Democratic Republic of": "Ethiopia",
    "South Sudan, Republic of": "South Sudan",
    "Cameroon, Republic of": "Cameroon",
    "Libya, State of": "Libya",
    "Eritrea, The State of": "Eritrea",
    "Comoros, Union of the": "Comoros",
    "Fiji, Republic of": "Fiji",
    "Bahamas, The": "Bahamas",
    "Estonia, Republic of": "Estonia",
    "Taiwan Province of China": "Taiwan",
    "Aruba, Kingdom of the Netherlands": "Aruba",
    "Curaçao, Kingdom of the Netherlands": "Curaçao",
    "Anguilla, United Kingdom-British Overseas Territory": "Anguilla",
    "Montserrat, United Kingdom-British Overseas Territory": "Montserrat",
    "Turks and Caicos Islands": "Turks & Caicos",
    "Falkland Islands (Malvinas)": "Falkland Is.",
    "Guinea-Bissau": "Guinea-Bissau",
    "Cabo Verde": "Cabo Verde",
    "New Caledonia": "New Caledonia",
    "French Polynesia": "Fr. Polynesia",
    "Wallis and Futuna": "Wallis & Futuna",
    "San Marino, Republic of": "San Marino",
    "Palau, Republic of": "Palau",
    "Latvia, Republic of": "Latvia",
    "Lithuania, Republic of": "Lithuania",
    "Mauritania, Islamic Republic of": "Mauritania",
    "Yemen, Republic of": "Yemen",
    "São Tomé and Príncipe, Democratic Republic of": "São Tomé",
    "Syrian Arab Republic": "Syria",
    "Timor-Leste, Democratic Republic of": "Timor-Leste",
    "St. Lucia": "St. Lucia",
    "Sint Maarten, Kingdom of the Netherlands": "Sint Maarten",
    "Nauru, Republic of": "Nauru",
    "Türkiye, Republic of": "Turkey",
}

# ── IMF name → World Bank ISO2 code ────────────────────────
IMF_TO_WB = {
    "China, People's Republic of": "CN",
    "Hong Kong Special Administrative Region, People's Republic of China": "HK",
    "Macao Special Administrative Region, People's Republic of China": "MO",
    "Korea, Republic of": "KR",
    "Korea, Democratic People's Republic of": "KP",
    "Russian Federation": "RU",
    "Iran, Islamic Republic of": "IR",
    "Netherlands, The": "NL",
    "United Arab Emirates": "AE",
    "Saudi Arabia, Kingdom of": "SA",
    "Venezuela, República Bolivariana de": "VE",
    "Egypt, Arab Republic of": "EG",
    "Congo, Democratic Republic of the": "CD",
    "Congo, Republic of": "CG",
    "Tanzania, United Republic of": "TZ",
    "Lao People's Democratic Republic": "LA",
    "Brunei Darussalam": "BN",
    "Côte d'Ivoire": "CI",
    "Czech Republic": "CZ",
    "Slovak Republic": "SK",
    "Poland, Republic of": "PL",
    "Slovenia, Republic of": "SI",
    "Croatia, Republic of": "HR",
    "Serbia, Republic of": "RS",
    "Moldova, Republic of": "MD",
    "Kosovo, Republic of": "XK",
    "North Macedonia, Republic of": "MK",
    "Montenegro, Republic of": "ME",
    "Bosnia and Herzegovina": "BA",
    "Bahrain, Kingdom of": "BH",
    "Oman, Sultanate of": "OM",
    "Qatar, State of": "QA",
    "Timor-Leste, Dem. Rep. of": "TL",
    "Micronesia, Federated States of": "FM",
    "Marshall Islands, Republic of the": "MH",
    "Equatorial Guinea, Republic of": "GQ",
    "Central African Republic": "CF",
    "Dominican Republic": "DO",
    "Papua New Guinea": "PG",
    "Trinidad and Tobago": "TT",
    "Antigua and Barbuda": "AG",
    "St. Kitts and Nevis": "KN",
    "St. Vincent and the Grenadines": "VC",
    "São Tomé and Príncipe, Dem. Rep. of": "ST",
    "Eswatini, Kingdom of": "SZ",
    "Lesotho, Kingdom of": "LS",
    "Gambia, The": "GM",
    "Belarus, Republic of": "BY",
    "Armenia, Republic of": "AM",
    "Azerbaijan, Republic of": "AZ",
    "Kazakhstan, Republic of": "KZ",
    "Kyrgyz Republic": "KG",
    "Tajikistan, Republic of": "TJ",
    "Uzbekistan, Republic of": "UZ",
    "Afghanistan, Islamic Republic of": "AF",
    "Madagascar, Republic of": "MG",
    "Mozambique, Republic of": "MZ",
    "Namibia, Republic of": "NA",
    "Ethiopia, The Federal Democratic Republic of": "ET",
    "South Sudan, Republic of": "SS",
    "Cameroon, Republic of": "CM",
    "Libya, State of": "LY",
    "Eritrea, The State of": "ER",
    "Comoros, Union of the": "KM",
    "Fiji, Republic of": "FJ",
    "Bahamas, The": "BS",
    "Estonia, Republic of": "EE",
    "Taiwan Province of China": "TW",
    "Aruba, Kingdom of the Netherlands": "AW",
    "Curaçao, Kingdom of the Netherlands": "CW",
    "Anguilla, United Kingdom-British Overseas Territory": "AI",  # not in WB
    "Montserrat, United Kingdom-British Overseas Territory": "MS",  # not in WB
    "Turks and Caicos Islands": "TC",
    "Falkland Islands (Malvinas)": "FK",
    "Guinea-Bissau": "GW",
    "Cabo Verde": "CV",
    "Palau, Republic of": "PW",
    "San Marino, Republic of": "SM",
    "French Polynesia": "PF",
    "New Caledonia": "NC",
    # Simple 1-to-1 where IMF name == common name
    "Albania": "AL", "Algeria": "DZ", "Angola": "AO", "Argentina": "AR",
    "Australia": "AU", "Austria": "AT", "Bangladesh": "BD", "Barbados": "BB",
    "Belgium": "BE", "Belize": "BZ", "Benin": "BJ", "Bhutan": "BT",
    "Bolivia": "BO", "Botswana": "BW", "Brazil": "BR", "Bulgaria": "BG",
    "Burkina Faso": "BF", "Burundi": "BI", "Cambodia": "KH", "Cameroon": "CM",
    "Canada": "CA", "Chad": "TD", "Chile": "CL", "Colombia": "CO",
    "Costa Rica": "CR", "Cuba": "CU", "Cyprus": "CY", "Denmark": "DK",
    "Djibouti": "DJ", "Dominica": "DM", "Ecuador": "EC", "El Salvador": "SV",
    "Finland": "FI", "France": "FR", "Gabon": "GA", "Georgia": "GE",
    "Germany": "DE", "Ghana": "GH", "Greece": "GR", "Greenland": "GL",
    "Grenada": "GD", "Guatemala": "GT", "Guinea": "GN", "Guyana": "GY",
    "Haiti": "HT", "Honduras": "HN", "Hungary": "HU", "Iceland": "IS",
    "India": "IN", "Indonesia": "ID", "Iraq": "IQ", "Ireland": "IE",
    "Israel": "IL", "Italy": "IT", "Jamaica": "JM", "Japan": "JP",
    "Jordan": "JO", "Kenya": "KE", "Kiribati": "KI", "Kuwait": "KW",
    "Latvia": "LV", "Lebanon": "LB", "Liberia": "LR",
    "Lithuania": "LT", "Luxembourg": "LU", "Malawi": "MW", "Malaysia": "MY",
    "Maldives": "MV", "Mali": "ML", "Malta": "MT", "Mauritania": "MR",
    "Mauritius": "MU", "Mexico": "MX", "Mongolia": "MN",
    "Morocco": "MA", "Myanmar": "MM", "Nepal": "NP", "New Zealand": "NZ",
    "Nicaragua": "NI", "Niger": "NE", "Nigeria": "NG", "Norway": "NO",
    "Oman": "OM", "Pakistan": "PK", "Panama": "PA", "Paraguay": "PY",
    "Peru": "PE", "Philippines": "PH", "Portugal": "PT", "Romania": "RO",
    "Rwanda": "RW", "Samoa": "WS", "Senegal": "SN", "Seychelles": "SC",
    "Sierra Leone": "SL", "Singapore": "SG", "Solomon Islands": "SB",
    "Somalia": "SO", "South Africa": "ZA", "Spain": "ES", "Sri Lanka": "LK",
    "Sudan": "SD", "Suriname": "SR", "Sweden": "SE", "Switzerland": "CH",
    "Syria": "SY", "Thailand": "TH", "Togo": "TG", "Tonga": "TO",
    "Tunisia": "TN", "Turkmenistan": "TM", "Tuvalu": "TV", "Uganda": "UG",
    "Ukraine": "UA", "United Kingdom": "GB", "United States": "US",
    "Uruguay": "UY", "Vanuatu": "VU", "Vietnam": "VN", "Yemen": "YE",
    "Zambia": "ZM", "Zimbabwe": "ZW", "Bermuda": "BM",
    "Gibraltar": "GI", "Faroe Islands": "FO",
    "Latvia, Republic of": "LV",
    "Lithuania, Republic of": "LT",
    "Mauritania, Islamic Republic of": "MR",
    "Yemen, Republic of": "YE",
    "São Tomé and Príncipe, Democratic Republic of": "ST",
    "Syrian Arab Republic": "SY",
    "Timor-Leste, Democratic Republic of": "TL",
    "St. Lucia": "LC",
    "Sint Maarten, Kingdom of the Netherlands": "SX",
    "Nauru, Republic of": "NR",
    "Türkiye, Republic of": "TR",
}

# ── Region mapping (short name → region) ───────────────────
REGION_MAP = {
    "China": "East Asia", "Hong Kong": "East Asia", "Macao": "East Asia",
    "Japan": "East Asia", "South Korea": "East Asia", "North Korea": "East Asia",
    "Taiwan": "East Asia", "Mongolia": "East Asia",
    "India": "South Asia", "Pakistan": "South Asia", "Bangladesh": "South Asia",
    "Sri Lanka": "South Asia", "Nepal": "South Asia", "Maldives": "South Asia",
    "Bhutan": "South Asia", "Afghanistan": "South Asia",
    "Vietnam": "SE Asia", "Thailand": "SE Asia", "Singapore": "SE Asia",
    "Malaysia": "SE Asia", "Indonesia": "SE Asia", "Philippines": "SE Asia",
    "Myanmar": "SE Asia", "Cambodia": "SE Asia", "Laos": "SE Asia",
    "Brunei": "SE Asia", "Timor-Leste": "SE Asia",
    "United States": "N. America", "Canada": "N. America", "Mexico": "N. America",
    "Guatemala": "C. America", "Honduras": "C. America", "El Salvador": "C. America",
    "Nicaragua": "C. America", "Costa Rica": "C. America", "Panama": "C. America",
    "Belize": "C. America",
    "Brazil": "S. America", "Argentina": "S. America", "Chile": "S. America",
    "Colombia": "S. America", "Peru": "S. America", "Ecuador": "S. America",
    "Venezuela": "S. America", "Uruguay": "S. America", "Paraguay": "S. America",
    "Bolivia": "S. America", "Guyana": "S. America", "Suriname": "S. America",
    "Germany": "Europe", "France": "Europe", "United Kingdom": "Europe",
    "Italy": "Europe", "Spain": "Europe", "Netherlands": "Europe",
    "Belgium": "Europe", "Switzerland": "Europe", "Austria": "Europe",
    "Sweden": "Europe", "Norway": "Europe", "Denmark": "Europe",
    "Finland": "Europe", "Ireland": "Europe", "Portugal": "Europe",
    "Poland": "Europe", "Czechia": "Europe", "Romania": "Europe",
    "Hungary": "Europe", "Greece": "Europe", "Slovakia": "Europe",
    "Bulgaria": "Europe", "Croatia": "Europe", "Slovenia": "Europe",
    "Lithuania": "Europe", "Latvia": "Europe", "Estonia": "Europe",
    "Luxembourg": "Europe", "Serbia": "Europe", "Bosnia": "Europe",
    "N. Macedonia": "Europe", "Albania": "Europe", "Montenegro": "Europe",
    "Kosovo": "Europe", "Moldova": "Europe", "Iceland": "Europe",
    "Malta": "Europe", "Cyprus": "Europe", "San Marino": "Europe",
    "Russia": "Russia/CIS", "Ukraine": "Russia/CIS", "Belarus": "Russia/CIS",
    "Kazakhstan": "Central Asia", "Uzbekistan": "Central Asia",
    "Turkmenistan": "Central Asia", "Kyrgyzstan": "Central Asia",
    "Tajikistan": "Central Asia", "Armenia": "Central Asia",
    "Azerbaijan": "Central Asia", "Georgia": "Central Asia",
    "Saudi Arabia": "Middle East", "UAE": "Middle East", "Qatar": "Middle East",
    "Kuwait": "Middle East", "Bahrain": "Middle East", "Oman": "Middle East",
    "Iraq": "Middle East", "Iran": "Middle East", "Israel": "Middle East",
    "Jordan": "Middle East", "Lebanon": "Middle East", "Turkey": "Middle East",
    "Yemen": "Middle East", "Syria": "Middle East", "Turkey": "Middle East",
    "Australia": "Oceania", "New Zealand": "Oceania", "PNG": "Oceania",
    "Fiji": "Oceania", "Samoa": "Oceania", "Tonga": "Oceania",
    "Vanuatu": "Oceania", "Solomon Islands": "Oceania", "Kiribati": "Oceania",
    "Micronesia": "Oceania", "Palau": "Oceania", "Marshall Is.": "Oceania",
    "Tuvalu": "Oceania", "New Caledonia": "Oceania", "Fr. Polynesia": "Oceania",
    # Caribbean
    "Jamaica": "Caribbean", "Trinidad": "Caribbean", "Bahamas": "Caribbean",
    "Barbados": "Caribbean", "Haiti": "Caribbean", "Dominican Rep.": "Caribbean",
    "Antigua": "Caribbean", "St. Kitts": "Caribbean", "St. Vincent": "Caribbean",
    "Grenada": "Caribbean", "Dominica": "Caribbean", "Cuba": "Caribbean",
    "Curaçao": "Caribbean", "Aruba": "Caribbean",
    "St. Lucia": "Caribbean", "Sint Maarten": "Caribbean",
    "Latvia": "Europe", "Lithuania": "Europe",
    "Nauru": "Oceania", "Timor-Leste": "SE Asia",
}

# Africa: everything not already mapped
AFRICA_COUNTRIES = {
    "Nigeria", "South Africa", "Egypt", "Kenya", "Ethiopia", "Ghana",
    "Tanzania", "Ivory Coast", "Cameroon", "DR Congo", "Angola", "Mozambique",
    "Senegal", "Uganda", "Tunisia", "Morocco", "Algeria", "Libya",
    "Sudan", "South Sudan", "Somalia", "Eritrea", "Djibouti", "Comoros",
    "Madagascar", "Mauritius", "Seychelles", "Rwanda", "Burundi",
    "Malawi", "Zambia", "Zimbabwe", "Botswana", "Namibia", "Eswatini",
    "Lesotho", "Gabon", "Congo", "CAR", "Chad", "Niger", "Mali",
    "Burkina Faso", "Benin", "Togo", "Guinea", "Guinea-Bissau",
    "Sierra Leone", "Liberia", "Gambia", "Cabo Verde", "Eq. Guinea",
    "São Tomé", "Mauritania",
}
for c in AFRICA_COUNTRIES:
    REGION_MAP[c] = "Africa"


def is_country(name):
    if name in AGGREGATES:
        return False
    for term in SKIP_TERMS:
        if term in name:
            return False
    return True

def shorten(name):
    return SHORT_NAMES.get(name, name)

def get_region(short_name):
    return REGION_MAP.get(short_name, "Other")


# ── Louvain community detection ─────────────────────────────
def louvain(nodes_list, edges_list, weight_key="weight", resolution=1.0, seed=42):
    """
    Louvain method for community detection on a weighted undirected graph.
    Returns dict: node_id -> community_id (int starting at 0).
    """
    random.seed(seed)

    # Build adjacency: node -> {neighbor -> weight}
    adj = defaultdict(lambda: defaultdict(float))
    for e in edges_list:
        s, t, w = e["source"], e["target"], e[weight_key]
        adj[s][t] += w
        adj[t][s] += w

    nodes = list(nodes_list)
    m2 = sum(adj[n][nb] for n in nodes for nb in adj[n])  # 2 * total weight
    if m2 == 0:
        return {n: i for i, n in enumerate(nodes)}

    # Degree (weighted) of each node
    k = {n: sum(adj[n].values()) for n in nodes}

    # Initial: each node in its own community
    node2comm = {n: i for i, n in enumerate(nodes)}
    comm_nodes = {i: {n} for i, n in enumerate(nodes)}

    # Sum of weights inside each community, and total degree of each community
    sigma_in = defaultdict(float)  # sum of internal edges * 2
    sigma_tot = {}  # sum of degrees
    for i, n in enumerate(nodes):
        sigma_tot[i] = k[n]
        # self-loops counted as internal
        if n in adj[n]:
            sigma_in[i] = adj[n][n]

    def modularity_gain(node, comm_to, ki, ki_in):
        """Delta Q for moving node into comm_to."""
        st = sigma_tot.get(comm_to, 0)
        si = sigma_in.get(comm_to, 0)
        return (ki_in - resolution * st * ki / m2)

    improved = True
    iteration = 0
    while improved and iteration < 20:
        improved = False
        iteration += 1
        order = list(nodes)
        random.shuffle(order)

        for node in order:
            curr_comm = node2comm[node]
            ki = k[node]

            # Compute ki_in for current community and neighbor communities
            neighbor_comms = defaultdict(float)
            for nb, w in adj[node].items():
                neighbor_comms[node2comm[nb]] += w

            ki_in_curr = neighbor_comms.get(curr_comm, 0)

            # Remove node from current community
            best_comm = curr_comm
            best_gain = 0

            # Temporarily remove node from its community for calculations
            sigma_tot[curr_comm] -= ki
            sigma_in[curr_comm] -= 2 * ki_in_curr
            if node in adj[node]:
                sigma_in[curr_comm] -= adj[node][node]

            for comm, ki_in in neighbor_comms.items():
                gain = modularity_gain(node, comm, ki, ki_in)
                if gain > best_gain:
                    best_gain = gain
                    best_comm = comm

            # Also check staying removed (gain of re-inserting into current)
            gain_stay = modularity_gain(node, curr_comm, ki, ki_in_curr)
            if gain_stay >= best_gain:
                best_comm = curr_comm
                best_gain = gain_stay

            # Move node
            ki_in_best = neighbor_comms.get(best_comm, 0)
            sigma_tot[best_comm] = sigma_tot.get(best_comm, 0) + ki
            sigma_in[best_comm] = sigma_in.get(best_comm, 0) + 2 * ki_in_best
            if node in adj[node]:
                sigma_in[best_comm] += adj[node][node]

            if best_comm != curr_comm:
                comm_nodes[curr_comm].discard(node)
                if best_comm not in comm_nodes:
                    comm_nodes[best_comm] = set()
                comm_nodes[best_comm].add(node)
                node2comm[node] = best_comm
                improved = True

    # Renumber communities contiguously
    active_comms = sorted(set(node2comm.values()))
    remap = {c: i for i, c in enumerate(active_comms)}
    return {n: remap[c] for n, c in node2comm.items()}


def detect_communities(included, exports, gdp_by_name):
    """Run Louvain at multiple resolutions, return results."""
    # Build weighted undirected edge list.
    # Weight = max(pctSrcGdp, pctDstGdp) — captures trade importance to either side.
    edge_list = []
    for (src, dst), val in exports.items():
        if src in included and dst in included:
            src_gdp = gdp_by_name[src] / 1e6
            dst_gdp = gdp_by_name[dst] / 1e6
            pct_src = val / src_gdp * 100
            pct_dst = val / dst_gdp * 100
            weight = max(pct_src, pct_dst)
            if weight > 0.01:  # minimum threshold to avoid noise
                edge_list.append({"source": src, "target": dst, "weight": weight})

    print(f"\nCommunity detection: {len(included)} nodes, {len(edge_list)} edges")

    # Run at different resolutions to get hierarchy
    results = {}
    for res_name, res_val in [("coarse", 0.5), ("default", 1.0), ("fine", 2.0)]:
        comms = louvain(included, edge_list, resolution=res_val)
        n_comms = len(set(comms.values()))
        print(f"  Resolution {res_val} ({res_name}): {n_comms} communities")

        # Print community members (sorted by community size)
        comm_members = defaultdict(list)
        for node, comm in comms.items():
            comm_members[comm].append(node)

        for comm_id, members in sorted(comm_members.items(), key=lambda x: -len(x[1])):
            if len(members) >= 3:
                print(f"    Community {comm_id} ({len(members)}): {', '.join(sorted(members)[:12])}{'...' if len(members) > 12 else ''}")

        results[res_name] = comms

    return results


def fetch_gdp():
    """Fetch GDP (current USD) from World Bank API."""
    url = "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?date=2023:2025&format=json&per_page=1000"
    resp = urllib.request.urlopen(url, timeout=20)
    data = json.loads(resp.read())

    gdp = {}  # ISO2 code → GDP in USD
    for item in data[1]:
        code = item["country"]["id"]
        val = item["value"]
        if val and code not in gdp:
            gdp[code] = val  # already in USD

    print(f"GDP data: {len(gdp)} entries from World Bank")
    return gdp


def main():
    # ── Fetch GDP ──
    gdp_by_code = fetch_gdp()

    # ── Parse trade CSV ──
    with open(CSV_PATH) as f:
        rows = list(csv.reader(f))[1:]

    # Collect exports FOB between actual countries
    exports = {}
    for r in rows:
        indicator = r[4]
        if "Exports" in indicator and "FOB" in indicator and r[8]:
            src, dst = r[3], r[5]
            if is_country(src) and is_country(dst):
                val = float(r[8])
                if val > 0:
                    exports[(shorten(src), shorten(dst))] = val

    print(f"Export pairs: {len(exports)}")

    # ── Build GDP lookup by short name ──
    gdp_by_name = {}
    no_gdp = set()
    for imf_name, wb_code in IMF_TO_WB.items():
        short = shorten(imf_name)
        if wb_code in gdp_by_code:
            gdp_by_name[short] = gdp_by_code[wb_code]

    # Taiwan GDP (not in World Bank) - use IMF estimate ~$800B
    if "Taiwan" not in gdp_by_name:
        gdp_by_name["Taiwan"] = 800e9

    # ── Compute total trade per country ──
    total_trade = defaultdict(float)
    total_exports = defaultdict(float)
    total_imports = defaultdict(float)
    for (src, dst), val in exports.items():
        total_trade[src] += val
        total_trade[dst] += val
        total_exports[src] += val
        total_imports[dst] += val

    # ── Build nodes: all countries with both trade data AND GDP ──
    all_countries = set()
    for (src, dst) in exports:
        all_countries.add(src)
        all_countries.add(dst)

    nodes = []
    included = set()
    for country in sorted(all_countries):
        gdp = gdp_by_name.get(country)
        trade = total_trade.get(country, 0)
        if gdp and trade > 0:
            nodes.append({
                "id": country,
                "gdp": round(gdp / 1e6, 1),  # convert to millions USD to match trade
                "totalTrade": round(trade, 1),
                "totalExports": round(total_exports.get(country, 0), 1),
                "totalImports": round(total_imports.get(country, 0), 1),
                "tradeToGdp": round(trade / (gdp / 1e6) * 100, 2),  # trade as % of GDP
                "region": get_region(country),
            })
            included.add(country)
        elif trade > 0:
            no_gdp.add(country)

    print(f"\nCountries included: {len(included)}")
    print(f"Countries dropped (no GDP match): {len(no_gdp)}")
    if no_gdp:
        for c in sorted(no_gdp):
            print(f"  {c} (trade: ${total_trade[c]:,.0f}M)")

    # ── Build edges ──
    edges = []
    for (src, dst), val in exports.items():
        if src in included and dst in included:
            src_gdp = gdp_by_name[src] / 1e6  # in millions
            dst_gdp = gdp_by_name[dst] / 1e6
            edges.append({
                "source": src,
                "target": dst,
                "value": round(val, 1),  # absolute trade in $M
                "pctSrcGdp": round(val / src_gdp * 100, 4),  # % of exporter GDP
                "pctDstGdp": round(val / dst_gdp * 100, 4),  # % of importer GDP
            })

    # ── Detect trade communities ──
    community_results = detect_communities(included, exports, gdp_by_name)

    # Add community labels to nodes
    for node in nodes:
        nid = node["id"]
        for res_name in ["coarse", "default", "fine"]:
            node["comm_" + res_name] = community_results[res_name].get(nid, -1)

    # Name communities by their largest economy (highest GDP member)
    comm_names = {}
    for res_name in ["coarse", "default", "fine"]:
        comms = community_results[res_name]
        members_by_comm = defaultdict(list)
        for nid, cid in comms.items():
            members_by_comm[cid].append(nid)

        names = {}
        for cid, members in members_by_comm.items():
            # Pick the member with highest GDP as the community label
            top = max(members, key=lambda m: gdp_by_name.get(m, 0))
            names[cid] = top
        comm_names[res_name] = names

    # Add community name to nodes
    for node in nodes:
        for res_name in ["coarse", "default", "fine"]:
            cid = node["comm_" + res_name]
            node["commName_" + res_name] = comm_names[res_name].get(cid, "?")

    # Sort nodes by total trade desc
    nodes.sort(key=lambda x: -x["totalTrade"])

    data = {"nodes": nodes, "edges": edges}

    with open(OUT_PATH, "w") as f:
        json.dump(data, f)  # no indent — smaller file

    print(f"\nWrote {OUT_PATH}")
    print(f"  Nodes: {len(nodes)}")
    print(f"  Edges: {len(edges)}")
    size_mb = len(json.dumps(data)) / 1e6
    print(f"  File size: {size_mb:.1f} MB")

    # Stats
    print(f"\nTop 15 by trade/GDP ratio:")
    for n in sorted(nodes, key=lambda x: -x["tradeToGdp"])[:15]:
        print(f"  {n['id']}: {n['tradeToGdp']:.1f}% (trade ${n['totalTrade']:,.0f}M, GDP ${n['gdp']:,.0f}M)")

    print(f"\nTop 15 edges by % of exporter GDP:")
    for e in sorted(edges, key=lambda x: -x["pctSrcGdp"])[:15]:
        print(f"  {e['source']} -> {e['target']}: {e['pctSrcGdp']:.2f}% (${e['value']:,.0f}M)")

    from collections import Counter
    regions = Counter(n["region"] for n in nodes)
    print(f"\nRegion distribution:")
    for r, c in regions.most_common():
        print(f"  {r}: {c}")


if __name__ == "__main__":
    main()
