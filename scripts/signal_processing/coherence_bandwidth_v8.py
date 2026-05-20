import os
import csv
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# Enhanced Coherence Bandwidth Visualization
# ------------------------------------------------------------

input_csv = "results/coherence_v7/coherence_bandwidth.csv"

output_dir = "results/coherence_v7"

output_plot = os.path.join(
    output_dir,
    "coherence_bandwidth_v2.png"
)

scenarios = []
coherence_bw = []

with open(input_csv, "r") as f:

    reader = csv.DictReader(f)

    print("Detected CSV columns:")
    print(reader.fieldnames)

    for row in reader:

        # Auto-detect scenario column
        scenario_key = None

        for key in row.keys():
            if "scenario" in key.lower():
                scenario_key = key
                break

        if scenario_key is None:
            raise KeyError("Could not find scenario column.")

        scenarios.append(row[scenario_key])

        # Auto-detect coherence bandwidth column
        bw_key = None

        for key in row.keys():

            lower = key.lower()

            if (
                "coherence" in lower
                and ("bandwidth" in lower or "bw" in lower)
            ):
                bw_key = key
                break

        if bw_key is None:
            raise KeyError(
                "Could not find coherence bandwidth column."
            )

        value = float(row[bw_key])

        # Convert kHz → MHz if needed
        if value > 100:
            value = value / 1000.0

        coherence_bw.append(value)

plt.figure(figsize=(8, 5))

bars = plt.bar(
    scenarios,
    coherence_bw
)

plt.title("Estimated Coherence Bandwidth by Scenario")
plt.xlabel("Scenario")
plt.ylabel("Coherence Bandwidth (MHz)")

# Tightened axis for readability
plt.ylim(1.5, 2.1)

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.5
)

# Value labels
for bar, value in zip(bars, coherence_bw):

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + 0.015,
        f"{value:.2f}",
        ha="center",
        va="bottom",
        fontsize=9
    )

plt.xticks(rotation=10)

plt.tight_layout()

plt.savefig(
    output_plot,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(f"Saved updated plot to: {output_plot}")
