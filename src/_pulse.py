import subprocess
import re
from collections import namedtuple
from pprint import pprint
import pdb

_ParsedLine = namedtuple('_ParsedLine', ['level', 'key', 'value'])

class PulseAudioCommand:

    COMMAND = 'pacmd'

    def __getattr__(self, attr):
        return self._command(attr.replace('_', '-'))

    def _command(self, command_name):
        def f():
            data = subprocess.check_output([self.COMMAND, command_name]).splitlines()
            sink_data = self._parse(data)
            return sink_data
        return f

    def _key_mapper(self, value):
        if not value:
            return None
        value = value.strip().strip('"').strip("'")
        try:
            return int(value)
        except ValueError:
            pass
        try:
            return float(value)
        except ValueError:
            pass
        if value.lower() in ["true", "yes", "on"]:
            return True
        if value.lower() in ["false", "no", "off"]:
            return False
        return value

    def _parse(self, raw):
        parsed_lines = [self._parse_line(line) for line in raw]
        merged_lines = self._merge_lines(parsed_lines)
        lines_by_level = self._lines_by_level(merged_lines)
        return self._lines_to_tree(lines_by_level)

    def _lines_to_tree(self, lines_by_level, level=1):
        result = []
        key = "<unknown>"
        tmp = {}
        #pdb.set_trace()
        while lines_by_level:
            next_level = lines_by_level[0][0]
            if next_level < level: break
            current_level, lines = lines_by_level.pop(0)
            for line in lines:
                key = line.key
                if not line.key: raise Exception('No key %r' % (line,))
                if line.value:
                    tmp[line.key] = line.value

            if not lines_by_level: break

            next_level = lines_by_level[0][0]
            if next_level > level:
                child = self._lines_to_tree(lines_by_level, next_level)
                tmp[key] = child
                result.append(tmp)
                tmp = {}
                continue
        if tmp:
            result.append(tmp)
        if len(result) == 1: return result[0]
        return result
            

    def _lines_by_level(self, lines):
        lines_by_level = []
        level = 1
        tmp = []
        for line in lines:
            if line.level == 0: continue
            if line.level == level:
                tmp.append(line)
                continue
            if tmp: lines_by_level.append((level, tmp))
            level = line.level
            tmp = [line]
        if tmp: lines_by_level.append((level, tmp))
        return lines_by_level

    def _merge_lines(self, parsed_lines):
        merged_lines = []
        for line in parsed_lines:
            if line.key == line.value == None: continue
            if not merged_lines:
                merged_lines.append(line)
                continue
            prev = merged_lines[-1]
            if line.level > prev.level+1:
                merged = _ParsedLine(prev.level, prev.key,
                                     "%s\n%s" % (prev.value, line.value))
                merged_lines.pop()
                merged_lines.append(merged)
                continue
            merged_lines.append(line)
        return merged_lines        

    def _parse_line(self, line):
        """Return (level, key, value) of a line"""
        level = 0
        # Sometimes lines are indented by spaces..
        line = line.replace("    ", "\t")
        # ...probably because there's a * there sometimes
        line = line.replace("  * ", "\t")
        for i in range(len(line)):
            if line[i] == '\t':
                level += 1
        line = line.strip()
        m = re.match('^(?P<key>.*?)(: |:| = )(?P<value>.*)$', line)
        if m:
            value = self._key_mapper(m.group('value'))
            return _ParsedLine(level, m.group('key'), value)
        return _ParsedLine(level, None, self._key_mapper(line))

if __name__ == '__main__':
    pacmd = PulseAudioCommand()
    # print "list-sink-inputs, list-sinks"
    # while True:
    #     i = raw_input().strip()
    #     if not i: break
    #     method = getattr(pacmd, i)
    #     data = method()
    #     pprint(data)
    #pprint(pacmd.list_sink_inputs())
    pprint(pacmd.list_sinks())
