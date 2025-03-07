import re
def parse_tran_ngspice(path):
    with open(path, "r") as raw_file:
        raw_file = raw_file.read()

        #Deleting multiple spaces, etc. using regular expressions
        raw_file = re.sub(r'\t',' ',raw_file)
        raw_file = re.sub(r' +',' ',raw_file)
        raw_file = re.findall(r'[^\n]*', raw_file)
        raw_file = [line for line in raw_file if line.strip()]
        print(len(raw_file))

    #parse signals names
    signals = []
    start_index = None
    end_index = None
    for i in range(0,len(raw_file)):
            line = str.lower(raw_file[i])

            if 'variables' in line and 'no. ' not in line:
                    start_index = i

            if 'values' in line:
                end_index = i
                break

            if start_index:
                if start_index != i:
                    signals.append(line.split()[1])
    #get number of points
    end_line = raw_file[len(raw_file)-2];
    number_of_points =  int(end_line.split()[0]) + 1

    #parse signals values
    signals_values = [[0] * number_of_points for _ in range(len(signals))]
    line_index = 1
    for i in range(number_of_points):
        for j in range(len(signals)):
            line = raw_file[end_index + line_index]
            if j == 0:
                signals_values[j][i] = float(line.split()[1])
            else:
                signals_values[j][i] = float(line.split()[0])
            line_index = line_index + 1
    return signals, signals_values