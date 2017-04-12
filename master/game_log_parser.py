"""
Log example :
1490775781.222226   new game
1490775781.22323    new enigma
1490775781.3244967  vector subenigmas solved    [False]
1490775825.113059   button pushed   Button object - panel: 3 button: 8 status: DOWN color: None
1490775825.117054   button pushed   Button object - panel: 3 button: 8 status: UP color: None
1490775825.2141545  vector subenigmas solved    [True]
"""

import re
import sys
import datetime


def parse_new_game(line):
    return {"event": "new_game"}


def parse_new_enigma(line):
    return {"event": "new_enigma"}


def parse_vector_subenigmas(line):
    parameters = eval(line[1])
    return {"event": "subenigmas", "params": parameters}


def parse_button_pushed(line):
    #Button object - panel: 7 button: 8 status: DOWN color: None
    pattern = "Button object - panel: (?P<panel_id>\d+) button: (?P<button_id>\d+) status: (?P<status>\w+) color: (?P<color>\w+)"
    if not re.match(pattern, line[1]):
        print(line[1])
        return {}
    return {"event": "", "params": re.match(pattern, line[1]).groupdict()}


def parse_on_error(line):
    return {"event": "error"}


def parse_log(fname):
    logs = []
    with open(fname, 'r') as f:
        for line in f:
            line = line.strip().split("\t")
            ts = float(line[0])

            event = line[1]
            line = line[1:]
            if event == "new game":
                parsed = parse_new_game(line)
            elif event == "new enigma":
                parsed = parse_new_enigma(line)
            elif event == "vector subenigmas solved":
                parsed = parse_vector_subenigmas(line)
            elif event == "button pushed":
                parsed = parse_button_pushed(line)
            elif event == "on error":
                parsed = parse_on_error(line)
            else:
                print("unknown event:" + event)
                continue
            parsed["ts"] = ts
            logs.append(parsed)
        return logs


def get_total_duration(logs):
    time_start = logs[0]["ts"]
    time_stop = logs[-1]["ts"]
    total_time = time_stop - time_start
    return datetime.timedelta(seconds=total_time)


def get_total_errors(logs):
    def is_error(log):
        return log["event"] == "error"
    return len(list(filter(is_error, logs)))


def get_subenigma_analysis(logs):
    sub_enigmas_logs = [[]]
    for log in logs:
        if log["event"] == "new_enigma":
            sub_enigmas_logs.append([])
        else:
            sub_enigmas_logs[-1].append(log)
    return sub_enigmas_logs


def analyze_logs(logs):
    total_duration = get_total_duration(logs)
    sub_enigmas_logs = get_subenigma_analysis(logs)
    se_durations = [get_total_duration(l) for l in sub_enigmas_logs]
    se_errors = [get_total_errors(l) for l in sub_enigmas_logs]
    return total_duration, se_durations, se_errors


def print_analysis(log_name):
    logs = parse_log(log_name)
    total_dur, se_durs, se_errors = analyze_logs(logs)
    print("durée totale (hh:mm:ss) : {}".format(total_dur))
    for i, (se_dur, se_error) in enumerate(zip(se_durs, se_errors)):
        print("  * enigme {} résolue en {} (hh:mm:ss) / {} erreurs".format(i, se_dur, se_error))


if __name__ == "__main__":
    log_name = sys.argv[1]
    print_analysis(log_name)
