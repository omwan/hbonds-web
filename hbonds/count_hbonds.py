import pandas
from bokeh.plotting import figure

data = pandas.read_csv("/Users/olivia/Documents/GitHub/hbonds-web/moe/output.csv")

MOE_HEADERS = ["PDB", "Type", "cb.cb", "sc_.exp_avg", "hb_energy", "Residue.1",
               "Residue.2", "chainId", "expressionHost", "source", "refinementResolution",
               "averageBFactor", "chainLength", "ligandId", "hetId", "residueCount"]


def build_graph():
    # filter out peptides and high-res species
    filtered_data = data[data["hbonds"] > 50]
    filtered_data = filtered_data[data["resolution"] > 1]

    x = filtered_data["hbonds/residues"]
    y = filtered_data["resolution"]

    p = figure()
    p.scatter(x, y)

    return p
