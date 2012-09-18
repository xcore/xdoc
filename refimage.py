import re
import os

try:
    from BeautifulSoup import BeautifulSoup as Soup
    from soupselect import select
    import_ok = True
except:
    import_ok = False


def get_references(html_files, css_files):
    if not import_ok:
        return None

    refs = set([])

    style_to_image_map = []

    for css_file in css_files:
        f = open(css_file)
        lines = f.readlines()
        f.close()
        css = ' '.join(lines)

        entries = re.findall('^(.*){([^}]*)}',css,re.MULTILINE)

        for select_expr, contents in entries:
            select_expr = select_expr.strip()
            urls = re.findall('url\(([^)]*)\)',contents)
            images = [os.path.basename(x) for x in urls]

            if images != []:
                style_to_image_map.append((select_expr, images))


    for f in html_files:
        lines = open(f).readlines()
        for line in lines:
            matches = re.findall("\"([^\"]*)\"",line)
            for ref in [os.path.basename(ref) for ref in matches]:
                refs.add(ref)

        soup = Soup(open(f))
        for select_expr, images in style_to_image_map:
            select_expr = select_expr.replace(":first-child","")
            if select(soup, select_expr) != []:
                for img in images:
                    refs.add(img)


    return refs


if __name__ == "__main__":
    get_references(['/home/davel/dev/docs_tools/user-guides/xde-run-a-program/_build/xdehtml/run.html'],
                   ['/home/davel/dev/docs_tools/user-guides/xde-run-a-program/_build/xdehtml/_static/styles.css'])

