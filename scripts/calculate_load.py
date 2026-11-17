#!/usr/bin/env python3
"""Reproduce the capacity estimates; all assumptions are explicit below."""

from decimal import Decimal, getcontext

getcontext().prec = 28
D = Decimal
SECONDS_PER_DAY = D(86_400)
DAU = D(3_000_000)
MAU = D(10_000_000)
DAILY_COUNTS = {"transactional": D(2), "service": D(3), "marketing": D(5)}
PEAK_FACTOR = D(10)
CAMPAIGN_USERS = D(1_000_000)
CAMPAIGN_SECONDS = D(1_800)


def show(label, value, unit=""):
    print(f"{label:48} {value:>16,.2f} {unit}")


def main():
    campaign_rps = CAMPAIGN_USERS / CAMPAIGN_SECONDS
    total_daily = DAU * sum(DAILY_COUNTS.values())
    average_rps = total_daily / SECONDS_PER_DAY
    for category, count in DAILY_COUNTS.items():
        daily = DAU * count
        show(f"{category}: daily", daily)
        show(f"{category}: average", daily / SECONDS_PER_DAY, "/s")
        show(f"{category}: peak", daily / SECONDS_PER_DAY * PEAK_FACTOR, "/s")
    show("total daily", total_daily)
    show("total average", average_rps, "/s")
    show("total peak", average_rps * PEAK_FACTOR, "/s")
    show("additional campaign", campaign_rps, "/s")
    show("combined ordinary peak", average_rps * PEAK_FACTOR + campaign_rps, "/s")
    critical_stress = D(300_000) / D(60)
    bulk_peak = DAU * (DAILY_COUNTS["service"] + DAILY_COUNTS["marketing"]) / SECONDS_PER_DAY * PEAK_FACTOR
    show("combined stress peak", critical_stress + bulk_peak + campaign_rps, "/s")
    show("critical external attempts: healthy", critical_stress * D("1.05"), "/s")
    show("critical external attempts: 3 channels", critical_stress * D(3), "/s")
    show("availability error budget: 30 days", D(30 * 24 * 60) * D("0.0005"), "min")
    critical_average = DAU * DAILY_COUNTS["transactional"] / SECONDS_PER_DAY
    backlog = critical_average * D(600)
    show("critical backlog: 10 min at average", backlog)
    show("backlog drain: capacity 2000, incoming peak", backlog / (D(2_000) - critical_average * PEAK_FACTOR), "s")
    raw_gb = total_daily * D(2_000) / D(10**9)
    show("DB logical: daily", raw_gb, "GB")
    show("DB: 30d, RF3, overhead x2", raw_gb * D(30 * 3 * 2) / D(1_000), "TB")
    show("Kafka: 7d, RF3, four 2KB events", raw_gb * D(7 * 3 * 4) / D(1_000), "TB")
    show("Temporal history: 7d, three copies", D(6_000_000 * 12 * 1_000 * 7 * 3) / D(10**12), "TB")
    upper_daily = MAU * sum(DAILY_COUNTS.values())
    show("MAU interpretation: daily", upper_daily)
    show("MAU interpretation: average", upper_daily / SECONDS_PER_DAY, "/s")
    show("MAU interpretation: peak + campaign", upper_daily / SECONDS_PER_DAY * PEAK_FACTOR + campaign_rps, "/s")
    show("cost: push-first + SMS 5% + email 0.1%", D(6_000_000) * (D("0.05") * D(3) + D("0.001") * D("0.02")), "RUB/day")
    show("cost: all SMS", D(6_000_000) * D(3), "RUB/day")


if __name__ == "__main__":
    main()
