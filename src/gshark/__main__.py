import argparse

from gshark.gshark import (
    load_google_sheet,
    get_aviary_metadata,
    get_islandora_metadata,
    mint_arks,
    save_google_sheet
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("username")
    parser.add_argument("password")
    parser.add_argument("shoulder")
    parser.add_argument("source")
    parser.add_argument("outfile")
    parser.add_argument("platform")
    args = parser.parse_args()

    gs_md = load_google_sheet(args.source)
    arks_md = get_islandora_metadata(gs_md) if args.platform == "islandora" else get_aviary_metadata(gs_md)
    arks = mint_arks(arks_md, args.username, args.password, args.shoulder)
    save_google_sheet(gs_md, arks, args.outfile, args.platform)


if __name__ == "__main__":
    main()