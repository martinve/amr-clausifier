import json
import re
import sys

from logger import logger

failed = []

def cleanup_tree(ptree, remove_first_line=True):
    """
    Cleanup AMR graph by removing parser output metadata and compressing the output

    :param ptree:
    :param remove_first_line:
    :return:
    """
    if remove_first_line:
        ptree = '\n'.join(ptree.split('\n')[1:])

    ptree = ptree.replace("\n", " ")
    ptree = re.sub(' {2,}', ' ', ptree)
    return ptree


def quote_json_strings(s):
    """
    Wrap JSON strings in quotes
    :param s:
    :return:
    """
    ret = re.sub(r'(:?[a-zA-Z0-9-]+)', r'"\1"', s)
    return ret.replace('""', '"')


def amr_to_json(amr_str, debug=False):

    if amr_str[0] == "#":
        amr_str = cleanup_tree(amr_str)

    depth = 0
    ret = []
    read_op = False
    edge_op = True
    extra_bracket = 0

    for char in amr_str:

        outp = "".join(ret)

        if char == "(":
            char = "["
            depth = depth + 1
        elif char == ")":
            char = "]"
            if extra_bracket:
                if debug:
                    logger.debug(f"Extra ], d={depth}, e={extra_bracket}")
                char = (1 + extra_bracket) * "]"
                extra_bracket = 0
            depth -= 1
        elif char == "/":
            char = ","
        elif char == ":":
            if debug:
                logger.debug(f": op={int(read_op)}, d={depth}, e={extra_bracket}, {outp}")

            if edge_op:
                ret.append("]")
                extra_bracket -= 1
                edge_op = False

            ret.append(",[")
            extra_bracket += 1
            depth += 1

            read_op = True
            edge_op = True

            # print(f": d={depth}, e={extra_bracket}", outp)
        elif char == " ":
            if read_op:
                char = ","
                read_op = False
            else:
                char = ""
        elif char == "+":
            char = '"+"'
        ret.append(char)

    ret = "".join(ret)
    ret = quote_json_strings(ret)
    ret = f"[{ret}]"

    return_arr = []
    try:
        return_arr = json.loads(ret)
    except:
        logger.error(f"Invalid JSON: {ret}")
        failed.append(ret)

    if debug:
        logger.debug("AMR -> JSON:")
        logger.debug(return_arr)

    return return_arr
