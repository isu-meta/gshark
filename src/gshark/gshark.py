"""Devouring Google Sheets and making baby ARKs doo doo, doo doo doo doo"""
import argparse
import csv

from arkimedes.ezid import build_anvl, upload_anvl


def load_google_sheet(gs_file, delimiter="\t", quotechar=None):
    with open(gs_file, "r", newline="", encoding="utf8") as fh:
        if quotechar is None:
            reader = csv.DictReader(fh, delimiter=delimiter, quoting=csv.QUOTE_NONE)
        else:
            reader = csv.DictReader(fh, delimiter=delimiter, quotechar=quotechar)

        return list(reader)


def get_aviary_metadata(gs_md):
    return [
        {
            "dc.creator": "; ".join(
                [
                    a.split(";;")[-1].strip()
                    for a
                    in g.get("Agent").split("|")
                ]
            ).strip("; "),
            "dc.title": g.get("Title", ""),
            "dc.date": g.get("Date", ""),
            "_target": "".join(
                [
                    "https://iastate.aviaryplatform.com/c/",
                    g.get("Custom Unique Identifier", "")
                ] 
            ),
            "dc.type": g.get("Type", "").split("|")[-1]
        }
        for g
        in gs_md
    ]

def get_islandora_metadata(gs_md):
    return [
        {
            "dc.creator": "; ".join(
                [
                    g.get("personal_creator", ""),
                    g.get("corporate_creator", "")
                ]
            ).strip("; "),
            "dc.title": g.get("title", ""),
            "dc.date": g.get("date_original", ""),
            "_target": "".join(
                [
                    "https://digitalcollections.lib.iastate.edu/islandora/object/",
                    g.get("pid", "")
                ] 
            ),
            "dc.type": g.get("dcmi_type", "")
        }
        if g.get("parent_predicate") == "isMemberOfCollection"
        else ""
        for g
        in gs_md
    ]



def mint_arks(md, user_name, password, shoulder):
    return [
        "".join(
            [
                "https://n2t.net/",
                upload_anvl(
                    user_name,
                    password,
                    shoulder,
                    build_anvl(
                        row["dc.creator"],
                        row["dc.title"],
                        row["dc.date"],
                        row["_target"],
                        type_=row["dc.type"]
                    )
                )
            ]
        )
        if row != ""
        else ""
        for row
        in md
    ]


def save_google_sheet(gs_md, arks, out_file, platform, dialect=csv.excel_tab):
    ark_column = "ark" if platform == "islandora" else "ARK"
    for g, a in zip(gs_md, arks):
        g[ark_column] = a

    with open(out_file, "w", encoding="utf8", newline="") as fh:
        fieldnames = list(gs_md[0].keys())
        writer = csv.DictWriter(fh, fieldnames=fieldnames, dialect=dialect)

        writer.writeheader()
        writer.writerows(gs_md)
