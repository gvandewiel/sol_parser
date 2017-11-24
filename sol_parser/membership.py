class list(object):
    """Create printable list of scouts.
    Uses the parsed SOL output as input
    And creates a list with all relevant data
    """
    def __init__(self, parser):
        self.parser = parser

    def generate_list(self):
        scout_list = self.parser
        out_list = open(list.html, “w”)
        out_list.write(“<table>”)
        out_list.write(“<tr>”)
        for key in scout_list[0].keys():
            out_list.write(“<th>{}</th>”.format(key))
        out_list.write(“</tr>”)

        for scout in scout_list:
            out_list.write(“<tr>”)
            for ,v in scout.items():
                out_list.write(“<td>{}</td>”.format(v))
            out_list.write(“</tr>”)
        out_file.write(“</table>”)
