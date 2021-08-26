from http.server import HTTPServer, SimpleHTTPRequestHandler
import json

host_name = "0.0.0.0"
server_port = 8080

MAX_NUM = 1000 * 1000 * 1000 * 1.0
MIN_NUM = 1000 * 1000 * 1000 * -1.0


class Server(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        received_data = self.rfile.read(content_length)
        input_json = json.loads(received_data.decode('utf-8'))

        operation = input_json["operation"]
        input_file_path = input_json["input_path"]
        file_input = open(input_file_path, "r")
        result = ""

        if operation == "min":
            min_val = MAX_NUM
            for num in file_input:
                if float(num) < min_val:
                    min_val = float(num)
            result = min_val

        if operation == "max":
            max_val = MIN_NUM
            for num in file_input:
                if float(num) > max_val:
                    max_val = float(num)
            result = max_val

        if operation == "average":
            sum_val = 0.0
            count = 0.0
            for num in file_input:
                sum_val += float(num)
                count += 1
            avg = sum_val / count
            result = avg

        if operation == "sort":
            sorted_list = []
            for num in file_input:
                new_num = float(num)
                if len(sorted_list) == 0:
                    sorted_list.append(new_num)
                else:
                    for cur_idx, list_num in enumerate(sorted_list):
                        if new_num < list_num:
                            sorted_list.insert(cur_idx, new_num)
                            break
                        else:
                            if cur_idx == len(sorted_list) - 1:
                                sorted_list.append(new_num)
                                break
            result = sorted_list

        if operation == "wordcount":
            unsorted_words = {}
            for line in file_input:
                line_words = line.replace("\n", "").split(" ")
                for word in line_words:
                    if word != "":
                        if word in unsorted_words:
                            unsorted_words[word] += 1
                        else:
                            unsorted_words[word] = 1
            sorted_words = sorted(unsorted_words, key=unsorted_words.get, reverse=True)
            result = sorted_words

        file_input.close()
        output_file_directory = input_json["output_path"]
        output_file_path = output_file_directory + "/" + operation + ".txt"
        file_output = open(output_file_path, "w")
        if operation == "min" or operation == "max" or operation == "average":
            file_output.write(str(result))
        if operation == "sort":
            for num in reversed(result):
                file_output.write(str(num) + "\n")
        if operation == "wordcount":
            for key in result:
                file_output.write(str(key) + " " + str(unsorted_words[key]) + "\n")

        file_output.close()

        response_text = {"finished": "ok"}
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(str(response_text).encode('utf-8'))


if __name__ == "__main__":
    webServer = HTTPServer((host_name, server_port), Server)
    print("Server started http://%s:%s" % (host_name, server_port))
    webServer.serve_forever()
