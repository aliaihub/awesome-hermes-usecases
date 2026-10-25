#!/usr/bin/env python3
"""Emit one alert only when disk use reaches the threshold; silent otherwise."""

import argparse
import shutil


def alert_for(used, total, threshold):
    if total <= 0:
        raise ValueError("Disk total must be positive")
    percent = used / total * 100
    return f"Disk usage is {percent:.1f}% (threshold {threshold:g}%)." if percent >= threshold else ""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", default="/")
    parser.add_argument("--threshold", type=float, default=90)
    args = parser.parse_args()
    if not 0 < args.threshold <= 100:
        parser.error("threshold must be greater than 0 and at most 100")
    usage = shutil.disk_usage(args.path)
    message = alert_for(usage.used, usage.total, args.threshold)
    if message:
        print(message)


if __name__ == "__main__":
    main()
