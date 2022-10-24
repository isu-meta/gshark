import argparse

from gshark.gshark import (
    load_google_sheet,
    get_aviary_metadata,
    get_islandora_metadata,
    mint_arks,
    save_tsv
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("username")
    parser.add_argument("password")
    parser.add_argument("shoulder")
    parser.add_argument("source")
    parser.add_argument("outfile")
    parser.add_argument("platform")
    parser.add_argument("--tsv-only", action="store_true")
    args = parser.parse_args()

    gs_md = load_google_sheet(args.source)
    if args.platform == "islandora":
        arks_md = get_islandora_metadata(gs_md)
    elif args.platform == "aviary":
        arks_md = get_aviary_metadata(gs_md)
    elif args.platform == "aviary-to-islandora":
        arks_md = get_aviary_metadata(gs_md, True)
    if not args.tsv_only:
        arks = mint_arks(arks_md, args.username, args.password, args.shoulder)
        save_tsv(gs_md, args.outfile, args.platform, arks)
    else:
        save_tsv(arks_md, args.outfile, "arkimedes")


if __name__ == "__main__":
    main()